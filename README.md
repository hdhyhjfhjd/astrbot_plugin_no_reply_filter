# no_reply过滤器

当大模型输出内容包含 `<<NO_REPLY>>` 时，拦截该消息，不发送给用户。

## 功能说明

- 拦截条件：模型输出文本**包含** `<<NO_REPLY>>`（大小写不敏感，`<<no_reply>>`、`<<No_Reply>>` 等均会命中）
- 拦截方式：在 `on_llm_response` 钩子中调用 `event.stop_event()`，终止消息发送
- 控制台日志仍会显示模型输出，只是不会推送给用户

## 工作原理

AstrBot 的 `on_llm_response` 事件在模型生成结果之后、发送给用户**之前**触发。
本插件在该事件中检查输出内容：

```
模型输出 ──→ on_llm_result 钩子 ──→ 包含 <<NO_REPLY>> ? ── 是 → 拦截，不发送
                                              │
                                              └─ 否 → 正常发送给用户
```

## 安装方法

1. 在 AstrBot 管理面板 → 插件 → 安装插件，上传本 zip 文件
2. 重启 AstrBot 使插件生效
3. 启动日志中出现插件加载成功提示即为正常

## 使用示例

在提示词中引导模型：当无需回复时输出 `<<NO_REPLY>>`。

例如模型返回：
```
<<NO_REPLY>>
```
→ 机器人保持沉默，用户不会收到任何消息。

## 常见问题

| 问题 | 说明 |
|------|------|
| 机器人仍然回复 | 检查模型输出是否真的包含 `<<NO_REPLY>>`，注意空格、全角/半角符号差异 |
| 想改成完全匹配 | 修改 main.py 中的判断逻辑为 `result.strip() == "<<NO_REPLY>>"` |
| 想拦截其他标记 | 修改 main.py 中 `"<<NO_REPLY>>" in result.upper()` 这一行 |

## 文件结构

```
astbot_plugin_no_reply_filter/
├── README.md        # 本说明文件
├── main.py          # 插件主代码
└── metadata.yaml    # 插件元数据
```

## 版本记录

- v1.0：初始版本，支持 `<<NO_REPLY>>` 包含匹配拦截


---

## 致谢

本插件由 [Doubao Seed 2.1 Lite](https://www.doubao.com)（豆包 AI 助手）设计与开发。
