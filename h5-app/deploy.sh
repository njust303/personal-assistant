#!/bin/bash
# 个人理财助手 v3.7 部署脚本

set -e

echo "========================================"
echo "💰 个人理财助手 v3.7 部署脚本"
echo "========================================"

APP_DIR="/home/admin/.openclaw/workspace/projects/个人理财助手/h5-app"
LOG_DIR="$APP_DIR/logs"
PID_FILE="$APP_DIR/server.pid"

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "📂 工作目录：$APP_DIR"
echo "📝 日志目录：$LOG_DIR"

# 检查依赖
echo ""
echo "🔍 检查依赖..."
python3 -c "import flask" 2>/dev/null && echo "  ✅ Flask 已安装" || echo "  ❌ Flask 未安装"
python3 -c "import flask_cors" 2>/dev/null && echo "  ✅ Flask-CORS 已安装" || echo "  ❌ Flask-CORS 未安装"
python3 -c "import requests" 2>/dev/null && echo "  ✅ Requests 已安装" || echo "  ❌ Requests 未安装"

# 停止旧服务
echo ""
echo "🛑 停止旧服务..."
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        kill $OLD_PID && echo "  ✅ 已停止旧服务 (PID: $OLD_PID)" || echo "  ⚠️ 停止失败"
    fi
    rm -f "$PID_FILE"
fi

# 启动新服务
echo ""
echo "🚀 启动 API 服务器..."
cd "$APP_DIR"
nohup python3 server.py > "$LOG_DIR/server.log" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"
sleep 2

if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "  ✅ 服务启动成功 (PID: $NEW_PID)"
else
    echo "  ❌ 服务启动失败，请检查日志：$LOG_DIR/server.log"
    exit 1
fi

# 设置 cron 定时任务
echo ""
echo "⏰ 配置 cron 定时任务..."
CRON_JOB="* * * * * cd $APP_DIR && python3 fetch_stock_data.py >> $LOG_DIR/cron.log 2>&1"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "fetch_stock_data.py"; then
    echo "  ⚠️ Cron 任务已存在"
else
    (crontab -l 2>/dev/null | grep -v "fetch_stock_data.py"; echo "$CRON_JOB") | crontab -
    echo "  ✅ Cron 任务已添加（每分钟执行一次）"
fi

# 显示状态
echo ""
echo "========================================"
echo "📊 部署状态"
echo "========================================"
echo "  服务 PID: $NEW_PID"
echo "  访问地址：http://localhost:5000"
echo "  API 接口：http://localhost:5000/api/stock-data"
echo "  日志文件：$LOG_DIR/server.log"
echo ""
echo "📋 常用命令："
echo "  查看日志：tail -f $LOG_DIR/server.log"
echo "  停止服务：kill $NEW_PID"
echo "  重启服务：$APP_DIR/deploy.sh"
echo "  查看 cron: crontab -l"
echo ""
echo "✅ 部署完成！"
