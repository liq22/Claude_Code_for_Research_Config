# 📚 Claude Code 双轨缓存系统使用指南

## 🎯 概述

你的 Claude Code 现在配备了**双轨缓存系统**，同时提供：
- **🔍 JSON 缓存** - 用于程序化搜索和数据分析
- **📖 Markdown 对话日志** - 人类可读的对话记录

## 📁 文件结构

```
src/dev/cache/
├── conversations/           # 📝 人类可读的对话日志
│   ├── README.md           # 索引文件
│   ├── 2025-08-25.md      # 每日对话记录
│   └── 2025-08-26.md
├── claude_thinking/        # 🧠 思考过程 JSON 缓存
├── agent_execution/        # 🤖 代理执行记录
└── research_sessions/      # 🔬 研究会话记录
```

## 🚀 快速开始

### 查看最近的对话
```bash
# 查看最近 7 天的对话
python src/scripts/cache/cache_viewer.py recent

# 查看对话预览
python src/scripts/cache/cache_viewer.py recent --format preview

# 查看完整对话
python src/scripts/cache/cache_viewer.py recent --format full
```

### 搜索对话内容
```bash
# 搜索关键词
python src/scripts/cache/cache_viewer.py search "缓存系统"

# 搜索最近 30 天
python src/scripts/cache/cache_viewer.py search "research" --days 30
```

### 查看系统状态
```bash
# 显示缓存系统概览
python src/scripts/cache/cache_viewer.py summary

# 显示详细统计
python src/scripts/cache/cache_dashboard.py
```

## 📖 Markdown 对话日志特性

### 自动格式化
- **用户消息**：👤 User
- **Claude 响应**：🤖 Claude  
- **工具使用**：🔧 Tool
- **完整格式保留**：emoji、列表、代码块等

### 示例格式
```markdown
## 10:30:56 - 👤 User

请展示一个带有emoji和格式的回答测试。

## 10:31:15 - 🤖 Claude

✅ 这是一个格式化的回答示例！

### 🔧 特性展示
- **粗体文本**
- *斜体文本*  
- `代码片段`
- 📝 Emoji 支持

<details>
<summary>🔧 Tools Used (2)</summary>
- Read
- Write
</details>
```

## 🔍 高级功能

### 会话线程查看
```bash
# 查看特定会话的完整对话线程
python src/scripts/cache/cache_viewer.py session "session-id-123"
```

### 导出对话
```bash  
# 导出特定日期的对话
python src/scripts/cache/cache_viewer.py export "2025-08-25"

# 指定输出文件
python src/scripts/cache/cache_viewer.py export "2025-08-25" --output "my_conversation.md"
```

### JSON 缓存搜索
```bash
# 搜索 JSON 缓存
python src/scripts/cache/cache_query.py search "关键词"

# 查看缓存统计
python src/scripts/cache/cache_query.py stats

# 列出缓存文件
python src/scripts/cache/cache_query.py list --type thinking
```

## 🎨 自定义配置

在 `.claude/settings.json` 中可以配置：

```json
{
  "cache_system": {
    "save_markdown": true,           // 启用 Markdown 对话日志
    "conversation_logs": true,       // 启用对话记录
    "preserve_formatting": true,     // 保留格式
    "unicode_friendly": true         // Unicode 友好
  }
}
```

## 📊 缓存管理

### 清理旧文件
```bash
# 清理 30 天前的文件
python src/scripts/cache/cache_query.py cleanup --days 30
```

### 备份缓存
```bash
# 创建完整备份
python src/scripts/cache/cache_export.py --backup
```

### 导出数据
```bash
# 导出为 JSON
python src/scripts/cache/cache_export.py --format json

# 导出为 Markdown
python src/scripts/cache/cache_export.py --format markdown

# 导出所有格式
python src/scripts/cache/cache_export.py --format all
```

## 🔧 故障排除

### 缓存未更新
```bash
# 检查缓存系统状态
.claude/hooks/auto-cache.sh status

# 重启缓存系统
.claude/hooks/auto-cache.sh restart
```

### 权限问题
```bash
# 确保 hooks 可执行
chmod +x .claude/hooks/capture_*.py
```

### 查看日志
```bash
# 查看 hooks 日志
tail -f src/dev/cache/hooks.log

# 查看缓存日志
tail -f src/dev/cache/cache.log
```

## 💡 使用建议

### 日常使用
1. **回顾对话**：直接打开 `src/dev/cache/conversations/YYYY-MM-DD.md`
2. **搜索问题**：使用 `cache_viewer.py search` 找到相关讨论
3. **项目记录**：导出重要对话作为项目文档

### 研究工作流
1. **问题记录**：所有提问自动记录，便于回顾
2. **解决方案追踪**：完整的问题-解决过程保存
3. **知识积累**：可搜索的个人知识库

### 团队协作
1. **经验分享**：导出有价值的对话分享给团队
2. **问题库**：建立常见问题和解决方案库
3. **学习材料**：保存优质对话作为学习资源

## 🎉 成果展示

现在你拥有：
- **📝 人类可读**的对话记录
- **🔍 可搜索**的知识库
- **📊 完整统计**和分析工具
- **🚀 自动化**的缓存系统

享受你的 AI 助手完整记录和可追溯的研究之旅！