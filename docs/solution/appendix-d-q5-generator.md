# 附录 D：第 5 题生成器去混淆版

> **用途：** 给出可读、可运行、可验证的 Q5 参考生成器。
>
> 相关章节：第 43–50 章。原始答案文件见 `original files/第5题.答案`（863 字节）。

---

## D.1 原始代码

```python
def step(n):
    return 3*n+1 if n%2 else n//2

def count(n,m=1):
    return count(step(n),m+1) if n-1 else m

def round(n,m=0,s=0):
    return round(n,m-1 if m else count(n),count(s) if s else count(n)) if m-1 else s

def calc(n,m=1,s={},u=set(),v=[]):
    return calc(n,m+1 if m else 0,{**s,round(m):[*s[round(m)],m] if round(m) in s else [m]} if m else {},u,[next(((l + v) * (l + v + 1) // 2 + v for i, l, v in u if i == j), 0) for j in range(max((i for i, _, _ in u), default=-1) + 1)] if u else set()) if not (bool(m-n-1) ^ bool(m or v)) else sum(([-len(list(g))] if k == 0 else list(g) for k, g in __import__('itertools').groupby(v)), []) if u else calc(-1,0,{},set({k:(k,len(v),sum(v)) for k,v in s.items()}.values()),[])

if __name__ == '__main__':
    for n in range(1,int(input("loop："))+1):
        print(f"[{n}]{calc(n)}",end="  " if n%1 else "\n")
```

三个函数名 `count`、`round`、`calc` 都遮蔽了内置名或常用名；`v` 同时表示输出向量和三元组中的和。

---

## D.2 去混淆版

```python
#!/usr/bin/env python3
"""Generate rows of puzzle 5."""

import itertools
import sys
from functools import lru_cache


def step(n: int) -> int:
    return 3 * n + 1 if n % 2 else n // 2


@lru_cache(maxsize=None)
def C(n: int) -> int:
    """Number of terms from n to 1, counting both ends."""
    k = 1
    while n != 1:
        n = step(n)
        k += 1
    return k


def R(n: int) -> int:
    """C applied C(n)-1 times to C(n)."""
    s = C(n)
    for _ in range(C(n) - 1):
        s = C(s)
    return s


def encode(l: int, s: int) -> int:
    """Triangular encoding of (count, sum)."""
    return (l + s) * (l + s + 1) // 2 + s


def row(n: int) -> list[int]:
    groups: dict[int, list[int]] = {}
    for m in range(1, n + 1):
        groups.setdefault(R(m), []).append(m)

    width = max(groups) + 1
    vec = [0] * width
    for k, members in groups.items():
        vec[k] = encode(len(members), sum(members))
    return vec


def compress(vec: list[int]) -> list[int]:
    out: list[int] = []
    for value, group in itertools.groupby(vec):
        length = len(list(group))
        if value == 0:
            out.append(-length)
        else:
            out.extend([value] * length)
    return out


def generate(n: int) -> str:
    return f"[{n}]{compress(row(n))}"


def main() -> None:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    for n in range(1, limit + 1):
        print(generate(n))


if __name__ == "__main__":
    main()
```

运行：

```bash
python q5_generator.py 500 > q5.out
```

---

## D.3 输出示例

前 20 行（压缩格式，与原始数据一致）：

```text
[1][-1, 4]
[2][-1, 4, 8]
[3][-1, 4, 8, -1, 13]
[4][-1, 4, 8, -1, 52]
[5][-1, 4, 8, 26, 52]
[6][-1, 4, 8, 26, 52, -3, 34]
[7][-1, 4, 8, 26, 52, -3, 34, -8, 43]
[8][-1, 4, 8, 26, 186, -3, 34, -8, 43]
[9][-1, 4, 8, 26, 186, -3, 168, -8, 43]
[10][-1, 4, 8, 26, 186, -3, 168, -4, 76, -3, 43]
[11][-1, 4, 8, 187, 186, -3, 168, -4, 76, -3, 43]
[12][-1, 4, 8, 187, 186, -2, 103, 168, -4, 76, -3, 43]
[13][-1, 4, 8, 187, 186, -2, 403, 168, -4, 76, -3, 43]
[14][-1, 4, 8, 187, 186, -2, 403, 557, -4, 76, -3, 43]
[15][-1, 4, 8, 187, 186, -2, 403, 1220, -4, 76, -3, 43]
[16][-1, 4, 8, 187, 186, -2, 403, 2205, -4, 76, -3, 43]
[17][-1, 4, 8, 187, 186, -2, 403, 2205, -4, 462, -3, 43]
[18][-1, 4, 8, 187, 736, -2, 403, 2205, -4, 462, -3, 43]
[19][-1, 4, 8, 187, 1705, -2, 403, 2205, -4, 462, -3, 43]
[20][-1, 4, 8, 187, 3153, -2, 403, 2205, -4, 462, -3, 43]
```

第 12 行与第 13 行的差别正好说明 `R(13)=7`：

```text
第 12 行：桶 7 的成员 [12]      → l=1, s=12 → V = 91 + 12 = 103
第 13 行：桶 7 的成员 [12, 13]  → l=2, s=25 → V = 378 + 25 = 403
```

其余位置不变，所以只有 103 变成 403。这就是“每行只变一个桶”的最小例子。

---

## D.4 验证 500/500

```python
import re
from pathlib import Path

def parse(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\[(\d+)\]\s*\[(.*)\]$", line.strip())
        rows.append([int(x) for x in m.group(2).split(",")])
    return rows

actual = parse("第5题")
for n in range(1, 501):
    assert compress(row(n)) == actual[n - 1], n
print("500/500 OK")
```

这段脚本不比较空格，只比较整数列表。若要比字节，需要统一逗号后的空格和行尾。

---

## D.5 关键函数说明

### `C(n)`

```python
k = 1
while n != 1:
    n = step(n)
    k += 1
return k
```

`C(1)=1`，`C(2)=2`，`C(3)=8`，`C(4)=3`，`C(5)=6`，`C(6)=9`，`C(7)=17`。

### `R(n)`

```python
s = C(n)
for _ in range(C(n) - 1):
    s = C(s)
return s
```

例：

```text
R(3): C(3)=8; 迭代 7 次 C → 4
R(5): C(5)=6; 迭代 5 次 C → 3
R(7): C(7)=17; 迭代 16 次 C → 17
```

### `row(n)`

```python
groups = {}
for m in range(1, n + 1):
    groups.setdefault(R(m), []).append(m)
```

每个 `m` 只进一个桶。桶键最大 17，所以向量宽度最多 18。

### `compress`

```python
for value, group in itertools.groupby(vec):
    if value == 0:
        out.append(-len(list(group)))
    else:
        out.extend([value] * len(list(group)))
```

连续零变成负数，非零原样展开。

---

## D.6 复杂度与复现

- `C` 用 `lru_cache` 后，`R(1..n)` 的摊还成本很低；
- 每行重新分组是 `O(n)`；
- 生成 500 行是 `O(n²)`，在普通机器上不到一秒；
- 原始代码没有缓存，但因为 500 很小，也能跑。

---

## D.7 答案形态

第 5 题要求“生成程序”，不要求单个数字。一个合格答案应包含：

1. `step` / `C` / `R` 的定义；
2. 按 `R(m)` 分组；
3. 三角数编码；
4. 零游程压缩；
5. `[n][...]` 输出格式。

本附录的 `q5_generator.py` 就是一份完整答案。包内 `第5题.答案` 是 1,010 字节嘲讽文本，不是这份代码；真实参考代码在 `original files/第5题.答案`（863 字节）。
