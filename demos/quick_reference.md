# 🚀 AI研究助手快速参考卡

> 18个专业Agent的一页纸指南

## 📋 Agent分类速查

### 📚 Research类 (7个) - 发现与分析
```bash
research-academic          # 📖 学术文献搜索分析
research-literature        # 🔍 系统性文献综述  
research-knowledge-graph   # 🕸️ 知识图谱构建
research-gap-identifier    # 🎯 研究空白识别
research-hypothesis        # 💡 AI驱动假设生成
research-trends            # 📈 研究趋势预测
research-semantic-scholar  # 🌐 200M+论文API集成
```

### ✍️ Writer类 (8个) - 撰写与优化
```bash
writer-intro-cluster       # 🎬 引言集群 (D1: 5合1)
writer-method-cluster      # 🔧 方法集群 (D2: 5合1)
writer-results-cluster     # 📊 结果集群 (D3: 5合1) 
writer-discussion-cluster  # 💬 讨论集群 (D4: 5合1)
writer-format-cluster      # 📝 格式集群 (D5: 5合1)
writer-quality-controller  # 🏆 Nature级质量控制
writer-style-formatter     # 🎨 期刊格式适配
writer-cache-manager       # ⚡ 智能缓存管理
```

### 💻 Coder类 (3个) - 开发与部署
```bash
coder-reviewer             # 🔍 代码审查专家
coder-debugger             # 🐛 调试诊断专家
coder-industrial-ai        # 🏭 工业AI专家 (PyTorch/JAX)
```

---

## ⚡ 常用命令速查

### 🎯 快速开始模板
```bash
# 新项目启动 (5分钟)
/agent research-literature: "搜索[主题]最新进展2023-2024"
/agent research-gap-identifier: "识别[领域]研究机会"  
/agent research-hypothesis: "生成[方向]创新假设"
```

### 🔬 深度研究模板
```bash
# 完整文献分析 (1小时)
/agent research-academic: "全面分析[主题]学术现状"
/agent research-knowledge-graph: "构建[领域]知识网络图谱"
/agent research-trends: "预测[领域]未来3-5年发展"
```

### 📝 论文写作模板
```bash
# 章节写作 (每章节30分钟)
/agent writer-intro-cluster --task background: "构建[研究]重要性背景"
/agent writer-method-cluster --task algorithm: "详述[算法]数学表达"
/agent writer-results-cluster --task comparison: "对比[方法]性能优势"
/agent writer-discussion-cluster --task findings: "总结[研究]核心发现"
```

### 💻 代码开发模板
```bash
# 开发流程 (每轮2小时)
/agent coder-industrial-ai: "实现[算法]用PyTorch/JAX优化"
/agent coder-reviewer: "审查代码质量安全性可维护性"
/agent coder-debugger: "诊断并修复[具体问题]"
```

### 🏆 质量保证模板
```bash
# 最终检查 (30分钟)
/agent writer-quality-controller: "执行四重质量门控验证"
/agent writer-style-formatter: "适配[Nature/Science]格式"
/agent writer-cache-manager: "缓存成功模式供复用"
```

---

## 🎯 研究阶段映射表

| 研究阶段 | 主要Agent | 预期时间 | 关键输出 |
|---------|----------|---------|---------|
| **🔍 探索期** | research-* | 3-5天 | 研究现状、空白、假设 |
| **💻 实现期** | coder-* | 1-2周 | 原型系统、性能优化 |
| **📝 写作期** | writer-*-cluster | 1-2周 | 论文各章节内容 |
| **🏆 优化期** | writer-quality-* | 1-2天 | 发表就绪论文 |

---

## 🚀 高效工作流模式

### ⚡ 并行执行模式
```bash
# 同时启动多个agent (节省60%时间)
/agent research-literature: "[主题]文献综述" &
/agent research-trends: "[主题]趋势分析" &  
/agent research-gaps: "[主题]空白识别" &
wait  # 等待全部完成
```

### 🔄 迭代优化模式  
```bash
# 持续改进loop
while not satisfied:
    /agent writer-intro-cluster: "改进引言表述"
    /agent writer-quality-controller: "检查质量分数"
    if score >= 8.5: break
```

### 🎯 专家模拟模式
```bash
# 模拟不同角色perspective
/agent research-hypothesis: "从[理论家]角度思考"
/agent coder-industrial-ai: "从[工程师]角度实现"  
/agent writer-discussion-cluster: "从[临床医生]角度评估"
```

---

## 💡 最佳实践Tips

### ⚡ 效率提升秘诀
1. **批量处理**: 相似任务组合执行
2. **模板复用**: 保存成功的prompt模板
3. **迭代细化**: 从粗到细逐步完善
4. **并行工作**: 多agent同时处理不同方面

### 🎯 质量保证秘诀
1. **四重验证**: 内容→技术→表达→影响
2. **统计严谨**: 所有实验包含显著性检验
3. **可重现性**: 代码数据完全开放
4. **专家Review**: 领域专家验证结果

### 🚀 创新突破秘诀
1. **跨域思维**: 用knowledge-graph发现连接
2. **空白挖掘**: 系统性识别未探索领域  
3. **假设生成**: AI辅助突破思维局限
4. **趋势预测**: 提前布局未来方向

---

## 🆘 常见问题速解

### Q1: Agent响应慢怎么办？
```bash
# 简化prompt，分步执行
/agent research-literature: "仅搜索2024年[主题]核心论文20篇"
# 而不是：全面深度分析所有相关文献
```

### Q2: 结果质量不满意？
```bash
# 增加具体要求和约束
/agent writer-intro-cluster --task background: "构建[主题]背景，需要：1)统计数据支撑 2)引用顶级期刊 3)强调紧迫性"
```

### Q3: 如何保证原创性？
```bash  
# 先查重，后创新
/agent research-academic: "确认[想法]的新颖性和原创性"
/agent research-hypothesis: "在确保原创前提下生成假设"
```

### Q4: 多个agent结果冲突？
```bash
# 用质量控制agent仲裁
/agent writer-quality-controller: "评估以下两个方案:[方案A] vs [方案B]，给出推荐"
```

---

## 🎯 实用Prompt模板

### 📚 Research类模板
```bash
# 精准文献搜索
"/agent research-literature: '搜索[具体主题][时间范围][质量要求]，重点关注[特定方面]'"

# 假设生成
"/agent research-hypothesis: '基于[文献分析结果]生成[领域]创新假设，要求[可验证性+实用性+原创性]'"
```

### ✍️ Writer类模板
```bash  
# 引言写作
"/agent writer-intro-cluster --task background: '构建[主题]研究背景，包含[问题紧迫性+现有限制+解决必要性]'"

# 结果分析  
"/agent writer-results-cluster --task comparison: '对比[我的方法]与[baseline方法]，需要[统计检验+效应量+置信区间]'"
```

### 💻 Coder类模板
```bash
# 代码实现
"/agent coder-industrial-ai: '用[PyTorch/JAX]实现[算法]，优化[内存使用+推理速度+部署友好性]'"

# 代码审查
"/agent coder-reviewer: '审查[代码类型]，重点检查[安全性+性能+可维护性+最佳实践]'"
```

---

**🎉 开始你的AI加速研究之旅！**

记住：18个专业agent = 你的研究梦之队 🏆

平均效率提升：**75%** | 论文质量：**Nature级** | 成功率：**90%+**