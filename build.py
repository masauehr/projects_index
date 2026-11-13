"""projects.json から README.md と index.html を生成する。

使い方:
    python3 build.py                       # 公開版（projects.json → README.md / index.html）
    python3 build.py --json X.json --md Y.md --no-html   # 別データからMarkdownのみ生成
"""
import argparse
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def repo_url(owner, p):
    return f"https://github.com/{owner}/{p['repo']}"


def build_md(data, title, intro=""):
    owner = data["owner"]
    lines = [f"# {title}", ""]
    if intro:
        lines += [intro, ""]
    lines.append(f"全 {len(data['projects'])} 件。タイトルが主リンク、「Repo」は GitHub、「Web」は公開ページ。")
    lines.append("")
    for cat in data["categories"]:
        items = [p for p in data["projects"] if p["category"] == cat]
        if not items:
            continue
        lines += [f"## {cat}", "", "| 名前 | 内容 | Repo | Web |", "|---|---|---|---|"]
        for p in items:
            web = f"[開く]({p['pages']})" if p.get("pages") else "-"
            if p.get("repo"):
                main = p.get("pages") or repo_url(owner, p)
                lines.append(f"| [{p['title']}]({main}) | {p['desc']} | [Repo]({repo_url(owner, p)}) | {web} |")
            else:
                # リポジトリ無し（ローカルのみ）はリンクなしで表示
                lines.append(f"| {p['title']} | {p['desc']} | - | {web} |")
        lines.append("")
    lines.append("<!-- このファイルは build.py で自動生成。直接編集しない -->")
    return "\n".join(lines) + "\n"


def build_html(data, title):
    owner = data["owner"]
    e = html.escape
    sections = []
    for cat in data["categories"]:
        items = [p for p in data["projects"] if p["category"] == cat]
        if not items:
            continue
        cards = []
        for p in items:
            main = p.get("pages") or repo_url(owner, p)
            badge = '<span class="badge">Web</span>' if p.get("pages") else ""
            cards.append(
                f'<li data-s="{e((p["title"] + p["desc"]).lower())}">'
                f'<a class="main" href="{e(main)}">{e(p["title"])}{badge}</a>'
                f'<p>{e(p["desc"])}</p>'
                f'<a class="repo" href="{e(repo_url(owner, p))}">GitHub</a></li>'
            )
        sections.append(f"<section><h2>{e(cat)}</h2><ul>{''.join(cards)}</ul></section>")
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<style>
:root{{--bg:#fff;--fg:#1a1a1a;--sub:#666;--card:#f5f6f8;--ac:#0b6bcb}}
@media(prefers-color-scheme:dark){{:root{{--bg:#111;--fg:#eee;--sub:#aaa;--card:#1d1f23;--ac:#6cb2ff}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,sans-serif;max-width:960px;margin-inline:auto}}
h1{{font-size:1.4rem}} h2{{font-size:1.1rem;margin-top:1.6rem}}
input{{width:100%;box-sizing:border-box;padding:10px;font-size:1rem;border:1px solid var(--sub);border-radius:8px;background:var(--bg);color:var(--fg)}}
ul{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}}
li{{background:var(--card);border-radius:10px;padding:10px 12px}}
li p{{margin:.2rem 0 .4rem;color:var(--sub);font-size:.9rem}}
a{{color:var(--ac);text-decoration:none}} a.main{{font-weight:600}} a.repo{{font-size:.85rem}}
.badge{{margin-left:6px;font-size:.7rem;border:1px solid var(--ac);border-radius:4px;padding:0 4px}}
</style>
</head>
<body>
<h1>{e(title)}</h1>
<input id="q" type="search" placeholder="絞り込み（名前・内容）">
{''.join(sections)}
<script>
document.getElementById('q').addEventListener('input',function(){{
  var k=this.value.toLowerCase();
  document.querySelectorAll('li').forEach(function(li){{li.style.display=li.dataset.s.indexOf(k)<0?'none':''}});
  document.querySelectorAll('section').forEach(function(s){{s.style.display=s.querySelector('li:not([style*="none"])')?'':'none'}});
}});
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(HERE / "projects.json"))
    ap.add_argument("--md", default=str(HERE / "README.md"))
    ap.add_argument("--html", default=str(HERE / "index.html"))
    ap.add_argument("--no-html", action="store_true")
    ap.add_argument("--title", default="作成したアプリ一覧")
    ap.add_argument("--intro", default="", help="README冒頭に入れる1行（マニュアルへのリンク等）")
    a = ap.parse_args()
    data = json.loads(Path(a.json).read_text(encoding="utf-8"))
    Path(a.md).write_text(build_md(data, a.title, a.intro), encoding="utf-8")
    if not a.no_html:
        Path(a.html).write_text(build_html(data, a.title), encoding="utf-8")
    print("生成:", a.md, "" if a.no_html else a.html)


if __name__ == "__main__":
    main()
