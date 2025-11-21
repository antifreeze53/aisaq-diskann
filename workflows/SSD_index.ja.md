**SSDベースインデックスの使い方**
===============================

SSDフレンドリーなインデックスを作るには、`apps/build_disk_index`を使います。
-------------------------------------------------------------------------------

引数は次の通り：

1. **--data_type**: 構築対象データの型。float（32bit）、signed int8、unsigned uint8に対応。データ型ごとに適切な型で読み込みます（int8_t, uint8_t, float）。
2. **--dist_fn**: 距離関数。cosine、l2（最小ユークリッド）、mips（最大内積）を選択。
3. **--data_file**: .bin形式の入力データ。先頭4バイトが点数、次の4バイトが次元数、以降 `n*d*sizeof(T)` バイトにデータ本体。`sizeof(T)`はbyte型なら1、floatなら4。
4. **--index_path_prefix**: 生成されるファイル全てに共通するプレフィックス。例：`~/index_test`を指定すると `~/index_test_pq_pivots.bin` など 8〜10個のファイルが作成される。
5. **-R (--max_degree)**（デフォルト64）: グラフの最大次数。大きいほど高品質だが時間・容量が増す。R以上の数値を選ぶのが無難。
6. **-L (--Lbuild)**（デフォルト100）: ビルド中の探索リストサイズ。75〜200程度。大きいほど高速検索だが時間が増える。
7. **-B (--search_DRAM_budget)**: 検索時のメモリ上限（GB）。指定したRAM内で収まるようデータを圧縮。
8. **-M (--build_DRAM_budget)**: ビルド中のRAM上限（GB）。足りなければ分割ビルドで対応（1.5倍程度遅くなる可能性）。
9. **-T (--num_threads)**（デフォルトは`get_omp_num_procs()`）: ビルド用スレッド数。コア数に応じてほぼ線形で高速化。
10. **--PQ_disk_bytes**（デフォルト0）: SSD上に保管する各点のバイト数。0なら非圧縮表示。大きいほどリコールは上がるが容量増。
11. **--build_PQ_bytes**（デフォルト0）: PQ圧縮によるビルド短縮。
12. **--use_opq**: OPQを使うフラグ。高次元で効率的だが時間は少し増える。

SSDインデックスを検索するときは`apps/search_disk_index`を使います。
-------------------------------------------------------------------

引数：

1. **--data_type**: インデックス構築時と同じデータ型。
2. **--dist_fn**: 駆使する距離関数（l2またはmips）。
3. **--index_path_prefix**: 構築時と同じプレフィックス。
4. **--num_nodes_to_cache**（デフォルト0）: 頻繁に使うノードをメモリにキャッシュ。パフォーマンス向上。
5. **-T (--num_threads)**（デフォルト`get_omp_num_procs()`）: 検索に用いるスレッド数。一スレッドあたり1クエリ。
6. **-W (--beamwidth)**（デフォルト2）: 各探索反復での最大I/O数。大きいほどI/Oラウンドトリップが減るが、1クエリの総I/Oは増える可能性。W=1でスループット最大、W=4~8ならレイテンシを優先。0ならスレッド数に応じて自動調整（その分チューニング）。
7. **--query_file**: `--data_type`と同じバイナリ形式のクエリファイル。
8. **--gt_file**: クエリごとのグラウンドトゥルース。形式：4バイトn、4バイトd、n*d個のID（int）、n*d個の距離（float）。存在しないときは`apps/utils/compute_groundtruth`で生成。「null」を指定するとリコール計測なし。
9. **K**: 何個の近傍を検索するか。検索結果との交差（Recall@K）を計測。
10. **result_output_prefix**: 出力ファイルのプレフィックス。
11. **-L (--search_list)**: 検索する際のリストサイズ。大きいほど高精度だが遅くなる。K以上を指定。


### BIGANNによる例

以下はBIGANNデータセット（SIFT128）100Kサンプルの流れです。

1. データをダウンロード・展開・bin変換。
```bash
mkdir -p DiskANN/build/data && cd DiskANN/build/data
wget ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz
tar -xf sift.tar.gz
cd ..
./apps/utils/fvecs_to_bin float data/sift/sift_learn.fvecs data/sift/sift_learn.fbin
./apps/utils/fvecs_to_bin float data/sift/sift_query.fvecs data/sift/sift_query.fbin
```

2. グラウンドトゥルースを計算。
```bash
./apps/utils/compute_groundtruth --data_type float --dist_fn l2 --base_file data/sift/sift_learn.fbin --query_file data/sift/sift_query.fbin --gt_file data/sift/sift_query_learn_gt100 --K 100
```

3. インデックス構築。
```bash
# 0.003GBの検索メモリバジェット（100K点、32バイトPQ）
./apps/build_disk_index --data_type float --dist_fn l2 --data_path data/sift/sift_learn.fbin --index_path_prefix data/sift/disk_index_sift_learn_R32_L50_A1.2 -R 32 -L 50 -B 0.003 -M 1
```

4. 検索と結果出力。
```bash
./apps/search_disk_index --data_type float --dist_fn l2 --index_path_prefix data/sift/disk_index_sift_learn_R32_L50_A1.2 --query_file data/sift/sift_query.fbin --gt_file data/sift/sift_query_learn_gt100 -K 10 -L 10 20 30 40 50 100 --result_path data/sift/res --num_nodes_to_cache 10000
```

リモートSSDでは遅くなる可能性あり。出力にはクエリスループット、平均/99.9パーセンタイルレイテンシ、`L`ごとの平均4KB I/O、CPU時間、Recall@10などが表示されます。

```
    L   Beamwidth             QPS    Mean Latency    99.9 Latency        Mean IOs         CPU (s)       Recall@10
======================================================================================================================
    10           2        27723.95         2271.92         4700.00            8.81           40.47           81.79
    20           2        15369.23         4121.04         7576.00           15.93           61.60           96.42
    30           2        10335.75         6147.14        11424.00           23.30           74.96           98.78
    40           2         7684.18         8278.83        14714.00           30.78           94.27           99.40
    50           2         6421.66         9913.28        16550.00           38.35          116.86           99.63
   100           2         3337.98        19107.81        29292.00           76.59          226.88           99.91
```



