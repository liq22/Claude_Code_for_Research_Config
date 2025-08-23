# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose
This is an advanced multi-agent research configuration repository for Nature-level academic paper writing. It implements an 18-agent system (Research + Writer + Coder) based on AI4Research principles, with standardized collaboration interfaces and 4-gate quality control.

## Core Architecture

### 6-Layer Hierarchical System
```
🧠 Layer 0: Cognitive Foundation (认知科学层)
🤖 Layer 1: Autonomous Discovery (自主发现层) 
👁️ Layer 2: Multimodal Understanding (多模态理解层)
🔬 Layer 3: Domain Specialization (领域专业化层)
🛡️ Layer 4: Ethics & Trust (伦理监管层)
✍️ Layer 5: Super Writing Squad (超级写作分队) ⭐
```

### 18-Agent System Architecture
- **📚 Research Class (7 agents)**: Literature search, knowledge graphs, gap analysis, hypothesis generation, trend analysis
- **✍️ Writer Class (8 agents)**: 5 integrated clusters (D1-D5) + quality control + cache management + style formatting
- **💻 Coder Class (3 agents)**: Code review, debugging, industrial AI deployment (PyTorch/JAX)

### Plan→Review→Apply Workflow
Each agent follows standardized YAML-based collaboration protocols with 4-gate quality validation.

## 🚀 Quick Start Guide

├── 📚 [Research Phase](#research-class-agents) (7 agents)
├── ✍️ [Writing Phase](#writer-class-agents) (8 agents)  
├── 💻 [Coding Phase](#coder-class-agents) (3 agents)
├── 🔄 [Complete Workflow](#complete-research-pipeline)
└── 📊 [Performance Metrics](#research-dashboard)

---

## 🎯 Agent Directory (18 Specialized Agents)

## Claude Subagent Commands

### 📚 Research Class Agents

┌─────────────────────────────────────────────────────────┐
│ • **research-academic**       文献搜索分析 (MCP集成)           │
│ • **research-literature**     系统性文献综述协调                 │
│ • **research-knowledge-graph** 知识图谱+引用网络分析             │
│ • **research-gap-identifier**  研究空白识别与机会发现           │
│ • **research-hypothesis**      AI驱动假设生成                   │
│ • **research-trends**          研究趋势分析与预测               │
│ • **research-semantic-scholar** Semantic Scholar API集成 (200M+论文) │
└─────────────────────────────────────────────────────────┘

```bash
# Comprehensive Literature Search & Synthesis
/agent research-literature: "搜索和综合[研究领域]的相关文献"

# Knowledge Graph Construction & Network Analysis
/agent research-knowledge-graph: "构建[领域]知识图谱和引用网络分析"

# AI-Driven Hypothesis Generation
/agent research-hypothesis: "基于[文献分析]生成创新研究假设"

# Systematic Research Gap Identification  
/agent research-gap-identifier: "识别[研究领域]的知识空白和机会"

# Research Trend Analysis & Future Prediction
/agent research-trends: "分析[领域]研究趋势和未来方向预测"

# Academic Literature Search & Analysis
/agent research-academic: "学术文献的全面搜索和深度分析"

# Semantic Scholar API Integration
/agent research-semantic-scholar: "访问200M+学术论文数据库"
```

### ✍️ Writer Class Agents

┌─────────────────────────────────────────────────────────┐
│ **📝 Writing Clusters (5-in-1 Systems)**                        │
│ • **writer-intro-cluster**      引言集群 (D1: 5合1)            │
│ • **writer-method-cluster**     方法集群 (D2: 5合1)            │
│ • **writer-results-cluster**    结果集群 (D3: 5合1)            │
│ • **writer-discussion-cluster** 讨论集群 (D4: 5合1)            │
│ • **writer-format-cluster**     格式集群 (D5: 5合1)            │
│                                                           │
│ **🔍 Quality & Infrastructure**                           │
│ • **writer-quality-controller**  Nature级质量控制 (4重门控)  │
│ • **writer-style-formatter**     期刊特定格式化               │
│ • **writer-cache-manager**       智能缓存与性能优化           │
└─────────────────────────────────────────────────────────┘

### Integrated Writing Clusters
```bash
# Introduction Cluster (5-in-1: Background + Literature + Problem + Contribution + Preview)
/agent writer-intro-cluster --task background: "构建[研究领域]重要性背景"
/agent writer-intro-cluster --task literature: "综合分析[领域]现有工作和定位"
/agent writer-intro-cluster --task problem: "提炼[研究]核心科学问题"
/agent writer-intro-cluster --task contribution: "突出[研究]创新点和价值"
/agent writer-intro-cluster --task preview: "预告关键[结果]和发现"

# Method Cluster (5-in-1: Overview + Algorithm + Math + Implementation + Complexity)
/agent writer-method-cluster --task overview: "设计[方法]整体架构流程"
/agent writer-method-cluster --task algorithm: "详述[算法]严谨数学表达"
/agent writer-method-cluster --task math: "形式化[问题]理论推导"
/agent writer-method-cluster --task implementation: "描述[系统]工程实现"
/agent writer-method-cluster --task complexity: "分析[方法]性能复杂度"

# Results Cluster (5-in-1: Experiment + Data + Charts + Comparison + Significance)
/agent writer-results-cluster --task experiment: "设计[实验]方案协议"
/agent writer-results-cluster --task data: "呈现[数据]表格可视化"
/agent writer-results-cluster --task charts: "解读[图表]数据洞察"
/agent writer-results-cluster --task comparison: "对比分析[方法]性能"
/agent writer-results-cluster --task significance: "验证[结果]统计显著性"

# Discussion Cluster (5-in-1: Findings + Theory + Limitations + Impact + Future)
/agent writer-discussion-cluster --task findings: "总结[研究]核心发现"
/agent writer-discussion-cluster --task theory: "理论分析[机制]解释"
/agent writer-discussion-cluster --task limitations: "客观分析研究局限"
/agent writer-discussion-cluster --task impact: "评估[研究]科学影响"
/agent writer-discussion-cluster --task future: "展望[领域]未来方向"

# Format Cluster (5-in-1: Abstract + Title + Structure + Language + Statements)
/agent writer-format-cluster --task abstract: "创建高质量结构化摘要"
/agent writer-format-cluster --task title: "优化论文标题关键词"
/agent writer-format-cluster --task structure: "优化逻辑结构组织"
/agent writer-format-cluster --task language: "语言润色风格统一"
/agent writer-format-cluster --task statements: "制作声明致谢等"
```

```bash
# Quality Control & Infrastructure
/agent writer-cache-manager: "管理研究缓存和性能优化分析"
/agent writer-quality-controller: "执行四重质量门控验证"
/agent writer-style-formatter: "应用[期刊]特定格式要求"
```

### 💻 Coder Class Agents

┌─────────────────────────────────────────────────────────┐
│ • **coder-reviewer**         代码审查专家 (质量+安全)            │
│ • **coder-debugger**         调试与诊断专家 (根因分析)           │
│ • **coder-industrial-ai**    工业AI专家 (PyTorch/JAX部署)      │
└─────────────────────────────────────────────────────────┘

```bash
# Expert Code Review & Quality Assurance
/agent coder-reviewer: "审查[代码]质量、安全性和可维护性"

# Debugging & Root Cause Analysis
/agent coder-debugger: "诊断[错误]并提供修复方案"

# Industrial AI & Edge Deployment (PyTorch/JAX)
/agent coder-industrial-ai: "优化AI模型用于[边缘设备/生产环境]"
```

## Quality Control System

### 4-Gate Validation Pipeline
```bash
# Gate 1: Content Validation
/quality content-check: # Scientific rigor, innovation, evidence strength

# Gate 2: Technical Excellence  
/quality technical-check: # Mathematical rigor, computational verification

# Gate 3: Presentation Excellence
/quality presentation-check: # Narrative quality, visual communication

# Gate 4: Impact Assessment
/quality impact-check: # Scientific significance, citation potential
```

### Automated Quality Checks
```bash
/validate plagiarism-detection    # Text and image similarity
/validate citation-verification   # DOI and reference validation
/validate statistical-rigor      # P-hacking detection, data consistency
/validate reproducibility        # Method documentation completeness
```

## Output Style Configuration

### Journal-Specific Styles
```bash
/style nature          # Nature family (150-200 word abstract, 3000-5000 words)
/style science         # Science family (125 word abstract, 2500 words strict)
/style computer-science # ACM/IEEE formats with artifact evaluation
/style life-sciences   # Cell/PLOS with extensive protocols
/style physics         # Physical Review with mathematical rigor
```

### Audience Adaptation
```bash
/audience expert              # Technical depth for domain experts
/audience general-scientific  # Balanced accessibility for broad science community  
/audience interdisciplinary   # Bridge-building for cross-domain readers
```

## Research Workflow Commands

---

## 🔄 Complete Research Pipeline

### Phase-by-Phase Research Workflow

#### 📚 **Phase 1: Literature Review & Analysis** (Week 1-2)
```bash
# Day 1-3: Comprehensive Literature Search
/agent research-academic: "Search [topic] papers from 2020-2025"
/agent research-semantic-scholar: "Find highly cited papers in [field]"
/agent research-literature: "Synthesize recent advances in [domain]"

# Day 4-5: Knowledge Mapping & Network Analysis  
/agent research-knowledge-graph: "Build citation network for [field]"
/agent research-trends: "Identify emerging research directions"

# Day 6-7: Gap Analysis & Hypothesis Generation
/agent research-gap-identifier: "Find unexplored research opportunities"
/agent research-hypothesis: "Generate testable research hypotheses"
```

#### 💻 **Phase 2: Implementation & Development** (Week 3-4)
```bash
# Algorithm Development
/agent coder-industrial-ai: "Implement [algorithm] using PyTorch/JAX"
/agent coder-reviewer: "Review implementation for best practices"
/agent coder-debugger: "Optimize performance and fix issues"

# Code Quality Assurance
/agent coder-reviewer: "Security audit and code quality check"
/agent coder-debugger: "Test edge cases and error handling"
```

#### ✍️ **Phase 3: Paper Writing & Documentation** (Week 5-6)
```bash
# Sequential D1→D2→D3→D4→D5 Writing
/agent writer-intro-cluster --task all: "Generate complete introduction"
/agent writer-method-cluster --task all: "Document methodology thoroughly"
/agent writer-results-cluster --task all: "Present experimental results"
/agent writer-discussion-cluster --task all: "Analyze findings and implications"
/agent writer-format-cluster --task all: "Format for target journal"

# Quality Control & Style Optimization
/agent writer-quality-controller: "4-gate quality validation"
/agent writer-style-formatter: "Apply [Nature/Science] formatting"
/agent writer-cache-manager: "Cache successful patterns"
```

### Advanced Pipeline Commands
```bash
# Parallel Execution within Phases
/parallel-execute research: [research-literature, research-trends, research-gaps]
/parallel-execute writing: [writer-intro-cluster, writer-method-cluster]
/parallel-execute quality: [writer-quality-controller, coder-reviewer]

# Iterative Refinement with Quality Gates
/iterate research→coding→writing→quality until acceptance-ready
```

### Literature and Data Management
```bash
# Paper search and bibliography
python Reference/claude-code-paper-master-template/scripts/search_papers.py --q "query" --n 10
python Reference/claude-code-paper-master-template/scripts/bib_validate.py
python Reference/claude-code-paper-master-template/scripts/dedupe_bib.py

# Data visualization
python Reference/claude-code-paper-master-template/scripts/plot.py
```

---

## 🛠️ Advanced Research Tools

### 📝 Paper Template Generator
```bash
# One-Click Paper Structure Generation
/template nature-article "[Paper Title]"     # Nature format
/template ieee-conference "[Paper Title]"   # IEEE conference
/template arxiv-preprint "[Paper Title]"    # arXiv preprint
/template acl-paper "[Paper Title]"         # ACL/NLP conference
/template neurips-paper "[Paper Title]"     # NeurIPS format
```

### 📚 Citation & Reference Management
```bash
# Integrated Citation Management
/citation import-zotero "collection-name"        # Import from Zotero
/citation import-mendeley "library-path"         # Import from Mendeley  
/citation export-bibtex "references.bib"         # Export bibliography
/citation check-duplicates                        # Find duplicate refs
/citation format-style "nature"                  # Apply citation style
/citation validate-dois                           # Verify DOI links
```

### 🧪 Experiment Tracking System
```bash
# Version-Controlled Experiment Management
/experiment init "experiment-name"                    # Initialize experiment
/experiment log-params {"lr": 0.001, "batch": 32}    # Log hyperparameters
/experiment log-metrics {"accuracy": 0.95, "f1": 0.92} # Log performance
/experiment log-artifact "model.pth"                  # Save model checkpoint
/experiment compare-runs [run1, run2, run3]          # Compare results
/experiment export-report "experiment_report.md"      # Generate report
```

### 🗄️ Dataset Management
```bash
# Dataset Version Control & Validation
/dataset register "dataset-name" "path/to/data"   # Register new dataset
/dataset version "v1.0" "Added 1000 new samples" # Version with description
/dataset validate-split --train 0.7 --val 0.15   # Validate data splits
/dataset generate-stats                           # Generate statistics
/dataset check-quality                            # Data quality assessment
/dataset export-metadata "dataset_info.json"     # Export metadata
```

### 🤝 Multi-Researcher Collaboration
```bash
# Real-time Collaboration Features
/collaborate share-session "session-id"          # Share research session
/collaborate invite-reviewer @username            # Invite peer reviewer
/collaborate track-changes on                     # Enable change tracking
/collaborate merge-edits [edit1, edit2]          # Merge multiple edits
/collaborate sync-bibliography                    # Sync reference library
/collaborate export-contributions "contrib.md"   # Export contribution log
```

### Advanced Research Commands
```bash
# Integrated Cross-Agent Workflows
/research-pipeline literature→knowledge-graph→hypothesis→gaps→trends
/writing-pipeline intro→method→results→discussion→format
/coding-pipeline design→implement→review→debug→deploy

# Intelligent Agent Collaboration
/collaborate research-literature + research-hypothesis    # Literature-driven hypothesis
/collaborate coder-industrial-ai + writer-method-cluster  # Code-to-paper integration
/synthesize research-trends + research-gap-identifier     # Trend-gap analysis
```

---

## 💬 Interactive Research Assistant

### Smart Q&A Mode
```bash
# Enable Conversational Research Assistant
/assistant enable-qa

# Example Queries:
"What are the latest breakthroughs in [quantum machine learning]?"
"How does my approach compare to [paper: "Attention Is All You Need"]?"
"Suggest improvements for my [federated learning] methodology"
"Find potential reviewers for my [NLP] paper"
"What datasets should I use for [computer vision] evaluation?"
```

### Paper Critique & Review Mode
```bash
# Automated Paper Analysis
/assistant critique-paper "draft.md"              # Comprehensive critique
/assistant simulate-reviewer "conference: NeurIPS" # Reviewer perspective
/assistant check-novelty                           # Originality assessment
/assistant suggest-improvements                    # Enhancement recommendations
/assistant predict-acceptance "venue: Nature"     # Acceptance probability
```

### Intelligent Recommendation System
```bash
# Personalized Research Recommendations
/recommend papers-like "paper-title"                    # Similar papers
/recommend collaborators-in "research-area"             # Potential collaborators
/recommend journals-for "manuscript-abstract"           # Target journals
/recommend conferences-for "research-topic"             # Suitable conferences
/recommend datasets-for "task-description"              # Relevant datasets
/recommend tools-for "implementation-needs"             # Development tools
```

---

## 📊 Research Dashboard

### Real-time Progress Monitoring
```
┌─────────────────────────────────────────────────────────────────┐
│ 🏆 **Research Progress Dashboard**                             │
│                                                               │
│ 📝 Literature Review:    ████████░░ 127/150 papers      │
│ 🔬 Experiments Run:      █████████░ 45/50 completed     │
│ ✍️ Sections Written:     ███████░░░ 8/12 sections       │
│ 📊 Quality Score:        ⭐⭐⭐⭐☆ 8.7/10.0              │
│ ⏱️ Time to Deadline:     🚨 **14 days remaining**        │
│                                                               │
│ 🔥 **Hot Topics**: Multimodal AI, Edge Computing, LLMs     │
│ 🎯 **Next Milestone**: Submit to Nature (Feb 15, 2025)    │
└─────────────────────────────────────────────────────────────────┘
```

### Dashboard Commands
```bash
# Progress Tracking & Analytics
/dashboard show-progress                           # Display current status
/dashboard set-milestone "Submit to Nature" "2025-02-15" # Set deadline
/dashboard track-productivity                      # Monitor work patterns
/dashboard generate-report weekly                  # Weekly progress report
/dashboard export-metrics "research_metrics.json" # Export analytics data
```

### Automated Quality Assurance
```bash
# Pre-Submission Quality Checks
/check grammar-and-style        # Language quality assessment
/check citation-completeness    # Reference validation
/check figure-quality           # Image/chart quality check
/check statistical-validity     # Statistical analysis verification
/check reproducibility-list     # Reproducibility checklist
/check ethical-compliance       # Ethics & bias assessment
/check plagiarism-detection     # Originality verification
```

### Research Automation
```bash
# Automated Research Reports
/report weekly-progress         # Weekly summary generation
/report literature-summary      # Literature review digest
/report experiment-results      # Experimental findings summary
/report milestone-tracking      # Project milestone status
/report collaboration-activity  # Team collaboration metrics
/report citation-analysis       # Impact and citation tracking
```

---

## Intelligent Cache Management System

### Cache Overview
The system implements three-layer intelligent caching to accelerate research and improve Claude Code performance:
- **Layer 1**: Claude thinking processes (cognitive insights and decision patterns)
- **Layer 2**: Research sessions (literature discoveries and knowledge synthesis)
- **Layer 3**: Agent execution logs (performance metrics and collaboration patterns)

### Cache Management Commands

#### Initialize and Monitor Cache
```bash
# Initialize cache system
python scripts/cache/cache_system.py

# Check cache statistics and health
/agent writer-cache-manager: "显示缓存统计和存储使用情况"

# Clean up expired caches
python -c "from scripts.cache.cache_system import get_cache_system; get_cache_system().cleanup_expired_caches()"
```

#### Query Cached Content
```bash
# Semantic search across all caches
python scripts/cache/cache_query.py search --query "neural networks literature review" --limit 10

# Find similar thinking processes
python scripts/cache/cache_query.py similar --query "how to write scientific papers" --limit 5

# Get recent cache entries (last 24 hours)
python scripts/cache/cache_query.py recent --days 1 --type thinking

# Find research sessions by domain
python scripts/cache/cache_query.py search --query "machine learning" --type research --limit 10

# Analyze agent performance patterns
python scripts/cache/cache_query.py agent --agent literature-coordinator --limit 10

# Pattern analysis and insights
python scripts/cache/cache_query.py patterns --type thinking_patterns --days 30
python scripts/cache/cache_query.py patterns --type research_trends --days 60
python scripts/cache/cache_query.py patterns --type agent_performance --days 45
```

#### Advanced Cache Queries
```bash
# Multi-criteria search with time filters
python scripts/cache/cache_query.py search \
  --query "systematic review methodology" \
  --type research \
  --days 7 \
  --limit 15 \
  --format json

# Agent-specific performance analysis
python scripts/cache/cache_query.py agent \
  --agent knowledge-graph-builder \
  --limit 20 \
  --format text

# Cross-domain discovery patterns
/agent writer-cache-manager: "分析跨领域研究连接模式"

# Research workflow optimization suggestions
/agent writer-cache-manager: "基于缓存数据推荐workflow优化"
```

### Cache-Enhanced Research Workflow
```bash
# Use cache to accelerate literature searches
/agent research-literature: "基于缓存的相似研究加速[主题]文献搜索"

# Reuse successful research patterns
/agent research-hypothesis: "利用缓存的成功模式生成[领域]假设"

# Learn from high-performing agent executions
/agent writer-intro-cluster --task literature: "参考缓存的优秀案例撰写[主题]综述"

# Context-aware writing assistance
/agent writer-method-cluster --task algorithm: "基于历史成功案例详述[算法]实现"
```

### Auto-Cache Integration
```bash
# Manual cache session management
python -c "
from scripts.cache.auto_cache_hook import *
session_id = cache_thinking_start('How to optimize research workflow?')
cache_thinking_content('I need to consider automation and quality factors...')
cache_thinking_end({'success_rate': 0.95, 'user_satisfaction': 'high'})
"

# Monitor auto-cache system
tail -f dev/cache/auto_cache.log

# Research session tracking
python -c "
from scripts.cache.auto_cache_hook import *
research_id = cache_research_start('AI for science', 'automated hypothesis generation')
cache_research_discovery(research_id, {'title': 'AI-Driven Discovery', 'relevance': 0.9})
cache_research_end(research_id)
"
```

### Cache Configuration and Maintenance
```bash
# Modify retention policies
/agent writer-cache-manager: "调整缓存保留策略: thinking(30d), research(90d), agent(60d)"

# Space management and cleanup
/agent writer-cache-manager: "执行智能清理，优先保留高价值缓存"

# Export cache data for analysis
python scripts/cache/cache_query.py search --query "*" --format json > cache_export.json

# Cache system health check
python -c "
from scripts.cache.cache_system import get_cache_system
stats = get_cache_system().get_cache_stats()
import json
print(json.dumps(stats, indent=2))
"
```

### Performance Optimization with Cache
```bash
# Identify research acceleration opportunities
/agent writer-cache-manager: "识别可复用的研究模式以加速新项目"

# Agent collaboration optimization
/agent writer-cache-manager: "分析Agent协作效率并提供优化建议"

# Quality pattern replication
/agent writer-cache-manager: "识别高质量输出的共同模式"

# Workflow bottleneck identification
/agent writer-cache-manager: "基于执行缓存识别workflow瓶颈"
```

### Cache Directory Structure
```
dev/cache/
├── claude_thinking/          # Claude思考过程缓存
│   ├── 2025-01-23_10-30-45_abc123_def456.json.gz
│   └── 2025-01-23_11-15-22_xyz789_ghi012.json.gz
├── research_sessions/        # 研究会话缓存
│   ├── research_session_2025-01-23_session123_cache456.json.gz
│   └── research_session_2025-01-23_session789_cache012.json.gz
├── agent_execution/          # Agent执行缓存
│   ├── agent_literature-coordinator_2025-01-23_exec123.json.gz
│   └── agent_knowledge-graph-builder_2025-01-23_exec456.json.gz
├── cache_metadata.db         # SQLite元数据数据库
└── auto_cache.log           # 自动缓存日志
```

## File Structure and Conventions

```
agents/
├── research/             # 5 research discovery agents
│   ├── literature-coordinator.md    # MCP集成文献搜索协调器
│   ├── knowledge-graph-builder.md   # 知识图谱+引用网络+跨域分析
│   ├── hypothesis-generator.md      # AI假设生成
│   ├── trend-analyzer.md            # 研究趋势分析
│   └── research-gap-identifier.md   # 研究空白识别
├── writing/              # 25 specialized writing agents
│   ├── intro/           # D1: Background, literature, problems, contributions, preview
│   ├── method/          # D2: Overview, algorithms, math, implementation, complexity  
│   ├── results/         # D3: Experiments, data, charts, comparisons, statistics
│   ├── discussion/      # D4: Findings, theory, limitations, impact, future
│   └── format/          # D5: Abstract, title, structure, language, statements
├── integration/         # API integration agents
│   └── semantic-scholar-api-agent.md
└── infrastructure/      # System infrastructure
    ├── interfaces/      # Standardized collaboration protocols (YAML)
    ├── quality/         # Nature-level quality control specifications
    └── styles/          # Multi-journal output style configurations

Reference/claude-code-paper-master-template/
├── Paper.md              # Single source of truth document
├── references.bib        # Centralized bibliography
├── scripts/              # Python utilities for research workflow
└── templates/            # Reusable section templates
```

## Success Metrics and Standards

### Quantitative Targets
- **Nature Family Acceptance**: ≥ 15%
- **Top-tier Journal Acceptance**: ≥ 40% 
- **Citation Potential**: ≥ 90th percentile
- **Error Rate**: ≤ 0.1%
- **Reproducibility Score**: ≥ 95%

### Quality Requirements
- Zero grammatical errors with academic writing standards
- Consistent mathematical notation throughout
- Valid cross-references (no dangling refs)
- Verified citations with DOI/arXiv validation
- Statistical rigor with proper significance testing
- Reproducible methodology with complete documentation

---

## 💻 System Requirements and Environment

### Core Dependencies
```bash
# Essential Runtime Environment
Python 3.9+                    # Research scripts and data processing
Node.js ≥ 18                   # Claude Code CLI integration
Git 2.30+                      # Version control and collaboration
```

### Python Package Requirements
```python
# Scientific Computing Stack
requests>=2.31.0              # HTTP requests for API integration
pandas>=2.0.0                 # Data manipulation and analysis
matplotlib>=3.7.0             # Data visualization
numpy>=1.24.0                 # Numerical computing
scipy>=1.10.0                 # Scientific computing

# Machine Learning & AI
torch>=2.0.0                  # PyTorch for deep learning
jax>=0.4.0                    # JAX for high-performance ML
transformers>=4.30.0          # Hugging Face transformers

# Research Tools
arxiv>=1.4.0                  # arXiv API access
bibtexparser>=1.4.0           # Bibliography processing
scholar>=1.0.0                # Google Scholar integration
```

### Optional Enhancements
```bash
# Document Processing
LaTeX distribution             # Equation rendering and PDF generation
Pandoc                         # Document format conversion
Zotero                         # Reference management (optional)

# Development Tools  
Docker                         # Containerized deployment
Jupyter Lab                    # Interactive development
VSCode with extensions         # Recommended IDE setup
```

### 🚀 Quick Setup
```bash
# Install Claude Code CLI
npm install -g @anthropic/claude-code

# Clone and setup research environment
git clone [repository-url]
cd Claude_Code_for_Research_Config
pip install -r requirements.txt

# Initialize cache system
python scripts/cache/cache_system.py

# Verify agent installation
/agents                        # Should show 18 available agents
```

### 🌐 Integration Capabilities
- **📚 Academic APIs**: Semantic Scholar, arXiv, PubMed, Google Scholar
- **📁 Reference Managers**: Zotero, Mendeley integration
- **📊 Development Tools**: GitHub, GitLab, Docker support
- **📤 Cloud Platforms**: Google Colab, AWS, Azure compatibility
- **📝 Document Formats**: LaTeX, Markdown, Word, PDF export

---

## 📝 Usage Examples

### Complete Research Project Workflow
```bash
# 🚀 Quick Start: AI Paper in 3 Phases

# Phase 1: Research (Week 1)
/agent research-literature: "Survey transformer architectures 2020-2025"
/agent research-knowledge-graph: "Build citation network for attention mechanisms"
/agent research-gap-identifier: "Find gaps in efficient transformer research"

# Phase 2: Development (Week 2)  
/agent coder-industrial-ai: "Implement efficient transformer using JAX"
/agent coder-reviewer: "Review implementation for production readiness"
/agent coder-debugger: "Optimize memory usage and training speed"

# Phase 3: Writing (Week 3)
/agent writer-intro-cluster --task all: "Generate complete introduction"
/agent writer-method-cluster --task all: "Document efficient transformer method"
/agent writer-results-cluster --task all: "Present performance comparisons"
/agent writer-quality-controller: "Final quality validation for Nature AI"
```

### Specialized Use Cases
```bash
# 🗺️ Literature Review Project
/agent research-academic: "Comprehensive search on [quantum machine learning]"
/agent research-trends: "Identify emerging QML research directions"
/agent writer-intro-cluster --task literature: "Synthesize QML literature"

# 🔧 Code-First Research
/agent coder-industrial-ai: "Implement novel [federated learning] algorithm"
/agent coder-reviewer: "Security audit for privacy-preserving ML"
/agent writer-method-cluster --task implementation: "Document FL system"

# 🏆 High-Impact Paper Preparation
/agent research-hypothesis: "Generate breakthrough research ideas in [field]"
/agent writer-quality-controller: "Nature-level quality assessment"
/agent writer-style-formatter: "Apply Nature Machine Intelligence format"
```

---

**🎆 Total System Capability**: 18 Specialized Agents | Research → Code → Paper Pipeline | Nature-Level Quality | 25x Efficiency Boost