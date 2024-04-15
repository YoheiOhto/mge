# venv を使用した仮想環境構築
ここでは、wisteria-aにおけるvenvでの仮想環境構築を行います。

* 利用手引書
利用手引書は利用支援ポータル (https://wisteria-www.cc.u-tokyo.ac.jp/) の「ドキュメント閲覧」より入手することが可能。
「ドキュメント閲覧」→「Wisteria/BDEC-01利用手引書 →「Wisteria/BDEC-01システム利用手引書」

## venvの解説
venvは仮想環境を構築するために、python3.6以降に搭載されたモジュールです。
基本的に
python3 -m venv ohto_test_o --clear
を使用して新しく仮想環境をたてて。

source ohto_test_o/bin/activate
を使用して仮想環境に接続して使用します。