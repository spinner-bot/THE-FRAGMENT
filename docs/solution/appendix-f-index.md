# 附录 F：归档索引与术语表

> **用途：** 找到“某个东西在哪一章/哪个文件”，并统一本书的术语。
>
> 本附录也记录仓库的展示层与工具层；它们不属于解谜链，但属于这个项目的完整结构。

---

## F.1 文档索引

| 文件 | 内容 | 章节 |
|---|---|---|
| [`README.md`](README.md) | 全书目录、阅读路径、约定 | — |
| [`00-outline.md`](00-outline.md) | 55 章详细大纲 | — |
| [`part-01-overview.md`](part-01-overview.md) | 导读、全包一页图、术语、总路线 | 1–4 |
| [`part-02-entry.md`](part-02-entry.md) | 外层 ZIP、封面、说明书、P1 | 5–9 |
| [`part-03-lock.md`](part-03-lock.md) | ITC2RECIPE 格式与实现 | 10–17 |
| [`part-04-p2.md`](part-04-p2.md) | Q2、SHIT 层、仿射递推、K | 18–25 |
| [`part-05-p3.md`](part-05-p3.md) | Q3、`.entrance`、嵌套目录、五题入口 | 26–35 |
| [`part-06-five-questions.md`](part-06-five-questions.md) | Q1–Q4 与 Q5 概览 | 36–42 |
| [`part-07-q5.md`](part-07-q5.md) | Q5 数据、编码、Collatz、复现 | 43–50 |
| [`part-08-review.md`](part-08-review.md) | ChatGPT 时间线、错误、提示、设计复盘 | 51–55 |
| [`appendix-a-files.md`](appendix-a-files.md) | 文件树与 SHA-256 | 附录 A |
| [`appendix-b-decryptor.md`](appendix-b-decryptor.md) | 最小解密器 | 附录 B |
| [`appendix-c-p2-math.md`](appendix-c-p2-math.md) | P2 快速幂 | 附录 C |
| [`appendix-d-q5-generator.md`](appendix-d-q5-generator.md) | Q5 去混淆生成器 | 附录 D |
| [`appendix-e-answers.md`](appendix-e-answers.md) | 五题答案速查 | 附录 E |
| [`appendix-f-index.md`](appendix-f-index.md) | 本文件 | 附录 F |

---

## F.2 ChatGPT 归档索引

目录：[`archive/chatgpt/`](../../archive/chatgpt/README.md)

```text
archive/chatgpt/
├── README.md
├── timeline.md
├── 01/
│   ├── manifest.json
│   ├── share-01.raw.html
│   ├── share-01.raw.json
│   ├── transcript-full.md
│   └── transcript.md
└── 02/
    ├── manifest.json
    ├── share-02.raw.html
    ├── share-02.raw.json
    ├── transcript-full.md
    └── transcript.md
```

| 文件 | 大小 | 用途 |
|---|---:|---|
| `01/share-01.raw.json` | 4,428,674 | 第一段分享页的原始 JSON，最完整 |
| `01/share-01.raw.html` | 2,946,581 | 第一段分享页的原始 HTML |
| `01/transcript.md` | 93,078 | 可读正文（用户/助手/复盘） |
| `01/transcript-full.md` | 384,250 | 含工具调用与更多细节 |
| `01/manifest.json` | 872 | 来源、抓取时间、哈希、消息数 |
| `02/share-02.raw.json` | 5,753,478 | 第二段原始 JSON |
| `02/share-02.raw.html` | 3,907,392 | 第二段原始 HTML |
| `02/transcript.md` | 172,616 | 第二段可读正文 |
| `02/transcript-full.md` | 639,622 | 第二段完整记录 |
| `02/manifest.json` | 877 | 第二段元数据 |
| `timeline.md` | 7,809 | 两段合并时间线 |
| `README.md` | 2,010 | 归档说明与结构 |

### 两段对话

| 段 | 标题 | 时间范围（UTC） | 正文消息 |
|---|---|---|---:|
| 01 | 接受挑战 Fragment | 2026-11-08 11:18:23 → 13:22:37 | 36 |
| 02 | 接受挑战 Fragment (1) | 2026-11-08 13:17:53 → 15:42:44 | 80 |

两段在 13:17:53–13:22:37 重叠。02 段开头是接续摘要，不作为独立证据。第 51 章给出阶段划分。

### 引用约定

引用归档时写：

```text
archive/chatgpt/01/transcript.md, 2026-11-08 12:41:32 UTC
```

或：

```text
timeline.md, 提示 1
```

不要引用 02 段的接续摘要作为“新发现”；回到 01 段原文或 02 段的具体计算。

---

## F.3 仓库展示层

这些文件不参与解题，但决定仓库在 GitHub 上的呈现。

| 文件 | 大小 | 作用 |
|---|---:|---|
| `README.md` | 3,447 | GitHub 首页：标题、简介、结构图、入口 |
| `incipit.html` | 14,023 | 首页用的封面副本，与包内 `incipit/incipit.html` 哈希相同 |
| `assets/incipit-banner.svg` | 9,925 | 顶部横幅 |
| `assets/fragment-01.svg` | 4,732 | 章节/碎片图 1 |
| `assets/fragment-02.svg` | 4,684 | 碎片图 2 |
| `assets/fragment-03.svg` | 4,710 | 碎片图 3 |
| `assets/fragment-04.svg` | 4,559 | 碎片图 4 |
| `assets/fragment-05.svg` | 4,611 | 碎片图 5 |
| `assets/fragment-06.svg` | 4,591 | 碎片图 6 |
| `assets/epigraph.svg` | 2,714 | 题词图 |
| `assets/coda.svg` | 2,661 | 结尾图 |

`assets/*.svg` 是纯矢量图，不含答案。它们的文件名与六块“碎片”对应，用于首页排版。

### 根目录 `incipit.html` 与包内 `incipit.html`

两者内容相同（SHA-256 `f5853d8a...`），用途不同：

- 包内版本是解谜链的第 2 层（L2）；
- 仓库根版本是 GitHub Pages 的静态首页。

修改其中一个不会自动同步另一个；如果封面要改，两处都要改。

---

## F.4 工具层

目录：[`archive/chatgpt/tools/`](../../archive/chatgpt/tools/README.md)

| 文件 | 大小 | 作用 |
|---|---:|---|
| `extract_conversation.py` | 8,871 | 从分享页原始 JSON 提取消息，生成 `transcript.md` 与 `transcript-full.md` |
| `fetch-conversation.js` | 1,602 | 在浏览器控制台抓取分享页 JSON |
| `scrape-dom.js` | 2,641 | 从已渲染 DOM 抓取消息，作为 JSON 不可用时的后备 |
| `copy-fetch-js.bat` | 384 | 把抓取脚本复制到剪贴板 |
| `copy-dom-js.bat` | 360 | 把 DOM 脚本复制到剪贴板 |
| `README.md` | 4,735 | 工具使用说明 |

这些工具只处理公开分享页，不涉及账号登录或私有数据。

---

## F.5 仓库约定

### `.gitattributes`

```text
* -text
```

禁止 Git 做换行转换，保证压缩包、二进制数据和哈希可复现。

### `.gitignore`

```text
reference/
__pycache__/
*.pyc
```

`reference/` 是本地解包与抓取的工作区，不进入仓库；`archive/chatgpt/` 才是归档后的公开副本。

### 提交约定

- 自动提交，密集、按文件或模块拆分；
- 合并使用 `--no-ff`，保留分支历史；
- 不自动 push，除非明确要求。

---

## F.6 术语表

| 术语 | 含义 | 首次解释 |
|---|---|---|
| **P1** | 外层第一题，答案 `5050` | 第 9 章 |
| **P2** | 外层第二题，答案 K | 第 22–25 章 |
| **P3** | 外层第三题，评分与嵌套入口 | 第 26–28 章 |
| **Q1–Q5** | `puzzle.7z` 内的五道数据题 | 第 36–50 章 |
| **L0–L11** | 文件结构层级，L0 是发布 ZIP，L11 是 Q5 数据 | 第 2 章 2.7 节 |
| **答案链** | 上一题答案作为下一把锁的密钥 | 第 2 章 |
| **ITC2RECIPE** | 自描述锁格式；10 字节 marker 兼 XOR 密钥 | 第 10 章 |
| **marker** | 第一行 `ITC2RECIPE`，10 字节 | 第 11 章 |
| **recipe** | 第二行 hex 与 marker 循环 XOR 后的明文说明 | 第 11 章 |
| **CIPHER** | body base64 解码后去掉末 16 字节的部分 | 第 12 章 |
| **TAG** | 末 16 字节，`SHA-256(S ‖ 0x02 ‖ CIPHER)[:16]` | 第 12、15 章 |
| **D** | 锁的答案，十进制 ASCII 字符串 | 第 13 章 |
| **S** | `SHA-256(ASCII(D))`，32 字节 | 第 13 章 |
| **块流** | `SHA-256(S ‖ uint64_be(i))`，与 32 字节块 XOR | 第 14 章 |
| **Encrypt-then-MAC** | 先验证 TAG，再解密 | 第 15 章 |
| **K** | P2 的 77 位答案 | 第 24 章 |
| **`.entrance`** | 评分表与提示系统的静态文本 | 第 28 章 |
| **C(n)** | Collatz 从 n 到 1 的项数 | 第 46 章 |
| **R(n)** | `C^{C(n)-1}(C(n))`，Q5 的桶键 | 第 46 章 |
| **三角数编码** | `V = T_{l+s} + s` | 第 45 章 |
| **零游程** | `-k` 表示 k 个连续零 | 第 43–44 章 |
| **诱饵答案** | 包内 1,010 字节嘲讽文本，冒充 Q4/Q5 答案 | 第 35 章 |
| **归档** | `archive/chatgpt/` 中的两段对话与时间线 | 第 51 章 |

---

## F.7 按问题查章

| 问题 | 章节 |
|---|---|
| 这个包一共几层？ | 第 2 章、2.7 节 |
| 最外层 ZIP 里有什么？ | 第 5 章 |
| `incipit.html` 有什么用？ | 第 6 章 |
| 说明书里哪些话不能信？ | 第 8 章 |
| 5050 怎么来的？ | 第 9 章 |
| ITC2RECIPE 怎么解？ | 第 10–16 章、附录 B |
| 为什么不用 7z 密码？ | 第 17 章 |
| Q2 的 SHIT 层是什么？ | 第 20–22 章 |
| K 怎么算？ | 第 23–25 章、附录 C |
| `.entrance` 的分数怎么算？ | 第 28–30 章 |
| 为什么拿不到 B？ | 第 30 章 |
| 提示怎么收费？ | 第 31 章、第 53 章 |
| `P1-02C/B/A` 是什么？ | 第 32–33 章 |
| 33 字符目录名是什么？ | 第 34 章 |
| Q1–Q4 的公式？ | 第 37–40 章、附录 E |
| Q5 的数据怎么还原？ | 第 43–44 章 |
| Q5 的编码是什么？ | 第 45 章 |
| Q5 的桶键是什么？ | 第 46 章 |
| Q5 的生成器怎么写？ | 第 47、50 章、附录 D |
| ChatGPT 错在哪？ | 第 51–52 章 |
| 最短解法？ | 第 54 章 |
| 设计者怎么想？ | 第 55 章 |

---

## F.8 外部链接

- 仓库：`https://github.com/spinner-bot/THE-FRAGMENT`
- ChatGPT 分享页 01：`https://chatgpt.com/share/6af080c0-eaf8-83e8-ac1d-831c8490c346`
- ChatGPT 分享页 02：`https://chatgpt.com/share/6af098cb-ba44-83ec-83f4-17b825a602d3`

分享页可能失效；归档中的 `raw.json` 与 `transcript.md` 是长期副本。

---

## F.9 最后一句

如果只记一条路径：

```text
ZIP → incipit → instruction → P1=5050
→ Q2 锁 → SHIT → K
→ Q3 锁 → .entrance → 嵌套 → prompt/puzzle
→ Q1–Q4 → Q5 展开/三角数/Collatz
```

其余章节都是这条路径的展开、验证与复盘。
