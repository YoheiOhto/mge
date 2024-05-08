# docker + code-server + pyenv
dockerのコンテナ上でcode-serverを立て, 普段のvscode likeな環境と同じように開発できるようにしたもの, GPU版  
本年度のsetupからCUDAをインストールしなくなったため、これまでのcoder_gpuとはimageを変えている

# 対象
- vscode上でできることを計算機サーバー上でやりたい人  
- ユーザビリティが高いのでビギナー・玄人問わず  
- ただしクライアントPCを計算の間つけっぱなしにしてもいい人  

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
- 240508_coder_gpuフォルダを使用したいディレクトリに配置する  
    - だいたいは```/home/{計算機名}/{user名}/{各自の名前}/coder_gpu```といった形なはず  
    - scp辺りで転送しておく  


***
# HowToUse (ビギナー向け, ショート版)
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
4. ポートフォワード  
    - ```ssh -L 8080:localhost:8888 -p 491XX -i C:\Users\tadahaya\.ssh\id_rsa_XXX parentX@133.11.XX.XX```
    - ```ssh -L 8888:localhost:8888 hiegm4```
    - win側にてpowershellを立てて上記を入力  
    - 手段はなんでもよいが, powershellの場合はもう一つ立てて行う点に注意 (ssh接続とポートフォワードは別立て)  
5. ```localhost:8080```にwinのブラウザでアクセスして解析開始  
6. 解析後, コンテナを終了する  
    - ```docker compose down```  
    - ssh接続した計算機サーバー側で行う, docker-compose.ymlがあるdir (coder)で行う  


***
# HowToUse (詳細版)
- ポートが計6種類出てくるので違いを把握すること  
    - コンテナが晒すポート  
    - 計算機がコンテナを受けるポート  
    - 親機が計算機を受けるポート
    - 計算機がssh接続用に開けているポート
    - 親機がssh接続用に開けているポート
    - クライアントが親機を受けるポート
- 基本的にユーザーが弄る部分は.env, ctn内のrequirements.txtのみ  
1. .env内の書き換え  
    - 最低限bind先(BIND_SRC)を書き換える  
        - bind先: 計算機サーバー内のパス, コンテナ内のデータを永続化するため  
        - ホストマシンに合わせて書き換える  
        - 第一選択: ```/mnt/data1```などのマウントされたstorage用ディスク(外付けも可), 容量の心配が減る  
        - 第二選択: ```/home/[ホストのユーザー名]```, 手軽だが扱うデータ量によっては起動ディスクが死ぬ  
    - 基本不要だが必要に応じてHOST_PORTとBROWSER_PW, PYTHON_VERを変更する  
        - 複数のdocker composeをrunしたい場合はHOST_PORTを分ける必要がある
        - .envでHOST_PORTで定義したポート = 計算機がコンテナを受けるポート 
2. 必要に応じてDockerfile内のpythonの部分などを弄って好きなモジュールを入れたりする  
    - ctn内のrequirements.txtに記入するだけ  
3. windows powershellを立てるなりしてsshで計算機サーバーへアクセス  
    - ```ssh -i C:\Users\[winのユーザー名]\.ssh\[秘密鍵名] -p [親機のSSHポート] [親機のユーザー名]@[親機のIP]```
    - ```ssh [計算機のユーザー名] ```
    - 具体例: ```ssh -i C:\Users\tadahaya\.ssh\id_rsa_XXXX -p 491XX parentX@133.11.XXX.XXX```
    - ```ssh hiegm4```  
4. ```docker compose up -d```でコンテナ立てる
    - ssh接続した計算機サーバー側で行う, docker-compose.ymlがあるdir (coder)で行う  
    - 初回の場合は```--build```オプションをつけなくてもimageを作成される
6. もう一つpowershellなりを立てて, ポートフォワード  
    - ```ssh -L [ブラウンジグ用のポート]:localhost:[親機が計算機を受けるポート] -p [親機のSSHポート] -i C:\Users\[winのユーザー名]\.ssh\[秘密鍵名] [親機のユーザー名]@[親機のIP]```
    - ```ssh -L  [親機が計算機を受けるポート]:localhost:[計算機がコンテナを受けるポート] [計算機のユーザー名]```
    -具体例 ```ssh -L 8080:localhost:8888 -p 491XX -i C:\Users\tadahaya\.ssh\id_rsa_XXX parentX@133.11.XX.XX```
    - ```ssh -L 8888:localhost:8888 hiegm4```
7. winのブラウザに```localhost:[ブラウジング用のポート]```を打ち込むとアクセスできる  
    - 具体例: ```localhost:8080```
    - pwはdefaultだとcs24771になっている (.envから読み込むので打ち込む必要はない)  
    - 基本このままでいいと思うが, 細かいことを言うとセキュリティが気になりどころらしい  

***
# 更新
- 220730  
  - v0.1.0, 全体構成の変更  
-  220609  
  - docker-composeのバージョンを更新し, .envを導入
- 240508
  - 2024年の環境に最適化　(大戸陽平)

***
# 参考
[メイン](https://qiita.com/YKIYOLO/items/06cf44dead84188677ae)  
[docker-composeのインストール](https://qiita.com/kottyan/items/c892b525b14f293ab7b3)  
[docker-composeをWSL2に入れる](https://zenn.dev/taiga533/articles/11f1b21ef4a5ff)  
[WSL2にssh接続する](https://qiita.com/yuta-katayama-23/items/fad6928f37badf3391f2)  
[WSL2にssh接続する2](https://scratchpad.jp/ubuntu-on-windows11-5/)  
- 普通のlinuxマシン的に扱えばOKっぽい  
