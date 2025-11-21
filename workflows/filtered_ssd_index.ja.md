**フィルター付き SSD インデックスの使い方**
================================

## SSD ベースの filtered-vamana
`apps/build_disk_index` を使い、`--label_file`/`--universal_label`/`--filter_threshold` などを設定。主な引数：  
1. `--data_type`、`--dist_fn`、`--data_file`（`.bin`）  
2. `--index_path_prefix`（プレフィックス）  
3. `-R`、`-L`、`-B`、`-M`（ビルド／検索用 RAM 予算）  
4. `--PQ_disk_bytes`/`--build_PQ_bytes`/`--use_opq`（PQ 圧縮設定）  
5. `--label_file`：各点に対するフィルター  
6. `--universal_label`：任意フィルター  
7. `--FilteredLbuild`：フィルター用の検索リストサイズ  
8. `--filter_threshold`：密なノードを分割するしきい値

## ground truth
`compute_groundtruth` に `--label_file`/`--filter_label`/`--universal_label` を渡すとフィルター付き ground truth を生成。`--gt_file` には `n`, `d`, 整数ID, 距離を順に書く。

## 検索（`apps/search_disk_index`）
1. `--data_type`、`--dist_fn`、`--index_path_prefix`  
2. `--num_nodes_to_cache`（SSD 版キャッシュ）  
3. `-T`、`-W`（beamwidth）、`-L`（複数指定）  
4. `--query_file`、`--gt_file`  
5. `--filter_label`：フィルター検索時に必要  
6. `--result_path`：出力プレフィックス  

## SIFT10K フィルター例
1. `siftsmall` データを `fvecs_to_bin` で変換。  
2. `rand_labels_50_10K.txt` を `generate_synthetic_labels` で作る（Zipf 分布）。  
3. `compute_groundtruth`（`--filter_label 35`）  
4. `build_memory_index`, `build_stitched_index`, `search_memory_index` でカバーしつつ、フィルター付き SSD 検索は `search_disk_index` で `-W 4 -T 8`、`--filter_label 35`。  
5. 結果には `L` ごとの `QPS`/`Mean Latency`/`Mean IOs`/`Recall@10`（最低 11.8%、最大 23.9%）が示される。

