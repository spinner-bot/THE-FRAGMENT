# 《残卷》解题全书

> **剧透警告。** 本目录是《THE FRAGMENT / 残卷》的完整解题说明书与设计拆解，包含全部答案、密钥、生成器代码和评分机制。未完成挑战者请先离开。

## 这是什么

这不是一份“答案列表”，而是一份按真实解题顺序展开的技术文档：

- 从 ZIP 的第一层字节开始，逐层拆到最终的生成器；
- 对每一层说明“看到了什么、能推出什么、为什么这样设计”；
- 给出可复现的命令、脚本、哈希和验证方法；
- 同时保留解题者的错误路径，说明哪些统计规律是陷阱；
- 最后从设计者视角复盘：结构如何承担难度，叙事如何参与判定。

## 阅读路径

| 读者 | 建议路径 |
|---|---|
| 只想核对答案 | [附录 E：五题答案速查](appendix-e-answers.md) |
| 想完整走一遍 | 从 [第 1 章](part-01-overview.md) 顺序阅读 |
| 想复现解锁 | [第 10–17 章](part-03-lock.md) + [附录 B](appendix-b-decryptor.md) |
| 想理解 Q5 | [第 43–50 章](part-07-q5.md) + [附录 D](appendix-d-q5-generator.md) |
| 想看设计意图 | [第 55 章](part-08-review.md) |
| 想对照外部解题记录 | [`archive/chatgpt/`](../../archive/chatgpt/README.md) |

## 章节目录

### 第 0 部分 · 导读

1. [这本书是什么：定位、剧透级别与读法](part-01-overview.md#第-1-章这本书是什么)
2. [全包一页图：三层结构、答案链与五个阶段](part-01-overview.md#第-2-章全包一页图)
3. [术语与符号：P/Q、锁、recipe、payload、TAG、D/K](part-01-overview.md#第-3-章术语与符号)
4. [解题总路线：从 ZIP 到生成器的决策树](part-01-overview.md#第-4-章解题总路线)

### 第 I 部分 · 入口与 P1

5. [release/THE FRAGMENT.zip：两层七件套](part-02-entry.md#第-5-章releasethe-fragmentzip两层七件套)
6. [incipit：封面作为第零道题](part-02-entry.md#第-6-章incipit封面作为第零道题)
7. [Let's go.7z 与 instruction.gz：说明书层](part-02-entry.md#第-7-章lets-go7z-与-instructiongz说明书层)
8. [说明书的真假语法：R1–R6、W1–W5 与附录](part-02-entry.md#第-8-章说明书的真假语法)
9. [P1：5050 与答案规范化](part-02-entry.md#第-9-章p15050-与答案规范化)

### 第 II 部分 · 自描述锁 ITC2RECIPE

10. [ITC2RECIPE：一个文件如何描述自己](part-03-lock.md#第-10-章itc2recipe一个文件如何描述自己)
11. [Marker 与 recipe：XOR 的可逆性](part-03-lock.md#第-11-章marker-与-recipexor-的可逆性)
12. [Body：base64、CIPHER 与 TAG 的分帧](part-03-lock.md#第-12-章bodybase64cipher-与-tag-的分帧)
13. [密钥派生：S = SHA-256(ASCII(D))](part-03-lock.md#第-13-章密钥派生s--sha-256asciid)
14. [块流：SHA-256(S ‖ uint64_be(i))](part-03-lock.md#第-14-章块流sha-256s--uint64_bei)
15. [验证：Encrypt-then-MAC](part-03-lock.md#第-15-章验证encrypt-then-mac)
16. [最小解密器：从零实现](part-03-lock.md#第-16-章最小解密器从零实现)
17. [设计评估：为什么不用 7z 密码](part-03-lock.md#第-17-章设计评估为什么不用-7z-密码)

### 第 III 部分 · P2：SHIT 层

18. [Q2.zst：zstd 与第一把锁](part-04-p2.md#第-18-章q2zstzstd-与第一把锁)
19. [用 5050 打开 Q2](part-04-p2.md#第-19-章用-5050-打开-q2)
20. [Q2 payload：SHIT.tar.xz 与 map.bmp](part-04-p2.md#第-20-章q2-payloadshit.tar.xz-与-map.bmp)
21. [SHIT.README：可读的噪音](part-04-p2.md#第-21-章shitreadme可读的噪音)
22. [SHIT.bz2：真正的题面](part-04-p2.md#第-22-章shitbz2真正的题面)
23. [仿射递推：从 10^18 次到一次幂](part-04-p2.md#第-23-章仿射递推从-1018-次到一次幂)
24. [K 的计算：77 位整数](part-04-p2.md#第-24-章k-的计算77-位整数)
25. [K 的独立验证与交接](part-04-p2.md#第-25-章k-的独立验证与交接)

### 第 IV 部分 · P3 与嵌套结构

26. [Q3.7z：README 与锁](part-05-p3.md#第-26-章q37zreadme-与锁)
27. [用 K 打开 Q3](part-05-p3.md#第-27-章用-k-打开-q3)
28. [.entrance：评分表逐行](part-05-p3.md#第-28-章entrance评分表逐行)
29. [评分函数：60 + k(k+1)/2](part-05-p3.md#第-29-章评分函数60--kk12)
30. [为什么永远拿不到 B：可达等级分析](part-05-p3.md#第-30-章为什么永远拿不到-b可达等级分析)
31. [提示经济：F、无效与无法提供](part-05-p3.md#第-31-章提示经济f无效与无法提供)
32. [P1-02C → P1-02B：base64 文本伪装](part-05-p3.md#第-32-章p1-02c--p1-02bbase64-文本伪装)
33. [P1-02A：content.tar 与 README.7z](part-05-p3.md#第-33-章p1-02acontent.tar-与-readme7z)
34. [30 位目录名与 README.json 码点](part-05-p3.md#第-34-章30-位目录名与-readmejson-码点)
35. [prompt.7z 与 puzzle.7z：原始五题](part-05-p3.md#第-35-章prompt7z-与-puzzle7z原始五题)

### 第 V 部分 · 五题数据挑战

36. [数据格式与解析器](part-06-five-questions.md#第-36-章数据格式与解析器)
37. [第 1 题：三角数分块](part-06-five-questions.md#第-37-章第-1-题三角数分块)
38. [第 2 题：Fibonacci 长度与周期 ±1](part-06-five-questions.md#第-38-章第-2-题fibonacci-长度与周期-1)
39. [第 3 题：交替增量的二次分块](part-06-five-questions.md#第-39-章第-3-题交替增量的二次分块)
40. [第 4 题：显式公式与答案文件](part-06-five-questions.md#第-40-章第-4-题显式公式与答案文件)
41. [第 5 题：为什么它是终点](part-06-five-questions.md#第-41-章第-5-题为什么它是终点)
42. [五题难度曲线与设计意图](part-06-five-questions.md#第-42-章五题难度曲线与设计意图)

### 第 VI 部分 · 第 5 题逆向工程

43. [数据形态：500 行、12 字段、负数游程](part-07-q5.md#第-43-章数据形态500-行12-字段负数游程)
44. [第一层还原：稀疏数组](part-07-q5.md#第-44-章第一层还原稀疏数组)
45. [三角数编码：(l+s)(l+s+1)/2+s](part-07-q5.md#第-45-章三角数编码)
46. [Collatz 计数 C(n) 与 round R(n)](part-07-q5.md#第-46-章collatz-计数-cn-与-round-rn)
47. [calc 的控制流：三个递归分支](part-07-q5.md#第-47-章calc-的控制流三个递归分支)
48. [分组统计与“相邻行只变一列”](part-07-q5.md#第-48-章分组统计与相邻行只变一列)
49. [从数据反推：差分、平方根、三角数、分桶](part-07-q5.md#第-49-章从数据反推差分平方根三角数分桶)
50. [正确模型：索引驱动，不是动态系统](part-07-q5.md#第-50-章正确模型索引驱动不是动态系统)

### 第 VII 部分 · 复盘与设计

51. [ChatGPT 两段对话：时间线与阶段](part-08-review.md#第-51-章chatgpt-两段对话时间线与阶段)
52. [关键错误：把统计拟合当机制](part-08-review.md#第-52-章关键错误把统计拟合当机制)
53. [提示系统的信息论](part-08-review.md#第-53-章提示系统的信息论)
54. [如果重来：最短路径](part-08-review.md#第-54-章如果重来最短路径)
55. [设计者复盘：结构即难度](part-08-review.md#第-55-章设计者复盘结构即难度)

### 附录

- [附录 A：完整文件树与 SHA-256](appendix-a-files.md)
- [附录 B：最小解密器](appendix-b-decryptor.md)
- [附录 C：P2 快速幂计算](appendix-c-p2-math.md)
- [附录 D：第 5 题生成器去混淆版](appendix-d-q5-generator.md)
- [附录 E：五题答案速查](appendix-e-answers.md)
- [附录 F：归档索引与术语表](appendix-f-index.md)

## 约定

- 所有哈希均为 SHA-256，十六进制小写。
- 所有时间均为 UTC。
- 路径以仓库根目录为基准。
- 代码块中的 `$` 表示 shell 提示符，不包含在命令中。
- 答案中的大整数按十进制原样书写，不插入分隔符。
