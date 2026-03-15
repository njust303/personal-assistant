#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据 API 服务器
提供实时股票数据接口给前端页面调用
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from fetch_stock_data import get_all_data
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # 允许跨域请求

# 内存缓存
cache = {
    'data': None,
    'timestamp': None,
}

CACHE_DURATION = 60  # 缓存 60 秒


def get_cached_data():
    """获取缓存数据，过期则重新抓取"""
    now = datetime.now()
    
    # 检查缓存是否有效
    if cache['data'] and cache['timestamp']:
        age = (now - cache['timestamp']).total_seconds()
        if age < CACHE_DURATION:
            print(f"  使用缓存数据 (剩余 {int(CACHE_DURATION - age)}s)")
            return cache['data']
    
    # 重新获取数据
    print(f"\n📊 抓取新数据：{now.strftime('%Y-%m-%d %H:%M:%S')}")
    data = get_all_data()
    
    if data:
        cache['data'] = data
        cache['timestamp'] = now
        
        # 保存到文件
        with open('stock_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    return cache['data']


@app.route('/')
def index():
    """首页"""
    return send_from_directory('.', 'index-v3.6.html')


@app.route('/api/stock-data')
def api_stock_data():
    """股票数据 API"""
    data = get_cached_data()
    
    if data:
        return jsonify({
            'success': True,
            'data': data,
            'cache_time': cache['timestamp'].isoformat() if cache['timestamp'] else None,
        })
    else:
        return jsonify({
            'success': False,
            'error': '获取数据失败',
        }), 500


@app.route('/api/refresh')
def api_refresh():
    """强制刷新数据"""
    print(f"\n🔄 强制刷新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    cache['data'] = None  # 清除缓存
    cache['timestamp'] = None
    data = get_cached_data()
    
    if data:
        return jsonify({
            'success': True,
            'data': data,
            'message': '数据已刷新',
        })
    else:
        return jsonify({
            'success': False,
            'error': '刷新失败',
        }), 500


@app.route('/stock_data.json')
def static_json():
    """静态 JSON 文件"""
    return send_from_directory('.', 'stock_data.json')


if __name__ == '__main__':
    print("="*60)
    print("🚀 股票数据 API 服务器")
    print("="*60)
    print(f"📍 本地访问：http://localhost:5000")
    print(f"📡 API 接口：http://localhost:5000/api/stock-data")
    print(f"🔄 刷新接口：http://localhost:5000/api/refresh")
    print(f"💾 数据缓存：{CACHE_DURATION} 秒")
    print("="*60)
    print("\n按 Ctrl+C 停止服务\n")
    
    # 先获取一次数据
    get_cached_data()
    
    # 启动服务器
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
