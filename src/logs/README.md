# 📝 Claude Code Execution Logging System

## Overview

This directory contains the comprehensive logging system that automatically captures every Claude Code execution with intelligent keyword-based naming and powerful analytics capabilities.

## 🚀 Key Features

- **🏷️ Smart Naming**: Logs automatically named with timestamps and extracted keywords
- **🔍 Full-Text Search**: Search across all execution history
- **📊 Analytics Dashboard**: Performance insights and usage patterns
- **⚡ Real-Time Logging**: Streaming capture of execution details
- **🗜️ Automatic Compression**: Space-efficient storage with retention policies
- **🔗 Session Management**: Track and recover from interrupted sessions

## 📁 Directory Structure

```
logs/
├── executions/              # Daily execution logs
│   ├── 2025-01-23/         # Daily directories
│   │   ├── 10-30-45_literature_review_transformers.log
│   │   ├── 11-15-22_debug_pytorch_model.log
│   │   ├── 14-22-33_write_introduction_quantum.log
│   │   └── index.json      # Searchable daily index
│   └── 2025-01-24/
├── analytics/              # Generated analytics reports
│   ├── analytics_report_20250123_143022.md
│   ├── usage_patterns_weekly.json
│   └── claude_logger.log   # System logging
├── sessions/               # Extended session transcripts (future)
├── agents/                 # Agent-specific logs (future)
└── README.md              # This file
```

## 🎯 Quick Start

### **View Recent Executions**
```bash
# Interactive browser (recommended)
python scripts/logging/log_viewer.py

# Command line quick view
python scripts/logging/log_viewer.py --recent 10
```

### **Search Your History**
```bash
# Search by keywords
python scripts/logging/log_analyzer.py search "pytorch optimization" --days 30

# Interactive search with filters
python scripts/logging/log_viewer.py
# Choose option 2: Search Logs
```

### **Generate Analytics**
```bash
# Weekly performance report
python scripts/logging/log_analyzer.py analytics --days 7

# Export detailed analytics
python scripts/logging/log_analyzer.py analytics --export report.md --format markdown
```

### **Session Management**
```bash
# Check session status
python .claude/hooks/session-manager.py status

# Clean up stale sessions
python .claude/hooks/session-manager.py cleanup
```

## 📊 Log File Format

### **Individual Log Files**
Each execution creates a detailed log file with the format:

```
=== Claude Code Execution Log ===
Session ID: 550e8400-e29b-41d4-a716-446655440000
Start Time: 2025-01-23T10:30:45Z
User Query: Search for papers on transformer architectures
Keywords: search, papers, transformer, architectures
==================================================

[2025-01-23T10:30:46Z] TOOL_USAGE:
{
  "tool": "WebSearch",
  "timestamp": "2025-01-23T10:30:46Z",
  "parameters": {"query": "transformer architecture papers"},
  "duration": 5.2
}
------------------------------

[2025-01-23T10:30:52Z] FILE_ACCESS:
{
  "path": "/tmp/papers.md",
  "operation": "write",
  "timestamp": "2025-01-23T10:30:52Z"
}
------------------------------

[2025-01-23T10:31:15Z] RESPONSE:
{
  "response": "I found 15 relevant papers on transformer architectures...",
  "timestamp": "2025-01-23T10:31:15Z",
  "tokens_used": 245,
  "length": 1024
}
------------------------------

==================================================
=== EXECUTION SUMMARY ===
==================================================
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-23T10:30:45Z",
  "user_query": "Search for papers on transformer architectures",
  "keywords": ["search", "papers", "transformer", "architectures"],
  "log_filename": "10-30-45_search_papers_transformer.log",
  "execution": {
    "tools_used": [{"tool": "WebSearch", "duration": 5.2}],
    "files_accessed": [{"path": "/tmp/papers.md", "operation": "write"}],
    "duration_seconds": 45.3
  },
  "response": "I found 15 relevant papers...",
  "metrics": {
    "tools_count": 1,
    "files_accessed_count": 1,
    "execution_steps": 3,
    "duration_seconds": 45.3,
    "success_rate": 1.0
  }
}
==================================================
```

### **Daily Index Files**
Each day's directory contains an `index.json` file for fast searching:

```json
[
  {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-01-23T10:30:45Z",
    "user_query": "Search for papers on transformer architectures",
    "keywords": ["search", "papers", "transformer", "architectures"],
    "log_filename": "10-30-45_search_papers_transformer.log",
    "metrics": {
      "duration_seconds": 45.3,
      "success_rate": 1.0,
      "tools_count": 1,
      "files_accessed_count": 1
    }
  }
]
```

## 🔍 Search Capabilities

### **Search Modes**
1. **Keyword Search**: Match against extracted keywords
2. **Full-Text Search**: Search within complete log content  
3. **Metadata Search**: Filter by duration, success rate, dates
4. **Similarity Search**: Find sessions similar to a reference

### **Search Examples**
```bash
# Basic keyword search
python scripts/logging/log_analyzer.py search "pytorch"

# Advanced search with filters
python scripts/logging/log_analyzer.py search "machine learning" --days 60 --limit 20

# Search with content analysis
python scripts/logging/log_analyzer.py search "error" --content

# Find similar sessions
python scripts/logging/log_analyzer.py similar SESSION_ID --limit 10
```

### **Search Results Format**
```
Found 3 results for 'pytorch optimization':

1. [2025-01-23 10:30] Score: 0.95
   Query: Optimize PyTorch model training for better performance
   Keywords: optimize, pytorch, model, training, performance
   Matched: pytorch, optimization, performance
   Log: 10-30-45_optimize_pytorch_training.log

2. [2025-01-22 14:15] Score: 0.82
   Query: Debug PyTorch CUDA memory issues in training loop
   Keywords: debug, pytorch, cuda, memory, training
   Matched: pytorch, training
   Log: 14-15-22_debug_pytorch_memory.log
```

## 📈 Analytics & Insights

### **Available Analytics**
- **Usage Patterns**: Most active times, popular keywords
- **Performance Metrics**: Average duration, success rates
- **Tool Usage**: Most used tools and agents
- **Trend Analysis**: Usage trends over time
- **Bottleneck Identification**: Performance issues and solutions

### **Analytics Report Example**
```markdown
# Claude Code Analytics Report

**Time Period:** 2025-01-16 to 2025-01-23  
**Generated:** 2025-01-23 15:30:22

## 📊 Executive Summary
- **Total Executions:** 47
- **Success Rate:** 91.5%
- **Average Duration:** 32.4 seconds

## 📈 Activity Patterns
### Most Active Days
- **2025-01-23:** 12 executions
- **2025-01-22:** 8 executions
- **2025-01-21:** 7 executions

## 🔍 Popular Keywords
- **pytorch:** 15 occurrences
- **research:** 12 occurrences
- **paper:** 9 occurrences
- **debug:** 7 occurrences

## 💡 Recommendations
1. Success rate is 91.5%. Review failed executions for common issues.
2. You frequently work with 'pytorch'. Consider creating specialized workflows.
3. Try using Claude Code more regularly to build better analytics insights.
```

## ⚙️ Configuration

### **Main Configuration** (`.claude/config.yaml`)
```yaml
logging:
  enabled: true              # Enable/disable logging
  auto_capture: true         # Automatic capture mode
  retention_days: 90         # Log retention period  
  compression: true          # Compress old logs
  keyword_extraction: true   # Smart keyword naming
  max_keywords: 5           # Keywords per filename
  real_time: true           # Real-time log updates
  
  # File naming
  filename_format: "{timestamp}_{keywords}.log"
  timestamp_format: "%Y-%m-%d_%H-%M-%S"
  max_filename_length: 100
```

### **Advanced Settings**
```yaml
analytics:
  enabled: true
  auto_generate: true
  generation_interval: "daily"
  
search:
  index_content: true
  max_search_results: 100
  
monitoring:
  enabled: true
  check_interval: 300       # 5 minutes
  max_session_age_hours: 24
```

## 🛠️ Maintenance

### **Automatic Maintenance**
- **Daily**: Index generation, analytics updates
- **Weekly**: Performance report generation
- **Monthly**: Archive old logs, cleanup stale data

### **Manual Maintenance**
```bash
# Clean up old sessions
python .claude/hooks/session-manager.py cleanup --max-age-hours 24

# Force compress old logs
python -c "
from scripts.logging.claude_logger import get_claude_logger
logger = get_claude_logger()
# Compression happens automatically for files older than 1 day
"

# Export data before major cleanup
python scripts/logging/log_analyzer.py analytics --export backup_$(date +%Y%m%d).json
```

## 🔒 Privacy & Security

### **Privacy Features**
- **Path Anonymization**: Option to anonymize file paths
- **Sensitive Data Filtering**: Automatic removal of passwords, tokens, keys
- **Environment Variable Exclusion**: Skip sensitive environment data

### **Data Security**
- **Local Storage**: All data stored locally, never sent externally
- **Compression**: Old logs compressed to save space
- **Retention Policies**: Automatic cleanup after specified periods

## 🐛 Troubleshooting

### **Common Issues**

**Issue**: "No recent executions found"
```bash
# Solution: Check if logging is enabled
python .claude/hooks/session-manager.py status
# Enable in .claude/config.yaml if disabled
```

**Issue**: "Session not found"  
```bash
# Solution: Clean up stale sessions
python .claude/hooks/session-manager.py cleanup
```

**Issue**: "Disk space warnings"
```bash
# Solution: Compress old logs or increase retention
python scripts/logging/log_analyzer.py analytics --days 30  # Check usage
# Adjust retention_days in config.yaml
```

**Issue**: "Search returns no results"
```bash
# Solution: Check search terms and date range
python scripts/logging/log_analyzer.py search "term" --days 90 --limit 50
# Try broader terms or longer time range
```

### **Debug Mode**
Enable debug logging in `.claude/config.yaml`:
```yaml
debugging:
  verbose_logging: true
  debug_hooks: true
  trace_execution: true
```

## 📞 Support

### **Getting Help**
1. **Interactive Help**: Run `python scripts/logging/log_viewer.py` and choose option 8 (Help)
2. **Command Line Help**: Add `--help` to any analyzer command
3. **Configuration Help**: Check `.claude/config.yaml` comments
4. **System Status**: Run `python .claude/hooks/session-manager.py status`

### **Reporting Issues**
1. Check system status and recent logs
2. Try cleanup procedures first
3. Export relevant analytics data
4. Include configuration and error messages

---

**📝 Happy Logging!** Your Claude Code executions are now automatically tracked and searchable. Use the analytics insights to optimize your research workflow and never lose track of your progress again!