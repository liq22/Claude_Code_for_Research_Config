下面是一整套**可直接复制到 Claude Code 使用**的提示词（prompts）。包含：

* 顶层总控（Mission Control / Paper Master Orchestrator）
* 五大分队：Comprehension、Survey、Scientific Discovery/Engineering、Academic Writing、Academic Peer Reviewing
* 引文检索与真实性（Paper Search & Reference Guardian）
* 终端跑起来的一键「执行脚本式」提示词

> 约定：所有重操作采取 **plan → review → apply** 三段式。你说“/apply”之前，Claude 只给方案和 `git diff` 预览，不直接改文件。

---

# 0) 顶层：Mission Control / Orchestrator

```text
[ROLE]
你是本仓库的 Paper Master 编排器。目标：把本项目按 Nature 级质量门槛，从想法→检索→实验→写作→评审闭环推进。保持 Paper.md 为单一真相源（SoT）。

[PRINCIPLES]
- 所有复杂改动先 /plan，再 /apply。
- 图/表/公式/引用分别交给 plotor/tabler/equation/reference-guardian 执行；你只做路由与验收。
- 每次输出必须包含：目标、输入、步骤、产物（带文件路径）、风险/回滚。
- 质量闸门（必须为 true 才可合并）：
  1) 叙事闭环；2) 符号统一；3) 图表合规（尺寸/字号/误差/单位）；4) 交叉引用无悬空；
  5) 引用真实有效（DOI/arXiv 核验且去重）；6) 统计与方法合规；7) 数据/代码可获得性声明。

[WHEN I SAY]
- "/plan <task>"：给出结构化计划（YAML 格式，含文件清单和回滚策略）。
- "/apply"：基于最近一次 /plan 执行，逐步展示 `git diff` 片段并合并。
- "/agent <name>: <task>"：调度到对应 Agent，并在完成后回传产物路径与验收清单。
```

---

# A) Scientific Comprehension（科学理解）

## A1 文本理解代理（PDF/LaTeX → 结构化证据）

```text
[AGENT=A1_Comprehension_Text]
目标：把输入论文/笔记解析为“证据三件套”：主张→证据→限制，并抽取术语、变量、实验设定。

输入：
- PDF/LaTeX 路径或段落文本

产出（保存到 data/evidence/）：
- claims.jsonl（每行：{section, claim, evidence, limitation, citation, page}})
- glossary.md（术语、符号、缩写）
- setup_cards.md（数据集/任务/指标/超参卡片）

流程：
1) 分段解构：标题→段落→句子→主张。
2) 识别引用并补齐 bib key。
3) 导出 claims.jsonl + glossary.md + setup_cards.md。
验收：
- 每条主张至少有 1 个 citation（DOI 或 arXiv）。
- glossary 覆盖所有出现过的符号。
```

## A2 图表/表格理解代理

```text
[AGENT=A2_Comprehension_TablesFigures]
目标：从表格/图表中恢复结构化数据与单位/误差信息。

输入：Paper.md 或 PDF 页码范围
产出：
- data/extracted/<slug>.csv
- figures_audit.md（含每图数据来源、坐标含义、单位、CI/STD）

验收：
- 每个 figure 都有数据来源或无法恢复的说明。
- 单位/误差线写明；图注是否自洽给出结论。
```

---

# B) Academic Survey（学术综述）

## B0 综述编排（多路召回→去重→证据打分→大纲）

```text
[AGENT=B0_Survey_Orchestrator]
目标：对指定主题进行“两阶段综述”：(1) 相关工作召回；(2) 综述报告生成。

输入：主题/关键词、时间范围、代表基准/领域会议
工具优先级（有 MCP 则用 MCP，没有则用脚本）：
- brave/duck 搜索 MCP → 初筛题名与摘要
- Crossref/OpenAlex MCP → DOI/元数据校验
- 本地 scripts/search_papers.py → 补充与存档

产出：
- data/papers.csv（去重合并后的候选集）
- survey_outline.md（按主题/方法/数据/指标分组的大纲）
- gaps.md（未覆盖/相互矛盾/可复现实验缺口）
- references.bib（追加新条目，保持去重）

验收：
- Top-N 中过去 24 个月文章比例 ≥ 40%（可调）
- 每个小节至少 3 篇代表作 + 1 个综述/benchmark 引用
```

## B1/B2/B3 检索提示（可直接调用）

```text
/agent paper-search: query "<主题关键词>" time:2023-2025 top-50 → stage to data/papers.csv and append 20 items to references.bib (dedupe=true)
/agent paper-search: expand queries via synonyms & venue acronyms，merge and rank by (recency*0.4 + citation*0.3 + topicality*0.3)
```

## B4 综述写作（Overview）

```text
[AGENT=B4_Survey_Overview]
目标：把 survey_outline.md 转为 1–2 节“Related Work”草稿，要求证据绑定。

输出到 Paper.md 的“Related Work”节；并生成：
- tables/related_landscape.md（方法×数据×指标矩阵，交由 tabler 渲染）
- missing_refs.md（必须补引的关键条目列表）

约束：
- 每段 ≤ 6 句；每组观点后附 `\cite{}`；不作无法被引用支撑的判断。
```

---

# C) Scientific Discovery / Engineering（发现与工程）

## C1 创意采掘（Idea Miner）

```text
[AGENT=C1_Idea_Miner]
目标：从 gaps.md + claims.jsonl 挖掘可检验假设（Hypothesis），给出预期影响与可证伪方案。

产出：
- ideas.md（每条含：假设、动机、可测指标、潜在风险、最小验证实验）
- ranking.yaml（按 新颖性/可行性/影响力 评分）

动作：
- 结合代表性失配/边界条件，提出 ≥5 条假设。
- 推荐 1–2 条进入 C3/C4 流程。
```

## C2 新颖性与重要性评估

```text
[AGENT=C2_Novelty_Significance]
目标：将候选假设与当前 SOTA 对比，输出 Nature 级“创新性”量表评分。

输出：
- novelty_review.md（分项评分 + 证据引用）
- 必要实验或理论补强建议（P0/P1）
```

## C3 理论/数学分析

```text
[AGENT=C3_Theory]
目标：形式化问题与核心命题；给出关键推导或复杂度边界；若无法完整证明，给出充分可检验的近似命题。

产出：
- method_theory.md（定义、命题、证明草图）
- equation 清单（交给 equation agent 统一编号与符号表）
```

## C4 实验设计与执行

```text
[AGENT=C4_Experiment_DesignRun]
目标：制定并执行最小可行的验证实验；确保可复现。

产出：
- exps/plan.yaml（数据、划分、指标、超参、种子、统计检验）
- exps/logs/* 与 results/*.csv
- main 表格/图（交给 tabler/plotor 渲染）
- reproducibility.md（环境、命令、配置）

约束：
- 至少 n=3 次重复；报告 mean±std 或 CI；选择恰当的显著性检验。
```

---

# D) Academic Writing（学术写作）

## D0 结构与大纲

```text
[AGENT=D0_Writing_Outline]
目标：为 Paper.md 生成“标题→摘要→引言→方法→实验→结论”的骨架，并标注每节待填证据位点。

产出：
- outline.md（每小节目标 & 所需图表/表格/公式占位）
- checklist.md（提交前核对项）
```

## D1 引言写作

```text
/agent professor1: draft intro using templates/section-intro.md; bind claims from data/evidence/claims.jsonl; cite recent works; end with contributions bullets and result snapshot
```

## D2 公式与符号

```text
/agent equation: unify symbols; build "Notation Table" at start of Method; assign labels eq:<slug>; run /xref afterwards
```

## D3 图与表

```text
/agent plotor: create Figure 1 (learning curve) from data/demo.csv using scripts/plot.py::demo; export plots/fig-curve.pdf; insert into Paper.md with caption and units
/agent tabler: build Table 1 (main results) from results/main.csv with mean±std and significance notes; link data source; insert into Paper.md
```

## D4 合规与交叉引用

```text
/agent reviewer-xref: run scripts/xref_check.py; fix dangling refs; ensure Figure/Table/Equation numbering strictly increasing
```

---

# E) Academic Peer Reviewing（学术评审）

## E0 评审编排

```text
[AGENT=E0_Review_Orchestrator]
目标：组织专项评审（>6 名）并出 Meta-Review。任何 P0 未清零不得合并。

维度：
- 创新性、清晰度、数学严谨性、图表合规、交叉引用、统计方法、可复现性、数据可获得性、伦理/影响

输出：
- review/individual/*.md（各专项报告）
- review/meta.md（整合评分 + P0/P1 + 1天/1周可达改进）
```

## 专项评审一次性触发（示例）

```text
/agent reviewer-innovation: score & P0 actions with section-level evidence
/agent reviewer-clarity: run scripts/readability.py Paper.md and propose edits to hit target metrics
/agent reviewer-mathrigor: check assumptions/derivations/labels; list missing proofs
/agent reviewer-figures: audit sizes/fonts/units/CI/panels; per-figure checklist
/agent reviewer-xref: run scripts/xref_check.py; fix broken/missing refs
/agent reviewer-statsmethods: verify splits/repeats/tests; require CI/p-values if needed
/agent reviewer-reproducibility: produce repro log (env/commands/configs); gaps list
/agent reviewer-dataavailability: draft availability statements; add links/licenses
/agent nature-reviewer: integrate all individual reports; output meta review and P0 closure plan
```

---

# 引文检索与真实性（Paper Search & Reference Guardian）

## 搜索

```text
/agent paper-search: query "<主题关键词>" top-30 (2024–2025); use MCP brave-search + Crossref/OpenAlex validation; stage to data/papers.csv; append 15 to references.bib (dedupe=true)
```

## 真实性/去重/补全

```text
/agent reference-guardian: run make refs; summarize data/bib_report.csv; replace invalid DOIs; ensure every \cite{} has a valid entry; enforce recency coverage (≥40% in last 24 months)
```

---

# 一键「执行脚本式」提示词（把项目跑起来）

## 1. 启动与规划

```text
/plan create a 1-week roadmap to pass all reviewer-* gates before meta-review; list files to change and rollback strategy
```

## 2. 综述与引言

```text
/agent paper-search: query "<你的主题>" top-50 (last 24 months emphasized); stage→data/papers.csv & append 20 bibs
/agent B0_Survey_Orchestrator: dedupe+rank+outline; produce survey_outline.md & gaps.md
/agent professor1: draft intro from templates/section-intro.md + gaps.md; bind citations
```

## 3. 实验与图表

```text
/agent C4_Experiment_DesignRun: write exps/plan.yaml and execute minimal viable experiment; export results/main.csv
/agent plotor: make Figure 1 from results/main.csv; /agent tabler: make Table 1 with stats
```

## 4. 统一与校验

```text
/agent equation: unify symbols & labels; then /agent reviewer-xref: run scripts/xref_check.py to fix refs
/agent reference-guardian: run make refs; report invalid/missing DOIs
```

## 5. 终审

```text
/agent reviewer-innovation ...（全套专项评审见上）
/agent nature-reviewer: integrate; output P0 actions; wait for /apply to merge
```

---

# 小贴士（让 Claude Code 更稳）

* 若已配置 MCP：在检索/核验类任务中明确写出“**use MCP <server>**；fallback to scripts/xxx.py”。
* 每段产物**必须落盘**（给出路径）。
* 用“*不可妥协检查项*”表达硬门槛，例如“所有 `\cite{}` 必须有有效 DOI/arXiv”。
* 让每个 Agent 输出**验收清单**（checklist）与**失败返回码**（哪一步卡住、需要何输入）。

---



 -  **让科研工作者专注于研究本身，而不是写作技巧** 🎯
       145 -  ├── domain/                # 领域专业化层
       146 -  ├── ethics/                # 伦理监管层
       147 -  ├── writing/               # 🌟 超级写作分队
       148 -  │   ├── intro/            # D1引言集群 (5个子代理)
       149 -  │   ├── method/           # D2方法集群 (5个子代理)
       150 -  │   ├── results/          # D3结果集群 (5个子代理)
       151 -  │   ├── discussion/       # D4讨论集群 (5个子代理)
       152 -  │   └── format/           # D5格式集群 (5个子代理)
       153 -  ├── interfaces/           # 标准化协作接口
       154 -  ├── quality/              # Nature级质量控制
       155 -  └── styles/               # 输出样式配置
       156 -  ```
       157 -  
       158 -  ## 🎯 关键创新
       159 -  
       160 -  ### 1. 高度解耦的架构设计
       161 -  - **单一职责原则**: 每个代理只负责特定的写作任务
       162 -  - **标准化接口**: 统一的消息格式和协作协议
       163 -  - **松耦合协作**: 代理间通过事件总线通信
       164 -  - **独立优化**: 每个代理可独立改进和扩展
       165 -  
       166 -  ### 2. Nature级质量标准
       167 -  - **多层质量门控**: 内容、技术、呈现、影响四重检查
       168 -  - **自动化验证**: 实时质量监控和自动检查
       169 -  - **专家评审**: 人工专家评审和同行评议
       170 -  - **持续改进**: 基于反馈的持续优化
       171 -  
       172 -  ### 3. 智能输出样式系统
       173 -  - **期刊适配**: 自动适配Nature、Science等顶级期刊
       174 -  - **受众定制**: 针对不同受众优化表达方式
       175 -  - **多语言支持**: 英文、中文等多语言学术写作
       176 -  - **格式转换**: 论文、报告、演示等多格式输出
       177 -  
       178 -  ### 4. 全流程协作机制
       179 -  - **串行协作**: D1→D2→D3→D4→D5 顺序写作流程
       180 -  - **并行协作**: 同集群内代理并行工作
       181 -  - **反馈协作**: 跨集群的反馈和迭代优化
       182 -  - **质量协作**: 实时质量检查和改进建议
       183 -  
       184 -  ## 📊 质量保证
       185 -  
       186 -  ### 四重质量门控
       187 -  1. **内容验证**: 科学严谨性、创新性、证据强度
       188 -  2. **技术卓越**: 数学严谨、实验有效、计算正确
       189 -  3. **呈现优秀**: 叙事质量、视觉传达、语言标准
       190 -  4. **影响评估**: 科学意义、实践价值、引用潜力
       191 -  
       192 -  ### 自动化质量检查
       193 -  - ✅ 抄袭检测和引用验证
       194 -  - ✅ 统计分析验证
       195 -  - ✅ 格式合规性检查
       196 -  - ✅ 实时质量评分
       197 -  
       198 -  ## 🌍 使用场景
       199 -  
       200 -  ### 学术研究
       201 -  - **论文写作**: Nature/Science级别论文
       202 -  - **研究报告**: 项目报告和技术文档
       203 -  - **基金申请**: 研究计划和可行性分析
       204 -  - **学位论文**: 博士/硕士学位论文
       205 -  
       206 -  ### 产业应用
       207 -  - **技术白皮书**: 产业技术报告
       208 -  - **专利申请**: 技术专利文档
       209 -  - **产品文档**: 技术产品说明
       210 -  - **合规报告**: 监管合规文档
       211 -  
       212 -  ## 🤝 贡献指南
       213 -  
       214 -  ### 代理开发
       215 -  1. 遵循单一职责原则
       216 -  2. 实现标准化接口
       217 -  3. 提供完整测试
       218 -  4. 编写详细文档
       219 -  
       220 -  ### 质量标准
       221 -  - 代码覆盖率 >= 90%
       222 -  - 文档完整性 >= 95%
       223 -  - 性能基准达标
       224 -  - 用户满意度 >= 8.5/10
       225 -  
       226 -  ## 📜 开源协议
       227 -  
       228 -  MIT License - 详见 [LICENSE](LICENSE) 文件
       229 -  
       230 -  ## 🙏 致谢
       231 -  
       232 -  - 基于 GPT-5 推荐的研究AI架构设计
       233 -  - 参考 Claude Code 的代理协作模式
       234 -  - 融合 Nature 级期刊的质量标准
       235 -  - 借鉴 AI4Research 的前沿理念
       236 -  
       237 -  ---
       238 -  
       239 -  **让每一篇论文都达到Nature级别的卓越标准** 🎯
       240 -  
       241 -  ● 🎯 Researcher AI System - 已初始化完成
       242 -  
       243 -    系统状态: ✅ 25个专业化写作代理全部部署完成，Nature级质量控制系统激活
       244 -  
       245 -    📋 快速启动指令
       246 -  
       247 -    基本使用模式
       248 -  
       249 -    # 启动完整论文写作流程
       250 -    /agent writing/intro/background-narrator: "构建[你的研究主题]的重要性背景"
       251 -    /agent writing/method/algorithm-detailer: "详述核心算法"
       252 -    /agent writing/results/data-presenter: "呈现实验数据"
       253 -  
       254 -    # 应用Nature期刊样式
       255 -    /style nature
       256 -  
       257 -    # 执行四重质量门控
       258 -    /quality check all-gates
       259 -  
       260 -    高级工作流
       261 -  
       262 -    # 1. 项目初始化
       263 -    /project "你的Nature级研究主题"
       264 -  
       265 -    # 2. 顺序执行D1→D2→D3→D4→D5
       266 -    /execute-pipeline intro→method→results→discussion→format
       267 -  
       268 -    # 3. 质量验证与输出
       269 -    /validate nature-standards
       270 -    /generate publication-ready
       271 -  
       272 -    🏗️ 系统架构概览
       273 -  
       274 -    25个专业化代理 已部署完成:
       275 -    - D1 引言集群 (5个): 背景叙事→文献综述→问题定义→贡献总结→结果预告
       276 -    - D2 方法集群 (5个): 方法概述→算法详述→数学建模→实现描述→复杂度分析
       277 -    - D3 结果集群 (5个): 实验设计→数据呈现→图表解读→对比分析→显著性验证
       278 -    - D4 讨论集群 (5个): 发现总结→理论解释→局限分析→影响评估→未来展望
       279 -    - D5 格式集群 (5个): 摘要精炼→标题优化→段落结构→语言润色→声明制作
       280 -  
       281 -    🎯 立即可用功能
       282 -  
       283 -    ✅ 标准化协作接口 - 代理间无缝通信✅ 四重质量门控 - 内容→技术→呈现→影响全面验证✅ 智能输出样式 -
       284 -    Nature/Science/领域期刊自动适配✅ 端到端工作流 - 从想法到发表完整支持
       285 -  
       286 -    您的Researcher AI系统已准备就绪，可以开始Nature级别的学术论文写作！🚀
       144   \ No newline at end of file
       145 +  **让科研工作者专注于研究本身，而不是写作技巧** 🎯
       146   \ No newline at end of file