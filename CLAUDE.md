# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose
This is an advanced multi-agent research configuration repository for Nature-level academic paper writing. It implements a 25-agent system based on GPT-5 recommendations and AI4Research principles, with standardized collaboration interfaces and 4-gate quality control.

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

### 25-Agent Writing System (D1-D5 Clusters)
- **D1 Introduction Cluster (5 agents)**: Background, literature, problems, contributions, results preview
- **D2 Method Cluster (5 agents)**: Overview, algorithms, math modeling, implementation, complexity
- **D3 Results Cluster (5 agents)**: Experiments, data, charts, comparisons, statistical validation  
- **D4 Discussion Cluster (5 agents)**: Findings, theory, limitations, impact, future work
- **D5 Format Cluster (5 agents)**: Abstract, title, structure, language, statements

### Plan→Review→Apply Workflow
Each agent follows standardized YAML-based collaboration protocols with 4-gate quality validation.

## Agent Invocation Commands

### Research Discovery Commands
```bash
# Literature Search and Analysis (调用MCP academic-researcher + 增强功能)
/agent research/literature-coordinator: "搜索和综合[研究领域]的相关文献"

# Knowledge Graph and Network Analysis (整合citation网络和跨域分析)
/agent research/knowledge-graph-builder: "构建[领域]知识图谱和引用网络"

# Research Innovation and Gaps
/agent research/hypothesis-generator: "基于[文献分析]生成研究假设"
/agent research/research-gap-identifier: "识别[研究领域]的知识空白"
/agent research/trend-analyzer: "分析[领域]研究趋势和未来方向"
```

### D1 Introduction Writing Cluster
```bash
/agent writing/intro/background-narrator: "构建[研究领域]的问题重要性和背景"
/agent writing/intro/literature-synthesizer: "综合分析[领域]现有工作并准确定位"
/agent writing/intro/problem-definer: "提炼[研究]的核心科学问题和挑战"
/agent writing/intro/contribution-summarizer: "突出[研究]创新点和差异化价值"
/agent writing/intro/result-previewer: "选择最有说服力的[结果]预告"
```

### D2 Method Writing Cluster
```bash
/agent writing/method/method-overview: "设计[方法]整体架构和处理流程"
/agent writing/method/algorithm-detailer: "提供[算法]严谨的数学表达"
/agent writing/method/math-modeler: "形式化[问题]和理论推导"
/agent writing/method/implementation-describer: "详细描述[系统]工程实现细节"
/agent writing/method/complexity-analyzer: "全面分析[方法]性能和复杂度"
```

### D3 Results Writing Cluster  
```bash
/agent writing/results/experiment-designer: "详细说明[实验]设计方案和协议"
/agent writing/results/data-presenter: "设计清晰的[数据]表格和可视化"
/agent writing/results/chart-interpreter: "深入分析[图表]数据洞察"
/agent writing/results/comparison-analyst: "公平客观的[方法]对比分析"
/agent writing/results/significance-validator: "严谨的[结果]统计分析验证"
```

### D4 Discussion Writing Cluster
```bash
/agent writing/discussion/findings-summarizer: "提炼[研究]核心发现和价值"
/agent writing/discussion/theory-explainer: "深入[机制]理论分析和解释"
/agent writing/discussion/limitation-analyst: "客观分析[研究]不足和局限"
/agent writing/discussion/impact-assessor: "全面评估[研究]科学影响"
/agent writing/discussion/future-prospector: "规划[领域]研究方向和趋势"
```

### D5 Format Writing Cluster
```bash
/agent writing/format/abstract-refiner: "创建高质量结构化摘要"
/agent writing/format/title-optimizer: "优化论文标题和关键词"
/agent writing/format/paragraph-structurer: "优化逻辑流程和段落结构"
/agent writing/format/language-polisher: "确保语言质量和风格统一"
/agent writing/format/statement-crafter: "制作各类声明和致谢"
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

### Complete Pipeline Execution
```bash
# Sequential D1→D2→D3→D4→D5 workflow
/execute-pipeline intro→method→results→discussion→format

# Parallel execution within clusters
/parallel-execute D1: [background-narrator, literature-synthesizer]

# Iterative refinement with quality gates
/iterate D1→D5→D1 until quality-threshold-met
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

### Advanced Research Commands
```bash
# Integrated Research Workflow (整合MCP academic-researcher)
/research-pipeline literature-search→knowledge-graph→hypothesis→gaps→trends

# Cross-agent Collaboration
/collaborate research/literature-coordinator research/hypothesis-generator
/synthesize research/trend-analyzer research/research-gap-identifier

# MCP Integration Examples
/agent research/literature-coordinator: "使用academic-researcher搜索[主题]并扩展分析"
```

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
/agent infrastructure/intelligent-cache-manager: "显示缓存统计和存储使用情况"

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
/agent infrastructure/intelligent-cache-manager: "分析跨领域研究连接模式"

# Research workflow optimization suggestions
/agent infrastructure/intelligent-cache-manager: "基于缓存数据推荐workflow优化"
```

### Cache-Enhanced Research Workflow
```bash
# Use cache to accelerate literature searches
/agent research/literature-coordinator: "基于缓存的相似研究加速[主题]文献搜索"

# Reuse successful research patterns
/agent research/hypothesis-generator: "利用缓存的成功模式生成[领域]假设"

# Learn from high-performing agent executions
/agent writing/intro/literature-synthesizer: "参考缓存的优秀案例撰写[主题]综述"

# Context-aware writing assistance
/agent writing/method/algorithm-detailer: "基于历史成功案例详述[算法]实现"
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
/agent infrastructure/intelligent-cache-manager: "调整缓存保留策略: thinking(30d), research(90d), agent(60d)"

# Space management and cleanup
/agent infrastructure/intelligent-cache-manager: "执行智能清理，优先保留高价值缓存"

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
/agent infrastructure/intelligent-cache-manager: "识别可复用的研究模式以加速新项目"

# Agent collaboration optimization
/agent infrastructure/intelligent-cache-manager: "分析Agent协作效率并提供优化建议"

# Quality pattern replication
/agent infrastructure/intelligent-cache-manager: "识别高质量输出的共同模式"

# Workflow bottleneck identification
/agent infrastructure/intelligent-cache-manager: "基于执行缓存识别workflow瓶颈"
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

## Dependencies and Environment
- Python 3.9+ (for research scripts and data processing)
- Node.js ≥ 18 (for Claude Code CLI integration)  
- Standard libraries: requests, pandas, matplotlib, numpy
- LaTeX distribution (for equation rendering)
- Git (for version control and collaboration)