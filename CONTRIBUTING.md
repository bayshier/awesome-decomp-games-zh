# 参与贡献

感谢参与！本列表是**自动生成**的。请勿直接编辑 `README.md` 或其中的表格；它们每天从 `data/` 重建。

## 收录新项目
提交一个 PR，在 [`data/additions.json`](data/additions.json) 末尾追加：

```json
{"title": "Game Name", "url": "https://github.com/owner/repo", "platform": "N64", "type": "decomp", "description": "One line"}
```

`type` 是分类提示：`decomp`（反编译）、`recomp`（重编译）、`port`（移植）、`remake`（重制）、`browser`（浏览器版）或 `tool`（工具）。星标数、最近提交、decomp.dev 进度、链接状态和评分都会自动填充。

**收录标准**
- **商业发行**游戏（或知名免费游戏）的反编译、反汇编、静态重编译、源代码移植、引擎重新实现/重制，或浏览器移植版。
- 源代码公开，或有公开的项目页面。
- 不收录 mod、ROM hack 或同人游戏。被其来源列表标记为 AI 生成的项目会标注 ⚠️。

**永远不会被收录的**
- 指向 ROM、ISO、BIOS 文件、提取出的游戏资源或托管它们的网站的链接。
- 附带受版权保护游戏数据的仓库。

## 修正条目
使用 [`data/overrides.json`](data/overrides.json)：
- `"exclude": ["https://github.com/owner/repo"]` 移除某个条目。
- `"set": {"https://github.com/owner/repo": {"type": "source-port", "platform": "PS2"}}` 覆盖任意字段。

截图、视频链接和热门推荐语在 [`data/media.json`](data/media.json)。截图放入 `screenshots/` 目录，JPEG 格式，宽约 1280 像素、小于 300 KB，且必须是你自己的截图，或来自项目自己的 README。

## 本地运行
```bash
pip install requests Pillow
gh auth login           # GraphQL 数据补充依赖 gh
scripts/refresh         # 抓取、补充、评分，重新生成 README.md + data/games.json
```
通过本地服务器（`python3 -m http.server`）打开 `index.html` 可预览网站。

## 权利人
如果你是权利人并希望移除某个条目，请提交 issue，我们会立即处理。
