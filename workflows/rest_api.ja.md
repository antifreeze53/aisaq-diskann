**DiskANN インデックスを REST で公開する**
=======================================================================

## 依存関係とビルド（Ubuntu）
README の共通依存に加えて、[Microsoft C++ REST SDK](https://github.com/Microsoft/cpprestsdk) をインストール。

```bash
sudo apt install libcpprest-dev
mkdir -p build && cd build
cmake -DRESTAPI=True -DCMAKE_BUILD_TYPE=Release ..
make -j
```

## インデックス公開サービスの起動
メモリ内 or SSD インデックスを構築したあと、適切なIP:portでサービスを立ち上げる。
ローカルからなら `http://127.0.0.1:port`、外部からアクセスするなら `http://0.0.0.0:port` など。

```bash
# メモリ内インデックス用
./apps/restapi/inmem_server --address <http://ip_addr:port> --data_type <float/int8/uint8> --data_file <data_file> --index_path_prefix <index_file> --num_threads <number of threads> --l_search <L値> --tags_file [tags_file]

# SSDインデックス用
./apps/restapi/ssd_server --address <http://ip_addr:port> --data_type <float/int8/uint8> --index_path_prefix <index_file_prefix> --num_nodes_to_cache <キャッシュノード数> --num_threads <thread数> --tags_file [tags_file]
```

`data_type`/`data_file` は構築時と一致させ、タグファイルがあれば各ベクトルに文字列を対応させた検索結果を返せる。SSD 版では `num_nodes_to_cache` や `num_threads` で I/O/CPU を調整。複数インデックスを束ねるには、プレフィックスを1行ずつ並べたファイルを `index_prefix_paths` パラメータに渡す `multiple_ssdserver` を使う。

## クエリの投げ方
JSON リクエストを POST するだけ：

```json
{
  "Ls": 256,
  "query_id": 1234,
  "query": [0.00407, 0.01534, 0.02498, ...],
  "k": 10
}
```

Python で送信する例：

```python
import requests
jsonquery = {"Ls": 256,
             "query_id": 1234,
             "query": [...],
             "k": 10}

response = requests.post('http://ip_addr:port', json=jsonquery)
print(response.text)
```

レスポンスは距離・インデックス・ (複数インデックス構成なら) `partition`、`tags`（有効なら）、処理時間 `time_taken_in_us` を含む。

## ファイルから複数クエリを投げる CLI
```bash
client ip_addr:port data_type<float/int8/uint8> query_file num_queries Ls
```

