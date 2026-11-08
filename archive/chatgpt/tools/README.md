# ChatGPT 对话导出工具

用于把网页版 ChatGPT 的完整对话保存为 JSON / Markdown，供解题全书做对照分析。
所有脚本只在本机运行，不经过第三方服务。

## 文件

| 文件 | 用途 |
|---|---|
| `fetch-conversation.js` | 在 ChatGPT 页面控制台运行，直接下载当前对话的完整 JSON |
| `scrape-dom.js` | 接口不可用时的兜底：滚动加载并抓取页面 DOM，导出 Markdown |
| `extract_conversation.py` | 把 JSON（完整导出或单对话）转成按角色排列的 Markdown |
| `copy-fetch-js.bat` | 把 `fetch-conversation.js` 放进剪贴板，避免手工复制 |
| `copy-dom-js.bat` | 把 `scrape-dom.js` 放进剪贴板 |

脚本本身只含 ASCII 字符；用 `.bat` 放入剪贴板，可以避免终端复制时混入零宽字符。

## 方案 A：本地抓取（推荐，私密）

1. 在浏览器打开目标对话，地址应形如 `https://chatgpt.com/c/<id>`。
2. 双击 `copy-fetch-js.bat`，脚本内容会进入剪贴板。
3. 按 F12 打开 DevTools，切到 **Console**，粘贴并回车。
   - 如果浏览器提示 “Don't paste code…”，先在 Console 里输入 `allow pasting` 再粘贴。
4. 浏览器会下载 `chatgpt-<id>.json`。
5. 把 JSON 放进项目的 `reference/` 目录（该目录默认被 `.gitignore` 忽略）。
6. 转成 Markdown：

```bash
python -I -X utf8 archive/chatgpt/tools/extract_conversation.py \
  reference/chatgpt-<id>.json -o reference/chatgpt-log.md
```

如果用的是账号完整导出包 `conversations.json`，先列对话：

```bash
python -I -X utf8 archive/chatgpt/tools/extract_conversation.py reference/conversations.json --list
```

再按 id 或标题选出目标：

```bash
python -I -X utf8 archive/chatgpt/tools/extract_conversation.py \
  reference/conversations.json --id <id> -o reference/chatgpt-log.md
```

## 方案 B：DOM 兜底

仅当方案 A 拿不到 JSON 时使用：

1. 打开对话，双击 `copy-dom-js.bat`。
2. F12 → Console，粘贴并回车。
3. 脚本会反复滚到顶部以加载历史消息，最后下载 `chatgpt-dom.md`。
4. 同样放进 `reference/`。

这个方式依赖页面渲染，超长对话可能缺少部分早期消息；所以优先方案 A。

## 方案 C：分享链接

把公开分享链接直接发给 Claude，由 Claude 尝试用 `curl` 或无头浏览器抓取。
前提：

- 链接权限必须是“任何拥有链接的人可查看”；
- 分享链接是公开的，任何拿到链接的人都能读到全文；
- 如果对话里含 5050、K 或答案推理，**不建议**用公开链接，优先方案 A。

## 方案 A 返回 401 / 403

说明前端不再用页面 cookie 直连接口。改用网络面板：

1. F12 → **Network**，过滤 `conversation`；
2. 刷新页面；
3. 找到 `/backend-api/conversation/<id>` 请求；
4. 右键 → **Copy as cURL (bash)**；
5. 把内容保存为 `reference/request.curl.sh`；
6. 在项目根目录执行：

```bash
bash reference/request.curl.sh -o reference/chatgpt.json
```

`request.curl.sh` 里含有登录凭据，不要外发，也不要提交到仓库。

## 分享链接的原始 JSON

公开分享页有一个可直接读取的接口：

```text
https://chatgpt.com/backend-api/share/<share_id>
```

返回的 JSON 包含 `mapping`、`linear_conversation`、隐藏的流式分片、代码调用和工具输出，是比页面 DOM 更完整的原始数据。保存后可用本工具转换。

注意：部分工具输出会被 OpenAI 在服务端标记为 `The output of this plugin was redacted.`，这不是抓取丢失，无法从分享接口恢复。

## 输出模式

- `--mode text`（默认）：只保留 user / assistant 的正文与 reasoning recap，适合作为主阅读稿。
- `--mode full`：额外保留代码解释器调用和执行输出，适合作为审计附录。

隐藏的流式分片（`is_visually_hidden_from_conversation`）默认不写入 Markdown，避免同一段报告重复十几次；原始 JSON 中仍然完整保留。

## 输出格式

每条消息如下：

```markdown
## 3 · assistant · 2026-11-08 10:12:33 UTC
```

- 编号、角色、UTC 时间；
- 对话头记录 id、created、source、extracted、messages；
- `create_time` 缺失时只写编号与角色，**不伪造时间**。

多个分享链接建议分别导出为 `01-*.md`、`02-*.md`，再按时间线合并；原文中的接续摘要保留并标注，不重复计入推理链。

## 隐私与提交

- `reference/` 已加入 `.gitignore`，导出的对话不会被提交。
- `archive/chatgpt/tools/` 本身只含通用脚本，可以提交。
- 不要使用会读取整段对话的第三方浏览器扩展；这类扩展会把内容上传到外部服务。
