# 🔧 Claude Code Research Template - 安装指南

一键部署您的AI研究助手环境，从零到完全可用仅需5分钟。

## ⚡ 快速安装（推荐）

### 1. 获取模板
```bash
# 方法1：直接在Claude Code中使用（推荐）
# 打开 claude.ai/code → 新建项目 → 选择此模板

# 方法2：克隆现有项目
git clone https://github.com/your-username/claude-code-research-template.git
cd claude-code-research-template
```

### 2. 自动安装
```bash
# 一键安装所有依赖和配置
python setup.py

# 或者最小化安装（仅核心功能）
python setup.py --minimal
```

### 3. 立即开始
在Claude Code中打开项目文件夹，开始对话：
```
"我想研究 [你的主题]，请帮我开始"
```

---

## 📋 系统要求

### 基本要求
- **Python**: 3.9或更高版本 ✅
- **内存**: 至少2GB可用内存
- **硬盘**: 2GB可用空间
- **网络**: 互联网连接（用于文献搜索）

### 推荐配置
- **Python**: 3.10+ （更好的性能）
- **内存**: 4GB+（处理大型数据集）
- **硬盘**: 5GB+（存储更多研究数据）
- **Git**: 版本控制（可选但推荐）

### 支持的操作系统
- ✅ **Windows**: 10/11 
- ✅ **macOS**: 10.15+
- ✅ **Linux**: Ubuntu 18.04+, CentOS 7+
- ✅ **Claude Code**: 所有平台通用

---

## 🛠️ 详细安装步骤

### Step 1: 环境准备

#### Windows
```powershell
# 检查Python版本
python --version

# 如果Python版本过低，从 https://python.org 下载最新版本
# 确保安装时勾选 "Add to PATH"

# 检查pip
python -m pip --version
```

#### macOS
```bash
# 检查Python版本
python3 --version

# 如果需要安装/升级Python
brew install python@3.10

# 创建软链接（如果需要）
ln -s /usr/local/bin/python3 /usr/local/bin/python
```

#### Linux (Ubuntu/Debian)
```bash
# 更新系统包
sudo apt update

# 安装Python和pip
sudo apt install python3 python3-pip python3-venv

# 检查版本
python3 --version
pip3 --version
```

### Step 2: 获取项目

#### 方法1: Claude Code中使用（推荐）
1. 打开 [claude.ai/code](https://claude.ai/code)
2. 点击"新建项目"
3. 选择"Claude Research Template"模板
4. 项目将自动初始化

#### 方法2: 克隆仓库
```bash
# 克隆项目
git clone https://github.com/your-username/claude-code-research-template.git
cd claude-code-research-template

# 或者下载ZIP文件并解压
# 从 https://github.com/your-username/claude-code-research-template/archive/main.zip
```

### Step 3: 安装依赖

#### 选项1: 自动安装（推荐）
```bash
# 完整安装（包含所有研究功能）
python setup.py

# 最小安装（仅核心功能）
python setup.py --minimal

# 仅检查系统要求（不安装）
python setup.py --check
```

#### 选项2: 手动安装
```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装核心依赖
pip install -r requirements-minimal.txt

# 或安装完整依赖
pip install -r requirements.txt
```

### Step 4: 环境配置

#### 基础配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置文件（可选）
nano .env  # 或使用你喜欢的编辑器
```

#### API密钥配置（可选）
编辑 `.env` 文件，添加以下API密钥以增强功能：

```bash
# 文献搜索增强（推荐）
SEMANTIC_SCHOLAR_API_KEY=your_key_here

# AI功能增强（可选）
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# 其他设置保持默认即可
```

**获取免费API密钥：**
- [Semantic Scholar](https://www.semanticscholar.org/product/api) - 免费注册
- [OpenAI](https://platform.openai.com/api-keys) - 有免费额度
- [Anthropic](https://console.anthropic.com/) - 有免费额度

### Step 5: 验证安装

#### 运行测试
```bash
# 测试Python环境
python -c "import psutil, yaml; print('✅ Core dependencies OK')"

# 测试推荐依赖
python -c "import pandas, matplotlib; print('✅ Analysis tools OK')"

# 运行系统检查
python setup.py --check
```

#### 测试目录结构
```bash
# 检查关键目录
ls -la workspace/
ls -la templates/
ls -la examples/
```

---

## 🚀 快速验证

### 第一次使用测试
1. **打开Claude Code**，加载项目目录
2. **开始对话**：`"运行一个简单测试，确认系统正常工作"`
3. **预期结果**：Claude会确认系统状态并提供下一步建议

### 功能测试清单
- ✅ 文献搜索：`"搜索关于机器学习的最新论文"`
- ✅ 数据分析：`"分析workspace/data/目录中的数据"`  
- ✅ 论文写作：`"用Nature格式写一个研究计划"`
- ✅ 模板使用：`"使用templates/中的模板创建文档"`

---

## 🔧 高级配置

### 性能优化
```bash
# .env 文件中的性能设置
WORKER_THREADS=4                    # 调整线程数
MAX_CACHE_SIZE_MB=1024             # 增加缓存大小
ENABLE_PARALLEL_PROCESSING=true    # 启用并行处理
```

### 自定义配置
```bash
# 研究偏好设置
DEFAULT_LANGUAGE=zh                # 中文优先
TARGET_JOURNAL=nature              # 默认期刊格式
DEFAULT_DOMAIN=computer_science     # 研究领域
```

### 日志配置
```bash
# 详细日志（用于调试）
LOG_LEVEL=DEBUG
DEBUG_LOGGING=true

# 生产环境（推荐）
LOG_LEVEL=INFO
ENABLE_ANALYTICS=true
LOG_RETENTION_DAYS=30
```

---

## ❓ 故障排除

### 常见问题

#### 1. Python版本错误
**问题**：`Python version not supported`
```bash
# 解决方案：升级Python
# Windows: 从python.org下载最新版
# macOS: brew install python@3.10
# Linux: sudo apt install python3.10
```

#### 2. pip安装失败
**问题**：`pip install failed`
```bash
# 解决方案：升级pip
python -m pip install --upgrade pip

# 或使用镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3. 依赖冲突
**问题**：`Package conflicts detected`
```bash
# 解决方案：使用虚拟环境
python -m venv fresh_env
source fresh_env/bin/activate  # Linux/Mac
# 或 fresh_env\Scripts\activate  # Windows
pip install -r requirements-minimal.txt
```

#### 4. 权限错误
**问题**：`Permission denied`
```bash
# Linux/macOS解决方案
sudo chown -R $USER:$USER ./claude-code-research-template
chmod +x setup.py

# Windows解决方案：以管理员身份运行命令提示符
```

#### 5. 网络连接问题
**问题**：无法下载依赖包
```bash
# 解决方案：使用国内镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 诊断工具

#### 系统状态检查
```bash
# 运行完整诊断
python setup.py --check

# 查看日志
python scripts/logging/log_viewer.py --recent 5

# 检查环境变量
python -c "import os; print('LOG_LEVEL:', os.getenv('LOG_LEVEL', 'INFO'))"
```

#### 重置环境
```bash
# 完全重置（慎用）
rm -rf venv/  # 删除虚拟环境
rm .env       # 删除配置文件  
cp .env.example .env
python setup.py  # 重新安装
```

---

## 🌟 不同安装场景

### 场景1: 研究新手
```bash
# 推荐配置
python setup.py --minimal
# 编辑.env，设置DEFAULT_LANGUAGE=zh
```

### 场景2: 数据科学研究者
```bash
# 完整安装，重点数据分析
python setup.py
pip install jupyter notebook
# 在.env中启用所有数据分析工具
```

### 场景3: 机器学习研究者
```bash
# 完整安装 + ML工具
python setup.py
pip install torch tensorflow scikit-learn
# 配置GPU支持（如果有）
```

### 场景4: 团队协作
```bash
# 标准化团队配置
git clone [repo]
python setup.py
# 共享.env模板，各自配置API密钥
```

---

## 📚 下一步

### 安装完成后
1. **阅读快速入门**：查看 [QUICKSTART.md](QUICKSTART.md)
2. **尝试示例**：从 [examples/1_hello_research.md](examples/1_hello_research.md) 开始
3. **查看模板**：浏览 [templates/](templates/) 目录
4. **配置偏好**：根据需要调整 `.env` 文件

### 获取帮助
- 📖 **文档**：[README.md](README.md) 完整功能介绍
- 🎯 **示例**：[examples/](examples/) 真实使用案例
- 📊 **日志**：[logs/README.md](logs/README.md) 系统监控
- 💬 **社区**：GitHub Issues 问题讨论

---

**🎉 恭喜！您的AI研究助手环境已准备就绪！**

现在打开Claude Code，开始您的第一次AI驱动的研究之旅吧！ 🚀