# 🚀 新用户快速设置指南 - Setup Guide for New Users

> 克隆项目后的完整设置和使用说明

## 📋 目录

- [前置要求](#-前置要求)
- [快速设置](#-快速设置-5分钟)
- [验证系统](#-验证系统)
- [首次使用](#-首次使用)
- [文件位置](#-重要文件位置)
- [常用命令](#-常用命令)
- [故障排除](#-故障排除)

---

## 🔧 前置要求

### 必需软件

1. **Python 3.8+**
   ```bash
   python --version  # 应显示 3.8 或更高版本
   ```

2. **Claude Code CLI**
   - 安装：访问 [claude.ai/code](https://claude.ai/code) 下载
   - 验证：`claude --version`

3. **Git** (用于克隆项目)
   ```bash
   git --version
   ```

### 系统兼容性
- ✅ **Linux** (Ubuntu, CentOS, etc.)
- ✅ **macOS** (Intel/Apple Silicon)  
- ✅ **Windows** (WSL 推荐)

---

## ⚡ 快速设置 (5分钟)

### 1️⃣ 克隆项目
```bash
git clone <repository-url>
cd <project-name>
```

### 2️⃣ 权限设置
```bash
# 确保 hooks 脚本可执行
chmod +x .claude/hooks/*.py
chmod +x .claude/hooks/*.sh

# 验证权限
ls -la .claude/hooks/ | grep -E "(capture|auto-cache)"
```

### 3️⃣ 在 Claude Code 中打开
```bash
# 方式1：使用 Claude Code 打开
claude code .

# 方式2：直接在 Claude Code 中打开此文件夹
```

### 4️⃣ **第一次对话**
在 Claude Code 中输入任意内容，例如：
```
"hi，这是我第一次使用这个系统"
```

**✨ 就这样！系统自动启动并开始记录对话。**

---

## 🧪 验证系统

### 检查缓存系统状态
```bash
# 检查缓存系统是否运行
.claude/hooks/auto-cache.sh status
```

**预期输出**：
```
✅ Cache system running (PID: xxxxx)
```

### 检查对话日志
```bash
# 查看今天的对话记录
ls -la src/dev/cache/conversations/$(date +%Y-%m-%d).md

# 或查看最新对话
python src/scripts/cache/cache_viewer.py recent
```

### 运行完整测试
```bash
# 运行系统测试
python src/scripts/cache/start_cache.py --test
```

**预期输出**：
```
✅ Simple cache system test passed!
```

---

## 👋 首次使用

### 1. **开始研究对话**
告诉 Claude 你的研究需求：
```
"我想研究深度学习在医疗影像中的应用，帮我开始"
```

### 2. **查看对话历史**
```bash
# 查看最近7天的对话
python src/scripts/cache/cache_viewer.py recent

# 搜索特定主题
python src/scripts/cache/cache_viewer.py search "深度学习"
```

### 3. **浏览对话文件**
直接打开人类可读的对话记录：
```bash
# 用文本编辑器打开今天的对话
code src/dev/cache/conversations/$(date +%Y-%m-%d).md
```

---

## 📁 重要文件位置

### 配置文件
```
.claude/
├── settings.json          # 项目级配置（包含 hooks 配置）
├── hooks/                 # 对话捕获脚本
│   ├── capture_prompt.py  # 捕获用户输入
│   ├── capture_response.py# 捕获 Claude 回复
│   ├── capture_tools.py   # 捕获工具使用
│   └── auto-cache.sh      # 自动启动脚本
```

### 缓存和日志
```
src/dev/cache/
├── conversations/         # 📝 人类可读对话日志
│   ├── README.md         # 索引文件
│   └── 2025-XX-XX.md     # 每日对话记录
├── claude_thinking/      # 🧠 思考过程缓存
├── agent_execution/      # 🤖 代理执行记录
└── research_sessions/    # 🔬 研究会话记录
```

### 用户工作空间
```
workspace/
├── papers/     # 论文草稿存放处
├── data/       # 实验数据存放处
└── figures/    # 图表文件存放处
```

---

## 🔧 常用命令

### 缓存系统管理
```bash
# 启动缓存系统
.claude/hooks/auto-cache.sh start

# 检查系统状态
.claude/hooks/auto-cache.sh status

# 重启缓存系统
.claude/hooks/auto-cache.sh restart

# 停止缓存系统
.claude/hooks/auto-cache.sh stop
```

### 对话浏览和搜索
```bash
# 查看最近对话
python src/scripts/cache/cache_viewer.py recent --format preview

# 搜索对话内容
python src/scripts/cache/cache_viewer.py search "关键词"

# 查看系统统计
python src/scripts/cache/cache_viewer.py summary

# 导出特定日期的对话
python src/scripts/cache/cache_viewer.py export "2025-08-25"
```

### JSON 缓存查询
```bash
# 搜索 JSON 缓存
python src/scripts/cache/cache_query.py search "关键词"

# 查看缓存统计
python src/scripts/cache/cache_query.py stats

# 列出缓存文件
python src/scripts/cache/cache_query.py list
```

---

## ❓ 故障排除

### 问题1：缓存系统未启动

**症状**：无对话记录生成
```bash
.claude/hooks/auto-cache.sh status
# 输出：❌ Cache system not running
```

**解决方案**：
```bash
# 手动启动
.claude/hooks/auto-cache.sh start

# 如果启动失败，检查Python路径
which python3
python3 src/scripts/cache/start_cache.py --test
```

### 问题2：权限错误

**症状**：Hook 脚本无法执行
```bash
# 错误：Permission denied
```

**解决方案**：
```bash
# 修复权限
chmod +x .claude/hooks/*.py
chmod +x .claude/hooks/*.sh

# 验证权限
ls -la .claude/hooks/
```

### 问题3：找不到对话文件

**症状**：`src/dev/cache/conversations/` 目录为空

**解决方案**：
```bash
# 检查目录结构
ls -la src/dev/cache/

# 创建缺失目录
mkdir -p src/dev/cache/conversations

# 重新启动缓存系统
.claude/hooks/auto-cache.sh restart
```

### 问题4：Claude Code 无法识别项目

**症状**：hooks 不被触发

**解决方案**：
```bash
# 检查项目配置
cat .claude/settings.json | grep -A5 "hooks"

# 确保在 Claude Code 中正确打开项目文件夹
# 重启 Claude Code
```

---

## 🎯 使用建议

### 日常工作流
1. **开启 Claude Code**：每天启动时会自动启动缓存系统
2. **正常对话**：系统自动记录所有交互
3. **定期查看**：使用 `cache_viewer.py recent` 回顾对话
4. **搜索历史**：需要时搜索特定主题的讨论

### 最佳实践
- **对话命名**：开始新主题时明确说明，便于后续搜索
- **定期导出**：重要对话可导出保存
- **备份重要数据**：定期备份 `workspace/` 下的重要文件
- **保持更新**：定期 `git pull` 获取系统更新

### 性能优化
- **清理旧缓存**：定期清理30天前的缓存文件
- **监控磁盘空间**：对话量大时注意磁盘使用
- **合理使用搜索**：使用具体关键词提高搜索效率

---

## 🚀 现在开始！

**恭喜！你的 Claude Code 研究助手系统已完全配置完成。**

现在就开始你的第一个研究对话：
```
"我是[你的专业/身份]，想研究[你的主题]，请帮我开始"
```

### 更多帮助
- 📚 查看 [src/docs/CLAUDE.md](CLAUDE.md) 了解完整功能
- 📖 浏览 [src/examples/](../examples/) 目录查看使用示例
- 🔍 查看 [src/docs/cache-system-guide.md](cache-system-guide.md) 了解缓存系统详情

**享受你的 AI 驱动研究之旅！** 🎉