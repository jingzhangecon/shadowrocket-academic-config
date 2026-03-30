# Shadowrocket 学术研究配置包

这个文件夹里有一份现在就能用的完整配置，也有 3 个以后可做自动更新的模块文件。

## 文件说明

- `academic_full.conf`
  - 推荐你现在直接导入这一份。
  - 已经包含 OpenAI / Prism 稳定规则和经济学研究常用学术站点规则。
- `modules/openai_prism.sgmodule`
  - 以后如果你最关心 `prism.openai.com` 稳定性，这个模块适合单独远程更新。
- `modules/economics_research.sgmodule`
  - 学术期刊、数据库、Google Scholar、学校认证相关规则。
- `modules/quic_block.sgmodule`
  - 只负责屏蔽 UDP 443，也就是 QUIC。这个模块留作排障用，默认不建议先开。

## 现在怎么用

如果你是第一次配，先只导入 `academic_full.conf`。

在 Shadowrocket 里按这个顺序操作：

1. 打开“配置”页面。
2. 点“导入...”或者“Wi-Fi 上传”。
3. 选择 `academic_full.conf`。
4. 导入后点“使用配置”。

## 建议再检查的设置

导入后，建议把这些开关确认一下：

1. `设置 > 代理 > 代理类型`
   - 如果你平时没有特殊需求，先保持你现在能稳定用的模式。
2. `设置 > UDP > 启用转发`
   - 如果你的节点支持 UDP，就打开。
3. `设置 > 订阅 > 打开时更新`
   - 如果你用的是订阅节点，建议打开。
4. `设置 > 订阅 > 自动后台更新`
   - 如果你用的是订阅节点，建议打开。

## 如果 Prism 还是掉线

按下面顺序排查：

1. 先换一个更稳定的节点。
2. 继续使用 `academic_full.conf`。
3. 如果你碰到 Prism / OpenAI 反复掉线，再临时打开 QUIC 屏蔽模块，或者确认 `[Rule]` 里还保留这行：

```conf
AND,((PROTOCOL,UDP),(DEST-PORT,443)),REJECT-NO-DROP
```

4. 如果别的 App 因为这条规则变得异常，就把它关掉再测。

## 以后怎么做自动更新

Shadowrocket 支持远程配置和远程模块。最省心的长期方案是：

1. 把 `academic_full.conf` 和 `modules/*.sgmodule` 上传到 GitHub 仓库或 Gist。
2. 复制它们的 Raw 链接。
3. 在 Shadowrocket 中导入远程文件：
   - 远程配置：`配置 > + > 从 URL 下载`
   - 远程模块：`配置 > 模块 > + > 粘贴模块 URL`
4. 打开 Shadowrocket 里的自动更新。

默认更稳的组合是：

1. `academic_full.conf` 负责主配置。
2. `modules/openai_prism.sgmodule` 负责 OpenAI / Prism 单独调优。
3. `modules/quic_block.sgmodule` 只在需要时再开。

Shadowrocket 支持的导入链接格式：

- 配置：
  - `shadowrocket://config/add/{url}`
- 模块：
  - `shadowrocket://install?module={url}`

## 你现在只需要记住两点

1. 先用 `academic_full.conf`，这是最简单的。
2. 以后如果你想“持续更新”，就把模块放到 GitHub 上，用远程模块方式导入。
