# INT LOCK 容器格式 v1

一种自定义容器:用**一个非负整数**作为唯一钥匙,对任意文件加密与认证。
不使用 7z/ZIP 的密码功能,仅依赖 PBKDF2、HMAC-SHA-256 与 SHA-256。

## 1. 容器布局

所有整数均为大端序。

| 偏移 | 长度 | 字段 | 说明 |
|---|---|---|---|
| 0 | 8 | magic | 固定为 ASCII `INTLOCK1` |
| 8 | 16 | salt | 随机盐,每次加密不同 |
| 24 | 4 | iterations | PBKDF2 迭代次数(uint32) |
| 28 | 8 | length | 密文长度(uint64) |
| 36 | length | ciphertext | 与明文等长 |
| 36+length | 16 | tag | HMAC-SHA-256 前 16 字节 |

整体大小 = 52 + 明文长度。

## 2. 密钥派生

```
password = ASCII(十进制字符串形式的整数 K,无前导零、无符号)
dk       = PBKDF2-HMAC-SHA-256(password, salt, iterations, 64 字节)
enc_key  = dk[0:32]
mac_key  = dk[32:64]
```

整数 K 必须规范化:`0` 写作 `'0'`,正整数不带 `+`、不带前导零、不带千分位。
负数与带空格的写法均视为非法。

## 3. 加密

明文字节 `P` 按 32 字节分块,第 i 块(从 0 开始):

```
stream_i = SHA-256(enc_key || uint64_be(i))
C_i      = P_i XOR stream_i      (末块按实际长度截断)
```

## 4. 认证

```
header = magic || salt || uint32_be(iterations) || uint64_be(length)
tag    = HMAC-SHA-256(mac_key, header || ciphertext)[0:16]
```

## 5. 解密

1. 校验 magic、长度关系、`iterations > 0`;
2. 用给定的 K 重新派生密钥,重算 tag;
3. `hmac.compare_digest` 比较,失败则统一报 `unlock failed`(不区分钥匙错与文件损坏);
4. 认证通过后按同一流密钥异或还原明文。

**先认证后解密**,错误钥匙不会产生任何明文输出。

## 6. 命令行

```bash
python intlock/intlock.py lock   INPUT OUTPUT --key 12345678901234567890
python intlock/intlock.py unlock INPUT OUTPUT --key 12345678901234567890
```

- `--key` 接受任意长度的十进制非负整数(Python 大整数)。
- `lock` 可加 `--iterations N` 覆盖默认 600000。
- 输出采用临时文件 + 原子重命名,不会留下半截文件。
- 失败时退出码为 1(argparse 错误为 2)。

## 7. 安全说明

- **钥匙空间**:安全性完全取决于整数 K 的不可猜性。位数少的整数可被枚举;
  PBKDF2 的 60 万次迭代只是提高单次尝试成本,不能弥补过小的钥匙空间。
  建议 K 至少 12 位十进制,或直接使用计算题的 20+ 位结果。
- **认证**:tag 只有 16 字节(128 位),伪造成功概率可忽略;
  它防止"错误钥匙偶然解出看起来正常的数据"。
- **盐**:每次加密随机,相同明文+钥匙的两次输出不同。
- **流密钥**:SHA-256(enc_key || counter) 与 AES-CTR 同级别,
  但这是自定义构造,未经第三方密码学审计;适合挑战/封装场景,
  不建议用于保护真实机密。
- 不隐藏明文长度(容器长度即明文长度 + 52 字节)。
