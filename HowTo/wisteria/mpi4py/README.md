# mpi4py
## mpiとは
ノード間での通信を可能にして、ノード間の並列計算を可能にする
特にwisteria odysseyにおいて重要である

## mpi4pyとconcurrentfutureの違い
mpi4py → ノード間での並列計算
concurrent.future → ノード内での並列計算(コア単位)

例えば、10個のCPUをして、それぞれに仕事をさせたいのであればmpi4py (wisteria)
1個のCPU上で並列計算をしたいのであればconcurrent.future (onpremise) 

mpi4pyを使用してからconcurrent.futureを使用することは可能

## 環境構築
付属のshellscriptを参考

## 実行コード
付属の実行用shとpyを参考
実際にそれぞれのノードにcsvを読み込ませて処理をさせている
