# 附录 E：五题答案速查

> **剧透：** 本页是全部答案。只想核对时看这里；想理解过程回到第 37–50 章。
>
> 五题的“答案”不是单个数字，而是**生成公式或生成程序**，外加延伸预测。

---

## E.0 总表

| 题 | 行数 | 行长度 | 值公式 | 答案形态 |
|---|---:|---|---|---|
| Q1 | 6 | `n` | `n(n-1)/2 + k` | 公式 |
| Q2 | 8 | `F_n` | `-1 if k%5==0 else 1` | 公式 |
| Q3 | 10 | `n+2` | 行首递推 + 交替增量 | 公式/程序 |
| Q4 | 20 | `n + n%3 + 2` | `n^2 + k^2 + (n+k)%3` | 程序 |
| Q5 | 500 | 稀疏 2–18 | `R(n)` 分组 + 三角数编码 | 程序 |

外层答案链是另一条线：

```text
P1 = 5050
P2 = K = 55570866527475159802584688178377681056129853902315582853460115578675137387640
```

---

## E.1 第 1 题：三角数分块

### 公式

```text
L_n = n
a(n, k) = n(n-1)/2 + k,   k = 1..n
```

### 生成器

```python
for n in range(1, 7):
    row = [n*(n-1)//2 + k for k in range(1, n+1)]
    print(f"[{n}][{','.join(map(str, row))}]")
```

### 延伸

```text
[7][22,23,24,25,26,27,28]
[8][29,30,31,32,33,34,35,36]
```

---

## E.2 第 2 题：Fibonacci 长度与周期 ±1

### 公式

```text
F_1 = 1, F_2 = 1, F_{n+1} = F_n + F_{n-1}
L_n = F_n

a(n, k) = -1,  如果 k % 5 == 0
a(n, k) =  1,  否则
```

### 生成器

```python
fib = [1, 1]
for _ in range(20):
    fib.append(fib[-1] + fib[-2])

for n in range(1, 9):
    length = fib[n - 1]      # F_n
    row = [-1 if k % 5 == 0 else 1 for k in range(1, length + 1)]
    print(f"[{n}][{','.join(map(str, row))}]")
```

### 延伸

第 9 行长度 `F_9=34`，位置 5、10、15、20、25、30 为 `-1`，其余为 `1`。

---

## E.3 第 3 题：交替增量的二次分块

### 公式

```text
L_n = n + 2

S_1 = 1
S_{n+1} = S_n + n(n+1) + floor((n+1)/2) + 1

a(n, k) = S_n + n * ceil((k-1)/2) + (n+1) * floor((k-1)/2)
```

等价写法：

```text
t = k - 1
a(n, k) = S_n + n * ((t+1)//2) + (n+1) * (t//2)
```

### 行首表

| n | S_n |
|---:|---:|
| 1 | 1 |
| 2 | 5 |
| 3 | 13 |
| 4 | 28 |
| 5 | 51 |
| 6 | 85 |
| 7 | 131 |
| 8 | 192 |
| 9 | 269 |
| 10 | 365 |
| 11 | 481 |

### 生成器

```python
S = 1
for n in range(1, 11):
    length = n + 2
    row = []
    for k in range(1, length + 1):
        t = k - 1
        row.append(S + n * ((t + 1) // 2) + (n + 1) * (t // 2))
    print(f"[{n}][{','.join(map(str, row))}]")
    S += n * (n + 1) + (n + 1) // 2 + 1
```

### 延伸

```text
[11][481,492,504,515,527,538,550,561,573,584,596,607,619]
```

---

## E.4 第 4 题：显式公式

### 公式

```text
L_n = n + n % 3 + 2
a(n, k) = n^2 + k^2 + (n + k) % 3,   k = 1..L_n
```

### 真实答案程序

仓库 `original files/第4题.答案`，228 字节：

```python
if __name__ == "__main__":
    n = int(input())
    for i in range(1, n + 1):
        length = i + i % 3 + 2
        row = [i*i + k*k + (i+k) % 3 for k in range(1, length + 1)]
        print(f"[{i}] [{','.join(map(str, row))}]")
```

### 延伸

第 21 行长度 `21 + 0 + 2 = 23`：

```text
[21][443,447,450,458,468,477,491,507,522,542,564,585,611,639,666,698,732,765,803,843,882,926,972]
```

### 注意

发布包内 `第4题.答案` 是 1,010 字节嘲讽文本，哈希 `b1a558e2...`；真实答案在仓库 `original files/`。第 35 章解释了这个诱饵结构。

---

## E.5 第 5 题：生成程序

### 算法

```text
step(n) = 3n+1（奇）或 n/2（偶）
C(n)    = 从 n 到 1 的项数
R(n)    = C^{C(n)-1}(C(n))

对 m=1..n 按 R(m) 分组
V_k     = (l_k + s_k)(l_k + s_k + 1)/2 + s_k
压缩零游程
```

### 参考程序

```python
import itertools
from functools import lru_cache


def step(n):
    return 3 * n + 1 if n % 2 else n // 2


@lru_cache(maxsize=None)
def C(n):
    k = 1
    while n != 1:
        n = step(n)
        k += 1
    return k


def R(n):
    s = C(n)
    for _ in range(C(n) - 1):
        s = C(s)
    return s


def encode(l, s):
    return (l + s) * (l + s + 1) // 2 + s


def row(n):
    groups = {}
    for m in range(1, n + 1):
        groups.setdefault(R(m), []).append(m)

    vec = [0] * (max(groups) + 1)
    for k, members in groups.items():
        vec[k] = encode(len(members), sum(members))
    return vec


def compress(vec):
    out = []
    for value, grp in itertools.groupby(vec):
        length = len(list(grp))
        if value == 0:
            out.append(-length)
        else:
            out.extend([value] * length)
    return out


def generate(n):
    return f"[{n}]{compress(row(n))}"


for n in range(1, 501):
    print(generate(n))
```

### 延伸

第 501 行可由同一程序直接生成：

```bash
python q5_generator.py 501 | tail -1
```

不要手算 `R(501)`；用程序。

### 注意

发布包内 `第5题.答案` 是 1,010 字节嘲讽文本，哈希与 Q4 诱饵相同；真实答案在 `original files/第5题.答案`，863 字节。第 50 章给出完整验证。

---

## E.6 答案规范化

锁的密钥派生是：

```text
S = SHA-256(ASCII(D))
```

`D` 必须：

- 十进制；
- 无空格；
- 无下划线、逗号、单位；
- 无前导零（`5050` 不能写成 `05050`）；
- 无换行。

P1：

```text
5050
```

P2：

```text
55570866527475159802584688178377681056129853902315582853460115578675137387640
```

---

## E.7 答案文件对照

| 题 | 发布包内 | 仓库源文件 | 说明 |
|---|---|---|---|
| Q4 | `第4题.答案` 1,010 字节 | `original files/第4题.答案` 228 字节 | 前者诱饵，后者真实 |
| Q5 | `第5题.答案` 1,010 字节 | `original files/第5题.答案` 863 字节 | 前者诱饵，后者真实 |
| Q1–Q3 | 无答案文件 | 无 | 以公式/生成器为准 |

两个诱饵的 SHA-256 都是：

```text
b1a558e2a72a1eb9d93b3f970d5b85105f9daeeede34c44aca9babc94b483da5
```

它们就是 `original files/嘲讽文本.txt`。

---

## E.8 一句话核对

- Q1：连续整数按三角数分块。
- Q2：Fibonacci 长度 + 每 5 位一个 `-1`。
- Q3：行首二次递推 + 行内 `n, n+1` 交替。
- Q4：`n^2 + k^2 + (n+k)%3`。
- Q5：Collatz 计数再迭代 `C-1` 次，按结果分组，用三角数编码并压缩零游程。
