**動的インデックスの使い方**
================================

「動的」インデックスは挿入・削除をサポートし、`lazy delete` を使ったあと `consolidate_deletes` で空きスロットを再利用する。`apps/test_insert_deletes_consolidate` は初期構築・削除・挿入を指定して同時実行、`apps/test_streaming_scenario` はスライディングウィンドウ＋挿入削除のストリーミングをシミュレートする。

## `apps/test_insert_deletes_consolidate` の引数
1. **`--data_type`**：float/int8/uint8。  
2. **`--dist_fn`**：`l2`/`mips`。  
3. **`--data_file`**：`.bin`データ。  
4. **`--index_path_prefix`**：出力プレフィックス。  
5. **`-R`**：最大次数。  
6. **`-L`**：ビルド時の L。  
7. **`--alpha`**：グラフ直径。  
8. **`-T`**：スレッド数。  
9. **`--points_to_skip`**：先頭からスキップ。  
10. **`--max_points_to_insert`**：最大サイズ。  
11. **`--beginning_index_size`**：初期構築点数。  
12. **`--points_per_checkpoint`**：更新バッチサイズ。  
13. **`--checkpoints_per_snapshot`**：スナップショット間隔（逐次更新時）。  
14. **`--points_to_delete_from_beginning`**：挿入順序で削除する点数。  
15. **`--start_point_norm`**：初期ノードを球面上のランダム点に。  
16. **`--do_concurrent`**：挿入と削除を並列実行（半数スレッドずつ）。

## `apps/test_streaming_scenario` の引数
1.〜14. は `test_insert...` と同様（`--insert_threads`/`--consolidate_threads`/`--active_window`/`--consolidate_interval` など追加）。  
15. **`--max_points_to_insert`**：挿入最大。  
16. **`--active_window`**：アクティブ点数。  
17. **`--consolidate_interval`**：挿入・削除の間隔。  
18. **`--start_point_norm`**：最初の点を球面上に。  

### フィルター付きビルドのオプション
* `--label_file`：各点のフィルター。  
* `--FilteredLbuild`：フィルタ用の L。  
* `--num_start_points`：固定点数。  
* `--universal_label`：任意フィルター。  
* `--label_type`：`uint`/`short`。

## 検索（`apps/search_memory_index`）
1.〜9. は `in_memory_index` と共通。  
10. **`--dynamic`**：動的インデックス。  
11. **`--tags`**：タグ付き検索。  
12. **`--filter_label`**：フィルター検索。  

## BIGANN ストリーミング例
1. `sift_learn.fbin` の最初 50,000 点で構築。  
2. 各 25,000 点を削除／挿入しながら `consolidate`。  
3. `compute_groundtruth` → `search_memory_index --dynamic true --tags 1` で結果確認。  

## フィルター付きストリーミング例
* 50 個ラベルの合成ラベル `generate_synthetic_labels` で作成（Zipf 分布）。  
* `test_streaming_scenario` に `--label_file`/`--universal_label` を渡してフィルタ付き構築。  
* `compute_groundtruth_for_filters` → `search_memory_index --filter_label ... --dynamic true --tags 1` で評価。

