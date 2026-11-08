# ChatGPT 解题记录归档

这里保存外部模型对《残卷》的完整解题过程，供后续编写解题全书时对照。

## 结构

```text
archive/chatgpt/
├─ README.md
└─ 01/
   ├─ share-01.raw.json      # 分享接口返回的原始 JSON
   ├─ share-01.raw.html      # 分享页原始 HTML，用于交叉核对
   ├─ transcript.md          # 清洗稿：user / assistant 正文 + recap
   ├─ transcript-full.md     # 完整稿：额外包含代码调用与执行输出
   └─ manifest.json          # 来源、大小、SHA-256
```

## 约定

- 原始数据保持字节不变，不做换行转换（仓库 `.gitattributes` 已设置 `* -text`）。
- 清洗稿保留每条消息的编号、发言者和 UTC 时间戳。
- `transcript.md` 不包含隐藏的流式分片，避免同一段报告重复出现；原始 JSON 中仍完整保留。
- 部分工具输出被 OpenAI 在服务端标记为 `The output of this plugin was redacted.`，归档中保留该事实，不做补写。
- 本地工作副本放在 `reference/`，该目录被 `.gitignore` 忽略；本目录是正式归档。

## 分段

| 段 | 标题 | 来源 | 时间范围（UTC） | 消息数 |
|---|---|---|---|---|
| 01 | 接受挑战 Fragment | [链接](https://chatgpt.com/share/6af080c0-eaf8-83e8-ac1d-831c8490c346) | 2026-11-08 11:18:23 → 13:22:37 | 36 正文 / 420 完整 |
