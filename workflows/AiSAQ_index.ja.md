**AiSAQ インデックスの使い方**
===========================

## AiSAQ インデックス構築（`apps/build_disk_index`）
`--use_aisaq` を付けると PQ を必要に応じてオンデマンドで読み込む AiSAQ インデックスを生成。追加引数：  
1. **`--use_aisaq`**：AiSAQ 構築を有効化。  
2. **`--inline_pq`**（デフォルト `R`）: ノード内にインラインで保持する PQベクトル数。`R`（全量）または `-1`（ファイルサイズ維持の上限）。`-1〜R` の範囲。  
3. **`--rearrange`**：読み込み時の I/O を減らすようベクトルを再配置。`inline_pq` で全量を保存した場合は無視。  
4. **`--num_entry_points`**：検索開始ノード数（1〜1000）。`use_aisaq` 有効時のみ。  

### 補足
- `use_aisaq` を付けると DiskANN インデックス（通常版）は出力されない。  
- `use_aisaq` だけ有効なら旧バージョン（tag 0.1.0）相当。  
- DiskANN → AiSAQ 変換ツールは提供されない。

## AiSAQ 検索（`apps/search_disk_index`）
1. **`--use_aisaq`**：AiSAQ 用検索。  
2. **`--pq_read_io_engine`**：`aio` か `uring`（デフォルト `aio`）。  
3. **`-V (--vector_beamwidth)`**：`W` 以下のベクトルビーム幅。  
4. **`--pq_cache_size`**：PQ ベクトルキャッシュの DRAM サイズ（B/K/M/G/%）。  
5. **`--pq_read_page_cache_size`**：スレッドごとのページキャッシュ（最大 32MiB）。`rearrange` オプション付きで有効。  

### 補足
- `use_aisaq` を指定せず検索すれば、PQ ベクトルは DRAM へ読まれる普通のモード。  
- 古い AiSAQ インデックス（tag 0.1.0）も自動検出して検索可能。  
- フィルター付きで rearrange された AiSAQ インデックスはサポート外。

## 例
- **ビルド**：`./apps/build_disk_index … --use_aisaq --inline_pq 32 --rearrange` など。`--inline_pq -1` で自動最適化、`--num_entry_points 512` も指定可能。  
- **検索**：`./apps/search_disk_index … --use_aisaq --pq_read_io_engine uring -V 2 --pq_read_page_cache_size 4M` や `--use_aisaq` のみで既存 DiskANN 風に探す例。

