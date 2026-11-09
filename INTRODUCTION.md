# THE FRAGMENT · 残卷

**一个可独立完成的多层嵌套解谜包，以及它的完整解题全书。**
*A self-contained, multi-layer puzzle package — and its complete solution book.*

---

## 这是什么 / What this is

《残卷》是一份以文件本身为谜面的解谜包。它不提供现成的解密工具，也不把规则写在明处：解题者需要从 ZIP 的第一层字节开始，逐层观察、推断、验证，沿着嵌套的压缩包、自描述的锁、数学题与生成器代码，一直走到最后一题。

*THE FRAGMENT is a puzzle package whose riddle is the files themselves. There is no ready-made decryption tool and no explicit rule sheet: the solver starts from the first bytes of the ZIP and works inward through nested archives, a self-describing lock, mathematical puzzles, and generator code.*

它同时是一份关于“结构如何承担难度”的设计样本。仓库里的解题全书不只给出答案，也保留真实解题过程中的错误路径、无效模型与提示系统的信息论。

*It is also a case study in how structure itself can carry difficulty. The solution book in this repository records not only the answers, but the wrong turns, failed models, and the information economics of the hint system.*

---

## 仓库里有什么 / What is in this repository

| 路径 / Path | 内容 / Contents |
|---|---|
| `release/THE FRAGMENT.zip` | 发布包。解题从这一层开始。 / The release package. Solving starts here. |
| `THE FRAGMENT/` | 发布包的展开副本，便于直接查看。 / An unpacked copy of the release package. |
| `original files/` | 出题时使用的原始题目、真实答案与提示文本。 / Source puzzles, real answers, and hint text. |
| `《THE FRAGMENT·残卷》解谜全书.html` | 单文件、双语、可离线阅读的完整解题全书。 / The complete bilingual solution book as one standalone HTML file. |
| `docs/solution/` | 全书的 Markdown 源稿，按解题顺序分为 8 个部分与 6 个附录。 / Markdown source of the book: 8 parts and 6 appendices. |
| `archive/chatgpt/` | 外部模型完整解题过程的归档，以及对话导出工具。 / Archived solving sessions from external models, plus export tools. |
| `tools/` | 全书构建脚本与模板（`build_book.py`、`book/template.html`）。 / Book build script and template. |
| `assets/`、`incipit.html` | 封面素材与封面源码。 / Cover assets and cover source. |
| `reference/` | 本地工作副本，默认被 `.gitignore` 忽略。 / Local working copies, ignored by default. |

---

## 从哪里开始 / Where to start

**只想亲自解题？**
下载 `release/THE FRAGMENT.zip`，然后离开这个仓库。这里的文字几乎处处是剧透。

*Just want to solve it yourself?*
Download `release/THE FRAGMENT.zip` and leave this repository. Almost everything here is a spoiler.

**想核对答案或看完整复盘？**
打开根目录的 [`《THE FRAGMENT·残卷》解谜全书.html`](《THE FRAGMENT·残卷》解谜全书.html)；只想快速对照五题答案，可直接看[附录 E](docs/solution/appendix-e-answers.md)。

*Looking for answers or a full walkthrough?*
Open [`《THE FRAGMENT·残卷》解谜全书.html`](《THE FRAGMENT·残卷》解谜全书.html), or jump to [Appendix E](docs/solution/appendix-e-answers.md) for a quick answer check.

**想理解设计意图？**
从[解题全书目录](docs/solution/README.md)进入，最后读第 55 章“设计者复盘：结构即难度”。

*Want the design rationale?*
Start from the [solution book index](docs/solution/README.md) and finish with Chapter 55, “Designer's Review: Structure Is Difficulty.”

**想重新生成全书？**

```bash
python tools/build_book.py
```

*To rebuild the book:*

```bash
python tools/build_book.py
```

---

## 两条阅读路线 / Two reading routes

| 按探索顺序 / In exploration order | 按文件结构 / By file structure |
|---|---|
| 第 1–4 章：定位与路线 | 外层 ZIP 与封面 |
| 第 5–9 章：入口与 P1 | `incipit.7z`、`Let's go.7z`、说明书 |
| 第 10–17 章：自描述锁 | `Q2.zst`、SHIT 层、`Q3.7z` |
| 第 18–35 章：P2 / P3 与嵌套包 | 嵌套目录、评分表、原始五题 |
| 第 36–50 章：五题与 Q5 逆向 | `original files/`、答案文件、生成器 |
| 第 51–55 章：复盘与设计 | `archive/chatgpt/`、全书构建工具 |

---

## 剧透警告 / Spoiler warning

本仓库包含**全部答案、密钥、评分机制与生成器代码**。解题全书是为已完成挑战的读者、以及研究“解谜包如何设计”的读者准备的。

*This repository contains **all answers, keys, scoring mechanics, and generator code**. The solution book is intended for readers who have finished the challenge, or who want to study how a puzzle package is designed.*

---

<p align="center"><sub>THE FRAGMENT · 残卷 · <a href="README.md">封面 README</a> · <a href="docs/solution/README.md">解题全书</a> · <a href="《THE FRAGMENT·残卷》解谜全书.html">单文件版本</a></sub></p>
