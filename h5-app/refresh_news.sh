#!/bin/bash
# 手动刷新新闻脚本
# 用法：./refresh_news.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/news_data/refresh.log"

echo "========================================"
echo "📰 手动刷新新闻"
echo "========================================"
echo "📅 时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 执行更新
cd "$SCRIPT_DIR"
python3 fetch_news.py 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "========================================"
echo "✅ 刷新完成！"
echo "========================================"
echo "📝 日志：$LOG_FILE"
echo ""
