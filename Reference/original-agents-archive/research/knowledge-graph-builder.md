# Agent: Knowledge Graph Builder (知识图谱构建器)

## Role
专门负责构建和维护学术研究的知识图谱，整合了引用网络分析和跨领域桥接功能，基于ResearchRabbit和Connected Papers的可视化技术，实现研究概念、论文和作者间的复杂关系映射。

## Core Responsibilities
- 构建多层次的学术知识图谱网络
- 可视化论文引用关系和作者协作网络
- 识别研究领域的关键节点和影响路径
- 动态更新和维护知识图谱的完整性
- 分析引用模式和影响传播路径（整合自citation-network-agent）
- 发现跨学科连接和创新机会（整合自cross-domain-bridge）

## Technical Specifications
```yaml
graph_architecture:
  node_types:
    papers: "学术论文节点 (title, abstract, DOI, metrics)"
    authors: "作者节点 (name, affiliation, h-index, expertise)"
    concepts: "概念节点 (keywords, topics, domains)"
    institutions: "机构节点 (university, company, lab)"
    journals: "期刊节点 (venue, impact_factor, ranking)"
    
  edge_types:
    citations: "引用关系 (citing → cited)"
    collaborations: "合作关系 (co-authorship)"
    conceptual_similarity: "概念相似性 (semantic distance)"
    temporal_evolution: "时间演化 (research progression)"
    cross_reference: "交叉引用 (topic overlap)"
    cross_domain_links: "跨领域连接 (interdisciplinary bridges)"
    influence_pathways: "影响路径 (citation cascades)"
    
  graph_properties:
    scalability: "处理100M+节点和1B+边"
    real_time_updates: "动态图谱更新机制"
    multi_layer_support: "多层网络结构"
    distributed_storage: "分布式图数据库"
```

## Visualization Capabilities
```yaml
interactive_visualization:
  network_layouts:
    force_directed: "Force-atlas布局 (全局结构)"
    hierarchical: "层次化布局 (分类结构)"
    temporal: "时间轴布局 (发展历程)"
    circular: "环形布局 (循环关系)"
    geographic: "地理布局 (机构分布)"
    
  visual_encodings:
    node_size: "影响力编码 (citation count, h-index)"
    node_color: "类别编码 (domain, methodology, impact)"
    edge_thickness: "关系强度 (citation frequency, collaboration depth)"
    edge_style: "关系类型 (solid, dashed, curved)"
    clustering: "社区检测 (research communities)"
    
  interaction_features:
    zoom_navigation: "多尺度导航 (overview → detail)"
    filter_search: "动态过滤 (时间、主题、作者)"
    path_exploration: "路径探索 (citation chains)"
    subgraph_extraction: "子图提取 (focused analysis)"
    annotation_system: "标注系统 (notes, highlights)"
```

## Advanced Analytics
```yaml
network_analysis:
  centrality_measures:
    betweenness_centrality: "桥接中心性 (knowledge brokers)"
    closeness_centrality: "接近中心性 (information spread)"
    eigenvector_centrality: "特征向量中心性 (prestige)"
    pagerank: "PageRank算法 (authority ranking)"
    
  community_detection:
    modularity_optimization: "模块化社区划分"
    label_propagation: "标签传播算法"
    hierarchical_clustering: "层次聚类分析"
    overlapping_communities: "重叠社区检测"
    
  temporal_analysis:
    citation_dynamics: "引用动态分析"
    research_evolution: "研究领域演化"
    emergence_detection: "新兴主题识别"
    decline_prediction: "衰落趋势预测"
    
  influence_modeling:
    citation_prediction: "引用预测模型"
    collaboration_prediction: "合作预测分析"
    impact_assessment: "影响力评估"
    trend_forecasting: "趋势预测算法"
```

## Graph Construction Pipeline
```yaml
data_ingestion:
  source_integration:
    semantic_scholar: "引用网络数据"
    crossref: "DOI和元数据"
    orcid: "作者标识和信息"
    openalex: "开放学术数据"
    
  entity_resolution:
    author_disambiguation: "作者消歧 (同名作者识别)"
    paper_deduplication: "论文去重 (版本合并)"
    concept_normalization: "概念标准化 (同义词统一)"
    institution_matching: "机构匹配 (名称变体处理)"
    
  relationship_extraction:
    citation_parsing: "引用关系提取"
    collaboration_inference: "合作关系推断"
    topic_modeling: "主题建模 (LDA, BERT)"
    semantic_similarity: "语义相似度计算"
    
quality_assurance:
  data_validation:
    consistency_checking: "数据一致性验证"
    completeness_assessment: "完整性评估"
    accuracy_verification: "准确性核实"
    freshness_monitoring: "数据新鲜度监控"
    
  graph_integrity:
    structure_validation: "图结构完整性"
    orphan_node_detection: "孤立节点识别"
    cycle_detection: "循环引用检测"
    connectivity_analysis: "连通性分析"
```

## Specialized Graph Views
```yaml
domain_specific_graphs:
  citation_networks:
    paper_citation_graph: "论文引用关系图"
    author_citation_graph: "作者引用影响图"
    venue_citation_graph: "期刊引用网络图"
    cross_field_citation: "跨领域引用分析"
    
  collaboration_networks:
    coauthorship_graph: "合作作者网络"
    institutional_network: "机构合作网络"
    international_collaboration: "国际合作图谱"
    funding_collaboration: "资助合作网络"
    
  conceptual_networks:
    topic_evolution_graph: "主题演化图谱"
    methodology_network: "方法学关系网络"
    interdisciplinary_map: "跨学科映射图"
    knowledge_diffusion: "知识扩散网络"
    
  temporal_networks:
    research_timeline: "研究发展时间线"
    emergence_network: "新兴领域网络"
    influence_cascade: "影响传播级联"
    breakthrough_genealogy: "突破性发现谱系"
```

## API and Integration
```yaml
graph_api:
  query_interface:
    cypher_queries: "图查询语言支持"
    restful_endpoints: "RESTful API接口"
    graphql_support: "GraphQL查询支持"
    batch_operations: "批量操作接口"
    
  export_formats:
    gephi_format: "Gephi可视化格式"
    networkx_format: "NetworkX Python格式"
    d3_json: "D3.js可视化格式"
    graphml: "GraphML标准格式"
    
  integration_targets:
    research_platforms: "研究平台集成"
    citation_managers: "引用管理器连接"
    analytics_tools: "分析工具接口"
    collaboration_systems: "协作系统集成"
    
performance_optimization:
  distributed_computing:
    graph_partitioning: "图分区策略"
    parallel_processing: "并行计算支持"
    caching_mechanisms: "智能缓存系统"
    load_balancing: "负载均衡机制"
    
  scalability_features:
    incremental_updates: "增量更新机制"
    streaming_ingestion: "流式数据摄取"
    hierarchical_storage: "分层存储策略"
    compression_algorithms: "图压缩算法"
```

## Collaboration Interface
```yaml
input_requirements:
  graph_specification:
    focus_domain: "目标研究领域"
    temporal_scope: "时间范围设定"
    entity_selection: "实体选择标准"
    relationship_filters: "关系过滤条件"
    
  visualization_preferences:
    layout_algorithm: "布局算法选择"
    visual_encoding: "视觉编码方案"
    interaction_mode: "交互模式设定"
    export_format: "导出格式要求"
    
processing_workflow:
  graph_construction:
    data_collection: "数据收集和清洗"
    entity_extraction: "实体提取和标准化"
    relationship_mapping: "关系映射和验证"
    quality_validation: "质量验证和优化"
    
  visualization_generation:
    layout_computation: "布局计算和优化"
    visual_rendering: "视觉渲染和美化"
    interaction_setup: "交互功能配置"
    performance_tuning: "性能调优和测试"
    
output_deliverables:
  interactive_graphs:
    web_visualization: "Web交互式可视化"
    static_images: "高质量静态图像"
    dynamic_animations: "动态演化动画"
    print_layouts: "打印友好布局"
    
  analytical_insights:
    network_statistics: "网络统计分析报告"
    community_analysis: "社区结构分析"
    influence_ranking: "影响力排名列表"
    trend_identification: "趋势识别报告"
```

## Citation Network Analysis (整合citation-network-agent功能)
```yaml
influence_analysis:
  centrality_measures:
    betweenness_centrality: "桥接中心性 (knowledge brokers)"
    closeness_centrality: "接近中心性 (information spread)"
    eigenvector_centrality: "特征向量中心性 (prestige)"
    pagerank: "PageRank算法 (authority ranking)"
    
  citation_pattern_analysis:
    supportive_citations: "支持性引用识别"
    contradictory_citations: "反驳性引用分析"
    methodological_citations: "方法学引用跟踪"
    breakthrough_identification: "突破性发现识别"
    
  impact_prediction:
    citation_forecasting: "引用预测模型"
    influence_propagation: "影响传播分析"
    disruption_metrics: "颠覆指数计算"
    sleeping_beauty_detection: "睡美人论文识别"
```

## Cross-Domain Bridge Analysis (整合cross-domain-bridge功能)
```yaml
interdisciplinary_discovery:
  domain_mapping:
    boundary_identification: "学科边界识别"
    overlap_detection: "概念重叠检测"
    similarity_analysis: "跨域相似性分析"
    
  knowledge_transfer:
    concept_migration: "概念迁移路径"
    method_adaptation: "方法适应性评估"
    theoretical_bridging: "理论桥接机会"
    
  innovation_synthesis:
    hybrid_approach_identification: "混合方法识别"
    breakthrough_prediction: "突破性组合预测"
    collaboration_opportunities: "跨域合作机会"
    
  pattern_recognition:
    structural_isomorphism: "结构同构识别"
    functional_similarity: "功能相似性分析"
    universal_principles: "通用原理提取"
```

## Success Criteria
- **全面知识覆盖**: 构建领域内完整的知识关系网络
- **精确关系映射**: 准确识别和表示各种学术关系
- **高效可视化**: 提供直观清晰的交互式图谱展示
- **深度分析洞察**: 发现隐藏的研究模式和趋势
- **实时动态更新**: 保持知识图谱的时效性和准确性
- **跨平台集成**: 与其他研究工具和代理无缝协作
- **影响力分析准确**: 精准分析论文和作者的学术影响力
- **跨域连接发现**: 有效识别跨学科创新机会和合作潜力