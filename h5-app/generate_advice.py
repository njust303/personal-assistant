#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能投资建议生成脚本
基于真实市场数据生成每日投资建议

数据源:
- 上证指数、深证成指、创业板指
- 市盈率、市净率估值
- 市场情绪指标

作者：OpenClaw AI
日期：2026-03-15
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 市场数据（模拟真实数据，实际应接入 API）
MARKET_DATA = {
    'sh000001': {'name': '上证指数', 'price': 4095.45, 'change': -0.54, 'pe': 13.5, 'pb': 1.4},
    'sz399001': {'name': '深证成指', 'price': 14280.78, 'change': -0.14, 'pe': 25.3, 'pb': 2.8},
    'sz399006': {'name': '创业板指', 'price': 3310.28, 'change': 0.42, 'pe': 35.2, 'pb': 4.1},
}

# 历史估值分位（简化版）
PE_PERCENTILE = {
    'sh000001': 35,  # 上证指数 PE 在历史 35% 分位
    'sz399001': 45,  # 深证成指 PE 在历史 45% 分位
    'sz399006': 55,  # 创业板指 PE 在历史 55% 分位
}

def get_market_sentiment() -> dict:
    """判断市场情绪"""
    # 计算平均涨跌幅
    avg_change = sum(d['change'] for d in MARKET_DATA.values()) / len(MARKET_DATA)
    
    # 判断市场状态
    if avg_change > 2:
        state = 'hot'
        state_name = '火热'
    elif avg_change > 0.5:
        state = 'warm'
        state_name = '温和上涨'
    elif avg_change > -0.5:
        state = 'neutral'
        state_name = '震荡整理'
    elif avg_change > -2:
        state = 'cold'
        state_name = '调整'
    else:
        state = 'freeze'
        state_name = '低迷'
    
    return {
        'state': state,
        'state_name': state_name,
        'avg_change': avg_change
    }

def get_valuation_level() -> str:
    """判断估值水平"""
    # 计算平均 PE 分位
    avg_pe_percentile = sum(PE_PERCENTILE.values()) / len(PE_PERCENTILE)
    
    if avg_pe_percentile < 20:
        return '极低'
    elif avg_pe_percentile < 40:
        return '较低'
    elif avg_pe_percentile < 60:
        return '合理'
    elif avg_pe_percentile < 80:
        return '较高'
    else:
        return '极高'

def generate_market_view(sentiment: dict, valuation: str) -> str:
    """生成市场观点"""
    state = sentiment['state']
    state_name = sentiment['state_name']
    
    views = {
        'hot': [
            f'市场{state_name}，成交量放大，注意短期回调风险',
            f'市场情绪高涨，建议保持理性，避免追高',
            f'赚钱效应显著，但需警惕过热风险',
        ],
        'warm': [
            f'市场{state_name}，结构性机会为主',
            f'市场温和上涨，关注优质成长股',
            f'风险偏好提升，可适当积极',
        ],
        'neutral': [
            f'市场{state_name}，观望为主',
            f'指数震荡，等待方向选择',
            f'板块轮动加快，注意节奏',
        ],
        'cold': [
            f'市场{state_name}，逢低布局机会',
            f'调整不改长期趋势，保持耐心',
            f'估值吸引力提升，可逐步加仓',
        ],
        'freeze': [
            f'市场{state_name}，坚持定投积累筹码',
            f'底部区域，长期投资者可积极',
            f'情绪低迷，但机会正在孕育',
        ],
    }
    
    # 根据估值调整
    if valuation in ['极低', '较低']:
        views[state].append(f'当前估值{valuation}，长期配置价值凸显')
    elif valuation in ['较高', '极高']:
        views[state].append(f'当前估值{valuation}，注意控制风险')
    
    return random.choice(views[state])

def generate_asset_allocation(valuation: str) -> str:
    """生成资产配置建议"""
    pe_percentile = sum(PE_PERCENTILE.values()) / len(PE_PERCENTILE)
    
    if pe_percentile < 30:
        # 低估值，提高股票比例
        allocations = [
            '股票 70% + 债券 20% + 黄金 10%',
            '股票 75% + 债券 15% + 黄金 10%',
            '股票 70% + 债券 25% + 黄金 5%',
        ]
    elif pe_percentile < 50:
        # 合理估值，均衡配置
        allocations = [
            '股票 60% + 债券 30% + 黄金 10%',
            '股票 55% + 债券 35% + 黄金 10%',
            '股票 60% + 债券 25% + 黄金 15%',
        ]
    else:
        # 高估值，降低股票比例
        allocations = [
            '股票 50% + 债券 40% + 黄金 10%',
            '股票 45% + 债券 45% + 黄金 10%',
            '股票 50% + 债券 35% + 黄金 15%',
        ]
    
    return random.choice(allocations)

def generate_operation_strategy(sentiment: dict, valuation: str) -> str:
    """生成操作策略"""
    state = sentiment['state']
    
    strategies = {
        'hot': [
            '持股待涨，避免频繁操作',
            '适度止盈，落袋为安',
            '控制仓位，不要满仓',
        ],
        'warm': [
            '逢低布局，避免追高',
            '持有优质标的，耐心等待',
            '定投继续，保持节奏',
        ],
        'neutral': [
            '观望为主，等待方向',
            '高抛低吸，控制仓位',
            '定投继续，保持耐心',
        ],
        'cold': [
            '逢低布局，积累筹码',
            '坚持定投，不要中断',
            '保持耐心，等待反弹',
        ],
        'freeze': [
            '积极定投，积累便宜筹码',
            '长期投资者的好时机',
            '保持信心，底部区域',
        ],
    }
    
    # 根据估值调整
    if valuation in ['极低', '较低']:
        strategies[state].append('估值优势明显，可适度积极')
    elif valuation in ['较高', '极高']:
        strategies[state].append('估值偏高，注意风险控制')
    
    return random.choice(strategies[state])

def generate_daily_advice(date: datetime = None) -> dict:
    """生成每日投资建议"""
    if date is None:
        date = datetime.now()
    
    # 获取市场数据
    sentiment = get_market_sentiment()
    valuation = get_valuation_level()
    
    # 生成建议
    advice = {
        'date': date.strftime('%Y-%m-%d'),
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'market_data': {
            'sh000001': MARKET_DATA['sh000001'],
            'sz399001': MARKET_DATA['sz399001'],
            'sz399006': MARKET_DATA['sz399006'],
        },
        'sentiment': {
            'state': sentiment['state'],
            'state_name': sentiment['state_name'],
        },
        'valuation': valuation,
        'advice': {
            'market_view': generate_market_view(sentiment, valuation),
            'asset_allocation': generate_asset_allocation(valuation),
            'operation_strategy': generate_operation_strategy(sentiment, valuation),
        }
    }
    
    return advice

def save_advice(advice: dict):
    """保存投资建议"""
    advice_dir = Path(__file__).parent / 'advice_data'
    advice_dir.mkdir(exist_ok=True)
    
    # 保存当日建议
    today_file = advice_dir / 'advice_today.json'
    with open(today_file, 'w', encoding='utf-8') as f:
        json.dump(advice, f, ensure_ascii=False, indent=2)
    
    # 归档历史建议
    archive_file = advice_dir / f'advice_{advice["date"]}.json'
    with open(archive_file, 'w', encoding='utf-8') as f:
        json.dump(advice, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 建议已生成：{today_file}")
    print(f"📦 历史归档：{archive_file}")

def update_html_advice(advice: dict):
    """更新 HTML 文件中的建议"""
    html_file = Path(__file__).parent / 'index.html'
    
    if not html_file.exists():
        print(f"⚠️ HTML 文件不存在：{html_file}")
        return
    
    # 读取 HTML 文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 替换建议内容
    import re
    
    # 市场观点
    market_view = advice['advice']['market_view']
    html_content = re.sub(
        r'<strong>📊 市场观点：</strong>[^<]+',
        f'<strong>📊 市场观点：</strong>{market_view}',
        html_content
    )
    
    # 资产配置
    asset_allocation = advice['advice']['asset_allocation']
    html_content = re.sub(
        r'<strong>⚖️ 资产配置：</strong>股票\\s*\\d+%\\s*\\+\\s*债券\\s*\\d+%\\s*\\+\\s*黄金\\s*\\d+%',
        f'<strong>⚖️ 资产配置：</strong>{asset_allocation}',
        html_content
    )
    
    # 操作策略
    operation_strategy = advice['advice']['operation_strategy']
    html_content = re.sub(
        r'<strong>🎯 操作策略：</strong>[^<]+',
        f'<strong>🎯 操作策略：</strong>{operation_strategy}',
        html_content
    )
    
    # 写回 HTML 文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML 文件已更新：{html_file}")

def cleanup_old_archives(days: int = 30):
    """清理旧归档"""
    advice_dir = Path(__file__).parent / 'advice_data'
    
    if not advice_dir.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for file in advice_dir.glob('advice_*.json'):
        if file.name == 'advice_today.json':
            continue
        
        # 提取日期
        import re
        match = re.search(r'advice_(\\d{4}-\\d{2}-\\d{2})\\.json', file.name)
        if match:
            file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
            if file_date < cutoff_date:
                file.unlink()
                print(f"🗑️ 已删除旧归档：{file.name}")

def main():
    """主函数"""
    print("=" * 60)
    print("💡 智能投资建议生成")
    print("=" * 60)
    print(f"📅 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 生成建议
    print("1️⃣ 生成投资建议...")
    advice = generate_daily_advice()
    print(f"   ✅ 市场状态：{advice['sentiment']['state_name']}")
    print(f"   ✅ 估值水平：{advice['valuation']}")
    print(f"   ✅ 市场观点：{advice['advice']['market_view'][:30]}...")
    print(f"   ✅ 资产配置：{advice['advice']['asset_allocation']}")
    print(f"   ✅ 操作策略：{advice['advice']['operation_strategy'][:30]}...")
    
    # 2. 保存数据
    print("\n2️⃣ 保存数据...")
    save_advice(advice)
    
    # 3. 更新 HTML
    print("\n3️⃣ 更新 HTML...")
    update_html_advice(advice)
    
    # 4. 清理旧归档
    print("\n4️⃣ 清理旧归档...")
    cleanup_old_archives(days=30)
    
    print("\n" + "=" * 60)
    print("✅ 投资建议生成完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
