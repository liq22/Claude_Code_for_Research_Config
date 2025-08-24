# 🔧 故障排查指南

常见问题的快速诊断与解决方案。

## 🚨 紧急问题快速索引

### ⚡ 系统性能问题
- [Claude响应缓慢](#claude响应缓慢) 
- [内存不足错误](#内存不足错误)
- [GPU资源占用过高](#gpu资源占用过高)
- [网络连接超时](#网络连接超时)

### 📝 文档生成问题  
- [生成内容质量不佳](#生成内容质量不佳)
- [格式混乱错误](#格式混乱错误)
- [引用格式错误](#引用格式错误)
- [图表显示异常](#图表显示异常)

### 💻 代码执行问题
- [Python环境错误](#python环境错误)
- [依赖包冲突](#依赖包冲突)  
- [脚本执行失败](#脚本执行失败)
- [权限访问错误](#权限访问错误)

### 🔍 搜索功能问题
- [文献搜索结果过少](#文献搜索结果过少)
- [搜索结果不相关](#搜索结果不相关)
- [数据库访问失败](#数据库访问失败)
- [搜索速度过慢](#搜索速度过慢)

---

## 🖥️ 系统性能问题

### Claude响应缓慢

#### 🔍 问题症状
```
- 等待时间超过2分钟
- 系统显示"正在处理"但无进展
- 部分响应不完整
- 频繁出现超时错误
```

#### 🛠️ 诊断步骤
```
1. 检查网络连接
   - 测试网络延迟: ping claude.ai
   - 检查带宽使用情况
   - 确认防火墙设置

2. 系统资源检查  
   - CPU使用率: task manager / top
   - 内存使用量: 可用RAM < 2GB
   - 磁盘空间: 剩余空间 < 1GB

3. 请求复杂度分析
   - 单次请求长度 > 10,000字符
   - 并发请求数量 > 3个
   - 涉及大文件处理
```

#### ✅ 解决方案
```
immediate 立即措施:
1. 刷新页面重新开始
2. 关闭其他浏览器标签页
3. 重启Claude Code应用

short-term 短期优化:
1. 分解复杂任务为小块
2. 避免同时执行多个任务  
3. 清理本地缓存文件

long-term 长期改善:
1. 升级网络带宽
2. 增加系统RAM
3. 使用SSD提升I/O速度
```

### 内存不足错误

#### 🔍 问题症状
```
- "内存不足"错误提示
- 系统卡顿严重
- 程序意外终止
- 文件保存失败
```

#### 🛠️ 解决方案
```python
# 内存使用优化
import gc
import psutil

def check_memory():
    """检查当前内存使用情况"""
    memory = psutil.virtual_memory()
    print(f"可用内存: {memory.available / 1024**3:.2f} GB")
    print(f"使用率: {memory.percent}%")
    
    if memory.percent > 80:
        print("⚠️ 内存使用率过高，建议清理")
        return False
    return True

def optimize_memory():
    """优化内存使用"""
    # 强制垃圾回收
    gc.collect()
    
    # 清理大型变量
    # del large_variables
    
    # 分批处理数据
    chunk_size = 1000  # 调整批次大小
```

#### ✅ 系统级解决方案
```bash
# Linux/Mac系统优化
# 1. 增加虚拟内存
sudo swapon --show
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 2. 清理系统缓存
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

# 3. 关闭不必要的服务
systemctl list-units --type=service --state=running
```

### GPU资源占用过高

#### 🔍 问题诊断
```bash
# 检查GPU使用情况
nvidia-smi

# 持续监控
watch -n 1 nvidia-smi

# 查看占用GPU的进程
fuser -v /dev/nvidia*
```

#### ✅ 解决方案
```python
# GPU内存优化
import torch

def optimize_gpu_memory():
    """优化GPU内存使用"""
    if torch.cuda.is_available():
        # 清空GPU缓存
        torch.cuda.empty_cache()
        
        # 检查GPU内存
        allocated = torch.cuda.memory_allocated() / 1024**3
        cached = torch.cuda.memory_reserved() / 1024**3
        
        print(f"GPU内存已分配: {allocated:.2f} GB")
        print(f"GPU内存缓存: {cached:.2f} GB")
        
        # 设置内存增长策略
        torch.cuda.set_per_process_memory_fraction(0.8)

# 模型优化技巧
def train_with_memory_optimization(model, data_loader):
    """内存优化的训练循环"""
    for batch in data_loader:
        # 使用梯度检查点
        with torch.no_grad():
            # 推理阶段
            pass
        
        # 及时删除中间变量
        del batch
        torch.cuda.empty_cache()
```

---

## 📝 文档生成问题

### 生成内容质量不佳

#### 🔍 问题症状
```
- 内容过于简单或重复
- 缺乏专业深度
- 逻辑结构混乱
- 语言表达不准确
```

#### ✅ 优化策略
```markdown
# 提升输入质量
## 详细背景信息
"我是[专业背景]，研究领域是[具体方向]，
当前项目涉及[技术细节]，目标期刊是[期刊名称]"

## 明确具体需求
❌ 不好: "写个引言"
✅ 良好: "为transformer注意力机制优化的Nature AI论文写引言，
包含背景、现有方法局限、我们的贡献"

## 提供上下文
- 相关论文和引用
- 实验数据和结果  
- 技术细节和参数
- 目标读者和期刊要求
```

#### 🔄 迭代改进流程
```
初始生成 → 质量评估 → 具体反馈 → 重新生成 → 持续优化

示例反馈:
"这个引言需要更多技术深度，请添加：
1. 具体的性能数据对比
2. 更详细的方法描述
3. 与最新研究的关联
4. 更强的创新性表述"
```

### 格式混乱错误

#### 🔍 常见格式问题
```
- 标题层级混乱
- 引用格式不一致
- 图表编号错误
- 数学公式显示异常
```

#### ✅ 格式规范化
```latex
% LaTeX格式模板
\documentclass[journal]{IEEEtran}

% 标题层级规范
\section{Introduction}          % 一级标题
\subsection{Related Work}       % 二级标题  
\subsubsection{Deep Learning}   % 三级标题

% 引用格式统一
\bibliographystyle{IEEEtran}
\bibliography{references}

% 图表规范
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\columnwidth]{figure.pdf}
\caption{Caption text here.}
\label{fig:label}
\end{figure}
```

#### 🛠️ 自动格式检查
```python
def check_format_consistency(text):
    """检查格式一致性"""
    issues = []
    
    # 检查标题层级
    import re
    headers = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
    
    # 检查引用格式
    citations = re.findall(r'\[(\d+)\]', text)
    
    # 检查图表编号
    figures = re.findall(r'Figure\s+(\d+)', text)
    tables = re.findall(r'Table\s+(\d+)', text)
    
    return issues
```

### 引用格式错误

#### 🔍 常见引用问题
```
- 引用样式不一致: [1] vs (Smith, 2023)
- 缺少页码信息
- 作者姓名格式错误
- 期刊名称缩写不规范
```

#### ✅ 标准化解决方案
```python
# 使用标准引用管理
import pandas as pd

def standardize_citations(references):
    """标准化引用格式"""
    
    # APA格式模板
    apa_format = "{authors} ({year}). {title}. {journal}, {volume}({issue}), {pages}."
    
    # IEEE格式模板  
    ieee_format = "[{id}] {authors}, \"{title},\" {journal}, vol. {volume}, no. {issue}, pp. {pages}, {year}."
    
    # Nature格式模板
    nature_format = "{authors}. {title}. {journal} {volume}, {pages} ({year})."
    
    return formatted_refs

# 自动引用检查
def validate_references(text, style='IEEE'):
    """验证引用格式"""
    patterns = {
        'IEEE': r'\[\d+\]',
        'APA': r'\([A-Za-z]+,\s+\d{4}\)',
        'Nature': r'[A-Za-z]+\s+et\s+al\.\s+\(\d{4}\)'
    }
    
    found_citations = re.findall(patterns[style], text)
    return len(found_citations)
```

---

## 💻 代码执行问题

### Python环境错误

#### 🔍 问题症状
```
- ModuleNotFoundError: No module named 'xxx'
- Python版本不兼容
- 虚拟环境未激活
- 包版本冲突
```

#### ✅ 环境诊断与修复
```bash
# 1. 检查Python环境
python --version
which python
pip list

# 2. 虚拟环境管理
# 创建新环境
python -m venv research_env
source research_env/bin/activate  # Linux/Mac
# research_env\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r config/requirements.txt

# 4. 环境验证
python -c "import torch; print(torch.__version__)"
python -c "import numpy; print(numpy.__version__)"
```

#### 🛠️ 环境修复脚本
```python
#!/usr/bin/env python3
"""环境诊断和修复脚本"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"⚠️ Python版本过低: {version.major}.{version.minor}")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_required_packages():
    """检查必需包"""
    required = ['torch', 'numpy', 'pandas', 'matplotlib', 'scipy']
    missing = []
    
    for package in required:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing.append(package)
        else:
            print(f"✅ {package} 已安装")
    
    if missing:
        print(f"❌ 缺少包: {missing}")
        return False
    return True

def auto_fix_environment():
    """自动修复环境"""
    if not check_python_version():
        print("请升级Python到3.8+")
        return
    
    if not check_required_packages():
        print("正在安装缺少的包...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'config/requirements.txt'])

if __name__ == "__main__":
    auto_fix_environment()
```

### 依赖包冲突

#### 🔍 冲突诊断
```bash
# 检查包依赖树
pip show torch
pipdeptree

# 查找冲突
pip check

# 版本兼容性检查
pip list --outdated
```

#### ✅ 解决策略
```bash
# 1. 创建干净环境
conda create -n clean_env python=3.9
conda activate clean_env

# 2. 按优先级安装
# 首先安装核心深度学习框架
pip install torch torchvision torchaudio

# 然后安装科学计算包
pip install numpy scipy pandas matplotlib

# 最后安装其他依赖
pip install -r requirements_additional.txt

# 3. 锁定版本
pip freeze > requirements_locked.txt
```

### 脚本执行失败

#### 🔍 常见执行错误
```python
# 文件路径错误
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'

# 权限错误  
PermissionError: [Errno 13] Permission denied: '/protected/file'

# 编码错误
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff

# 内存错误
MemoryError: Unable to allocate array
```

#### ✅ 通用修复方案
```python
import os
import sys
from pathlib import Path

def robust_file_read(filepath, encodings=['utf-8', 'gbk', 'latin1']):
    """健壮的文件读取"""
    filepath = Path(filepath)
    
    # 检查文件是否存在
    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")
    
    # 检查文件权限
    if not filepath.is_file():
        raise ValueError(f"不是文件: {filepath}")
    
    # 尝试不同编码
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    raise UnicodeDecodeError("所有编码方式都失败")

def safe_script_execution(script_path, **kwargs):
    """安全的脚本执行"""
    try:
        # 设置工作目录
        original_cwd = os.getcwd()
        script_dir = Path(script_path).parent
        os.chdir(script_dir)
        
        # 执行脚本
        exec(compile(open(script_path).read(), script_path, 'exec'), kwargs)
        
    except Exception as e:
        print(f"脚本执行失败: {e}")
        return False
    finally:
        # 恢复工作目录
        os.chdir(original_cwd)
    
    return True
```

---

## 🔍 搜索功能问题

### 文献搜索结果过少

#### 🔍 可能原因
```
- 关键词过于具体
- 时间范围限制太严
- 数据库选择不当
- 搜索语法错误
```

#### ✅ 搜索策略优化
```python
def expand_search_terms(primary_keywords):
    """扩展搜索词策略"""
    
    # 同义词扩展
    synonyms = {
        'machine learning': ['ML', 'artificial intelligence', 'deep learning'],
        'natural language processing': ['NLP', 'text mining', 'computational linguistics'],
        'computer vision': ['image processing', 'pattern recognition', 'image analysis']
    }
    
    # 相关词扩展
    related_terms = {
        'transformer': ['attention mechanism', 'BERT', 'GPT', 'neural network'],
        'optimization': ['gradient descent', 'Adam', 'SGD', 'learning rate']
    }
    
    # 构建布尔搜索
    expanded_query = []
    for keyword in primary_keywords:
        if keyword in synonyms:
            terms = [keyword] + synonyms[keyword]
            expanded_query.append('(' + ' OR '.join(terms) + ')')
        else:
            expanded_query.append(keyword)
    
    return ' AND '.join(expanded_query)

# 搜索策略示例
search_strategies = [
    # 策略1: 宽泛搜索
    "transformer AND optimization",
    
    # 策略2: 具体搜索  
    "transformer AND (efficiency OR acceleration OR compression)",
    
    # 策略3: 综合搜索
    "(transformer OR attention mechanism) AND (optimization OR pruning OR quantization)"
]
```

#### 📊 多数据库搜索策略
```python
def multi_database_search(query, databases=['pubmed', 'arxiv', 'ieee']):
    """多数据库搜索"""
    
    database_configs = {
        'pubmed': {
            'url': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
            'fields': ['title', 'abstract', 'authors'],
            'format': 'xml'
        },
        'arxiv': {
            'url': 'http://export.arxiv.org/api/query',
            'fields': ['title', 'summary', 'authors'],
            'format': 'atom'
        },
        'ieee': {
            'url': 'https://ieeexploreapi.ieee.org/api/v1/search/articles',
            'fields': ['article_title', 'abstract', 'authors'],
            'format': 'json'
        }
    }
    
    all_results = []
    for db in databases:
        results = search_database(query, database_configs[db])
        all_results.extend(results)
    
    # 去重和合并
    unique_results = deduplicate_papers(all_results)
    return unique_results
```

### 搜索结果不相关

#### 🔍 问题分析
```
- 关键词歧义
- 搜索范围过宽  
- 相关性评分不准
- 领域交叉干扰
```

#### ✅ 精确度提升
```python
def improve_search_precision(query, domain='computer_science'):
    """提升搜索精确度"""
    
    # 领域限定词
    domain_filters = {
        'computer_science': ['algorithm', 'computation', 'software'],
        'biology': ['gene', 'protein', 'cell', 'molecular'],
        'physics': ['quantum', 'particle', 'wave', 'field'],
        'chemistry': ['molecule', 'reaction', 'compound', 'synthesis']
    }
    
    # 排除无关词
    exclude_terms = {
        'computer_science': ['medical', 'clinical', 'patient'],
        'biology': ['computer', 'algorithm', 'software'],
        'physics': ['social', 'economic', 'business'],
        'chemistry': ['political', 'historical', 'literary']
    }
    
    # 构建精确搜索查询
    domain_words = domain_filters.get(domain, [])
    exclude_words = exclude_terms.get(domain, [])
    
    refined_query = query
    if domain_words:
        refined_query += ' AND (' + ' OR '.join(domain_words) + ')'
    if exclude_words:
        refined_query += ' NOT (' + ' OR '.join(exclude_words) + ')'
    
    return refined_query

# 语义相关性过滤
def semantic_relevance_filter(papers, query, threshold=0.7):
    """基于语义相关性过滤"""
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    query_embedding = model.encode([query])
    relevant_papers = []
    
    for paper in papers:
        abstract = paper.get('abstract', '')
        paper_embedding = model.encode([abstract])
        similarity = cosine_similarity(query_embedding, paper_embedding)[0][0]
        
        if similarity > threshold:
            paper['relevance_score'] = similarity
            relevant_papers.append(paper)
    
    return sorted(relevant_papers, key=lambda x: x['relevance_score'], reverse=True)
```

---

## 🚨 系统错误恢复

### 数据丢失恢复

#### 🔍 数据丢失场景
```
- 意外删除文件
- 系统崩溃
- 存储设备故障
- 版本覆盖
```

#### ✅ 恢复策略
```bash
# 1. 本地文件恢复
# Linux/Mac
find /path -name "*deleted_file*" -type f 2>/dev/null
grep -r "content_snippet" /path/to/backup/

# Windows
dir /s "deleted_file*"

# 2. Git版本恢复
git log --oneline
git checkout <commit_hash> -- file_path
git reflog  # 查看所有操作历史

# 3. 系统级备份恢复
# Time Machine (Mac)
tmutil listlocalsnapshotdates
tmutil restore -v /path/to/backup

# System Restore (Windows)
vssadmin list shadows
```

#### 🛡️ 自动备份系统
```python
import shutil
import datetime
from pathlib import Path

class AutoBackup:
    def __init__(self, source_dir, backup_dir, max_backups=10):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.max_backups = max_backups
    
    def create_backup(self):
        """创建自动备份"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        try:
            shutil.copytree(self.source_dir, backup_path)
            print(f"✅ 备份成功: {backup_path}")
            
            # 清理旧备份
            self.cleanup_old_backups()
            return backup_path
            
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return None
    
    def cleanup_old_backups(self):
        """清理旧备份"""
        backups = sorted(self.backup_dir.glob("backup_*"), key=lambda x: x.stat().st_mtime)
        
        while len(backups) > self.max_backups:
            oldest = backups.pop(0)
            shutil.rmtree(oldest)
            print(f"🗑️ 删除旧备份: {oldest}")

# 使用示例
backup_system = AutoBackup("workspace", "backups")
backup_system.create_backup()
```

### 系统崩溃恢复

#### 🔍 崩溃检测
```python
import psutil
import logging
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.logger = self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('system_monitor.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def check_system_health(self):
        """检查系统健康状况"""
        health_report = {}
        
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        health_report['cpu'] = cpu_percent
        
        # 内存使用率
        memory = psutil.virtual_memory()
        health_report['memory'] = memory.percent
        
        # 磁盘使用率
        disk = psutil.disk_usage('/')
        health_report['disk'] = (disk.used / disk.total) * 100
        
        # 评估系统状态
        if cpu_percent > 90:
            self.logger.warning(f"CPU使用率过高: {cpu_percent}%")
        
        if memory.percent > 85:
            self.logger.warning(f"内存使用率过高: {memory.percent}%")
        
        if health_report['disk'] > 90:
            self.logger.warning(f"磁盘空间不足: {health_report['disk']:.1f}%")
        
        return health_report
    
    def emergency_cleanup(self):
        """紧急清理"""
        # 清理临时文件
        import tempfile
        temp_dir = tempfile.gettempdir()
        
        # 清理缓存
        cache_dirs = [
            "~/.cache",
            "~/Library/Caches",  # macOS
            "%TEMP%"  # Windows
        ]
        
        for cache_dir in cache_dirs:
            try:
                cache_path = Path(cache_dir).expanduser()
                if cache_path.exists():
                    self.logger.info(f"清理缓存目录: {cache_path}")
                    # 实际清理逻辑
            except Exception as e:
                self.logger.error(f"清理失败: {e}")

# 自动监控
monitor = SystemMonitor()
health = monitor.check_system_health()
```

---

## 📞 获取帮助

### 📧 问题报告模板
```markdown
## 问题报告

### 基本信息
- 操作系统: [Windows/macOS/Linux]
- Python版本: [x.x.x]  
- Claude Code版本: [x.x.x]
- 问题发生时间: [YYYY-MM-DD HH:MM]

### 问题描述  
[详细描述遇到的问题]

### 复现步骤
1. [步骤1]
2. [步骤2] 
3. [步骤3]

### 期望结果
[描述期望的正常行为]

### 实际结果
[描述实际发生的情况]

### 错误信息
```
[粘贴完整的错误信息和堆栈追踪]
```

### 环境信息
- 已安装的包: `pip list`
- 系统资源: CPU/内存/磁盘使用情况
- 网络状态: [网络连接情况]

### 已尝试的解决方案
[列出已经尝试过的解决方法]
```

### 🆘 紧急联系方式
```
1. 检查系统日志文件
   - logs/system.log
   - logs/error.log  
   - logs/debug.log

2. 社区支持渠道
   - GitHub Issues: [项目GitHub地址]
   - 讨论论坛: [论坛地址]
   - 用户群组: [群组信息]

3. 专业支持
   - 技术支持邮箱: support@example.com
   - 在线客服: [客服链接]
   - 电话支持: [支持电话]
```

### 🔧 自助诊断工具
```python
#!/usr/bin/env python3
"""系统自助诊断工具"""

def run_diagnostics():
    """运行完整的系统诊断"""
    
    print("🔍 开始系统诊断...")
    
    # 1. 环境检查
    check_environment()
    
    # 2. 依赖检查
    check_dependencies()
    
    # 3. 权限检查
    check_permissions()
    
    # 4. 网络检查
    check_network()
    
    # 5. 性能检查
    check_performance()
    
    print("✅ 诊断完成，请查看above输出")

if __name__ == "__main__":
    run_diagnostics()
```

---

**遇到问题不要慌，按步骤排查，快速解决** 🔧