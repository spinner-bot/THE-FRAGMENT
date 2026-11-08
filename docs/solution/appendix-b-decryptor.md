# 附录 B：最小解密器

> **用途：** 不依赖任何第三方库，打开任意一个 ITC2RECIPE 锁。
>
> 这份代码与第 16 章相同，附录只补充用法、测试向量与常见错误。

---

## B.1 完整代码

保存为 `unlock.py`：

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

---

## B.2 用法

### 读 recipe

先把 `Q2.zst` 解压成文本文件，记为 `Q2.lock.txt`。然后：

```bash
python unlock.py "Q2.lock.txt" 5050 --recipe
```

这会打印 1,182 字节的说明，不会解包。`5050` 只是占位参数，`--recipe` 分支不使用它。

### 打开 Q2

```bash
python unlock.py "Q2.lock.txt" 5050 -o "Q2.inner.7z"
```

输出应为 2,187 字节的 7z 文件，SHA-256：

```text
5d71138a6bbe2d4f4fee2f1f8e9dc657649c898b44106706a854010993bdcbf1
```

### 打开 Q3

```bash
python unlock.py "is this the true challenge == false" \
  "55570866527475159802584688178377681056129853902315582853460115578675137387640" \
  -o "Q3.payload.7z"
```

输出应为 9,831 字节，SHA-256：

```text
87f43baff2e005449cab1e68cb58d25e92429037f0b76b076838ecec608225fc
```

---

## B.3 测试向量

如果只实现核心函数，可以用这些值自检：

| 项 | 值 |
|---|---|
| `S(5050)` | `3f95b1b8a32c2c0251dfdbc3c8a30aab6d6e680cf0ef03e8af84a65dff0c4a85` |
| `S(K)` | `dd0c89d9e6528ab64403dbe3858bc9fca78c4fc18f5773068e2d52bb6f2ad3c1` |
| Q2 TAG | `feb55870ee9344f75e31597e4e68b5e8` |
| Q3 TAG | `f8fb0cca998ee5a96cd9cdc23c306e04` |
| Q2 CIPHER 长度 | 2,187 |
| Q3 CIPHER 长度 | 9,831 |

其中 `K` 为：

```text
55570866527475159802584688178377681056129853902315582853460115578675137387640
```

---

## B.4 逐段解释

### marker 与 recipe

```python
marker = lines[0]              # b"ITC2RECIPE"
encoded = bytes.fromhex(lines[1].decode("ascii"))
recipe = bytes(b ^ marker[i % len(marker)] for i, b in enumerate(encoded))
```

`ITC2RECIPE` 是 10 字节。第二行的每一个字节与 marker 循环 XOR，得到 recipe 明文。

### body 与分帧

```python
body = b"".join(lines[3:])
raw = base64.b64decode(body)
cipher, tag = raw[:-16], raw[-16:]
```

- 跳过前三行（marker、hex、空行）；
- 把所有 base64 行拼成一个字符串；
- 最后 16 字节是 TAG，前面是 CIPHER。

不要逐行 base64 解码：一行可能不是 4 的倍数。

### 密钥

```python
S = hashlib.sha256(answer.encode("ascii")).digest()
```

答案必须是 ASCII 十进制字符串，不能有空格、前导零、单位或换行。

### 验证

```python
expected = hashlib.sha256(S + b"\x02" + cipher).digest()[:16]
if not hmac.compare_digest(expected, tag):
    raise ValueError("wrong answer or corrupted lock")
```

这是 encrypt-then-MAC：先验证，再解密。验证失败时不要输出任何明文。

### 解密

```python
for offset in range(0, len(cipher), 32):
    counter = offset // 32
    stream = hashlib.sha256(S + struct.pack(">Q", counter)).digest()
    out.extend(a ^ b for a, b in zip(block, stream))
```

- 块大小 32 字节，与 SHA-256 输出一致；
- `counter` 是大端 64 位；
- 最后一块可能不足 32 字节，`zip` 会自动截断。

---

## B.5 常见错误

| 现象 | 原因 | 修正 |
|---|---|---|
| `binascii.Error: Invalid base64` | 逐行解码 | 先拼接所有行 |
| `ValueError: wrong answer` | 答案有空格/换行/前导零 | 规范化为纯十进制 |
| 解出的 7z 打不开 | 把 TAG 当密文 | `cipher = raw[:-16]` |
| `UnicodeDecodeError` | 对二进制做 `.decode()` | 只对 recipe 解码 |
| Q3 解不开 | 用了 5050 | Q3 的 `D` 是 K |
| 输出长度不对 | 最后一块处理错 | 用 `zip` 截断，不要补零 |

---

## B.6 安全边界

这不是生产级加密：

- XOR 流可被已知明文攻击；
- 没有盐、没有迭代、没有认证密钥分离；
- TAG 只覆盖 CIPHER，不覆盖 recipe。

它的目标是“可读、可推理、可手写解密器”，不是“抗攻击”。第 17 章讨论了这一取舍。

---

## B.7 一句话总结

一个锁文件 = 自描述的 10 字节 marker + 1,182 字节 recipe + base64(`CIPHER || TAG`)。解密只需标准库的 `hashlib`、`base64`、`struct` 和一次 XOR 循环。
