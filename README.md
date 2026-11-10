# cosmos-vector

Microsoft Build 2024 で発表された Azure Cosmos DB for NoSQL のベクトル検索（当時はプレビュー）を試したリポジトリです。

## 現状

2024-05-27 に作ったまま、更新していません。依存は requirements.txt で版を固定していません。

## 仕組み

1. Azure OpenAI の埋め込みモデルで、文章をベクトルにします。
2. ベクトルの列（`/contentvector`、1536 次元、コサイン距離、`quantizedFlat` の索引）を持つコンテナに保存します。
3. 質問文もベクトルにし、`VectorDistance` で近さを出して検索します。

| ファイル | すること |
| --- | --- |
| `add_data.py` | 見本の文章を埋め込んでコンテナに入れる |
| `main.py` | 「勤務規定について知りたい」でベクトル検索し、結果を表示する |
| `data/text.md` | 見本の文章（架空の社内規定） |
| `src/cosmosdb.py` | コンテナの作成、保存、ベクトル検索 |
| `src/vector.py` | Azure OpenAI で埋め込みを作る |

## 必要なもの

| 必要なもの | 用途 |
| --- | --- |
| Azure Cosmos DB for NoSQL のアカウント（ベクトル検索を有効にしたもの）とデータベース | 保存と検索。データベースは自動では作られないので、先に作っておく |
| Azure OpenAI の埋め込みモデル（1536 次元のもの） | 埋め込みの作成 |

設定は `.env.sample` を参考に `.env` に書きます。読み込む環境変数は [src/config.py](src/config.py) にあります。

## 動かし方

```bash
pip install -r requirements.txt
python add_data.py   # 下の「できないこと」を参照
python main.py
```

## できないこと

- `add_data.py` は、このままでは動きません。読み込むファイルが `./data/text.txt` になっている（実際は `data/text.md`）ことと、`CosmosDB` に無い `initialize()` を呼んでいる（あるのは `container_initialize()`）ためです。
- 検索の件数を絞らず、近い順にも並べていません（クエリに `TOP` と `ORDER BY` が無い）。保存した全件に距離を付けて返します。

## ライセンス

[MIT](LICENSE)
