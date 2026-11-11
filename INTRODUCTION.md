# THE FRAGMENT · 残卷

A self-contained, multi-layer puzzle package — and a reproducible artifact for studying how agents reason across unfamiliar file systems.

**Author:** Codex  (sqs_A100)

**Start the challenge:** [Download `THE-FRAGMENT-challenge.zip`](THE-FRAGMENT-challenge.zip). The repository also contains the complete solution, so avoid opening the other files if you want to solve it unaided.

## What it is

THE FRAGMENT is a public puzzle package built as a chain of nested archives, a self-describing encrypted container, mathematical data puzzles, and a generator that must be reverse-engineered. Every layer is a real format — ZIP, 7z, zstd, tar, custom binary framing — and the package ships with an in-built hint/scoring mechanic plus a complete bilingual solution book.

For developers, the interesting part is not the story. It is a **small, deterministic, fully documented corpus** for file-system reasoning, tool use under uncertainty, hypothesis revision, and long-horizon planning.

- 12 layers, from the outer ZIP to the final generator
- Heavy metanarrative framing and layered misdirection: plausible wrong models are deliberately supported by the data
- 55 solution chapters and 6 appendices, all included in the repository
- A complete bilingual (EN/ZH) standalone HTML book, generated from Markdown
- No pre-made solver: the intended workflow is inspection → inference → verification

## Technical properties

| Property | Detail |
|---|---|
| Deterministic artifacts | Every file has a size and SHA-256 recorded in the appendix |
| Self-describing lock | `ITC2RECIPE`: marker + recipe, XOR stream over SHA-256 blocks, encrypt-then-MAC |
| Hint economy | Hints consume score and can return `F`, “not a valid question”, or “unavailable” |
| Reproducible docs | Install `requirements.txt`, then run `python3 tools/build_book.py` to rebuild the 55-chapter book from `docs/solution/` |
| Self-contained output | One offline HTML file with embedded CSS, JS, and SVG diagrams |
| Bilingual by construction | English preludes above Chinese technical exposition; no external assets |

## Possible uses

| Use | Why it fits |
|---|---|
| **Agent capability testing** | Long tool-use episodes, ambiguous state, dead ends, and a measurable scoring signal |
| **Hypothesis-revision benchmark** | The archive documents wrong statistical models; success requires reframing, not more fitting |
| **File-format / RE teaching** | Nested containers, checksums, custom framing, obfuscated generator code |
| **Reproducible packaging demo** | Byte-level manifests, deterministic unpacking, rebuildable documentation |
| **Documentation engineering** | Markdown → single-file themed HTML with a small, readable build pipeline |
| **Portfolio / write-up sample** | Design notes explain the engineering trade-offs behind each layer |

For an agent evaluation, the release package can be handed to a sandboxed agent as-is. Useful signals include layers reached, commands used, hint budget consumed, time to first correct inference, and whether the agent revises a wrong model instead of over-fitting it.

## Repository map

| Path | Contents |
|---|---|
| [`THE-FRAGMENT-challenge.zip`](THE-FRAGMENT-challenge.zip) | The release package. Start here to solve. |
| `THE FRAGMENT/` | Unpacked copy of the release package |
| `original files/` | Source puzzles, real answers, and hint text |
| `《THE FRAGMENT·残卷》解谜全书.html` | Complete bilingual solution book, single offline file |
| `docs/solution/` | Markdown source: 8 parts + 6 appendices |
| `archive/chatgpt/` | Full solving transcripts from external models, plus export tools |
| `tools/` | Book builder and template |
| `assets/`, `incipit.html` | Cover assets and cover source |

## Quick start

```bash
# Solve from scratch
#   1. download THE-FRAGMENT-challenge.zip
#   2. do not read the rest of this repository

# Read the solution book
#   open 《THE FRAGMENT·残卷》解谜全书.html

# Rebuild the solution book
python3 -m pip install -r requirements.txt
python3 tools/build_book.py
```

## Spoiler warning

This repository contains **all answers, keys, scoring mechanics, and generator code**. The solution book is written for readers who have finished the challenge, or for developers studying how the package is built.

---

## 中文摘要

《残卷》是一个以文件本身为谜面的多层解谜包：从外层 ZIP 一路拆到最后一题的生成器，每一层都是真实的文件格式（ZIP、7z、zstd、tar、自定义二进制封装），并带有大量元叙事包装、分层误导，以及内置的提示与评分机制。

面向开发者，它更实际的价值是一份**可复现、带完整文档的小型语料**，可用于：

- **Agent 能力测试**：长程工具调用、不确定状态下的探索、错误模型修正、提示预算管理；
- **格式与逆向教学**：嵌套容器、校验和、自定义分帧、生成器反混淆；
- **可复现打包示例**：逐文件哈希、确定性解包、文档可重建；
- **文档工程示例**：Markdown 生成单文件双语 HTML，构建链小而清晰。

解题全书与设计复盘见 [`docs/solution/`](docs/solution/README.md) 和根目录的 [`《THE FRAGMENT·残卷》解谜全书.html`](《THE FRAGMENT·残卷》解谜全书.html)。

> 本仓库包含全部答案与生成器代码；未完成挑战者请先只使用根目录的 `THE-FRAGMENT-challenge.zip`。
