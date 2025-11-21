# diskannpy

[![DiskANN Paper](https://img.shields.io/badge/Paper-NeurIPS%3A_DiskANN-blue)](https://papers.nips.cc/paper/9527-rand-nsg-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node.pdf)
[![DiskANN Paper](https://img.shields.io/badge/Paper-Arxiv%3A_Fresh--DiskANN-blue)](https://arxiv.org/abs/2105.09613)
[![DiskANN Paper](https://img.shields.io/badge/Paper-Filtered--DiskANN-blue)](https://harsha-simhadri.org/pubs/Filtered-DiskANN23.pdf)
[![DiskANN Main](https://github.com/microsoft/DiskANN/actions/workflows/push-test.yml/badge.svg?branch=main)](https://github.com/microsoft/DiskANN/actions/workflows/push-test.yml)
[![PyPI version](https://img.shields.io/pypi/v/diskannpy.svg)](https://pypi.org/project/diskannpy/)
[![Downloads shield](https://pepy.tech/badge/diskannpy)](https://pepy.tech/project/diskannpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## インストール
PyPI に公開されているパッケージは常に最新の numpy major.minor リリース（現時点では 1.25）でビルドされます。

numpy 1.19〜1.25 向けの Conda パッケージは今後対応予定です。それまではリポジトリをクローンして自分でビルドしてください。

## ローカルビルド手順
必須のシステム依存や要件は [プロジェクト README](https://github.com/microsoft/DiskANN/blob/main/README.md) を参照して準備してください。

ライブラリと実行ファイルのビルドが完了すれば、以下の手順で `diskannpy` もビルド可能です。

### numpy バージョンの変更
DiskANN ルートにある `pyproject.toml` の `[build-system.requires]` セクションと `[project.dependencies]` セクションの両方で numpy バージョンを一致させてください。

#### Linux
```bash
python3.11 -m venv venv  # python3.9 以降なら動くはず
source venv/bin/activate
pip install build
python -m build
```

#### Windows
```powershell
py -3.11 -m venv venv  # python3.9 以降なら動くはず
venv\Scripts\Activate.ps1
pip install build
python -m build
```

ビルド後の wheel は DiskANN ルートの `dist` ディレクトリに置かれるので、`pip install dist/<wheel 名>.whl` でインストールしてください。

## 引用
以下のように引用してください：
```
@misc{diskann-github,
   author = {Simhadri, Harsha Vardhan and Krishnaswamy, Ravishankar and Srinivasa, Gopal and Subramanya, Suhas Jayaram and Antonijevic, Andrija and Pryce, Dax and Kaczynski, David and Williams, Shane and Gollapudi, Siddarth and Sivashankar, Varun and Karia, Neel and Singh, Aditi and Jaiswal, Shikhar and Mahapatro, Neelam and Adams, Philip and Tower, Bryan and Patel, Yash}},
   title = {{DiskANN: Graph-structured Indices for Scalable, Fast, Fresh and Filtered Approximate Nearest Neighbor Search}},
   url = {https://github.com/Microsoft/DiskANN},
   version = {0.6.1},
   year = {2023}
}
```

