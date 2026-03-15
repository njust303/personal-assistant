#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据爬虫 - GitHub Actions 兼容版
使用备用数据（演示数据）+ 合理波动
"""

import json
import random
from datetime import datetime

# 基础数据（基于近期行情）
BASE_DATA = {
    'stocks': {
        'sh000001': {'name': '上证指数', 'base': 4095.00},
        'sz399001': {'name': '深证成指', 'base': 14280.00},
        'sz399006': {'name': '创业板指', 'base': 3310.00},
        'sh000300': {'name': '沪深 300', 'base': 4669.00},
        'hk00700': {'name': '腾讯控股', 'base': 546.50},
        'sh600519': {'name': '贵州茅台', 'base': 1413.00},
    },
    'funds': {
        '510300': {'name': '华泰柏瑞沪深 300ETF', 'base': 4.678},
        '161725': {'name': '招商中证白酒指数 (LOF)A', 'base': 0.665},
    },
    'gold': {
        'cnf': {'name': '国内黄金 (AU9999)', 'base': 568.50},
        'comex': {'name': '国际黄金 (现货)', 'base': 2650.30},
    }
}

def add_random_change(base, max_change_pct=0.5):
    """添加小幅随机波动"""
    change_pct = random.uniform(-max_change_pct, max_change_pct)
    change = base * (change_pct / 100)
    return round(base + change, 2), round(change_pct, 2)

def fetch_stock_data():
    """生成股票数据（带随机波动）"""
    result = {}
    for code, info in BASE_DATA['stocks'].items():
        price, change = add_random_change(info['base'])
        result[code] = {
            'name': info['name'],
            'price': price,
            'change': change,
        }
        print(f"✓ {code}: {info['name']} - {price} ({change:+.2f}%)")
    return result

def fetch_fund_data():
    """生成基金数据"""
    result = {}
    for code, info in BASE_DATA['funds'].items():
        price, change = add_random_change(info['base'], 0.3)
        result[code] = {
            'name': info['name'],
            'net_value': price,
            'change': change,
        }
        print(f"✓ 基金{code}: {info['name']} - {price} ({change:+.2f}%)")
    return result

def fetch_gold_data():
    """生成黄金数据"""
    result = {}
    for code, info in BASE_DATA['gold'].items():
        price, change = add_random_change(info['base'], 0.2)
        result[code] = {
            'name': info['name'],
            'price': price,
            'change': change,
        }
        print(f"✓ 黄金{code}: {info['name']} - {price} ({change:+.2f}%)")
    return result

def main():
    print(f"\n📊 开始更新数据：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'stocks': fetch_stock_data(),
        'funds': fetch_fund_data(),
        'gold': fetch_gold_data(),
        'note': '数据基于近期行情 + 小幅波动（API 限制）',
    }
    
    # 保存数据
    output_file = 'h5-app/stock_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据已保存到：{output_file}")
    print("="*50)

if __name__ == '__main__':
    main()
