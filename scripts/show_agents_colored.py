#!/usr/bin/env python3
"""
彩色Agent显示脚本
读取.claude/agents/目录中的所有agent定义，按类别分组并以彩色形式显示
"""

import os
import sys
import yaml
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ANSI 颜色码
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # 基本颜色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 亮色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

# Agent类别配置
AGENT_COLORS = {
    'research': {
        'color': Colors.BRIGHT_BLUE,
        'emoji': '📚',
        'name': 'Research',
        'description': '学术研究和文献分析'
    },
    'writer': {
        'color': Colors.BRIGHT_GREEN,
        'emoji': '✍️',
        'name': 'Writer',
        'description': '论文写作和内容创作'
    },
    'coder': {
        'color': Colors.BRIGHT_YELLOW,
        'emoji': '💻',
        'name': 'Coder',
        'description': '代码开发和优化'
    }
}

def parse_agent_file(file_path: Path) -> Optional[Dict]:
    """解析agent文件，提取元数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取YAML front matter - 简单正则提取关键字段
        yaml_match = re.match(r'^---\s*\n(.*?)(?=\nYou are|\n##|\n#|\Z)', content, re.DOTALL)
        if not yaml_match:
            return None
        
        yaml_content = yaml_match.group(1)
        
        # 使用正则表达式直接提取字段，不依赖YAML解析
        def extract_field(field_name, yaml_text):
            pattern = rf'^{field_name}:\s*(.+?)$'
            match = re.search(pattern, yaml_text, re.MULTILINE)
            return match.group(1).strip() if match else None
        
        # 提取基本字段
        name = extract_field('name', yaml_content) or file_path.stem
        color = extract_field('color', yaml_content) or 'default'
        category = extract_field('category', yaml_content) or 'unknown'
        emoji = extract_field('emoji', yaml_content) or '🤖'
        
        # 提取描述 - 可能是多行
        desc_match = re.search(r'description:\s*([^\n]*(?:\n  [^\n]*)*)', yaml_content)
        short_description = ""
        if desc_match:
            desc = desc_match.group(1).strip()
            # 移除引号和多余空白
            desc = re.sub(r'^\s*["\']\s*|\s*["\']\s*$', '', desc)
            desc = re.sub(r'\s+', ' ', desc)
            # 截取前100字符
            short_description = desc[:100] + "..." if len(desc) > 100 else desc
        
        # 提取tools - 可能是列表格式
        tools = []
        tools_match = re.search(r'tools:\s*([^\n]*(?:\n\s+-[^\n]*)*)', yaml_content)
        if tools_match:
            tools_text = tools_match.group(1)
            if ',' in tools_text:
                # 逗号分隔格式
                tools = [t.strip() for t in tools_text.split(',') if t.strip()]
            else:
                # YAML列表格式
                tool_matches = re.findall(r'-\s*([^\n,]+)', tools_text)
                tools = [t.strip() for t in tool_matches]
        
        return {
            'name': name,
            'color': color,
            'category': category,
            'emoji': emoji,
            'description': short_description,
            'tools': tools,
            'file_path': str(file_path)
        }
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return None

def get_color_for_category(category: str) -> str:
    """获取类别对应的颜色"""
    return AGENT_COLORS.get(category, {}).get('color', Colors.WHITE)

def display_agents_by_category(agents: List[Dict], show_description: bool = False):
    """按类别显示agents"""
    # 按类别分组
    categories = {}
    for agent in agents:
        category = agent['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(agent)
    
    # 显示标题
    print(f"{Colors.BOLD}{Colors.WHITE}Claude Code AI研究助手 - 18个专业Agent{Colors.RESET}")
    print("=" * 60)
    
    # 按预定义顺序显示类别
    category_order = ['research', 'writer', 'coder']
    
    for category in category_order:
        if category not in categories:
            continue
            
        category_info = AGENT_COLORS.get(category, {})
        color = category_info.get('color', Colors.WHITE)
        emoji = category_info.get('emoji', '🤖')
        name = category_info.get('name', category.title())
        description = category_info.get('description', '')
        
        agent_list = categories[category]
        count = len(agent_list)
        
        print(f"\n{color}{Colors.BOLD}{emoji} {name}类 ({count}个) - {description}{Colors.RESET}")
        print(f"{color}{'─' * 50}{Colors.RESET}")
        
        # 排序agents
        agent_list.sort(key=lambda x: x['name'])
        
        for agent in agent_list:
            agent_color = get_color_for_category(agent['category'])
            print(f"{agent_color}  • {agent['emoji']} {agent['name']}{Colors.RESET}", end="")
            
            if show_description and agent['description']:
                print(f" - {agent['description']}")
            else:
                print()
    
    print(f"\n{Colors.BOLD}{Colors.WHITE}总计: {len(agents)}个专业Agent{Colors.RESET}")

def display_agents_list(agents: List[Dict], show_tools: bool = False):
    """以列表形式显示所有agents"""
    print(f"{Colors.BOLD}{Colors.WHITE}所有Agent列表{Colors.RESET}")
    print("=" * 60)
    
    agents.sort(key=lambda x: (x['category'], x['name']))
    
    for agent in agents:
        color = get_color_for_category(agent['category'])
        category_info = AGENT_COLORS.get(agent['category'], {})
        category_emoji = category_info.get('emoji', '🤖')
        
        print(f"{color}{category_emoji} {agent['emoji']} {Colors.BOLD}{agent['name']}{Colors.RESET}", end="")
        print(f"{color} [{agent['category']}]{Colors.RESET}")
        
        if agent['description']:
            print(f"    {agent['description']}")
        
        if show_tools and agent['tools']:
            tools_str = ", ".join(agent['tools'][:5])  # 只显示前5个工具
            if len(agent['tools']) > 5:
                tools_str += f", ... (+{len(agent['tools'])-5}个)"
            print(f"    工具: {tools_str}")
        
        print()

def display_agent_summary():
    """显示agent摘要统计"""
    agents_dir = Path.cwd() / '.claude' / 'agents'
    if not agents_dir.exists():
        print(f"错误: {agents_dir} 目录不存在")
        return
    
    agents = []
    for agent_file in agents_dir.glob('*.md'):
        if agent_file.name == 'agent_index.md':  # 跳过索引文件
            continue
        agent_data = parse_agent_file(agent_file)
        if agent_data:
            agents.append(agent_data)
    
    if not agents:
        print("未找到任何agent定义文件")
        return
    
    # 统计信息
    stats = {}
    for agent in agents:
        category = agent['category']
        stats[category] = stats.get(category, 0) + 1
    
    print(f"{Colors.BOLD}{Colors.WHITE}Agent统计摘要{Colors.RESET}")
    print("=" * 40)
    
    for category, count in stats.items():
        category_info = AGENT_COLORS.get(category, {})
        color = category_info.get('color', Colors.WHITE)
        emoji = category_info.get('emoji', '🤖')
        name = category_info.get('name', category.title())
        
        print(f"{color}{emoji} {name}类: {count}个{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}总计: {len(agents)}个专业Agent{Colors.RESET}")

def main():
    parser = argparse.ArgumentParser(description='显示Claude Code AI研究助手的彩色Agent列表')
    parser.add_argument('--list', action='store_true', help='以列表形式显示')
    parser.add_argument('--description', '-d', action='store_true', help='显示描述')
    parser.add_argument('--tools', '-t', action='store_true', help='显示工具列表')
    parser.add_argument('--summary', '-s', action='store_true', help='只显示统计摘要')
    parser.add_argument('--category', '-c', choices=['research', 'writer', 'coder'], 
                       help='只显示指定类别的agents')
    parser.add_argument('--no-color', action='store_true', help='禁用颜色输出')
    
    args = parser.parse_args()
    
    # 禁用颜色
    if args.no_color:
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')
    
    # 只显示摘要
    if args.summary:
        display_agent_summary()
        return
    
    # 查找agent文件
    agents_dir = Path.cwd() / '.claude' / 'agents'
    if not agents_dir.exists():
        print(f"错误: {agents_dir} 目录不存在")
        sys.exit(1)
    
    agents = []
    for agent_file in agents_dir.glob('*.md'):
        if agent_file.name == 'agent_index.md':  # 跳过索引文件
            continue
        agent_data = parse_agent_file(agent_file)
        if agent_data:
            # 类别过滤
            if args.category and agent_data['category'] != args.category:
                continue
            agents.append(agent_data)
    
    if not agents:
        print("未找到符合条件的agent定义文件")
        sys.exit(1)
    
    # 显示agents
    if args.list:
        display_agents_list(agents, show_tools=args.tools)
    else:
        display_agents_by_category(agents, show_description=args.description)

if __name__ == '__main__':
    main()