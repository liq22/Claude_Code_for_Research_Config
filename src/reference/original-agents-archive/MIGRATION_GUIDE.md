# AI4Research Agent迁移指南

本文档说明从原始34个agents到新14个Claude subagents的迁移映射关系。

## 📋 迁移概览

| 原始架构 | 新架构 | 简化率 |
|---------|-------|--------|
| 34个独立agents | 14个Claude subagents | 59% ⬇️ |
| 复杂调用语法 | 统一`/agent`命令 | 标准化 ✅ |
| 维护困难 | 集群化管理 | 高效率 ✅ |

## 🔄 详细映射关系

### 研究发现类 (5→5, 1:1映射)

| 原始Agent | 新Subagent | 调用方式 |
|----------|------------|---------|
| `agents/research/literature-coordinator.md` | `.claude/agents/research/literature-coordinator.md` | `/agent literature-coordinator` |
| `agents/research/knowledge-graph-builder.md` | `.claude/agents/research/knowledge-graph-builder.md` | `/agent knowledge-graph-builder` |
| `agents/research/hypothesis-generator.md` | `.claude/agents/research/hypothesis-generator.md` | `/agent hypothesis-generator` |
| `agents/research/trend-analyzer.md` | `.claude/agents/research/trend-analyzer.md` | `/agent trend-analyzer` |
| `agents/research/research-gap-identifier.md` | `.claude/agents/research/research-gap-identifier.md` | `/agent research-gap-identifier` |

### 写作类 (25→5, 5:1集群化)

#### D1 引言集群 (5→1)
| 原始Agents | 新Subagent | 调用方式 |
|-----------|------------|---------|
| `writing/intro/background-narrator.md` | `.claude/agents/writing/intro-cluster.md` | `/agent intro-cluster --task background` |
| `writing/intro/literature-synthesizer.md` | 同上 | `/agent intro-cluster --task literature` |
| `writing/intro/problem-definer.md` | 同上 | `/agent intro-cluster --task problem` |
| `writing/intro/contribution-summarizer.md` | 同上 | `/agent intro-cluster --task contribution` |
| `writing/intro/result-previewer.md` | 同上 | `/agent intro-cluster --task preview` |

#### D2 方法集群 (5→1)
| 原始Agents | 新Subagent | 调用方式 |
|-----------|------------|---------|
| `writing/method/method-overview.md` | `.claude/agents/writing/method-cluster.md` | `/agent method-cluster --task overview` |
| `writing/method/algorithm-detailer.md` | 同上 | `/agent method-cluster --task algorithm` |
| `writing/method/math-modeler.md` | 同上 | `/agent method-cluster --task math` |
| `writing/method/implementation-describer.md` | 同上 | `/agent method-cluster --task implementation` |
| `writing/method/complexity-analyzer.md` | 同上 | `/agent method-cluster --task complexity` |

#### D3 结果集群 (5→1)
| 原始Agents | 新Subagent | 调用方式 |
|-----------|------------|---------|
| `writing/results/experiment-designer.md` | `.claude/agents/writing/results-cluster.md` | `/agent results-cluster --task experiment` |
| `writing/results/data-presenter.md` | 同上 | `/agent results-cluster --task data` |
| `writing/results/chart-interpreter.md` | 同上 | `/agent results-cluster --task charts` |
| `writing/results/comparison-analyst.md` | 同上 | `/agent results-cluster --task comparison` |
| `writing/results/significance-validator.md` | 同上 | `/agent results-cluster --task significance` |

#### D4 讨论集群 (5→1)
| 原始Agents | 新Subagent | 调用方式 |
|-----------|------------|---------|
| `writing/discussion/findings-summarizer.md` | `.claude/agents/writing/discussion-cluster.md` | `/agent discussion-cluster --task findings` |
| `writing/discussion/theory-explainer.md` | 同上 | `/agent discussion-cluster --task theory` |
| `writing/discussion/limitation-analyst.md` | 同上 | `/agent discussion-cluster --task limitations` |
| `writing/discussion/impact-assessor.md` | 同上 | `/agent discussion-cluster --task impact` |
| `writing/discussion/future-prospector.md` | 同上 | `/agent discussion-cluster --task future` |

#### D5 格式集群 (5→1)
| 原始Agents | 新Subagent | 调用方式 |
|-----------|------------|---------|
| `writing/format/abstract-refiner.md` | `.claude/agents/writing/format-cluster.md` | `/agent format-cluster --task abstract` |
| `writing/format/title-optimizer.md` | 同上 | `/agent format-cluster --task title` |
| `writing/format/paragraph-structurer.md` | 同上 | `/agent format-cluster --task structure` |
| `writing/format/language-polisher.md` | 同上 | `/agent format-cluster --task language` |
| `writing/format/statement-crafter.md` | 同上 | `/agent format-cluster --task statements` |

### 基础设施类 (3→3, 1:1映射优化)

| 原始Agent | 新Subagent | 调用方式 |
|----------|------------|---------|
| `infrastructure/intelligent-cache-manager.md` | `.claude/agents/infrastructure/cache-manager.md` | `/agent cache-manager` |
| `infrastructure/quality/*` | `.claude/agents/infrastructure/quality-controller.md` | `/agent quality-controller` |
| `infrastructure/styles/*` | `.claude/agents/infrastructure/style-formatter.md` | `/agent style-formatter` |

### 集成类 (1→1, 1:1映射)

| 原始Agent | 新Subagent | 调用方式 |
|----------|------------|---------|
| `integration/semantic-scholar-api-agent.md` | `.claude/agents/integration/semantic-scholar-api.md` | `/agent semantic-scholar-api` |

## 🚀 迁移优势

### 1. 调用简化
**原来**: 需要记住34个不同的agent名称和调用语法
**现在**: 只需要14个subagent + 参数化调用

### 2. 功能整合
**原来**: 写作agents分散，需要多次调用
**现在**: 集群化设计，一次调用完成复杂任务

### 3. 标准化
**原来**: 各agent有不同的输入输出格式
**现在**: 统一的Claude subagent标准

### 4. 维护性
**原来**: 34个文件分散维护
**现在**: 14个文件集中管理，减少重复

## 📝 使用示例对比

### 原始调用方式 (复杂)
```bash
# 需要多次调用不同agents
/agent writing/intro/background-narrator: "构建背景"
/agent writing/intro/literature-synthesizer: "综合文献"  
/agent writing/intro/problem-definer: "定义问题"
/agent writing/intro/contribution-summarizer: "总结贡献"
/agent writing/intro/result-previewer: "预告结果"
```

### 新调用方式 (简化)
```bash
# 一个agent通过参数完成所有功能
/agent intro-cluster --task background: "构建背景"
/agent intro-cluster --task literature: "综合文献"
/agent intro-cluster --task problem: "定义问题"
/agent intro-cluster --task contribution: "总结贡献"
/agent intro-cluster --task preview: "预告结果"
```

## 🔧 迁移检查清单

### 用户迁移步骤
- [ ] 更新调用命令：使用新的`/agent`语法
- [ ] 学习参数化：掌握`--task`参数使用
- [ ] 测试功能：确认所有功能正常工作
- [ ] 更新文档：修改个人笔记和流程文档

### 开发者迁移步骤
- [ ] 代码引用：更新所有agent路径引用
- [ ] 测试用例：修改测试脚本中的调用方式
- [ ] 文档更新：更新API文档和使用指南
- [ ] 培训材料：更新培训和演示材料

## 📚 参考资源

- **新使用指南**: `Reference/SUBAGENT_USAGE.md`
- **Claude集成**: `Reference/CLAUDE_INTEGRATION.md`
- **演示示例**: `tests/subagent_demos.md`
- **原始存档**: `Reference/original-agents-archive/`

## ❓ 常见问题

**Q: 原来的功能是否都保留了？**
A: 是的，所有功能都完整保留，只是调用方式更简化。

**Q: 性能是否有影响？**
A: 性能不受影响，集群化设计实际上提高了执行效率。

**Q: 可以混用新旧方式吗？**
A: 建议统一使用新方式，旧方式已存档仅供参考。

**Q: 如何快速上手新方式？**
A: 查看`tests/subagent_demos.md`中的详细对话示例。

---

*迁移完成后，您将拥有更高效、更易维护的AI4Research系统！*