import sys, os
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
from addict import Dict
from collections import defaultdict
import transformers
from mpi4py import MPI
import slackweb

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

if rank == 0:
    data = []
    for i in range(0,112):
        data_i = []
        data_i.append(i)
        data.append(data_i)
    print(data)

else:
    data = None

data = comm.scatter(data, root=0)

if rank % 100 == 0:
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(text=f"<!channel> rank:{rank} pubmed sentence sampling start!")


config = Dict()
config.chemical_icuis = "chemical_icuis.pkl"
config.icui2proper_names = "icui2proper_lower_names.pkl"
config.proper_name2icuis = "proper_name2icuis.pkl"

with open(config.chemical_icuis, 'rb') as f:
    chemical_icuis = pickle.load(f)
with open(config.icui2proper_names, 'rb') as f:
    icui2proper_names = pickle.load(f)
with open(config.proper_name2icuis, 'rb') as f:
    proper_name2icuis = pickle.load(f)
chemical_names = set()
for icui in chemical_icuis & set(icui2proper_names.keys()):
    chemical_names |= icui2proper_names[icui]
with open("ctcae_names.pkl", 'rb') as f:
    tox_names = pickle.load(f) 

# mask
def pubmed_mask(i_df):
    df = pd.read_csv(f"/work/ga97/a97006/nlp_chem_tox/pubmed_mask_samppling/notitle_over5words/{i_df}.tsv",
        sep='\t')
    n_tox_hit = n_chem_hit = n_tox_masked = n_chem_masked = 0
    rsens = []
    rtoxs = []
    rchems = []

    for i in range(len(df)):
        sen = df.iloc[i,1]
        sen = sen.lower()
        
        # 毒性の名前を探索 (rough)
        tox_hit_names = []
        for name in tox_names:
            if name in sen:
                tox_hit_names.append(name)
        if len(tox_hit_names) == 0:
            continue
        n_tox_hit += 1

        # 化合物の名前を探索(rough)
        chemical_hit_names = []
        for name in chemical_names:
            if name in sen:
                chemical_hit_names.append(name)
        if len(chemical_hit_names) == 0:
            continue
        n_chem_hit += 1

        # 毒性の名前を探索 (precise)
        tox_masked_names = []
        for name in sorted(tox_hit_names, key=len, reverse=True):
            masked = False
            splits = sen.split(name)
            sen = splits[0]
            for split in splits[1:]:
                prev_letter = ' ' if len(sen) == 0 else sen[-1]
                post_letter = ' ' if len(split) == 0 else split[0]
                if (prev_letter in 'abcdefghijklmnopqrstuvwxyz-') \
                    or (post_letter in 'abcdefghijklmnopqrstuvwxyz-') \
                    or (prev_letter == '(' and post_letter == ')'):
                    sen = sen+name+split
                else:
                    sen = sen+"<<<"+name.upper()+"<<<"+split
                    masked = True
            if masked:
                tox_masked_names.append(name)
        if len(tox_masked_names) == 0:
            continue
        n_tox_masked += 1
        
        # 化合物の名前を探索 (precise)
        chemical_masked_names = []
        for name in sorted(chemical_hit_names, key=len, reverse=True):
            masked = False
            splits = sen.split(name)
            sen = splits[0]
            for split in splits[1:]:
                prev_letter = ' ' if len(sen) == 0 else sen[-1]
                post_letter = ' ' if len(split) == 0 else split[0]
                if (prev_letter in 'abcdefghijklmnopqrstuvwxyz-') \
                    or (post_letter in 'abcdefghijklmnopqrstuvwxyz-') \
                    or (prev_letter == '(' and post_letter == ')'):
                    sen = sen+name+split
                else:
                    sen = sen+"<<<"+name.upper()+"<<<"+split
                    masked = True
            if masked:
                chemical_masked_names.append(name)
        if len(chemical_masked_names) == 0:
            continue
        n_chem_masked += 1

        # 名前をicuiごとに整理
        mtox_icui2names = defaultdict(list)
        for name in tox_masked_names:
            for icui in proper_name2icuis[name]:
                mtox_icui2names[icui].append(name)
        mtox_namess = {tuple(names) for names in mtox_icui2names.values()}
        mchem_icui2names = defaultdict(list)
        for name in chemical_masked_names:
            for icui in proper_name2icuis[name]:
                mchem_icui2names[icui].append(name)
        mchem_namess = {tuple(names) for names in mchem_icui2names.values()}

        for mtox_names in mtox_namess:
            sen0 = sen
            for name in mtox_names:
                sen0 = sen0.replace("<<<"+name.upper()+"<<<", "[TOXICITY]")
            for mchem_names in mchem_namess:
                sen1 = sen0
                for name in mchem_names:
                    sen1 = sen1.replace("<<<"+name.upper()+"<<<", "[COMPOUND]")
                sen1 = sen1.replace("<<<", "")
                rsens.append(sen1)
                rtoxs.append(mtox_names)
                rchems.append(mchem_names)
    pd.DataFrame({"SENTENCE": rsens, "TOXICITY": rtoxs, "COMPOUND": rchems}).to_csv(f"/work/ga97/a97006/nlp_chem_tox/pubmed_mask_samppling/pubmed_mask/{i_df:04}.tsv", sep='\t', index=False)

#ここにconcurrentfutureを指定すればもう何倍か早くなる
for x in data:
    pubmed_mask(x)