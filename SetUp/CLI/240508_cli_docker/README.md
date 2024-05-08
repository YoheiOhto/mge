# CLI docker + pyenv
本年度のセットアップに伴い、CLIdockerのimageをnvidia/cudaに変更し、docker conposeで建てる、従来のcoder gpuに揃えるようにした。

# 構成
★付きのファイルのみ弄る  
- coder_gpu  
    - ctn  
        - Dockerfile (containerの記述)  
        - ★requirements.txt (必要なpythonパッケージを指定)  
    - docker-compose.yml (composeの実行ファイル)  
    - ★.env (bindなどの設定ファイル)  
    - README.md  

***
# 事前準備
想定としては、クライアントのセットアップ、オンプレ(親機、計算機)のセットアップ、クライアント-オンプレ間のSSH接続が行われているものとする。

## 計算機(オンプレ, linux)側
- 240508_cli_dockerフォルダを使用したいディレクトリに配置する  
    - だいたいは```/home/{計算機名}/{user名}/{各自の名前}/cli_docker```といった形なはず  
    - scp辺りで転送しておく  

***
# HowToUse
- 基本的にユーザーが弄る部分は.env, ctn内のrequirements.txtのみ  
1. .env内のbind先(BIND_SRC)、pythonのversionを書き換える  
    - ```BIND_SRC=/mnt/data1```などとする  
    - bind先：サーバーマシン内の領域かつコンテナと共有したい領域
    - ```PYTHON_VER=3.10.9```などとする
    - python version: pyenvでインストールするpythonのバージョン
    - vimなどでlinux上で書き換える
2. sshで計算機サーバーへアクセス  
    - ```ssh -i C:\Users\tadahaya\.ssh\id_rsa_XXXX -p 491XX parentX@133.11.XX.XX```
    - ```ssh hiegm4```
    - win側にてpowershellを立てて上記を入力  
        - configに記載しておけばサボれる  
3. コンテナ立てる  
    - ```docker compose up -d```  
    - ssh接続した計算機サーバー側で行う, docker-compose.ymlがあるdir (coder)で行う  
    - 初回の場合は```--build```オプションをつけなくてもimageを作成される
    - 2回目以降でimageの変更が必要な場合に```--build```をつける  
6. 解析後, コンテナを終了する  
    - ```docker compose down```  
    - ssh接続した計算機サーバー側で行う, docker-compose.ymlがあるdir (coder)で行う

***
# HowToUse(詳細版)
- ポートが一つ出てくる(計算機がコンテナを受けるポート)
- yamlファイル内のports: 8080:8080の前の方
- ports:
      - 8080:8080
- 複数のコンテナを立てる際にはここを他のコンテナと被らないようにする
