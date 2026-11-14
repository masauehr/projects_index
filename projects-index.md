# projects_index（作成アプリ一覧）

作成したアプリを、公開版の一覧ページ（GitHub Pages）とリポジトリ README にまとめ、GitHub から簡単に飛べるようにするプロジェクト。2026-11-14 作成。

## 構成

| ファイル | 役割 |
|---|---|
| `projects.json` | 公開版の元データ。**公開リポジトリのみ**を記載する（private名は入れない） |
| `build.py` | `projects.json` から `README.md` と `index.html` を生成 |
| `README.md` | 公開版の一覧（自動生成・直接編集しない） |
| `index.html` | GitHub Pages 用の一覧。検索ボックスで絞り込み、ダーク対応、スマホ幅対応 |

## 公開版とローカル版の分離

- **公開版**: このリポジトリ（public）。公開リポジトリのみ。Pages ありはそちらを主リンク、無いものは GitHub リポジトリへリンク
- **ローカル版**: private・ローカルのみ・ツール類（公開一覧から除外）は、非公開側の別リポジトリで同じ形式のデータから Markdown を生成して管理（public にはこの内容を入れない）

## プロフィールからの導線

GitHub のプロフィール（`github.com/masauehr`）上部には、プロフィール用リポジトリ `masauehr/masauehr`（public）の README が表示される。ここに一覧ページ（`https://masauehr.github.io/projects_index/`）と `projects_index` へのリンクを置いている（個人情報は載せない）。

## 更新手順

1. `projects.json` にプロジェクトを追加・修正する（`repo` は GitHub のリポジトリ名。Pages があれば `pages` に URL）
2. `python3 build.py --intro "詳しくは [projects-index.md](projects-index.md) を参照"` を実行
3. `git add` → `git commit` → `git push`

ローカル版の生成は `--json` `--md` `--no-html` で別データを指定する。手書きの Markdown（Jupyter とローカルサーバーの起動ガイド）を一覧の先頭に差し込むには `--intro-file <ファイル>` を使う。ローカルサーバーを追加・変更したら、そのファイルも直す。

## 注意

- 新しい public リポジトリを作ったら `projects.json` に追加する（載せ忘れ防止）
- private リポジトリを public にしたときも追加する。逆に private 化したら `projects.json` から**必ず外す**
- フォルダ名とリポジトリ名が違うもの（例: `mobile_app` → `iphone-weather-app`）は、`repo` に GitHub 側の名前を書く
- `pages` は**実際に画面が開くURL**を書く。ルートに `index.html` が無いサイト（例: `weather_chart_vlm` は `webui/index.html`）はファイルまで指定する。画面が無いデータ配信用（例: `taiwan-radar-frames`）は `pages` を付けず GitHub リポジトリへリンクする。追加時は URL を実際に開いて確認する
- ツール類（共通部品・MCP補助など）と、公開アプリのないもの・作成中のものは公開一覧に載せない方針
