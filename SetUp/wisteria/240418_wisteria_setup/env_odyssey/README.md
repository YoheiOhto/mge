# pyenv を使用した仮想環境構築
ここでは、wisteria-oにおけるpyenvでの仮想環境構築を行います。

* 利用手引書
利用手引書は利用支援ポータル (https://wisteria-www.cc.u-tokyo.ac.jp/) の「ドキュメント閲覧」より入手することが可能。
「ドキュメント閲覧」→「Wisteria/BDEC-01利用手引書 →「Wisteria/BDEC-01システム利用手引書」

## pyenvを使用できるようにするために
1. ホームディレクトリの変更
chhomeコマンドを使用して、ホームディレクトリを/home領域(/home/a97000)から
/work領域(/work/group_name/a97000)にご変更ください。

2. pyenvのインストール
pyenvをインストールして環境変数を変更する。

login$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv

login$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc

login$ echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

login$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc

login$ source ~/.bashrc

これでpyenvを使用できるようになる。
1-240814_ohto_test_o.sh　を実行して、実際に仮想環境を構築する

## pyenvの解説
pyenvとは、pythonのversionを仮想環境ようにインストールができるようになるためのモジュール。
通常では、PCにインストール済みのversionしか使用できないが、pyenvを使用してインストールすることで、それ以外のversionを使用することができるようになる。

CPUにはアーキテクチャというものが存在し、それらに最適化されたものがinstallされるように、pythonなどはなっている。しかし、wisteriaではodysseyとaquariusではアーキテクチャが異なるため、odysseyで構築した仮想環境をaquariusで使用することはできない。

そのため、比較的新しいバージョンのpythonが入っているaquariusではpyenvを使用しない仮想環境構築, odysseyではpyenvを使用した仮想環境構築にすることですみわけを図っている。

流れとしては、pyenvでバージョンをinstall、installされたversionに搭載されているvenvを使用して仮想環境を構築する。

## code serverの構築
★基盤様から、odysseyでバッチジョブとしてcode-serverを立てる方法
1. code serverのバイナリをダウンロードし展開
(requireされるものの関係で、wisteria-a(水野さんが載せているもの)とバージョン、アーキテクチャが違うことに注意)
login$ cd /work/$(id -gn)/$(id -un)

login$ wget https://github.com/coder/code-server/releases/download/v4.20.1/code-server-4.20.1-linux-arm64.tar.gz

login$ tar zxf code-server-4.20.1-linux-arm64.tar.gz

login$

2. インタラクティブジョブを使用して設定ファイルを作成します。
login$ pjsub -g <group name> -L rscgrp=interactive-o,node=1 --interact

calc$ ./code-server-4.20.1-linux-arm64/bin/code-server --cert

[XXXX-XX-XXXXX:XX:XX.XXXX] info Wrote default config file to .config/code-server/config.yaml

[XXXX-XX-XXXXX:XX:XX.XXXX] info code-server 4.20.1 e76afa4a2bf4667a3c9f71bf56ef34b8ad365fbe

[XXXX-XX-XXXXX:XX:XX.XXXX] info Using user-data-dir /work/group/user/.local/share/code-server

[XXXX-XX-XXXXX:XX:XX.XXXX] info Using config file /work/group/user/.config/code-server/config.yaml

[XXXX-XX-XXXXX:XX:XX.XXXX] info HTTPS server listening on https://xx.xx.xx.xx:8080/

[XXXX-XX-XXXXX:XX:XX.XXXX] info  - Authentication is enabled

[XXXX-XX-XXXXX:XX:XX.XXXX] info   - Using password from /work/group/user/.config/code-server/config.yaml

[XXXX-XX-XXXXX:XX:XX.XXXX] info  - Using certificate for HTTPS: /work/group/user/.local/share/code-server/localhost.crt

[XXXX-XX-XXXXX:XX:XX.XXXX] info Session server listening on /work/group/user/.local/share/code-server/code-server-ipc.sock

★上記メッセージが出力されたら、Ctrl+Cで終了してください。

calc$ exit

3. 生成されたパスワードを確認します。パスワードは、code-server へのWebアクセス時に必要となります。

login$ cat ~/.config/code-server/config.yaml

4. code-server の起動と起動ノードの確認  バッチジョブを使用して計算ノードで code-server を起動します。
(1) バッチジョブスクリプトを作成します。

login$ vi run.sh

#PJM -L rscgrp=regular-o

#PJM -L node=1

#PJM -L elapse=1:00:00　←ここで使用可能時間がきまる

#PJM -g <group_name>

#PJM -o stdout.log

#PJM -j

./bin/code-server <実行環境のディレクトリ> \

--config="/work/$(id -gn)/$(id -un)/.config/code-server/config.yaml" \

--cert="/work/$(id -gn)/$(id -un)/.local/share/code-server/localhost.crt" \

--cert-key="/work/$(id -gn)/$(id -un)/.local/share/code-server/localhost.key" \

--bind-addr=`uname -n`:8080

(2) ジョブを投入します。
login$ pjsub run.sh
(3) code-server の起動ノードの確認します。ジョブの標準出力結果(stdout.log)にcode-serverの起動ログが出力され、
下記★の情報からcode-serverを起動した計算ノードを確認します。

login$ cat stdout.log

[XXXX-XX-XXXXX:XX:XX.XXXX] info code-server 4.20.1 e76afa4a2bf4667a3c9f71bf56ef34b8ad365fbe

[XXXX-XX-XXXXX:XX:XX.XXXX] info Using user-data-dir /work/group/user/.local/share/code-server

[XXXX-XX-XXXXX:XX:XX.XXXX] info Using config file /work/group/user/.config/config.yaml

[XXXX-XX-XXXXX:XX:XX.XXXX] info HTTPS server listening on https://10.XX.XX.XX:8080/ ★code-serverを起動したノード

[XXXX-XX-XXXXX:XX:XX.XXXX] info  - Authentication is enabled

[XXXX-XX-XXXXX:XX:XX.XXXX] info   - Using password from /work/group/user/.config/code-server/config.yaml

[XXXX-XX-XXXXX:XX:XX.XXXX] info  - Using certificate for HTTPS: /work/group/user/.local/share/code-server/localhost.crt

[XXXX-XX-XXXXX:XX:XX.XXXX] info Session server listening on /work/group/user/.local/share/code-serve/code-server-ipc.sock

5. code serverへのアクセス
code serverを起動したノードへログインノードからsshポート転送を用いてアクセス。
別のシェルを立てて以下でクライアント→ログインノード→計算ノード(内のコードサーバー)へとポートフォワード。

ssh -L 8888:10.1.6.XX:8080 -i {wisteriaへの秘密鍵のパス} {自身のユーザーID}@wisteria.cc.u-tokyo.ac.jp

ローカルのポート : 8888     ★任意のポート番号を指定

リモート側ホスト : 10.1.6.XX:8080 ★code serverを起動したノードとポート番号を指定

アクセス     : http://localhost:8888/login

PWが要求されるので, 先に表示したPWで入れる

## 発行した自己証明書の登録方法(chrome)
code-server --certで作成した証明書が自己証明書であることに起因して、上記までの方法でcode-serverを作成しても.ipynbをJupyter Notebookの形式で編集できない等のerrorが起こります。chromeを使用している場合には、以下の通り証明書を登録してください。
0. 自己署名証明書を自身のクライアントPCに転送する
 1. メニューから「設定」を開く。
 2. 左側のメニューから「プライバシーとセキュリティ」をクリックする。
 3. 「セキュリティ」をクリックする。
 4. 「証明書の管理」をクリックする。
 5. 証明書ダイアログが表示される。
 6. 「信頼されたルート証明機関」タブを選択し、「インポート」をクリックする。
 7. インポートウィザードに従って、証明書ファイル(~/.local/share/code-server/localhost.crt)をアップロードする。
 8. 証明書ファイルをアップロードした後、ブラウザを再起動して設定を反映させる。