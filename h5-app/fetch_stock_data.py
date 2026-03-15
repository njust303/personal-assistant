#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据爬虫 - 方案一：使用新浪财经 API
新浪财经 API 更开放，适合获取实时股票行情
"""

import requests
import re
import json
import time
import random
from datetime import datetime

# 新浪财经 API 接口
STOCK_API_URL = "https://hq.sinajs.cn/list="
GOLD_API_URL = "https://hq.sinajs.cn/list="

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://finance.sina.com.cn/',
}

# 新浪财经股票代码格式
SINA_STOCK_CODES = {
    'sh000001': 'sh000001',  # 上证指数
    'sz399001': 'sz399001',  # 深证成指
    'sz399006': 'sz399006',  # 创业板指
    'sh000300': 'sh000300',  # 沪深 300
    'hk00700': 'rt_hk00700', # 腾讯控股（港股）
    'sh600519': 'sh600519',  # 贵州茅台
}

# 基金代码
SINA_FUND_CODES = {
    '510300': 'sh510300',    # 沪深 300ETF
    '005827': 'sz005827',    # 易方达蓝筹（这个可能没有，需要调整）
    '161725': 'sz161725',    # 招商中证白酒
    '000198': 'sz000198',    # 余额宝（这个可能没有）
}

# 黄金代码（新浪财经）
SINA_GOLD_CODES = {
    'cnf': 'gf_DAU',         # 国内黄金（黄金 T+D）
    'comex': 'nf_AU0',       # 国际黄金（沪金主力）
}

session = requests.Session()
session.headers.update(HEADERS)


def fetch_stock_data():
    """获取股票行情数据 - 新浪财经"""
    try:
        # 构建股票代码字符串
        codes = ','.join(SINA_STOCK_CODES.values())
        url = f"{STOCK_API_URL}{codes}"
        
        print(f"  请求 URL: {url[:80]}...")
        
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        # 新浪财经返回的是 JavaScript 变量格式
        content = response.text
        print(f"  响应长度：{len(content)} 字节")
        
        result = {}
        
        # 解析每只股票数据
        for line in content.strip().split('\n'):
            if not line.strip():
                continue
                
            # 格式：var hq_str_sh000001="上证指数，3050.23,..."
            match = re.search(r'var hq_str_(\w+)="([^"]+)"', line)
            if match:
                code = match.group(1)
                data_str = match.group(2).split(',')
                
                # 反向查找自定义代码
                for custom_code, sina_code in SINA_STOCK_CODES.items():
                    if sina_code == code or sina_code.replace('rt_', '') == code:
                        try:
                            if len(data_str) >= 4:
                                name = data_str[0]
                                # 处理港股（腾讯控股等）
                                if 'hk' in code.lower():
                                    # 港股格式可能不同，用昨收和现价
                                    current_price = float(data_str[3]) if data_str[3] else 0
                                    prev_close = float(data_str[2]) if data_str[2] else current_price
                                    open_price = prev_close  # 用昨收代替开盘价计算
                                else:
                                    current_price = float(data_str[3]) if data_str[3] else 0
                                    open_price = float(data_str[1]) if data_str[1] else current_price
                                
                                # 计算涨跌幅
                                change = ((current_price - open_price) / open_price * 100) if open_price else 0
                                change_amount = current_price - open_price
                                
                                result[custom_code] = {
                                    'name': name,
                                    'price': round(current_price, 2),
                                    'change': round(change, 2),
                                    'change_amount': round(change_amount, 2),
                                }
                                print(f"  ✓ {custom_code}: {name} - {current_price} ({change:+.2f}%)")
                        except (ValueError, IndexError) as e:
                            print(f"  ⚠ 解析{custom_code}数据失败：{e}")
                        break
        
        return result if result else None
        
    except Exception as e:
        print(f"  获取股票数据失败：{e}")
        return None


def fetch_gold_data():
    """获取黄金价格数据 - 新浪财经"""
    result = {}
    
    # 尝试多个黄金代码
    gold_alternatives = {
        'cnf': ['gf_DAU', 'nf_AU0', 'XAU'],  # 国内黄金
        'comex': ['XAU', 'nf_AU0', 'gf_DAU'], # 国际黄金
    }
    
    for name, codes in gold_alternatives.items():
        for code in codes:
            try:
                url = f"{GOLD_API_URL}{code}"
                response = session.get(url, timeout=15)
                response.raise_for_status()
                
                content = response.text
                match = re.search(r'var hq_str_\w+="([^"]+)"', content)
                
                if match:
                    data_str = match.group(1).split(',')
                    # 检查是否有有效数据
                    if len(data_str) >= 4 and data_str[3]:
                        try:
                            price = float(data_str[3])
                            open_price = float(data_str[1]) if data_str[1] else price
                            change = ((price - open_price) / open_price * 100) if open_price else 0
                            
                            result[name] = {
                                'name': f"{name.upper()}黄金",
                                'price': round(price, 2),
                                'change': round(change, 2),
                                'change_amount': round(price - open_price, 2),
                            }
                            print(f"  ✓ {name}黄金 ({code}): {price} ({change:+.2f}%)")
                            break  # 找到有效数据就跳出
                        except (ValueError, IndexError):
                            continue
                            
            except Exception as e:
                continue
        
        if name not in result:
            print(f"  ✗ {name}黄金：未获取到有效数据")
    
    return result if result else None


def fetch_fund_data():
    """获取基金数据 - 使用天天基金网 API"""
    # 天天基金网 API
    fund_codes = ['510300', '161725']  # 只获取确定有的基金
    result = {}
    
    for code in fund_codes:
        try:
            url = f"http://fundgz.1234567.com.cn/js/{code}.js"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'http://fund.eastmoney.com/',
            }
            
            response = session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # 解析 JSONP
            content = response.text
            match = re.search(r'jsonpgz\((\{[^}]+\})\)', content)
            
            if match:
                data = json.loads(match.group(1))
                result[code] = {
                    'name': data.get('name', ''),
                    'net_value': float(data.get('gsz', 0)),
                    'change': float(data.get('gszzl', 0)),
                    'change_amount': 0,  # 估算净值没有涨跌额
                }
                print(f"  ✓ 基金{code}: {data.get('name', '')} - {data.get('gsz', 0)} ({data.get('gszzl', 0)}%)")
                
        except Exception as e:
            print(f"  获取基金{code}数据失败：{e}")
            continue
    
    return result if result else None


def get_all_data():
    """获取所有数据"""
    print(f"\n开始获取数据：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    stock_data = fetch_stock_data()
    print()
    fund_data = fetch_fund_data()
    print()
    gold_data = fetch_gold_data()
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'stocks': stock_data,
        'funds': fund_data,
        'gold': gold_data,
    }
    
    return result


def main():
    """主函数"""
    data = get_all_data()
    
    # 输出 JSON 格式
    print("\n" + "="*50)
    print("完整数据：")
    print("="*50)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    # 保存到文件
    output_file = 'stock_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n数据已保存到：{output_file}")


if __name__ == '__main__':
    main()
