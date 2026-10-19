#!/usr/bin/env python3
"""Generate README.md from data/games.json. Do not edit README.md by hand."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
doc = json.load(open(os.path.join(ROOT, "data", "games.json")))
G, T = doc["games"], doc["topics"]
SITE = "https://bayshier.github.io/awesome-decomp-games-zh/"
SING = {"static-recomp": "静态重编译", "source-port": "源代码移植", "engine-remake": "引擎重制", "browser-port": "浏览器移植",
        "decompilation": "反编译", "disassembly": "反汇编", "tool": "工具"}
def esc(s): return (s or "").replace("|", "\\|").replace("\n", " ").strip()
def stars(n): return "" if n is None else (f"{n/1000:.1f}k" if n >= 1000 else str(n))
def date(s): return (s or "")[:10]
def anchor(name): return re.sub(r"[^\w -]", "", name.lower()).strip().replace(" ", "-")
def links(e):
    l = []
    if e.get("play_url"): l.append(f"[试玩]({e['play_url']})")
    if e.get("release_url"): l.append(f"[发布页]({e['release_url']})")
    if e.get("decompdev_url"): l.append(f"[进度]({e['decompdev_url']})")
    if e.get("video"): l.append(f"[视频]({e['video']})")
    if e.get("reddit_post"): l.append(f"[reddit]({e['reddit_post']} \"{e.get('reddit_user','')} · {e.get('reddit_upvotes',0)} 赞 · {e.get('reddit_comments',0)} 评论\")")
    return " · ".join(l)
def title(e):
    t = f"[{esc(e['title'])}]({e['url']})"
    if e.get("ai_flag"): t += " ⚠️"
    if e.get("archived"): t += " 🗄️"
    if e.get("old") and not e.get("inactive"): t += " 🕰️"
    return t

L = []
L += ["<!-- GENERATED FILE: edit data/ and run scripts/refresh, not this file -->",
"# Awesome Decomp Games（中文版）[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)", "",
'<p align="center">',
'  <a href="https://games.omgithub.com/">',
'    <img src="assets/play-decomp-games.svg" alt="Play Decomp Games" width="800">',
'  </a>',
'</p>', "",
"> [!NOTE]",
"> **汉化说明**：本仓库是 [SubmitGame/awesome-decomp-games](https://github.com/SubmitGame/awesome-decomp-games) 的非官方中文版，页面由 `scripts/gen_readme.py` 从 `data/` 自动生成，可跟随上游每日刷新。条目名称与链接保持英文原文；**每日刷新新收录的条目，其描述可能暂为英文**。列表与数据遵循上游的 CC0 许可，脚本与网站代码为 MIT。",
"> 一份带评分、每日自动刷新的**反编译、重编译与逆向工程游戏**榜单：涵盖对应的反编译项目、静态重编译、源代码移植、引擎重制、反汇编与浏览器移植版。", "",
f"**{doc['total']} 个项目**，覆盖 **{doc['unique_games']} 款游戏** · 更新于 {date(doc['generated_at'])} · 在**[网站]({SITE})**上浏览与筛选 · 数据见 [`data/games.json`](data/games.json)", "",
"> [!IMPORTANT]",
"> 本列表只链接源代码与项目页面，**不**托管、也不链接 ROM、ISO、游戏资源或其他受版权保护的内容。多数项目需要你自备一份正版游戏的文件。参见[免责声明](#免责声明)。", "",
"## 目录", "", f"- [在浏览器中游玩](#在浏览器中游玩) ({sum(1 for e in G if e.get('browser_playable'))})", "- [热门可玩推荐](#热门可玩推荐)"]
for k in T:
    if doc["counts"].get(k): L.append(f"- [{T[k]['name']}](#{anchor(T[k]['name'])}) ({doc['counts'][k]})")
if doc.get("mods"): L.append(f"- [Mod 与混搭作品](#mod-与混搭作品) ({len(doc['mods'])})")
if doc.get("inactive"): L.append(f"- [已停止维护](#已停止维护) ({doc['inactive']})")
L += ["- [评分规则](#评分规则)", "- [数据来源](#数据来源)", "- [参与贡献](#参与贡献)", "- [免责声明](#免责声明)", "- [许可证](#许可证)", ""]

browser = sorted([e for e in G if e.get("browser_playable")], key=lambda e: (-(e.get("screenshot") is not None), -e["score"], e["title"].lower()))
L += ["## 在浏览器中游玩", "", f"{len(browser)} 款游戏可直接在浏览器标签页中启动（WebAssembly/JS 移植与重编译版）。链接每天在真实浏览器里复核，已下线或失效的会被隐藏。部分游戏需要你自备游戏文件。切勿安装网站向你推销的启动器或浏览器扩展。", ""]
ASSETS = {"instant": "打开即玩", "byo": "需自备游戏文件", "demo": "免费试玩，无需游戏文件", "unknown": ""}
cells = []
for e in browser:
    img = f'<a href="{e["play_url"]}"><img src="{e["screenshot"]}" width="240" alt="{esc(e["title"])}"></a><br>' if e.get("screenshot") else ""
    extra = " · ".join(x for x in [esc(e["platform"]), ASSETS.get(e.get("needs_assets") or "", ""), "多人联机" if e.get("multiplayer") else ""] if x)
    cells.append(f'{img}<b>{esc(e["title"])}</b><br><a href="{e["play_url"]}"><b>▶ 在浏览器中游玩</b></a><br><sub>{extra}</sub>')
L.append("<table>")
for i in range(0, len(cells), 3):
    L.append("<tr>" + "".join(f'<td align="center" valign="top" width="33%">{c}</td>' for c in cells[i:i+3]) + "</tr>")
L += ["</table>", ""]
picks = sorted([e for e in G if e.get("top_pick")], key=lambda e: e["top_pick"])
L += ["## 热门可玩推荐", "", "在可玩性、完成度、活跃度与人气之间综合表现最好、今天就能真正玩起来的项目（部分需自备游戏文件）。", ""]
for i, e in enumerate(picks, 1):
    L.append(f"### {i}. {esc(e['title'])}")
    meta = f"**{SING.get(e['type'], e['type'])}** · {e['platform'] or '未知'} · ⭐ {stars(e['stars']) or '未知'} · 评分 **{e['score']:.1f}/5**"
    L.append(meta + "  ")
    note = e.get("note") or e.get("description") or ""
    if note: L.append(esc(note) + "  ")
    lk = " · ".join(x for x in [f"[项目主页]({e['url']})", links(e)] if x)
    L.append(lk)
    if e.get("screenshot"):
        L += ["", f'<a href="{e["url"]}"><img src="{e["screenshot"]}" width="480" alt="{esc(e["title"])} screenshot"></a>']
    L.append("")


for k in T:
    rows = sorted([e for e in G if e["type"] == k and not e.get("inactive")], key=lambda e: (-e["score"], e["title"].lower()))
    if not rows: continue
    L += [f"## {T[k]['name']}", "", T[k]["description"], "",
          "| 游戏 | 平台 | 评分 | ⭐ | 最近提交 | 进度 | 链接 |", "|---|---|---|---|---|---|---|"]
    for e in rows:
        prog = f"{e['progress']:.1f}%" if e.get("progress") is not None else ""
        L.append(f"| {title(e)} | {esc(e['platform'])} | {e['score']:.1f} | {stars(e['stars'])} | {date(e['last_commit'])} | {prog} | {links(e)} |")
    L.append("")

MODS = doc.get("mods", [])
if MODS:
    L += ["## Mod 与混搭作品", "", f"{len(MODS)} 个基于反编译项目、libsm64 与逆向工程重写的已发布 mod 与联名混搭作品（25+ 星，现在就能玩）。它们独立于上方各主题列表和热门推荐之外，精选自 [awesome-game-mashups](https://github.com/bailo167/awesome-game-mashups)（CC0）。全部需要自备相关游戏。", ""]
    for grp in dict.fromkeys(e.get("mod_group") or "其他 mod 与混搭" for e in MODS):
        L += [f"### {grp}", "", "| Mod | 运行于 | 引入内容 | ⭐ | 最近提交 | 链接 |", "|---|---|---|---|---|---|"]
        for e in [e for e in MODS if (e.get("mod_group") or "其他 mod 与混搭") == grp]:
            L.append(f"| {title(e)}<br><sub>{esc(e['description'])[:160]}</sub> | {esc(e.get('host'))[:60]} | {esc(e.get('guest'))[:60]} | {stars(e['stars'])} | {date(e['last_commit'])} | {links(e)} |")
        L.append("")

OLD = [e for e in G if e.get("inactive")]
if OLD:
    L += ["## 已停止维护", "", f"{len(OLD)} 个项目已被归档，或自 {doc['inactive_cutoff']}（两年前）起没有任何提交。它们可能仍能运行，但别指望再获得修复。可在浏览器上游玩的作品与人工挑选的热门推荐会留在主列表中，并标注 🕰️。", ""]
    for k in T:
        rows = sorted([e for e in OLD if e["type"] == k], key=lambda e: (-e["score"], e["title"].lower()))
        if not rows: continue
        L += [f"<details><summary><b>{T[k]['name']}</b> ({len(rows)})</summary>", "", "| 游戏 | 平台 | 评分 | ⭐ | 最近提交 | 进度 | 链接 |", "|---|---|---|---|---|---|---|"]
        for e in rows:
            prog = f"{e['progress']:.1f}%" if e.get("progress") is not None else ""
            L.append(f"| {title(e)} | {esc(e['platform'])} | {e['score']:.1f} | {stars(e['stars'])} | {date(e['last_commit'])} | {prog} | {links(e)} |")
        L += ["", "</details>", ""]

L += ["## 评分规则", "",
"每个条目都会得到四个 1-5 分的子评分，由 [`scripts/build.py`](scripts/build.py) 根据 GitHub 元数据和 decomp.dev 计算：", "",
"- **可玩性**：普通用户今天能不能玩上？有发布版、可用的浏览器链接或已完成的反编译得分高；早期研究型仓库得分低。",
"- **完成度**：decomp.dev 的代码匹配百分比、发布历史与自述状态。",
"- **活跃度**：最近一次提交的时间（已归档仓库计 1 分）。",
"- **人气**：GitHub star 数。", "",
"`score = 0.35×可玩性 + 0.25×完成度 + 0.2×活跃度 + 0.2×人气`（若其来源列表将其标记为 AI 生成则再扣 0.2 分 ⚠️）。🗄️ = 仓库已归档。每次刷新都会检查所有链接，失效链接会被移除（见 [`data/dropped.json`](data/dropped.json)）。", "",
"## 数据来源", "", "本列表从以下榜单获取种子数据，并每日对照它们刷新（感谢各位维护者）：", ""]
for s in doc["sources"]: L.append(f"- [{s['name']}]({s['url']})")
L += ["", "## 参与贡献", "", "发现缺少某个项目，或评分有误？参见 [CONTRIBUTING.md](CONTRIBUTING.md)。新增条目提交到 [`data/additions.json`](data/additions.json)，修正提交到 [`data/overrides.json`](data/overrides.json)。README.md 与网站均为自动生成，请勿手改。", "",
"## 免责声明", "",
"本仓库是第三方开源项目的索引。它**不**分发 ROM、ISO、BIOS 文件、游戏资源或任何受版权保护的游戏内容，也不链接到分发此类内容的网站。所列项目均由其各自作者在其各自的许可证与责任下创作；收录不代表认可，也不构成法律意见。其中大多数项目需要来自合法获得的原版游戏的数据文件。所有商标与游戏名称归其各自所有者所有。如果您是权利人并希望移除某个条目，请提交 issue。", "",
"## 许可证", "", "列表与数据以 [CC0 1.0](LICENSE) 发布；脚本与网站代码采用 [MIT 许可证](LICENSE-CODE)。", ""]
open(os.path.join(ROOT, "README.md"), "w").write("\n".join(L))
print("README.md written:", len("\n".join(L)) // 1024, "KB")
