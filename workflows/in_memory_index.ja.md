**メモリ内インデックスの使い方**
================================

## インデックス構築（`apps/build_memory_index`）
1. **`--data_type`**：float/int8/uint8 から選択。  
2. **`--dist_fn`**：`l2`または`mips`。  
3. **`--data_file`**：`.bin`形式のデータ（先頭4バイトが点数、次の4バイトが次元、残りが生データ）。  
4. **`--index_path_prefix`**：出力ファイルのプレフィックス。  
5. **`-R (--max_degree)`**：グラフの最大次数（通常32〜150）。  
6. **`-L (--Lbuild)`**：ビルド中の探索リストサイズ（75〜400、`R` 以上推奨）。  
7. **`--alpha`**：1.0〜1.5 の範囲でグラフ直径を決定。  
8. **`-T (--num_threads)`**：ビルド用スレッド数（デフォルトはコア数）。  
9. **`--build_PQ_bytes`**：PQ 圧縮によるビルド高速化。  
10. **`--use_opq`**：OPQ を使うか（高次元で効果あり）。

## 検索（`apps/search_memory_index`）
1. **`data_type`**：構築時と同じ型。  
2. **`dist_fn`**：`l2`/`mips`（`fast_l2` もあり）。  
3. **`memory_index_path`**：ビルド済みインデックス。  
4. **`T`**：検索スレッド数。  
5. **`query_bin`**：`.bin`形式のクエリ。  
6. **`truthset.bin`**：`compute_groundtruth` で生成（`null` も可）。  
7. **`K`**：近傍数（Recall@K）。  
8. **`result_output_prefix`**：出力プレフィックス。  
9. **`-L (--search_list)`**：検索リストサイズ。`K` 以上。

## BIGANN の例（100K SIFT）
1. データ変換：
    ```bash
    mkdir -p DiskANN/build/data && cd DiskANN/build/data
    wget ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz
    tar -xf sift.tar.gz
    cd ..
    ./apps/utils/fvecs_to_bin float data/sift/sift_learn.fvecs data/sift/sift_learn.fbin
    ./apps/utils/fvecs_to_bin float data/sift/sift_query.fvecs data/sift/sift_query.fbin
    ```
2. グラウンドトゥルース生成 / インデックス構築 / 検索：`workflows/SSD_index.ja.md` と同じ `compute_groundtruth` → `./apps/build_memory_index ...` → `./apps/search_memory_index ...` で `-L 10 20 30 40 50 100` の性能表が表示される。

