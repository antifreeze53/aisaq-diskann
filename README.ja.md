# AiSAQ-DiskANN

AiSAQ（All-in-Storage ANNS with Product Quantization）は、スケーラブルでDRAMを使わない近似最近傍探索（ANNS）の手法です。
全てのPQベクトルをノード内にインラインで保持して高速化するか、必要に応じてオンデマンドで読み込むことでコストを抑えるか、その中間の設定を自由に選べます。
本コードは[Microsoft DiskANN](https://github.com/Microsoft/DiskANN)のフォークです。インデックス探索は[arXiv論文](https://arxiv.org/abs/2404.06004)で詳述されています。

### AiSAQ-DiskANNで追加された機能
1. スケーラブルでDRAMを使わない探索 - ディスクインデックス検索中にPQベクトルをDRAMに読み込まず、必要なときだけメディアから取得します。
2. インラインPQベクトル - 一部または全部のPQベクトルをインデックスノードに持たせることでI/O回数を削減。
3. ベクトル並び替え - 探索時の読み込み回数を最小化するための最適なベクトル配置。
4. 複数エントリポイント - 反復回数を減らすため複数のエントリポイントを生成。
5. ベクトルビーム幅 - 探索ごとの使用ノード数を調整することで、PQベクトル読み込みのI/Oを並列化。
6. 貪欲探索アルゴリズムの改善。
7. 静的PQキャッシュ - 探索前に作成される共有キャッシュ。
8. 動的PQリとードキャッシュ - スレッドごのLRU付きページキャッシュ。

追加のAiSAQインデックスの使い方は以下参照：

- [SSDベースインデックスの構築／検索コマンドライン](workflows/AiSAQ_index.md)

#### インストール補足
`liburing`を非同期読み込みに使うので、`liburing-dev`を必ずインストールしてください。
```bash
sudo apt install liburing-dev
```
`aio-max-nr`を拡張する必要があるかもしれません。`/etc/sysctl.conf`に以下を追加：
```bash
fs.aio-max-nr = 1048576
```
設定を反映させるには：
```bash
sysctl -p /etc/sysctl.conf
```

#### 論文引用
```
@misc{aisaq-diskann,
    author = {Shimon Tsalmon, Kento Tatsuno, Daisuke Miyashita},
    title = {AiSAQ-DiskANN: Scalable implementation for ANNS based on DiskANN},
    url = {https://github.com/KioxiaAmerica/aisaq-diskann},
    year = {2025}
}
```

# DiskANN

[![DiskANN Main](https://github.com/microsoft/DiskANN/actions/workflows/push-test.yml/badge.svg?branch=main)](https://github.com/microsoft/DiskANN/actions/workflows/push-test.yml)
[![PyPI version](https://img.shields.io/pypi/v/diskannpy.svg)](https://pypi.org/project/diskannpy/)
[![Downloads shield](https://pepy.tech/badge/diskannpy)](https://pepy.tech/project/diskannpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![DiskANN Paper](https://img.shields.io/badge/Paper-NeurIPS%3A_DiskANN-blue)](https://papers.nips.cc/paper/9527-rand-nsg-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node.pdf)
[![DiskANN Paper](https://img.shields.io/badge/Paper-Arxiv%3A_Fresh--DiskANN-blue)](https://arxiv.org/abs/2105.09613)
[![DiskANN Paper](https://img.shields.io/badge/Paper-Filtered--DiskANN-blue)](https://harsha-simhadri.org/pubs/Filtered-DiskANN23.pdf)

DiskANNはリアルタイムの更新やフィルターをサポートする大規模ベクトル探索のための、スケーラブルで精度もコスト効率も高い近似最近傍探索のスイートです。
本コードは[DiskANN](https://papers.nips.cc/paper/9527-rand-nsg-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node.pdf)、[Fresh-DiskANN](https://arxiv.org/abs/2105.09613)、[Filtered-DiskANN](https://harsha-simhadri.org/pubs/Filtered-DiskANN23.pdf)のアイデアに基づいてさらに改良を加えています。
このコードは[NSG](https://github.com/ZJULearning/nsg)アルゴリズムから派生しました。

本プロジェクトは[Microsoftオープンソース行動規範](https://opensource.microsoft.com/codeofconduct/)を採用しています。
詳細は[行動規範FAQ](https://opensource.microsoft.com/codeofconduct/faq/) を参照、または[email](mailto:opencode@microsoft.com)で問い合わせてください。

貢献を希望する方は[CONTRIBUTING.md](CONTRIBUTING.md)のガイドラインを確認してください。

## Linuxでのビルド

以下パッケージを`apt`でインストール：
```bash
sudo apt install make cmake g++ libaio-dev libgoogle-perftools-dev clang-format libboost-all-dev
```

### Intel MKLの導入
#### Ubuntu 20.04以降
```bash
sudo apt install libmkl-full-dev
```

#### 以前のUbuntu
[oneAPI MKL installer](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html)から入手するか、[apt](https://software.intel.com/en-us/articles/installing-intel-free-libs-and-python-apt-repo)を利用（動作確認済み：2019.4-070 と 2022.1.2.146）。
```bash
# OneAPI MKL Installer
wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18487/l_BaseKit_p_2022.1.2.146.sh
sudo sh l_BaseKit_p_2022.1.2.146.sh -a --components intel.oneapi.lin.mkl.devel --action install --eula accept -s
```

### ビルド手順
```bash
mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j 
```

## Windowsでのビルド

Visual Studio 2022/2019/2017 Enterpriseで動作確認済み。Community/Professional版でも同様に動く想定です。

**必要条件：**

* CMake 3.15+（Visual Studio 2019以降に同梱、または https://cmake.org から）
* NuGet.exe（https://www.nuget.org/downloads から取得）
* ビルドスクリプトはNuGet経由でMKL、OpenMP、Boostを取得。
* DiskANNリポジトリとサブモジュール。クローン後に以下を実行：
```
git submodule init
git submodule update
```
* 環境変数：
  * 任意：`windows/packages.config.in`のBoostを上書きしたい場合、`BOOST_ROOT`を設定。

**ビルド手順：**
* Visual Studioの「x64 Native Tools Command Prompt」を開き、DiskANNフォルダーへ移動
* `build`ディレクトリを作成
* `build`内で以下を実行
```
cmake ..
```
Visual Studio 2017以前の場合：
```
<フルパス>\cmake ..
```
**これで`diskann.sln`ソリューションが生成される**。以降：

- Visual Studioから開いてRelease/Debugをビルド
- `<フルパス>\cmake --build build`
- MSBuildを利用：
```
msbuild.exe diskann.sln /m /nologo /t:Build /p:Configuration="Release" /property:Platform="x64"
```

* gperftoolsサブモジュール（libtcmalloc_minimal）もビルドされる。
* 出力バイナリは`x64/Release`または`x64/Debug`に出る。

## 使い方

コンパイル済みコードの利用例：

- [SSDインデックス構築／検索](workflows/SSD_index.md)
- [メモリ内インデックス構築／検索](workflows/in_memory_index.md)
- [ストリーミングインデックス](workflows/dynamic_index.md)
- [ラベル付き/フィルター付きメモリインデックス](workflows/filtered_in_memory.md)
- [ラベル付き/フィルター付きSSDインデックス](workflows/filtered_ssd_index.md)
- [diskannpy（Python拡張）](python/README.md)

引用も同じく：
```
@misc{diskann-github,
   author = {Simhadri, Harsha Vardhan and Krishnaswamy, Ravishankar and Srinivasa, Gopal and Subramanya, Suhas Jayaram and Antonijevic, Andrija and Pryce, Dax and Kaczynski, David and Williams, Shane and Gollapudi, Siddarth and Sivashankar, Varun and Karia, Neel and Singh, Aditi and Jaiswal, Shikhar and Mahapatro, Neelam and Adams, Philip and Tower, Bryan and Patel, Yash}},
   title = {{DiskANN: Graph-structured Indices for Scalable, Fast, Fresh and Filtered Approximate Nearest Neighbor Search}},
   url = {https://github.com/Microsoft/DiskANN},
   version = {0.6.1},
   year = {2023}
}
```



