# 附录 A：完整文件树与 SHA-256

> **用途：** 核对包内每一个文件，确认没有遗漏的入口，也确认所有哈希可复现。
>
> 路径以仓库根目录为基准。大小为字节数。哈希为 SHA-256 小写十六进制。

---

## A.1 发布层

```text
release/
└── THE FRAGMENT.zip                      28,828
    └── THE FRAGMENT/
        ├── incipit.7z                     4,626
        └── Let's go.7z                   23,617
```

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `release/THE FRAGMENT.zip` | 28,828 | `e5e160e9b454629eb23d3e5c013b29feb92420e501e6d47d760ae97a74736708` |
| `THE FRAGMENT/incipit.7z` | 4,626 | `b26fad184df23dfe5c040453136814cd912ba0534853d0df9ced2f15badf837e` |
| `THE FRAGMENT/Let's go.7z` | 23,617 | `20a71b9d3d5814f831605927a10b4fae4d0d053e552c81408ab8d31349f515b8` |

`release/THE FRAGMENT.zip` 是发布包；仓库根目录的 `THE FRAGMENT/` 是同一结构的展开副本，便于直接查看。

---

## A.2 封面层

```text
incipit/
└── incipit.html                          14,023
```

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `incipit/incipit.html` | 14,023 | `f5853d8ae258a051c514520554a96fcce5e1c3aa01d040843e65ce4a05835d07` |

仓库根目录还有一个 `incipit.html`，大小与哈希相同，是 GitHub Pages 首页使用的副本。它不属于解谜链，但属于展示层，详见附录 F。

---

## A.3 行动包层

```text
letsgo/Let's go/
├── instruction.gz                         7,229
├── Q1.tar                                 2,560
├── Q2.zst                                 3,670
└── Q3.7z                                 12,040
```

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `letsgo/Let's go/instruction.gz` | 7,229 | `5166a35fed9d4f797e080a5cf847e06559584c25730c4477c27f9967ba0bd8d8` |
| `letsgo/Let's go/Q1.tar` | 2,560 | `7a34223cebc3044f1352c015204a6597aa8fd27948c8d8a0a40883fb6d5155c4` |
| `letsgo/Let's go/Q2.zst` | 3,670 | `adf64fe2d2b681126f7e884a2c58e843c807a39f27a47c2213b96a6d5111ac00` |
| `letsgo/Let's go/Q3.7z` | 12,040 | `7a2d5716f25cfd2659cf4fceacae558f8c68746d6919178ab4c2d3d76d9b21ef` |

`instruction.gz` 解压后：

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `instruction.html` | 17,872 | `7c4166bca901861b040c4759d94dde812808e39e256e50333be9ab694843f8d8` |

---

## A.4 Q1 与 Q2

```text
q1/Q1/Q1                                     20
q2/Q2/
├── SHIT.tar.xz                             1,960
└── the map.bmp                                17
Q2.inner.7z                                 2,187
```

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `Q1/Q1` | 20 | `a7a06f11a4598c9b67d2a5ba54ba529fe765cd17177cc474535c6696038bf931` |
| `Q2.zst` 解压后的 `Q2.inner.7z` | 2,187 | `5d71138a6bbe2d4f4fee2f1f8e9dc657649c898b44106706a854010993bdcbf1` |
| `Q2/SHIT.tar.xz` | 1,960 | `0b70a7b1ec2036212c06ef432e3411fe6fffe0ce18e4fdc70113da04d4cf4a14` |
| `Q2/the map.bmp` | 17 | `0041688b0b35badba156aad0b4103231303d49536cbf53f94b1a1239f3e53d94` |

`the map.bmp` 不是位图：17 字节，内容为 `answer is the key`。

---

## A.5 SHIT 层

```text
SHIT/
├── SHIT.README                            2,584
└── SHIT.bz2                                 491
```

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `SHIT/SHIT.README` | 2,584 | `c71f60de02e166cd0e03d55dd14c6de5c8eaadad3132ccce7114ea02d5ee0d5e` |
| `SHIT/SHIT.bz2` | 491 | `5d05a14d3e4283f0e43c312ac33d293da1164e0a7df7931ad81e79919c994ef3` |

`SHIT.tar.xz` 解压出上述两个文件。

---

## A.6 Q3 与评分表

```text
q3/Q3/
├── README.txt                               181
└── is this the true challenge == false    15,682
Q3.inner.7z                                 9,831
q3inner/is this the true challenge == false/
├── .entrance                                416
└── P1-02C.7z                              9,206
```

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `Q3/README.txt` | 181 | `464e55ebb11876f28b76bf8246468b76969998d5656f9ae362b9f0ce4f72d247` |
| `Q3/is this the true challenge == false` | 15,682 | `ceaea7395c5fdbd355de9bd586386476ec4cdf6d2891dd33a76ad4523bb16a80` |
| `Q3.inner.7z` | 9,831 | `87f43baff2e005449cab1e68cb58d25e92429037f0b76b076838ecec608225fc` |
| `.entrance` | 416 | `031742f94c6d6ddf0d8bc5aea18d4fdacfcac42b2b41b119446cd394eb02865a` |
| `P1-02C.7z` | 9,206 | `c0245ca3d85d0e014c2236b86791e768db3453878e614921bd5cfc287d278742` |

`is this the true challenge == false` 是 ITC2RECIPE 锁，文件名本身是叙事的一部分。

---

## A.7 嵌套目录层

```text
P1-02B                                     11,900
p102b.zip 解压后：
P1-02A/
├── content.tar                             9,728
└── README.7z                               1,451
content.tar 解压后：
1000000000000000000000000000001.5/
├── prompt.7z                               1,935
└── puzzle.7z                               4,851
README.7z 解压后：
README.json                                 8,980
```

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `P1-02B`（base64 文本） | 11,900 | `3078995dd215c9931e8814a53f68152faab0cc230d1f59ef92d1e40f8ce459ca` |
| `P1-02B` 解码后的 ZIP | 8,923 | `38cf759cb4d39945581a98eca09cae4613ec92e49439721ea64d9592003cedcb` |
| `P1-02A/content.tar` | 9,728 | `520b5c32a4d61765f736dfe6c4fecf7b85757c61e8213c8b9973f33e0430c1f6` |
| `P1-02A/README.7z` | 1,451 | `6666aad5e967a133d86ea01ce0c751cd09bcd17e36415895b97d78fb1957c64b` |
| `README/README.json` | 8,980 | `2095dfd6160c4bd0ef3010eb1145ae3e96167bef22e5e5922898730c854a8896` |
| `prompt/prompt.7z` | 1,935 | `7c69c6afea4136ec9133a21aad74c1e6ff187d29d83539cca849f20aad600ab4` |
| `puzzle/puzzle.7z` | 4,851 | `eff0ab5d94fd045d62b6a06e5c1d39f2c65185338c38d4305ea9d52d035fcfb8` |

33 字符目录名 `1000000000000000000000000000001.5` 是 `10^30 + 1.5`，不是哈希，也不是日期。详见第 34 章。

---

## A.8 五题数据层

```text
prompt/
├── prompt.md                               1,035
└── prompt.html                             3,349
puzzle/
├── 第1题                                      94
├── 第2题                                     170
├── 第3题                                     336
├── 第4题.tar                               5,120
└── 第5题.tar                               7,168
```

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `prompt.md` | 1,035 | `d5786bdabd7ce4bee6c2b8994dd0abf5b142a76a3c2418f178679f9d6c9769a3` |
| `prompt.html` | 3,349 | `b93dca8f1917c553ae2f02fabc57715d862f520766a7211616e33aae0e2143cc` |
| `第1题` | 94 | `8aacff507f0c95c297b237d1ad9adf1692bcf50417f303a104aec6067d007a3f` |
| `第2题` | 170 | `6dad500a9604765e894f12623f8579212a3e7142bf16a56349a446fe4c47da0a` |
| `第3题` | 336 | `49e26ebb0d6496bb5ac15fb5327ea31d3cf214862584032c793e1d42e42c4e70` |
| `第4题.tar` | 5,120 | `bbddf17f7a28a4ecc1e14419b7f33d7d955df27d8f932c292e15ae1f31b0128f` |
| `第5题.tar` | 7,168 | `63da3c91f45fe851b8922b26cd5ba5b111814561b9adbc3982657966add42d78` |

`第4题.tar` 与 `第5题.tar` 解压后：

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `第4题` | 1,177 | `af7cf587838be075d35aaaf1876a06d9eab8a112de452985255a6e422d68ab46` |
| `第4题.答案`（包内诱饵） | 1,010 | `b1a558e2a72a1eb9d93b3f970d5b85105f9daeeede34c44aca9babc94b483da5` |
| `第5题.7z` | 3,093 | `79cbfc048c7f58e1971948045e2f482db837a4830813bfe5ba17722a6d2b06c9` |
| `第5题.答案`（包内诱饵） | 1,010 | `b1a558e2a72a1eb9d93b3f970d5b85105f9daeeede34c44aca9babc94b483da5` |
| `第5题`（7z 内数据） | 40,520 | `f3afde82c4a5a4be7771b5b12a573023b98a8b5202b9d9cf432da8795b023fb9` |

两个诱饵答案的哈希完全相同，说明它们都是同一份 `嘲讽文本.txt`。

---

## A.9 仓库源文件

以下文件不在发布包内，但用于对照与复现：

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `original files/第1题` | 94 | `8aacff507f0c95c297b237d1ad9adf1692bcf50417f303a104aec6067d007a3f` |
| `original files/第2题` | 170 | `6dad500a9604765e894f12623f8579212a3e7142bf16a56349a446fe4c47da0a` |
| `original files/第3题` | 336 | `49e26ebb0d6496bb5ac15fb5327ea31d3cf214862584032c793e1d42e42c4e70` |
| `original files/第4题` | 1,177 | `af7cf587838be075d35aaaf1876a06d9eab8a112de452985255a6e422d68ab46` |
| `original files/第4题.答案` | 228 | `63c6567eda2b91fbd5e14812d2108747243cfe71be8a00173e3d9133940ed941` |
| `original files/第5题` | 40,520 | `f3afde82c4a5a4be7771b5b12a573023b98a8b5202b9d9cf432da8795b023fb9` |
| `original files/第5题.答案` | 863 | `b43ca4e82f4693a4d6499297efded02cf53086a168a069b5f7ab3d8c8ba545a6` |
| `original files/嘲讽文本.txt` | 1,010 | `b1a558e2a72a1eb9d93b3f970d5b85105f9daeeede34c44aca9babc94b483da5` |
| `original files/prompt.md` | 1,035 | `d5786bdabd7ce4bee6c2b8994dd0abf5b142a76a3c2418f178679f9d6c9769a3` |
| `original files/prompt.html` | 3,349 | `b93dca8f1917c553ae2f02fabc57715d862f520766a7211616e33aae0e2143cc` |

注意：`original files/第4题.答案` 与包内 `第4题.答案` 同名但不同哈希；前者是 228 字节真实 Python 代码，后者是 1,010 字节嘲讽文本。第 5 题同理。

---

## A.10 每个文件在哪里被讨论

| 文件/目录 | 首次出现 | 详细讨论 |
|---|---|---|
| `release/THE FRAGMENT.zip` | 第 5 章 | 第 5 章、2.7 节 |
| `THE FRAGMENT/incipit.7z` | 第 5 章 | 第 6 章 |
| `THE FRAGMENT/Let's go.7z` | 第 5 章 | 第 7 章 |
| `incipit/incipit.html` | 第 6 章 | 第 6 章、附录 F |
| `instruction.gz` | 第 7 章 | 第 7–8 章 |
| `instruction.html` | 第 7 章 | 第 7–8 章 |
| `Q1.tar` / `Q1/Q1` | 第 18 章 | 第 37 章 |
| `Q2.zst` | 第 18 章 | 第 18–19 章 |
| `Q2.inner.7z` | 第 19 章 | 第 19–20 章 |
| `SHIT.tar.xz` | 第 20 章 | 第 20 章 |
| `the map.bmp` | 第 20 章 | 第 20 章 |
| `SHIT.README` | 第 21 章 | 第 21 章 |
| `SHIT.bz2` | 第 22 章 | 第 22–24 章 |
| `Q3.7z` | 第 26 章 | 第 26–27 章 |
| `Q3/README.txt` | 第 26 章 | 第 26 章 |
| `is this the true challenge == false` | 第 27 章 | 第 27 章 |
| `Q3.inner.7z` | 第 27 章 | 第 27–28 章 |
| `.entrance` | 第 28 章 | 第 28–31 章 |
| `P1-02C.7z` | 第 32 章 | 第 32 章 |
| `P1-02B` | 第 32 章 | 第 32 章 |
| `p102b.zip`（解码后） | 第 32 章 | 第 33 章 |
| `P1-02A/content.tar` | 第 33 章 | 第 33–34 章 |
| `P1-02A/README.7z` | 第 33 章 | 第 34 章 |
| `README.json` | 第 34 章 | 第 34 章 |
| 33 字符目录名 | 第 34 章 | 第 34 章 |
| `prompt.7z` / `prompt.md` / `prompt.html` | 第 35 章 | 第 35–36 章 |
| `puzzle.7z` | 第 35 章 | 第 36 章 |
| `第1题` | 第 36 章 | 第 37 章 |
| `第2题` | 第 36 章 | 第 38 章 |
| `第3题` | 第 36 章 | 第 39 章 |
| `第4题.tar` / `第4题` | 第 40 章 | 第 40 章 |
| `第4题.答案`（包内） | 第 40 章 | 第 40 章、第 35 章 |
| `第5题.tar` / `第5题.7z` | 第 41 章 | 第 41 章 |
| `第5题.答案`（包内） | 第 41 章 | 第 41 章、第 50 章 |
| `第5题`（500 行数据） | 第 43 章 | 第 43–50 章 |
| `original files/*` | 第 35 章 | 第 40、50 章、附录 E |
| `README.md`（仓库首页） | 附录 F | 附录 F |
| `assets/*.svg` | 附录 F | 附录 F |
| `incipit.html`（仓库根） | 附录 F | 附录 F |
| `tools/chatgpt-export/*` | 附录 F | 附录 F |
| `archive/chatgpt/*` | 第 51 章 | 第 51 章、附录 F |
| `.gitattributes` / `.gitignore` | 附录 F | 附录 F |

---

## A.11 哈希验证

```bash
# 单个文件
sha256sum "release/THE FRAGMENT.zip"

# 包内所有文件（先解压到空目录）
find unpacked -type f -print0 | xargs -0 sha256sum

# Windows PowerShell
Get-FileHash "release/THE FRAGMENT.zip" -Algorithm SHA256
```

如果要验证两个诱饵答案是否相同：

```bash
sha256sum "第4题.答案" "第5题.答案"
```

两者应输出同一个 `b1a558e2...`。

---

## A.12 文件树的两个原则

1. **结构位置 ≠ 探索位置。** `Q3.7z` 在 L3 就已出现，但要到 L4 拿到 K 才能打开；`P1-02C` 在 L5，却要等 `.entrance` 读完才继续。
2. **同名文件 ≠ 同一文件。** 包内与源目录的 `第4题.答案` 同名、不同内容；仓库根与包内的 `incipit.html` 同名、同内容但用途不同。

附录 B 给出能打开 ITC2RECIPE 锁的最小代码。
