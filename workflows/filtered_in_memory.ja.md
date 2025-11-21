**フィルター付きメモリ内インデックスの使い方**
================================

DiskANN には `filtered-vamana` と `stitched-vamana` の2種類があり、`apps/build_memory_index`/`apps/build_stitched_index` で構築。  
共通引数：`--data_type`、`--dist_fn`、`--data_file`、`--index_path_prefix`、`-R`、`-L`、`--alpha`、`-T`。`filtered-vamana` では `--build_PQ_bytes`/`--use_opq` も指定可能。`--label_file` には各点に対応するラベル（CSV 形式）を渡し、`--universal_label` で任意フィルターを許可する。`--FilteredLbuild` はフィルタ用の `L`。

**stitched-vamana** では上記に加え `--Stitched_R` で最終的な次数を制御。

## 各種ファイル
* `apps/utils/compute_groundtruth` で ground truth を生成。`--label_file`/`--filter_label`/`--universal_label` を合わせる。
* `apps/search_memory_index` で `--filter_label` を渡して検索し、`--Lg` で複数 `L` を試す。

## SIFT10K 例
1. SIFT10K データを `fvecs_to_bin` で `.bin` に変換。  
2. `generate_synthetic_labels` で 50 ラベルの Zipf 分布ファイルを作成（0 は universal）。`stats_label_data` で確認。  
3. `compute_groundtruth`（`--filter_label 35`）→ `build_memory_index`/`build_stitched_index` でフィルター付き＆stitched インデックスをビルド。  
4. `search_memory_index` に `-L 10 20 30 40 50 100`、`-K 10`、`--filter_label 35` でベンチ。
5. 結果表に `qps`/`Mean Latency`/`Recall@10` が各 `L` について示されており、filtered より stitched の方が recall が低い（11%〜23%）という傾向。

