# 股票数据爬虫 - 使用说明

## 方案一：新浪财经 API 抓取

### 原理
通过访问新浪财经的公开 API 接口，获取实时股票行情数据。

### 数据源
- **股票/指数**: 新浪财经 (`hq.sinajs.cn`)
- **基金**: 天天基金网 (`fundgz.1234567.com.cn`)
- **黄金**: 新浪财经商品频道

### 使用方法

#### 1. 直接运行脚本
```bash
cd /home/admin/.openclaw/workspace/projects/个人理财助手/h5-app
python3 fetch_stock_data.py
```

#### 2. 输出数据
脚本会生成 `stock_data.json` 文件，包含：
```json
{
  "timestamp": "2026-03-15T08:17:09.804763",
  "stocks": {
    "sh000001": {
      "name": "上证指数",
      "price": 4095.45,
      "change": -0.54,
      "change_amount": -22.13
    },
    ...
  },
  "funds": {...},
  "gold": {...}
}
```

### 集成到 HTML 页面

#### 方案 A: 后端服务（推荐）
创建一个简单的 HTTP 服务，定时抓取数据并提供 API：

```python
# server.py
from flask import Flask, jsonify
from fetch_stock_data import get_all_data

app = Flask(__name__)

@app.route('/api/stock-data')
def get_data():
    return jsonify(get_all_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

然后在 HTML 中用 fetch 获取：
```javascript
fetch('/api/stock-data')
    .then(r => r.json())
    .then(data => updatePage(data));
```

#### 方案 B: 定时任务 + 静态文件
1. 设置 cron 定时任务，每分钟运行一次脚本
2. HTML 页面定期读取 `stock_data.json` 文件

```bash
# crontab -e
* * * * * cd /path/to/h5-app && python3 fetch_stock_data.py
```

### 支持的股票代码

#### 股票/指数
| 代码 | 名称 |
|------|------|
| sh000001 | 上证指数 |
| sz399001 | 深证成指 |
| sz399006 | 创业板指 |
| sh000300 | 沪深 300 |
| hk00700 | 腾讯控股 |
| sh600519 | 贵州茅台 |

#### 基金
| 代码 | 名称 |
|------|------|
| 510300 | 沪深 300ETF |
| 161725 | 招商中证白酒 |

### 注意事项

1. **API 限制**: 新浪财经 API 有频率限制，建议请求间隔 >= 1 秒
2. **交易时间**: 非交易时间数据不更新
3. **港股**: 港股代码需要加 `rt_` 前缀
4. **数据延迟**: 免费 API 可能有 1-5 分钟延迟

### 扩展更多股票

编辑 `fetch_stock_data.py`，在字典中添加：

```python
SINA_STOCK_CODES = {
    'sh000001': 'sh000001',  # 上证指数
    'sz399001': 'sz399001',  # 深证成指
    # 添加新股票:
    'sh600000': 'sh600000',  # 浦发银行
    'sz000001': 'sz000001',  # 平安银行
}
```

### 故障排查

1. **连接失败**: 检查网络连接，可能需要代理
2. **数据为空**: 可能是非交易时间或 API 限流
3. **解析错误**: 检查 API 返回格式是否变化

### 下一步优化

- [ ] 添加更多股票和基金代码
- [ ] 实现数据缓存，减少 API 调用
- [ ] 添加错误重试机制
- [ ] 集成到 HTML 页面自动刷新
- [ ] 添加历史数据记录
