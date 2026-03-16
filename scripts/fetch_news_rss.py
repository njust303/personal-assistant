#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人理财助手 - RSS 新闻抓取脚本 v2
从多个 RSS 源获取真实财经新闻（增强版）
"""

import feedparser
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import re
import requests

# RSS 订阅源配置（持续更新中）
RSS_FEEDS = {
    "finance": [
        "http://rss.sina.com.cn/finance/stock/sscj.xml",
        "http://rss.sina.com.cn/finance/finances/ssyq.xml",
        "http://app.eastmoney.com/rss/rss.xml",
        "http://rss.hexun.com/stock/24.xml",
        "http://finance.qq.com/rss/finance.xml",
        "https://xueqiu.com/hots/topic/rss"
    ],
    "ai": [
        "https://www.oschina.net/news/rss?catalog=ai",
        "https://blog.csdn.net/nav/ai/rss",
        "https://www.jiqizhixin.com/rss",
        "https://36kr.com/feed",
        "https://www.tmtpost.com/feed"
    ],
    "tea": [
        "http://news.foodmate.net/rss.php",
        "http://rss.winshang.com/news.xml",
        "http://www.canyinj.com/rss/",
        "http://www.linkshop.com.cn/rss/news.xml",
        "http://www.hongcan.com/rss/"
    ],
    "global": [
        "http://rss.sina.com.cn/news/world/rss.xml",
        "https://www.cankaoxiaoxi.com/rss/world.xml",
        "http://rss.chinadaily.com.cn/china/world.xml",
        "http://app.eastmoney.com/rss/global.xml",
        "http://rss.people.com.cn/rss/world.xml",
        "http://news.qq.com/rss/world.xml"
    ]
}

def fetch_with_timeout(url, timeout=5):
    """带超时的 RSS 抓取"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        return feedparser.parse(response.content)
    except Exception as e:
        print(f"    ⚠️ 超时或失败：{url[:50]}...")
        return None

def parse_rss_feed(feed_url, category):
    """解析 RSS 订阅源"""
    feed = fetch_with_timeout(feed_url)
    if not feed or not feed.entries:
        return []
    
    articles = []
    
    for entry in feed.entries[:15]:
        # 提取发布时间
        published = entry.get('published', '')
        if published:
            try:
                pub_date = datetime.strptime(published[:19], '%Y-%m-%dT%H:%M:%S')
                time_ago = get_time_ago(pub_date)
                date_str = pub_date.strftime('%Y-%m-%d')
            except:
                time_ago = "刚刚"
                date_str = datetime.now().strftime('%Y-%m-%d')
        else:
            time_ago = "刚刚"
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 只取 7 天内的新闻
        if time_ago.endswith("天前") and int(time_ago.replace("天前", "")) > 7:
            continue
        
        # 提取内容
        title = entry.get('title', '')
        # 尝试多个字段获取内容
        summary = entry.get('summary', '')
        if not summary:
            summary = entry.get('description', '')
        if not summary:
            summary = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
        
        link = entry.get('link', '')
        
        # 清理 HTML 标签
        summary = clean_html(summary)
        
        # 跳过标题或内容为空的
        if not title or len(title) < 5:
            continue
        
        # 如果 summary 为空，标注"详情见原文链接"
        if not summary or len(summary) < 10:
            summary = "👉 详情请点击文末原文链接查看完整报道。"
        
        articles.append({
            "t": title,
            "s": get_category_name(category),
            "time": time_ago,
            "date": date_str,
            "summary": summary[:300] + "..." if len(summary) > 300 else summary,
            "analysis": "",  # 移除假分析，等后续用 AI 真正分析
            "source_url": link
        })
        
        if len(articles) >= 6:
            break
    
    return articles

def get_category_name(category):
    """获取分类名称"""
    names = {
        "finance": "财经",
        "ai": "科技",
        "tea": "消费",
        "global": "国际"
    }
    return names.get(category, "网络")

def clean_html(text):
    """清理 HTML 标签"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_time_ago(pub_date):
    """计算相对时间"""
    now = datetime.now()
    delta = now - pub_date
    
    if delta.seconds < 60:
        return "刚刚"
    elif delta.seconds < 3600:
        return f"{delta.seconds // 60}分钟前"
    elif delta.seconds < 86400:
        return f"{delta.seconds // 3600}小时前"
    elif delta.days < 7:
        return f"{delta.days}天前"
    else:
        return pub_date.strftime('%m-%d')

def generate_analysis(title, summary, category):
    """生成 AI 分析"""
    analyses = {
        "finance": "💡 财经新闻反映宏观经济形势和政策动向。建议关注政策受益板块，如金融、地产、基建等。同时留意市场流动性变化，合理配置资产。",
        "ai": "💡 AI 产业发展迅速，算力、算法、应用三个环节都有投资机会。建议关注有核心技术、有应用场景的公司，如芯片、大模型、办公软件等。",
        "tea": "💡 消费行业稳定增长，新式茶饮、餐饮连锁等细分赛道机会多。建议关注头部品牌和供应链企业，留意消费升级和健康化趋势。",
        "global": "💡 国际形势变化影响全球资本市场。美联储政策、地缘政治、大宗商品价格等都是重要变量。建议关注外资流向和汇率变化。"
    }
    
    return analyses.get(category, "💡 建议结合宏观经济形势和行业动态，理性分析该消息的影响。投资需谨慎，注意风险控制。")

def fetch_all_news():
    """抓取所有 RSS 源"""
    all_news = {
        "finance": [],
        "ai": [],
        "tea": [],
        "global": []
    }
    
    for category, urls in RSS_FEEDS.items():
        print(f"\n📰 抓取 {get_category_name(category)} 新闻...")
        
        for url in urls:
            articles = parse_rss_feed(url, category)
            if articles:
                print(f"  ✅ {url[:40]}... - {len(articles)}条")
                all_news[category].extend(articles)
            
            # 每个分类够了就停止
            if len(all_news[category]) >= 6:
                break
        
        # 保留最新的 6 条
        all_news[category] = all_news[category][:6]
        print(f"  📊 {get_category_name(category)} 合计：{len(all_news[category])}条")
    
    return all_news

def save_news(news_data):
    """保存新闻数据"""
    output_dir = Path(__file__).parent.parent / "h5-app" / "news_data"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "news_today.json"
    
    data = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M 更新"),
        "version": "v4.7-RSS",
        "source": "RSS 实时抓取",
        "note": "数据来自真实 RSS 订阅源，确保时效性和真实性",
        "news": news_data
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 新闻数据已保存：{output_file}")
    return output_file

def main():
    """主函数"""
    print("=" * 60)
    print("📰 个人理财助手 - RSS 新闻抓取 v2")
    print("=" * 60)
    
    # 抓取新闻
    news_data = fetch_all_news()
    
    # 统计
    total = sum(len(v) for v in news_data.values())
    print()
    print(f"📊 总计抓取：{total} 条新闻")
    for category, articles in news_data.items():
        print(f"  {get_category_name(category)}: {len(articles)} 条")
    
    # 保存
    output_file = save_news(news_data)
    
    print()
    print("=" * 60)
    print("✅ RSS 新闻抓取完成！")
    print("=" * 60)
    
    return output_file

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 抓取失败：{e}")
        import traceback
        traceback.print_exc()
        exit(1)
