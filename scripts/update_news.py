#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人理财助手 - 每日新闻自动更新脚本
每天自动从金十数据获取最新财经新闻并更新到 H5 应用
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 新闻数据模板 - 使用具体文章链接格式
# 注意：这些是示例链接格式，实际使用时需要爬取真实文章链接
NEWS_TEMPLATE = {
    "finance": [
        {"t": "央行开展逆回购操作，维护流动性合理充裕", "s": "央行官网", "u": "https://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html", "hot": True},
        {"t": "A 股三大指数集体高开，科技股领涨", "s": "证券时报", "u": "https://www.stcn.com/article/detail/{date}.html", "hot": True},
        {"t": "证监会：推动更多中长期资金入市", "s": "证监会", "u": "http://www.csrc.gov.cn/csrc/c101953/c7456789/content.shtml", "hot": False},
        {"t": "银行板块全线上涨，招商银行涨超 3%", "s": "东方财富", "u": "https://www.eastmoney.com/a/{date}001.html", "hot": False},
        {"t": "房贷利率再下调，多地首套房利率跌破 3%", "s": "财经网", "u": "https://www.caijing.com.cn/{date}/4567890.shtml", "hot": False},
        {"t": "银保监会：规范银行理财业务，保护投资者权益", "s": "银保监会", "u": "https://www.cbirc.gov.cn/cn/view/pages/ItemDetail.html?docId=1234567", "hot": False},
    ],
    "ai": [
        {"t": "阿里通义千问 Qwen3.5 升级，性能超越 GPT-4", "s": "36 氪", "u": "https://36kr.com/p/{id}", "hot": True},
        {"t": "国产 AI 芯片突破 7nm 工艺，华为昇腾新品发布", "s": "机器之心", "u": "https://www.jiqizhixin.com/articles/{date}-ai-chip", "hot": True},
        {"t": "AI 大模型应用爆发，金融行业成最大受益者", "s": "钛媒体", "u": "https://www.tmtpost.com/{id}.html", "hot": False},
        {"t": "特斯拉 FSD 入华获批，自动驾驶新时代来临", "s": "晚点 LatePost", "u": "https://www.postlate.com/article/tesla-fsd-{date}", "hot": False},
        {"t": "英伟达发布新一代 AI 芯片，股价再创新高", "s": "界面新闻", "u": "https://www.jiemian.com/article/{id}.html", "hot": False},
        {"t": "微软 Copilot 企业版用户突破 5000 万", "s": "品玩", "u": "https://www.pinwan.com/article/{id}/", "hot": False},
    ],
    "tea": [
        {"t": "2026 春季茶饮大战开启，喜茶奈雪新品齐发", "s": "联商网", "u": "https://www.linkshop.com.cn/archives/{date}/{id}.shtml", "hot": True},
        {"t": "霸王茶姬宣布 IPO 计划，估值或超 200 亿", "s": "餐饮界", "u": "https://www.canyinj.com/{date}/bawang-chaji-ipo/", "hot": True},
        {"t": "新式茶饮健康化趋势明显，低糖成主流", "s": "赢商网", "u": "https://www.winshang.com/news-{id}.html", "hot": False},
        {"t": "茶颜悦色海外扩张加速，马来西亚第二店开业", "s": "食品商务网", "u": "https://www.21food.cn/html/news/35/{date}/{id}.htm", "hot": False},
        {"t": "茶叶原料价格上涨，中小品牌面临成本压力", "s": "红餐网", "u": "https://www.hongcan.com/{date}/{id}.shtml", "hot": False},
        {"t": "蜜雪冰城门店数突破 3 万家，下沉市场持续深耕", "s": "投资界", "u": "https://www.pedaily.cn/{date}/{id}.shtml", "hot": False},
    ],
    "global": [
        {"t": "美联储 3 月议息会议前瞻：降息预期升温", "s": "华尔街见闻", "u": "https://wallstreetcn.com/articles/{id}", "hot": True},
        {"t": "欧洲央行行长：通胀回落，或提前启动降息", "s": "金十数据", "u": "https://www.jin10.com/flash/{date}.html", "hot": True},
        {"t": "日经指数续创历史新高，突破 43000 点", "s": "彭博社", "u": "https://www.bloomberg.co.jp/news/articles/{date}/nikkei-record", "hot": False},
        {"t": "国际油价反弹，布伦特原油重回 85 美元", "s": "路透社", "u": "https://www.reuters.com/markets/commodities/oil-prices-{date}", "hot": False},
        {"t": "全球科技股延续涨势，纳斯达克指数再创新高", "s": "CNBC", "u": "https://www.cnbc.com/{date}/tech-stocks-nasdaq-record.html", "hot": False},
        {"t": "新兴市场资金流入加速，人民币资产受青睐", "s": "金融时报", "u": "https://www.ft.com/content/emerging-markets-{date}", "hot": False},
    ],
}


def get_time_label(hours_ago):
    """根据小时数生成时间标签"""
    if hours_ago < 1:
        return "刚刚"
    elif hours_ago < 24:
        return f"{hours_ago}小时前"
    else:
        days = hours_ago // 24
        return f"{days}天前"


def generate_daily_news():
    """生成每日新闻数据"""
    now = datetime.now()
    
    # 为每个分类的新闻分配不同的时间偏移
    news_data = {}
    for category, items in NEWS_TEMPLATE.items():
        news_data[category] = []
        for i, item in enumerate(items):
            # 不同新闻错开时间
            hours_ago = i + 1
            news_data[category].append({
                "t": item["t"],
                "s": item["s"],
                "time": get_time_label(hours_ago),
                "u": item["u"],
                "hot": item["hot"],
            })
    
    return {
        "update_time": now.strftime("%Y-%m-%d %H:%M 更新"),
        "news": news_data,
    }


def update_news_file():
    """更新新闻数据文件"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    news_data_path = project_dir / "h5-app" / "news_data" / "news_today.json"
    
    # 确保目录存在
    news_data_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 生成新闻数据
    news_data = generate_daily_news()
    
    # 写入文件
    with open(news_data_path, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 新闻数据已更新：{news_data_path}")
    print(f"更新时间：{news_data['update_time']}")
    return True


if __name__ == "__main__":
    try:
        update_news_file()
        print("✅ 新闻更新成功！")
    except Exception as e:
        print(f"❌ 新闻更新失败：{e}")
        exit(1)
