# 第 II 部分 · 自描述锁 ITC2RECIPE

> **结构位置：** Q2 锁在 `Let's go/Q2.zst` 解压之后（L3/L4）；Q3 锁在 `Q3.7z/Q3/` 内（L3/L4）。
> **探索位置：** 先拿到 5050，再读 Q2 锁；先拿到 K，再读 Q3 锁。
>
> 这一部分只讲锁本身。它是整个包的技术核心：一个文件如何在不发布解密器的前提下，把“方法”交给读者，把“钥匙”留在上一题。

---

## 第 10 章：ITC2RECIPE：一个文件如何描述自己

### 10.1 外形

一个 ITC2RECIPE 文件是纯文本，结构固定：

```text
ITC2RECIPE
<十六进制字符串>
<空行>
<base64 字符串，可能分成多行>
```

逐行说明：

| 行 | 内容 | 作用 |
|---|---|---|
| 1 | `ITC2RECIPE` | 魔数 / marker / XOR 密钥 |
| 2 | 十六进制 | 与 marker 循环 XOR 后得到 recipe 明文 |
| 3 | 空行 | 分隔说明与正文 |
| 4+ | base64 | 解码后是 `CIPHER || TAG` |

Q2 锁（`Q2.zst` 解压后）的第一行：

```text
ITC2RECIPE
```

第二行是 2,364 个十六进制字符（1,182 字节）。空行之后是 2,940 个 base64 字符，解码为 2,203 字节。

Q3 锁（`Q3/is this the true challenge == false`）结构相同，第二行也是 2,364 个十六进制字符，但正文是 13,132 个 base64 字符，解码为 9,847 字节。

### 10.2 recipe 明文

把第二行 XOR 解码后，得到一份 1,182 字节的英文说明。Q2 的版本是：

```text
INTLOCK RECIPE V2

This file is not a 7z archive, even though its name says otherwise.

PART 1 - THE MARKER
The first line of this file is ITC2RECIPE.
It is both a marker and the repeating XOR key for the hexadecimal
line right below it.
Decode that hex to bytes, XOR them with the marker bytes repeated in a
cycle, and you will recover this recipe text.

PART 2 - THE BODY
After the blank line, the remaining text is one base64 string.
Decode it to bytes. Call the result CT.
The final 16 bytes of CT are a TAG.
Everything before the TAG is CIPHER.

PART 3 - THE KEY
Let D be the answer to puzzle 1, written in decimal without spaces,
separators, or leading zeros.
Let S = SHA-256( ASCII bytes of D ), 32 bytes.

PART 4 - DECRYPTION
Number the 32-byte blocks of CIPHER as i = 0, 1, 2, ...
For block i compute
    STREAM = SHA-256( S || uint64_big_endian(i) )
and XOR it byte by byte with the block.
The concatenation of the results is the original 7z file.

PART 5 - VERIFICATION
Compute
    EXPECTED = SHA-256( S || byte 0x02 || CIPHER )
and compare the first 16 bytes with TAG.
If they differ, the key or the data is wrong.
Do not trust any plaintext produced by a failed check.
```

Q3 的 recipe 只有一处不同：

```text
- Let D be the answer to puzzle 1, ...
+ Let D be the answer to puzzle 2, ...
```

这处差异证明锁是“按题号生成”的：同一个模板，换一个 `D` 的来源说明。读者不需要外部文档，就能知道当前该用哪一题的答案。

### 10.3 为什么叫“自描述”

常规加密压缩包的逻辑是：

```text
文件 + 密码 → 解压工具 → 内容
```

工具是黑箱，方法不在文件里，密码错了只给“CRC 错误”或“密码错误”。

ITC2RECIPE 的逻辑是：

```text
文件 → 读 recipe → 自己写工具 → 内容
```

方法在文件里，工具由读者实现，密码错误会得到明确的 TAG 失败。

这不是“更难破解”，而是“更难跳过”。读者可以复制一个解密器，但他必须首先理解 recipe；理解之后，锁就不再是黑箱。

### 10.4 五个部分

recipe 把协议分成五部分：

| 部分 | 内容 | 读者产出 |
|---|---|---|
| PART 1 | marker 与 recipe 的 XOR | 读出说明 |
| PART 2 | base64、CIPHER、TAG 分帧 | 得到密文与校验码 |
| PART 3 | 密钥派生 `S = SHA-256(ASCII(D))` | 把答案变成 32 字节 |
| PART 4 | 块流 `SHA-256(S ‖ uint64_be(i))` | 解出明文 |
| PART 5 | `SHA-256(S ‖ 0x02 ‖ CIPHER)[:16]` | 验证钥匙 |

这五部分对应五个实现步骤，顺序不能乱：先读说明，再分帧，再派生，再解密，最后验证。注意“最后验证”是就解密流程而言；安全上应该“先验证，再解密”。第 15 章会解释这个区别。

### 10.5 锁的文件名

Q3 锁的文件名是：

```text
is this the true challenge == false
```

这个名字有三个特点：

- 它是一句问句，不是扩展名；
- `== false` 看起来像代码里的布尔比较；
- 它没有 `.7z`、`.bin`、`.enc` 之类的格式提示。

文件名本身在说：“这是真正的挑战吗？——假。”这是叙事挑衅，不是技术信息。读者如果按名字找工具，会一无所获；只有读文件内容，才能找到 recipe。

### 10.6 本章的结论

- ITC2RECIPE 是纯文本、自描述、可手写解密器的锁。
- 它由 marker、recipe、base64 body 三部分组成。
- recipe 明确写出五步协议，且会指明 `D` 来自第几题。
- 锁的安全性不依赖算法保密，而依赖答案空间与 TAG。

---

## 第 11 章：Marker 与 recipe：XOR 的可逆性

### 11.1 marker 是什么

第一行是 10 个 ASCII 字节：

```text
I  T  C  2  R  E  C  I  P  E
49 54 43 32 52 45 43 49 50 45
```

它同时扮演两个角色：

1. **魔数**：让读者一眼识别“这是 ITC2RECIPE 锁”；
2. **XOR 密钥**：用于解码第二行的 recipe。

### 11.2 XOR 解码

设第二行的十六进制字节为 `c[0..n-1]`，marker 为 `m[0..9]`，则：

```text
recipe[i] = c[i] XOR m[i mod 10]
```

因为 XOR 自逆，同一个操作既能加密也能解密：

```text
c[i] = recipe[i] XOR m[i mod 10]
```

### 11.3 前 32 字节演示

Q2 第二行开头是：

```text
001a177e1d06086902000a1d1377721371435a11213d3012342c2f2c702c3a74...
```

按字节切开：

```text
00 1a 17 7e 1d 06 08 69 02 00 0a 1d 13 77 72 13
71 43 5a 11 21 3d 30 12 34 2c 2f 2c 70 2c 3a 74
```

marker 循环：

```text
49 54 43 32 52 45 43 49 50 45 49 54 43 32 52 45
43 49 50 45 49 54 43 32 52 45 43 49 50 45 49 54
```

逐字节 XOR：

```text
49 4e 54 4c 4f 43 4b 20 52 45 43 49 50 45 20 56
32 0a 0a 54 68 69 73 20 66 69 6c 65 20 69 73 20
```

转成 ASCII：

```text
INTLOCK RECIPE V2

This file is 
```

这就是 recipe 的开头。

### 11.4 为什么用 XOR

XOR 在密码学上很弱，但在这里有三个设计优势：

1. **零依赖。** 不需要库，不需要密钥管理，读一行代码就能实现。
2. **自逆。** 加密与解密是同一个操作，recipe 可以说“XOR 它们”而不必区分方向。
3. **可读性。** 它不会让 recipe 看起来像随机噪音；它只是把明文轻轻翻了个面。

它保护的从来不是 recipe 的机密性。recipe 本来就打算给读者读。它保护的是“读者必须动手”的仪式感：你不能直接 `cat` 出说明，必须写三行代码。

### 11.5 如果 marker 被改

如果第一行不是 `ITC2RECIPE`，会出现两种情况：

- 读者按错误 marker 解码，得到乱码 recipe；
- 读者仍然按正确 marker 解码，但文件已经不是标准锁。

这说明 marker 同时是“格式标识”和“解码参数”。它不能随便改，否则锁就失去自描述性。

### 11.6 recipe 的版本

recipe 第一行是：

```text
INTLOCK RECIPE V2
```

`V2` 说明这个格式有版本概念。包内没有 V1 文件，但版本号的存在暗示：

- 设计者预留了演进空间；
- 读者不应把当前格式当成唯一可能；
- 如果未来出现 V3，marker 或分帧方式可能变化。

### 11.7 本章的结论

- marker 是 10 字节的 `ITC2RECIPE`。
- recipe 是第二行十六进制与 marker 循环 XOR 的结果。
- 这层 XOR 不是保密，而是“让读者动手”的轻量混淆。
- 解码后得到完整的五部分协议说明。

---

## 第 12 章：Body：base64、CIPHER 与 TAG 的分帧

### 12.1 body 的位置

文件前三行是：

```text
第 1 行：ITC2RECIPE
第 2 行：十六进制 recipe
第 3 行：空行
第 4 行起：base64 body
```

body 可能被分成多行，每行 76 或 60 个字符左右。读取时要把所有行拼接成一个字符串，再 base64 解码。

### 12.2 分帧

设 base64 解码后的字节串为 `raw`，长度至少 16：

```text
CIPHER = raw[:-16]
TAG    = raw[-16:]
```

- `TAG` 固定 16 字节（128 位）；
- `CIPHER` 是剩余部分；
- `CIPHER` 按 32 字节分块，最后一块可以不足 32 字节。

### 12.3 Q2 与 Q3 的实际数字

| 项目 | Q2 锁 | Q3 锁 |
|---|---:|---:|
| body 字符数 | 2,940 | 13,132 |
| base64 解码后 | 2,203 字节 | 9,847 字节 |
| TAG | 16 字节 | 16 字节 |
| CIPHER | 2,187 字节 | 9,831 字节 |
| 32 字节块数 | 69（最后一块 11 字节） | 308（最后一块 7 字节） |
| TAG 十六进制 | `feb55870ee9344f75e31597e4e68b5e8` | `f8fb0cca998ee5a96cd9cdc23c306e04` |

最后一块不足 32 字节是正常的：块流只取与密文等长的前缀进行 XOR。

### 12.4 base64 的换行

base64 标准允许每 76 个字符换行。Q2 的 body 有 42 行，Q3 有 176 行。读取时有两个选择：

```python
body = b"".join(lines[3:])
```

或：

```python
body = b"".join(blob.splitlines()[3:])
```

两者都会去掉换行。不要对每一行单独 base64 解码，因为一行可能不是 4 的倍数。

### 12.5 为什么先分帧再解密

如果先解密再找 TAG，会有一个问题：TAG 本身也是密文的一部分，解密后得到的是“明文 TAG”，但协议规定 TAG 是对 `CIPHER` 的 MAC，不是明文的一部分。

正确顺序：

1. base64 解码；
2. 切出最后 16 字节作为 TAG；
3. 用 `CIPHER` 和 `S` 计算期望 TAG；
4. 比较；
5. 只有通过后才解密 `CIPHER`。

### 12.6 如果长度不对

如果 `raw` 少于 16 字节，说明文件被截断或不是锁。如果 `CIPHER` 为空，TAG 仍然可以计算，但解密结果为空；这不是有效负载。

Q2 的 `CIPHER` 长度 2,187 不是 32 的倍数（2,187 = 68×32 + 11），这是正常的。不要因为“不是整块”就认为文件损坏。

### 12.7 本章的结论

- body 是一个 base64 字符串，可跨行。
- 解码后最后 16 字节是 TAG，前面是 CIPHER。
- CIPHER 按 32 字节分块，最后一块可短。
- Q2/Q3 的实际长度与 TAG 已在上表列出，可用于校验实现。

---

## 第 13 章：密钥派生：S = SHA-256(ASCII(D))

### 13.1 公式

recipe 的 PART 3 写得很清楚：

```text
Let D be the answer to puzzle N, written in decimal without spaces,
separators, or leading zeros.
Let S = SHA-256( ASCII bytes of D ), 32 bytes.
```

用 Python 表示：

```python
S = hashlib.sha256(str(D).encode("ascii")).digest()
```

### 13.2 D 是字符串，不是整数

这是最容易错的一点。`D` 参与哈希的是它的 **ASCII 字节**，不是整数的二进制表示。

以 5050 为例：

| 表示 | 字节 | SHA-256 |
|---|---|---|
| `"5050"` | `35 30 35 30` | `3f95b1b8...`（正确） |
| 整数 5050 的 8 字节大端 | `00 00 00 00 00 00 13 BA` | 不同 |
| `"5,050"` | `35 2C 30 35 30` | 不同 |
| `"5050\n"` | `35 30 35 30 0A` | 不同 |

锁只认第一种。

### 13.3 实际值

**Q2 锁：**

```text
D = "5050"
S = 3f95b1b8a32c2c0251dfdbc3c8a30aab6d6e680cf0ef03e8af84a65dff0c4a85
```

**Q3 锁：**

```text
D = "55570866527475159802584688178377681056129853902315582853460115578675137387640"
S = dd0c89d9e6528ab64403dbe3858bc9fca78c4fc18f5773068e2d52bb6f2ad3c1
```

### 13.4 为什么先哈希

直接拿答案当 XOR 密钥会有两个问题：

1. **长度不固定。** 5050 只有 2 字节，K 有 77 字节；流生成需要固定长度的种子。
2. **答案长度泄露。** 如果直接用答案字节，密钥流长度会暴露答案长度。

SHA-256 把任意长度压成 32 字节，解决这两个问题。它不增加答案的熵，但把格式统一了。

### 13.5 为什么没有盐

这个协议没有盐，也没有 KDF 迭代。原因是：

- 每个锁只用一个答案，没有多用户/多密码场景；
- 答案空间由题目决定，不依赖抗暴力破解；
- 盐会引入额外参数，破坏“容器自己说明自己”的简洁性。

代价是：如果答案可猜，`S` 可预计算。对 5050 这种小答案，暴力枚举 0–10000 是瞬间的事。但这不是安全问题，因为 5050 本来就写在题面里；锁的目的不是防止别人打开，而是确保“你必须先解题”。

### 13.6 错误答案会发生什么

如果 `D` 错：

```text
S' != S
→ 块流不同
→ 解密出的明文是垃圾
→ EXPECTED' != TAG
→ 校验失败
```

关键：**不要先解密再判断**。错误答案产生的垃圾可能恰好以 `7z` 魔数开头（概率极低，但理论上可能），如果先解密再“看像不像”，会被误导。正确做法是先验 TAG。

### 13.7 本章的结论

- `S = SHA-256(ASCII(D))`，32 字节。
- `D` 是十进制字符串，不能有空格、逗号、前导零、换行。
- 5050 与 K 的 `S` 已给出，可用于校验实现。
- 无盐设计是为了简洁，不是生产级安全。

---

## 第 14 章：块流：SHA-256(S ‖ uint64_be(i))

### 14.1 公式

recipe 的 PART 4：

```text
Number the 32-byte blocks of CIPHER as i = 0, 1, 2, ...
For block i compute
    STREAM = SHA-256( S || uint64_big_endian(i) )
and XOR it byte by byte with the block.
```

用 Python：

```python
for i in range(0, len(cipher), 32):
    block = cipher[i:i+32]
    counter = i // 32
    stream = hashlib.sha256(S + struct.pack(">Q", counter)).digest()
    plaintext += bytes(a ^ b for a, b in zip(block, stream))
```

### 14.2 计数器

- `i` 是块序号，从 0 开始；
- 编码为 8 字节无符号大端整数；
- 最大可表示 `2^64 - 1` 个块，即约 `2^69` 字节，远超本包需要。

`struct.pack(">Q", counter)` 的 `>` 表示大端，`Q` 表示 8 字节无符号。

### 14.3 为什么是 32 字节

SHA-256 输出 32 字节，正好一个块。这样每个块只需要一次哈希，不需要截断或拼接。

如果 CIPHER 最后一块不足 32 字节，仍然计算完整的 32 字节 STREAM，只取前 `len(block)` 字节进行 XOR。

### 14.4 没有 IV / nonce

每个锁的 `S` 都不同（因为答案不同），所以不需要额外的 IV。同一个 `S` 不会用于两个文件；即使 5050 被重复使用，也只会打开同一个 Q2。

这不是通用的流密码设计。如果同一个 `S` 加密两个不同消息，块流会复用，导致 XOR 泄露。包内不存在这种情况。

### 14.5 一个块的计算示例

以 Q2 的第一块为例（示意，不展开全部字节）：

```text
S       = 3f95...4a85
i       = 0
STREAM  = SHA-256(S || 00 00 00 00 00 00 00 00)
CIPHER0 = 前 32 字节密文
PLAIN0  = CIPHER0 XOR STREAM
```

`PLAIN0` 的前几个字节应该是 `37 7A BC AF 27 1C`（7z 魔数），可以用这个做快速自检。

### 14.6 为什么用哈希而不是 AES

三个原因：

1. **可手写。** 读者只需要 `hashlib` 和 `struct`，不需要 AES 库。
2. **自描述。** recipe 可以用一行公式说清楚，不需要解释 S-box、模式、填充。
3. **教学性。** 它展示的是“哈希可以构造流密码”这一原理，而不是生产级加密。

代价是性能较低（每 32 字节一次 SHA-256），但对几 KB 的锁完全可接受。

### 14.7 本章的结论

- 块流 = `SHA-256(S ‖ uint64_be(i))`，每块 32 字节。
- 最后一块按实际长度截断。
- 没有 IV，因为每个锁的 `S` 唯一。
- 解密后应以 7z 魔数自检。

---

## 第 15 章：验证：Encrypt-then-MAC

### 15.1 公式

recipe 的 PART 5：

```text
EXPECTED = SHA-256( S || byte 0x02 || CIPHER )
compare the first 16 bytes with TAG.
```

用 Python：

```python
expected = hashlib.sha256(S + b"\x02" + cipher).digest()[:16]
if not hmac.compare_digest(expected, tag):
    raise ValueError("wrong key or corrupted data")
```

### 15.2 为什么是 Encrypt-then-MAC

三种常见组合：

| 模式 | 做法 | 问题 |
|---|---|---|
| MAC-then-Encrypt | 先 MAC 明文，再加密 | 解密后才能验，容易受填充预言 |
| Encrypt-and-MAC | 同时加密和 MAC 明文 | MAC 可能泄露明文信息 |
| **Encrypt-then-MAC** | 先加密，再对密文 MAC | 可以先验后解，最安全 |

本锁采用第三种：TAG 是对 `CIPHER` 的 MAC，不是对明文的 MAC。因此可以在解密前验证钥匙。

### 15.3 0x02 是什么

`0x02` 是一个域分隔字节，作用是把“MAC 计算”与“其他哈希用途”分开。

没有它，`SHA-256(S || CIPHER)` 可能与块流 `SHA-256(S || counter)` 在某处混淆。加入一个固定前缀字节，可以避免不同用途的哈希输入发生碰撞。

这不是标准 KDF 域分隔，但在自定义协议里是合理做法。

### 15.4 实际 TAG

| 锁 | TAG |
|---|---|
| Q2 | `feb55870ee9344f75e31597e4e68b5e8` |
| Q3 | `f8fb0cca998ee5a96cd9cdc23c306e04` |

这些是密文的 MAC，不是明文的哈希。不要用它们去比对解密结果。

### 15.5 先验后解

正确顺序：

```python
raw = base64.b64decode(body)
cipher, tag = raw[:-16], raw[-16:]
S = sha256(answer)
expected = sha256(S + b"\x02" + cipher)[:16]
if not compare_digest(tag, expected):
    fail()
plaintext = decrypt(cipher, S)
```

错误顺序：

```python
plaintext = decrypt(cipher, S)   # 先解
if plaintext[:2] == b"7z":      # 再看像不像
    ...
```

错误顺序的问题：

- 错误钥匙可能产生以 `7z` 开头的垃圾（概率极低，但不是零）；
- 解密过程本身可能对畸形输入产生异常；
- 你无法区分“钥匙错”与“数据损坏”。

先验后解把失败点提前，并且给出明确错误。

### 15.6 16 字节截断

TAG 只取 SHA-256 的前 16 字节（128 位）。暴力伪造成功的概率是 `2^-128`，对本挑战足够。

如果要更严格，可以用完整 32 字节。截断到 16 字节是为了让 TAG 短一些，文件更紧凑。

### 15.7 本章的结论

- TAG = `SHA-256(S ‖ 0x02 ‖ CIPHER)[:16]`。
- 必须先验 TAG，再解密。
- 比较使用常量时间函数 `hmac.compare_digest`。
- Q2/Q3 的 TAG 已给出，可用于测试。

---

## 第 16 章：最小解密器：从零实现

### 16.1 完整代码

以下脚本只依赖 Python 标准库：

```python
#!/usr/bin/env python3
"""Open an ITC2RECIPE lock with a decimal answer."""

import argparse
import base64
import hashlib
import hmac
import struct
import sys
from pathlib import Path


def decode_recipe(blob: bytes) -> bytes:
    lines = blob.splitlines()
    if len(lines) < 3 or lines[0] != b"ITC2RECIPE":
        raise ValueError("not an ITC2RECIPE file")
    marker = lines[0]
    encoded = bytes.fromhex(lines[1].decode("ascii"))
    return bytes(b ^ marker[i % len(marker)] for i, b in enumerate(encoded))


def unlock(blob: bytes, answer: str) -> bytes:
    lines = blob.splitlines()
    if len(lines) < 4 or lines[0] != b"ITC2RECIPE":
        raise ValueError("not an ITC2RECIPE file")

    body = b"".join(lines[3:])
    raw = base64.b64decode(body)
    if len(raw) < 16:
        raise ValueError("body too short")

    cipher, tag = raw[:-16], raw[-16:]
    S = hashlib.sha256(answer.encode("ascii")).digest()

    expected = hashlib.sha256(S + b"\x02" + cipher).digest()[:16]
    if not hmac.compare_digest(expected, tag):
        raise ValueError("wrong answer or corrupted lock")

    out = bytearray()
    for offset in range(0, len(cipher), 32):
        block = cipher[offset:offset + 32]
        counter = offset // 32
        stream = hashlib.sha256(S + struct.pack(">Q", counter)).digest()
        out.extend(a ^ b for a, b in zip(block, stream))
    return bytes(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("lock", type=Path)
    parser.add_argument("answer")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--recipe", action="store_true", help="print recipe and exit")
    args = parser.parse_args()

    blob = args.lock.read_bytes()
    if args.recipe:
        sys.stdout.write(decode_recipe(blob).decode("utf-8", "replace"))
        return

    plaintext = unlock(blob, args.answer)
    args.output.write_bytes(plaintext)
    print(f"wrote {args.output} ({len(plaintext)} bytes)")


if __name__ == "__main__":
    main()
```

### 16.2 逐行解释

**`splitlines()`**

按 `\n`、`\r\n` 等换行符切分，不保留行尾。这样不必担心 CRLF。

**`lines[0] != b"ITC2RECIPE"`**

检查魔数。注意比较的是 bytes，不是 str。

**`bytes.fromhex(lines[1].decode("ascii"))`**

将十六进制字符串转为字节。`fromhex` 允许空格，但这里没有。

**XOR 循环**

`marker[i % len(marker)]` 实现循环密钥。marker 长度 10，所以第 10 个字节回到 `I`。

**`body = b"".join(lines[3:])`**

跳过前三行（marker、hex、空行），把剩余 base64 行拼起来。

**`raw[:-16]` / `raw[-16:]`**

Python 负索引切片，简洁且不易错。

**`answer.encode("ascii")`**

强制 ASCII。如果答案含非 ASCII 字符，会抛异常，而不是悄悄用 UTF-8。

**`hmac.compare_digest`**

常量时间比较，避免时间侧信道。对这个挑战不是必需，但是好习惯。

**`struct.pack(">Q", counter)`**

8 字节大端无符号整数。`>` 是大端，`Q` 是 unsigned long long。

**最后一块**

`cipher[offset:offset+32]` 自动截断；`zip(block, stream)` 只取较短长度，所以不会多 XOR。

### 16.3 用法

**查看 recipe：**

```bash
python -I -X utf8 unlock.py "reference/unpack/letsgo/Let's go/Q2.zst.dec" --recipe
```

（假设已把 zstd 解压后的内容保存为 `Q2.zst.dec`。）

**用 5050 打开 Q2：**

```bash
python -I -X utf8 unlock.py Q2.lock 5050 -o Q2.inner.7z
```

**用 K 打开 Q3：**

```bash
python -I -X utf8 unlock.py "Q3.lock" \
  55570866527475159802584688178377681056129853902315582853460115578675137387640 \
  -o Q3.inner.7z
```

### 16.4 验证输出

解密后的文件应以 7z 魔数开头：

```text
37 7A BC AF 27 1C
```

Q2 输出 2,187 字节，SHA-256：

```text
5d71138a6bbe2d4f4fee2f1f8e9dc657649c898b44106706a854010993bdcbf1
```

Q3 输出 9,831 字节，SHA-256：

```text
87f43baff2e005449cab1e68cb58d25e92429037f0b76b076838ecec608225fc
```

如果这两个哈希匹配，说明解密器实现正确。

### 16.5 常见错误

| 错误 | 症状 | 修正 |
|---|---|---|
| 答案带换行 | TAG 失败 | 去掉 `\n` |
| 答案带逗号 | TAG 失败 | 去掉分隔符 |
| 先解密再验 TAG | 垃圾明文 | 先验后解 |
| 计数器用原生字节序 | 明文乱码 | 用大端 `>Q` |
| 最后一块补零后再 XOR | 尾部字节错 | 只 XOR 实际长度 |
| 对每行单独 base64 解码 | 解码异常 | 先拼接所有行 |

### 16.6 本章的结论

- 一个约 60 行的 Python 脚本就能打开任意 ITC2RECIPE 锁。
- 关键是顺序：读 recipe → 分帧 → 派生 → 验 TAG → 解密。
- 输出哈希与 7z 魔数可用于自检。

---

## 第 17 章：设计评估：为什么不用 7z 密码

### 17.1 如果直接用 7z 密码

最直接的做法是：

```text
7z a -p5050 Q2.7z SHIT/
```

优点是：

- 工具现成；
- 加密标准（AES-256）；
- 一行命令完成。

缺点是：

- 方法被工具隐藏，读者不需要理解任何东西；
- 密码错误只给“密码错误”，没有自描述；
- 读者会把“找密码”当成唯一任务，而不是“读容器”；
- 与“容器自己说明自己”的设计原则冲突。

更根本的是：用 7z 密码，这个包就变成了“猜密码 + 拖工具”，而不是“读文件 + 写代码”。

### 17.2 ITC2RECIPE 的设计取舍

| 维度 | 7z 密码 | ITC2RECIPE |
|---|---|---|
| 方法可见性 | 黑箱 | 完全可见 |
| 工具依赖 | 7z | 任意语言 + 标准库 |
| 错误反馈 | “密码错误” | TAG 失败，明确 |
| 自描述 | 否 | 是 |
| 密码学强度 | 高（AES-256） | 中（自定义流 + 128 位 MAC） |
| 读者参与 | 低 | 高 |
| 叙事一致性 | 弱 | 强 |

这不是“哪个更安全”的比较，而是“哪个更适合谜题”的比较。

### 17.3 安全边界

ITC2RECIPE 不是生产级加密：

- 块流是自定义构造，没有经过密码学审计；
- 没有盐，答案可预计算；
- TAG 截断到 128 位；
- 没有密钥轮换、没有 nonce 管理；
- recipe 本身没有认证（但改 recipe 不会帮助解密）。

它的威胁模型是：

> 防止读者在没有上一题答案的情况下直接得到下一层内容；不防止有答案的人打开。

在这个模型下，它是足够的。

### 17.4 如果重做

可以改进的地方：

1. **用 HKDF 代替裸 SHA-256**：`S = HKDF(answer, salt=file_nonce)`，增加域分隔。
2. **用完整 32 字节 TAG**：减少截断带来的理论风险。
3. **加入文件头认证**：把 recipe 的长度/版本也纳入 MAC。
4. **用标准 AEAD**：如 ChaCha20-Poly1305，但会牺牲“可手写”性。
5. **给答案加规范化函数**：明确去除空白/分隔符，减少格式错误。

但这些改进会让锁更“工程化”，更少“谜题感”。当前版本在两者之间取得了平衡。

### 17.5 本章的结论

- 不用 7z 密码，是为了让方法可见、读者参与、失败明确。
- ITC2RECIPE 在密码学上不强，但在谜题设计上合适。
- 它的真正门槛不是破解，而是理解 recipe 并写出解密器。

下一部分将用 5050 打开 Q2，进入 SHIT 层。
