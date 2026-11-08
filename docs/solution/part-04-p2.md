# 第 III 部分 · P2：SHIT 层

> **结构位置：** `Let's go/Q2.zst` 解压后的锁（L3/L4）→ Q2 payload（L5）→ SHIT 容器（L6）→ 数学题（L7）。
> **探索位置：** 拿到 5050 后，开 Q2 锁，读 `map.bmp` 与 `SHIT.README`，最后解 `SHIT.bz2`。
>
> 这一部分是“答案链”的第二次闭环：5050 打开 Q2，Q2 的答案 K 打开 Q3。它同时展示了三种误导：扩展名、README 噪音、数学题的“不可直接迭代”。

---

## 第 18 章：Q2.zst：zstd 与第一把锁

### 18.1 文件事实

```text
路径：THE FRAGMENT/Let's go/Q2.zst
大小：3,670 字节
SHA-256：adf64fe2d2b681126f7e884a2c58e843c807a39f27a47c2213b96a6d5111ac00
```

它确实是 zstd 帧，魔数为：

```text
28 B5 2F FD
```

解压后得到 5,356 字节的 UTF-8 文本，第一行：

```text
ITC2RECIPE
```

### 18.2 为什么先 zstd 再锁

`Q2.zst` 是“压缩 + 锁”的两层：

1. zstd 压缩：把 5,356 字节的锁文本压到 3,670 字节；
2. ITC2RECIPE 锁：把 2,187 字节的 7z 加密成 base64 文本。

必须先解压，才能看到锁；先看到锁，才知道怎么解。这和外层 ZIP → 7z 的“压缩套压缩”不同：这里是“压缩套加密”。

### 18.3 解压方法

Python（需要 `backports.zstd` 或 `zstandard`）：

```python
from backports import zstd
blob = open("Q2.zst", "rb").read()
text = zstd.decompress(blob)
open("Q2.lock", "wb").write(text)
```

命令行（如果安装了 zstd）：

```bash
zstd -d Q2.zst -o Q2.lock
```

### 18.4 解压后的文本结构

```text
ITC2RECIPE
<2,364 个十六进制字符>
<空行>
<2,940 个 base64 字符，分 42 行>
```

共 42 行。前两行是锁头，第三行空行，后面是 body。

### 18.5 名字这次没有骗人

与后面的 `the map.bmp`、`P1-02B` 不同，`Q2.zst` 的扩展名是准确的：它确实是 zstd。这是设计上的“先建立信任，再打破信任”：

- 如果第一个压缩文件就骗人，读者会过度警惕；
- 先让读者成功一次，再在 `map.bmp` 和 `P1-02B` 上制造错位，效果更强。

### 18.6 本章的结论

- `Q2.zst` 是 zstd，解压后是 ITC2RECIPE 锁文本。
- 解压后 5,356 字节，42 行。
- 这是读者第一次遇到“压缩 + 自描述锁”的组合。

---

## 第 19 章：用 5050 打开 Q2

### 19.1 输入

```text
D = "5050"
S = 3f95b1b8a32c2c0251dfdbc3c8a30aab6d6e680cf0ef03e8af84a65dff0c4a85
```

### 19.2 验证与解密

按第 16 章的脚本：

```bash
python -I -X utf8 unlock.py Q2.lock 5050 -o Q2.inner.7z
```

TAG 校验通过，输出：

```text
2,187 字节
SHA-256：5d71138a6bbe2d4f4fee2f1f8e9dc657649c898b44106706a854010993bdcbf1
```

前 6 字节：

```text
37 7A BC AF 27 1C
```

这是 7z 魔数，确认解密成功。

### 19.3 为什么 2,187 字节

`CIPHER` 长度就是 2,187 字节。解密不改变长度，所以明文也是 2,187 字节。这个大小刚好能装下：

- 一个 1,960 字节的 `SHIT.tar.xz`；
- 一个 17 字节的 `the map.bmp`；
- 7z 的目录与元数据开销约 210 字节。

### 19.4 失败会怎样

如果输入 `5051`：

- `S` 不同；
- 块流不同；
- `EXPECTED` 与 TAG 不匹配；
- 脚本在解密前抛出 `wrong answer or corrupted lock`。

不会得到“部分正确”的 7z，也不会得到可读的垃圾。这是 Encrypt-then-MAC 的好处。

### 19.5 第一次答案闭环

到这里，答案链完成了第一次循环：

```text
P1 的题面（1+...+100）
  → 答案 5050
  → 作为 D
  → S = SHA-256("5050")
  → 打开 Q2 锁
  → 得到 Q2 payload
```

这就是说明书说的“第 1 题答案 → 打开第 2 题”。

### 19.6 本章的结论

- 5050 是 Q2 锁的唯一正确钥匙。
- 解密输出 2,187 字节的 7z，哈希已给出。
- 失败是明确的 TAG 失败，不会产生“看起来像答案”的垃圾。

---

## 第 20 章：Q2 payload：SHIT.tar.xz 与 map.bmp

> **结构位置：** Q2 锁解开后的 7z（L5）→ `Q2/` 目录（L6）。
> **探索位置：** 先看 `the map.bmp`（叙事提示），再解 `SHIT.tar.xz`（真正内容）。

### 20.1 目录

```text
Q2/
├─ SHIT.tar.xz    1,960 字节
└─ the map.bmp       17 字节
```

### 20.2 `the map.bmp`

文件大小 17 字节，内容：

```text
answer is the key
```

没有换行，没有位图头，没有像素数据。扩展名 `.bmp` 是假的。

它的作用不是技术提示，而是叙事提示：

- 字面：答案是钥匙；
- 但结合说明书 W4：钥匙不等于答案，答案也不等于你现在需要的答案；
- 在 P2 这一层，答案 K 确实是 Q3 的钥匙；但到了 P3，答案不再是“下一个锁的钥匙”，而是生成器。

它同时是一个“格式陷阱”：如果读者按 `.bmp` 去找图片解析器，会得到“不是有效 BMP”。正确做法是先 `file` 或 `xxd`，再决定。

### 20.3 `SHIT.tar.xz`

1,960 字节，xz 压缩的 tar。解包后：

```text
SHIT/
├─ SHIT.README    2,584 字节
└─ SHIT.bz2         491 字节
```

`SHIT.README` 是噪音，`SHIT.bz2` 是题面。这个命名顺序是反的：README 看起来应该先读，但它故意不可靠；真正的题面在一个压缩文件里。

### 20.4 为什么用 `.tar.xz`

`.tar.xz` 是“打包 + 压缩”的标准组合：

- tar 负责保留文件名与目录结构；
- xz 负责高压缩率。

对 2.5 KB 的文本，压缩收益不大，但它增加了“需要知道两层格式”的门槛。读者必须先用 xz 解压，再用 tar 解包，或者直接用 `tar -xf`（现代 tar 会自动识别 xz）。

### 20.5 解包命令

```bash
tar -xJf SHIT.tar.xz
```

或 Python：

```python
import tarfile
with tarfile.open("SHIT.tar.xz") as t:
    t.extractall("SHIT")
```

### 20.6 本章的结论

- `the map.bmp` 是 17 字节文本，不是位图。
- `SHIT.tar.xz` 内含 `SHIT.README` 与 `SHIT.bz2`。
- README 是噪音，bz2 是题面。
- 文件名与格式的错位，是这一层的核心训练。

---

## 第 21 章：SHIT.README：可读的噪音

### 21.1 文件事实

```text
路径：SHIT/SHIT.README
大小：2,584 字节
SHA-256：c71f60de02e166cd0e03d55dd14c6de5c8eaadad3132ccce7114ea02d5ee0d5e
```

它是一份故意写坏的文件：拼写错误、重复、自指、矛盾指令、伪校验和。

### 21.2 逐段分析

**标题**

```text
PUZLE 2 — README (a copie of a copie of a copie)
```

`PUZLE` 少了一个 `Z`；`copie` 是法语/古英语拼法。标题在说：这是复制品，不是原件。

**警告**

```text
WARNING: this file was corupted in transit. Severel lines are missing.
Some lines were never there. Do not trust the line numbers. Do not trust
the file name. Do not trust this warning. It was written by the same
person who corupted the file, and that person was me, and I was not me.
```

这一段包含三个层次：

1. 文件被损坏，行号不可信；
2. 有些行从来不存在；
3. 连“不要相信”这句话也不可信，因为写它的人就是损坏文件的人。

这是典型的自指悖论：如果“不要相信这份警告”，那么“不要相信”本身也不可信；如果相信它，又要相信一个自称不可信的人。

**指令 1–5**

```text
INSTRCTIONS (read in the wrong order):
  1. Read the file called SHIT.
  2. Do not read the file called SHIT.
  3. The previos two steps are in the wrong order.
  4. If step 3 is true, step 1 is also true. This is not helpful.
  5. Rotate the page 90 degrees. There is no page. There is no 90.
```

五条指令互相取消：

- 1 与 2 直接矛盾；
- 3 说前两步顺序错了；
- 4 从 3 推出 1，但自己说“这没用”；
- 5 要求旋转一个不存在的页面。

读者能带走的唯一信息是：**不要按字面执行 README 的指令。**

**序列段落**

```text
The sequnce is not a sequnce. It is a recurance, wich is a sequnce that
has learned to repeat itself with intent. x_0 = 1 is a lie told by peple
who start counting at 1. Or at 0. Or at the place where the number stops
being a number and starts being a rumor.
```

这里有一个真假混合：

- “不是序列，是递推”——真；
- “x_0 = 1 是谎言”——假，题面确实是 `x_0 = 1`；
- “从 1 开始数的人”/“从 0 开始”——叙事噪音。

它的作用是让读者怀疑初始条件，但真正的题面在 `SHIT.bz2` 里，不受这段影响。

**重复的“钥匙不在此文件”**

```text
± ± ±  ãƒ†ã‚¹ãƒˆ ãƒ†ã‚¹ãƒˆ  ± ± ±
â€œthe key is not in this fileâ€
â€œthe key is not in this fileâ€
â€œthe key is nÃµt in this fÃ®leâ€
� � � ▓▒░ ░▒▓ ░░▒▒ � � �
```

三行同一句话，编码逐渐损坏：

- 第一行是 UTF-8 被当作 Latin-1 显示的乱码；
- 第二行是同样的乱码；
- 第三行有 `õ`、`î` 等替换字符；
- 最后一行是块字符。

字面信息是“钥匙不在此文件”。这是真的：钥匙在 `SHIT.bz2` 的数学题里。

**TRANSMISSION FRAGMENT 7/3**

```text
TRANSMISSION FRAGMENT 7/3 (recovered upside-down):
    C = [DATA EXPUNGED BY THE PERSON WHO EXPUNGED IT]
    N = 10^18   (or 10^81, the ink is bad here)
    M = 2^255 - 19  (this one is probaly right, dont quote me)

    the operater is adition, then multiplication, then regret
    the operater is not adition, it only looks like it from a distance
```

这是 README 里信息密度最高的一段：

- `C` 被涂掉——真正的 C 在 `SHIT.bz2` 里；
- `N = 10^18`（或 `10^81`）——真正的 N 是 `10^18`；
- `M = 2^255 - 19`——正确；
- “运算符是加法，然后乘法，然后后悔”——对仿射映射的戏谑描述；
- “运算符不是加法，只是远看像”——提醒读者：`f(x)=3x+C` 是仿射，不是纯加法。

这一段是“可读的噪音”：它包含真信息，但被错误、犹豫和玩笑包裹。

**UNREADABLE SEGMENT**

十六进制：

```text
4f 62 65 79 3f 20 4f 62 65 79 2e 20 54 68 65 20 73 65 71 75 65
6e 63 65 20 64 6f 65 73 20 6e 6f 74 20 63 61 72 65 20 61 62 6f
75 74 20 79 6f 75 2e 20 49 74 20 63 61 72 65 64 20 6f 6e 63 65
2e 20 54 68 61 74 20 77 61 73 20 65 6e 6f 75 67 68 2e
```

解码：

```text
Obey? Obey. The sequence does not care about you. It cared once. That was enough.
```

这是整份 README 里唯一“看起来不可读、实际完全可读”的段落。它的内容是叙事，不是数学。

**结尾**

```text
If you are reding this, you have alredy failed once. Congradulations.
The answar is a number. It is not in this file. It is not in any file.
It is in the space between two files, wich is also a file, wich is also
not a file. The space has a checksum. The checksum is wrong.
```

- “答案是一个数”——真；
- “不在这个文件里，不在任何文件里”——半真：答案由题面计算，不在文件里；
- “在两个文件之间的空间里”——叙事，指答案链；
- “空间有校验和，校验和是错的”——自指玩笑。

**作者注**

```text
Note on the aouthor: they definately existed, and they definately did
not want you to seperate the hint from the noise. Unfortunatly for them,
the noise is the hint, and the hint is missing, and the missing part is
the only part that was ever truely here.

checksum of this README: 0xDEADBEEF  (verifed twice, both times wrong)
encoding: UTF-8, then UTF-8 again, then somthing older than UTF-8
lenght: 3 lines (this is line 11)
```

- `0xDEADBEEF` 是经典占位符，不是真校验和；
- “UTF-8，再 UTF-8，再更老的东西”对应前面的乱码；
- “长度 3 行（这是第 11 行）”自相矛盾。

### 21.3 可信信息表

| 信息 | README 说法 | 实际 | 可信度 |
|---|---|---|---|
| `M` | `2^255 - 19` | 正确 | 高 |
| `N` | `10^18` 或 `10^81` | `10^18` | 中（有干扰项） |
| `C` | 被涂掉 | 在 `SHIT.bz2` | 无 |
| 初始条件 | `x_0 = 1 是谎言` | `x_0 = 1` | 低（反向误导） |
| 答案类型 | 一个数 | 正确 | 高 |
| 答案位置 | 不在文件里 | 由题面计算 | 高（半真） |
| 校验和 | `0xDEADBEEF` | 假 | 无 |

### 21.4 噪音设计的原则

这份 README 做到了三件事：

1. **可读**：不是乱码，读者能读完；
2. **不可执行**：指令互相矛盾，不能按字面做；
3. **有信息**：M、N、答案类型是真的，C 被引向 `SHIT.bz2`。

它不是“随便写乱”，而是“精确控制信噪比”：让读者在噪音中筛出三条真信息，同时不被假信息带偏。

### 21.5 本章的结论

- `SHIT.README` 是故意损坏的噪音文本。
- 可信信息：`M = 2^255 - 19`、`N = 10^18`、答案是一个数。
- `C` 不在 README 里，在 `SHIT.bz2`。
- 所有指令、校验和、行号都不可信。
- 它的功能是训练读者“从噪音中提取真信息”，为 Q5 做准备。

---

## 第 22 章：SHIT.bz2：真正的题面

### 22.1 文件事实

```text
路径：SHIT/SHIT.bz2
大小：491 字节
SHA-256：5d05a14d3e4283f0e43c312ac33d293da1164e0a7df7931ad81e79919c994ef3
解压后：665 字节
```

bzip2 魔数：

```text
42 5A 68   ("BZh")
```

### 22.2 解压后的全文

```text
Let M = 2^255 - 19.

Define a sequence of integers x_0, x_1, x_2, ... by

    x_0 = 1
    x_{n+1} = (3 * x_n + C) mod M     for every n >= 0

where

    C = 37034745566544782617569137203076208463588743464624141058302227831050492871311

Compute x_N for

    N = 10^18

ANSWER FORMAT

    Write the exact decimal representation of x_N as a single integer.
    Use only the digits 0-9 and a leading minus sign if needed.
    Do not use separators, spaces, leading zeros, or trailing characters.

HINT

    Iterating 10^18 times directly is not feasible. Note that
    f(x) = 3 * x + C is an affine map, and the N-fold composition of an
    affine map is again affine.
```

### 22.3 题面拆解

**模数**

```text
M = 2^255 - 19
```

这是 Curve25519 使用的素数，十进制为：

```text
57896044618658097711785492504343953926634992332820282019728792003956564819949
```

它是 255 位素数，常用于椭圆曲线密码学。选它有三个好处：

- 足够大，答案有 77 位十进制；
- 结构简单，`2^255 - 19` 容易验证；
- 与“密码学”主题呼应。

**初始条件**

```text
x_0 = 1
```

README 说“这是谎言”，但题面明确写 `1`。以题面为准。

**递推**

```text
x_{n+1} = (3 * x_n + C) mod M
```

这是一个仿射映射：

```text
f(x) = 3x + C  (mod M)
```

**常数 C**

```text
C = 37034745566544782617569137203076208463588743464624141058302227831050492871311
```

77 位十进制，小于 M。它不是随机数，而是设计者选定的偏移量，用来让 K 的十进制看起来“无规律”。

**N**

```text
N = 10^18
```

直接迭代不可行。提示已经给出方法：仿射映射的 N 次复合仍是仿射映射。

**答案格式**

- 精确十进制；
- 只允许数字与负号；
- 不允许分隔符、空格、前导零、尾随字符。

### 22.4 为什么把题面放在 bz2 里

`SHIT.bz2` 只有 491 字节，解压后 665 字节。压缩本身不是难点，难点是：

- 读者要先解 `.tar.xz`；
- 再在 `SHIT.README` 的噪音中找到“去读 SHIT”的指令；
- 再解 `.bz2`；
- 才发现真正的题面。

这是一种“延迟揭示”：题面一直存在，但被两层容器和一份噪音 README 挡住。

### 22.5 本章的结论

- 真正题面在 `SHIT.bz2`，491 字节，解压后 665 字节。
- `M = 2^255 - 19`，`x_0 = 1`，`f(x)=3x+C`，`N=10^18`。
- 提示明确指向仿射复合，避免读者真的迭代 10^18 次。

---

## 第 23 章：仿射递推：从 10^18 次到一次幂

### 23.1 仿射映射

定义：

```text
f(x) = 3x + C  (mod M)
```

它不是线性映射（因为有 `+C`），而是仿射映射。仿射映射的复合仍然是仿射映射。

### 23.2 前几次复合

```text
f^1(x) = 3x + C
f^2(x) = 3(3x + C) + C
       = 9x + 4C
f^3(x) = 3(9x + 4C) + C
       = 27x + 13C
```

系数是 `3^n`，常数项是 `C(3^n - 1)/2`。

### 23.3 闭式公式

```text
f^N(x) = 3^N x + C * (3^N - 1) / 2  (mod M)
```

推导：把 `f^N` 写成 `a_N x + b_N`，则：

```text
a_{n+1} = 3 a_n,      a_0 = 1
b_{n+1} = 3 b_n + C,  b_0 = 0
```

所以：

```text
a_N = 3^N
b_N = C (1 + 3 + 3^2 + ... + 3^{N-1})
    = C (3^N - 1) / (3 - 1)
    = C (3^N - 1) / 2
```

### 23.4 模运算中的除法

`M` 是奇数，所以 2 在模 `M` 下可逆：

```text
2 * inv2 ≡ 1 (mod M)
inv2 = (M + 1) / 2
     = 28948022309329048855892746252171976963317496166410141009864396001978282409975
```

在 Python 中：

```python
inv2 = pow(2, -1, M)
```

不要用浮点除法，也不要用整数除法 `// 2` 后再取模——虽然对正数有时等价，但语义不清晰。

### 23.5 快速幂

```python
p = pow(3, N, M)
K = (p * 1 + C * ((p - 1) * inv2 % M)) % M
```

`pow(3, N, M)` 使用平方-乘算法，复杂度 `O(log N)`，约 60 次模乘。

### 23.6 中间值

```text
M       = 57896044618658097711785492504343953926634992332820282019728792003956564819949
3^N mod M = 21893486293358952694566852022249891404799341872887818397117434745586527038965
inv2    = 28948022309329048855892746252171976963317496166410141009864396001978282409975
C mod M = 37034745566544782617569137203076208463588743464624141058302227831050492871311
(3^N-1)/2 mod M = 10946743146679476347283426011124945702399670936443909198558717372793263519482
K       = 55570866527475159802584688178377681056129853902315582853460115578675137387640
```

### 23.7 本章的结论

- `f^N(x) = 3^N x + C(3^N - 1)/2 mod M`。
- 模逆元 `inv2 = (M+1)/2`。
- 快速幂把 10^18 次迭代降到约 60 次模乘。
- 中间值可用于校验实现。

---

## 第 24 章：K 的计算：77 位整数

### 24.1 结果

```text
K = 55570866527475159802584688178377681056129853902315582853460115578675137387640
```

属性：

| 属性 | 值 |
|---|---|
| 十进制位数 | 77 |
| 二进制位数 | 255 |
| 十六进制 | `0x7adbfeef3a37490e4bd46bb6fca3c1690005d6e1c30a798820ee733de3fc9c78` |
| 32 字节大端 | `7adbfeef3a37490e4bd46bb6fca3c1690005d6e1c30a798820ee733de3fc9c78` |
| 与 M 的关系 | `0 < K < M` |

### 24.2 十六进制展开

```text
7a db fe ef 3a 37 49 0e 4b d4 6b b6 fc a3 c1 69
00 05 d6 e1 c3 0a 79 88 20 ee 73 3d e3 fc 9c 78
```

正好 32 字节。这不是巧合：`M` 是 255 位，`K` 是模 `M` 的余数，最多 32 字节。

### 24.3 为什么是 77 位

`M ≈ 5.7896 × 10^76`，所以 `0 ≤ K < M` 最多有 77 位十进制。`K` 恰好是 77 位，说明它接近 `M` 的量级。

### 24.4 计算脚本

```python
M = 2**255 - 19
C = 37034745566544782617569137203076208463588743464624141058302227831050492871311
N = 10**18

p = pow(3, N, M)
inv2 = pow(2, -1, M)
K = (p + C * ((p - 1) * inv2 % M)) % M

print(K)
print(hex(K))
```

输出与上面一致。

### 24.5 常见错误

| 错误 | 结果 |
|---|---|
| 忘记 `mod M` | 数字巨大，无法计算 |
| 用 `C * (p - 1) // 2` 代替模逆 | 可能因负数/取整出错 |
| 把 `x_0` 当成 0 | K 不同 |
| 把 `N` 当成 `10^8` | K 不同 |
| 答案带换行/空格 | TAG 失败 |

### 24.6 本章的结论

- K 是 77 位、255 位二进制、32 字节的整数。
- 它由闭式公式与快速幂算出。
- 十六进制展开可用于交叉验证。

---

## 第 25 章：K 的独立验证与交接

### 25.1 方法一：闭式公式

第 23–24 章的方法：

```text
K = 3^N + C(3^N - 1)/2 mod M
```

### 25.2 方法二：2×2 矩阵快速幂

把仿射映射写成矩阵：

```text
[ x' ]   [ 3  C ] [ x ]
[ 1  ] = [ 0  1 ] [ 1 ]
```

N 次复合就是矩阵的 N 次幂：

```python
def compose(a, b, c, d):
    # (a x + b) ∘ (c x + d)
    return a * c % M, (a * d + b) % M

a, b = 1, 0          # identity: x
ca, cb = 3, C        # f: 3x + C
n = N
while n:
    if n & 1:
        a, b = compose(ca, cb, a, b)
    ca, cb = compose(ca, cb, ca, cb)
    n >>= 1

K2 = (a * 1 + b) % M
```

`K2` 与 `K` 相同。这说明闭式公式没有算错。

### 25.3 方法三：用 K 开 Q3 锁

最直接的验证：

```bash
python -I -X utf8 unlock.py Q3.lock "$K" -o Q3.inner.7z
```

如果 TAG 通过，说明 K 正确。因为 Q3 锁的 TAG 是用 `S = SHA-256(K)` 计算的，K 错一位就会失败。

### 25.4 方法四：检查 Q3 输出

Q3 解密后是 9,831 字节的 7z，SHA-256：

```text
87f43baff2e005449cab1e68cb58d25e92429037f0b76b076838ecec608225fc
```

内含 `.entrance` 与 `P1-02C.7z`。如果输出不是 7z 或哈希不符，说明 K 或实现有误。

### 25.5 交接

K 作为 Q3 锁的 `D`：

```text
D = "55570866527475159802584688178377681056129853902315582853460115578675137387640"
S = dd0c89d9e6528ab64403dbe3858bc9fca78c4fc18f5773068e2d52bb6f2ad3c1
```

注意：

- 不能加换行；
- 不能加空格；
- 不能加前导零；
- 不能写成十六进制；
- 不能写成科学计数法。

### 25.6 本章的结论

- K 通过闭式公式、矩阵快速幂、Q3 解锁三种方式交叉验证。
- K 是 Q3 锁的钥匙。
- 下一步进入 P3 的最终内容。

下一部分将打开 Q3，看到 `.entrance` 评分表与 `P1-02C` 嵌套链。
