#!/bin/bash
# 更新数据并推送到 GitHub

set -e

echo "📊 开始更新股票数据..."
cd /home/admin/.openclaw/workspace/projects/个人理财助手/h5-app

# 运行爬虫
python3 fetch_stock_data.py

# 检查数据文件
if [ ! -f stock_data.json ]; then
    echo "❌ 数据文件不存在"
    exit 1
fi

# 提交并推送
cd ..
git add h5-app/stock_data.json
git commit -m "data: $(date '+%Y-%m-%d %H:%M') 自动更新股票数据" || echo "ℹ️ 数据无变化"
git push github main
git push gitee main

echo "✅ 数据已更新并推送"
echo "📱 访问：https://njust303.github.io/personal-assistant/h5-app/"
