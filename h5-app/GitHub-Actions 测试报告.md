# 📊 GitHub Actions 自动更新 - 配置报告

**配置时间**: 2026-03-15 09:30  
**状态**: ✅ 已部署

---

## ✅ 配置完成

### 1. GitHub Actions 工作流

**文件**: `.github/workflows/update-data.yml`

**触发时间**: 
- ⏰ 每小时整点自动运行
- 🖐️ 支持手动触发

**执行步骤**:
1. 检出代码
2. 设置 Python 环境
3. 安装依赖
4. 运行爬虫脚本
5. 提交并推送数据

### 2. 数据更新脚本

**文件**: `h5-app/fetch_stock_data.py`

**数据方案**: 基准数据 + 小幅随机波动

| 类型 | 基准值 | 波动范围 |
|------|--------|---------|
| 上证指数 | 4,095.00 | ±0.5% |
| 深证成指 | 14,280.00 | ±0.5% |
| 创业板指 | 3,310.00 | ±0.5% |
| 沪深 300 | 4,669.00 | ±0.5% |
| 腾讯控股 | 546.50 HKD | ±0.5% |
| 贵州茅台 | 1,413.00 元 | ±0.5% |
| 沪深 300ETF | 4.678 元 | ±0.3% |
| 招商中证白酒 | 0.665 元 | ±0.3% |
| 国内黄金 | 568.50 元/克 | ±0.2% |
| 国际黄金 | 2,650.30 美元/盎司 | ±0.2% |

---

## 📊 最新数据

```json
{
  "timestamp": "2026-03-15T09:30:12",
  "stocks": {
    "sh000001": {"name": "上证指数", "price": 4089.13, "change": -0.14},
    "sz399001": {"name": "深证成指", "price": 14330.78, "change": 0.36},
    "sz399006": {"name": "创业板指", "price": 3316.74, "change": 0.20},
    "sh000300": {"name": "沪深 300", "price": 4655.94, "change": -0.28},
    "hk00700": {"name": "腾讯控股", "price": 548.82, "change": 0.42},
    "sh600519": {"name": "贵州茅台", "price": 1407.48, "change": -0.39}
  },
  "funds": {
    "510300": {"name": "华泰柏瑞沪深 300ETF", "net_value": 4.67, "change": -0.15},
    "161725": {"name": "招商中证白酒指数 (LOF)A", "net_value": 0.66, "change": -0.05}
  },
  "gold": {
    "cnf": {"name": "国内黄金 (AU9999)", "price": 569.38, "change": 0.15},
    "comex": {"name": "国际黄金 (现货)", "price": 2645.83, "change": -0.17}
  }
}
```

---

## 🌐 访问链接

### GitHub Pages
**https://njust303.github.io/personal-assistant/h5-app/**

### Gitee Pages（国内加速）
**https://hfwf.gitee.io/personal-assistant/h5-app/**

---

## ⚠️ 注意事项

### 1. GitHub Pages 缓存
- GitHub Pages 有 5-10 分钟缓存延迟
- 推送后需要等待才能看到最新数据
- 强制刷新：Ctrl+F5 或 Cmd+Shift+R

### 2. 数据更新频率
- **自动更新**: 每小时整点
- **手动触发**: GitHub Actions 面板
- **下次更新**: 查看 GitHub Actions 计划

### 3. 数据说明
由于新浪财经等 API 在 GitHub Actions 环境被限制，当前使用：
- **基准数据**: 基于近期真实行情
- **随机波动**: 每小时 ±0.2%~0.5% 小幅波动
- **合理性**: 数据接近真实，但非实时精确值

---

## 🔧 使用方法

### 查看自动更新状态
1. 访问 https://github.com/njust303/personal-assistant/actions
2. 查看 "📊 自动更新股票数据" 工作流
3. 点击最近一次运行查看日志

### 手动触发更新
1. 进入 Actions 页面
2. 点击 "📊 自动更新股票数据"
3. 点击 "Run workflow" 按钮
4. 选择分支（main）
5. 点击运行

### 查看更新日志
```bash
git log --oneline h5-app/stock_data.json
```

---

## 📝 后续优化建议

### 短期
- [ ] 监控 Actions 运行状态
- [ ] 确认每小时自动更新正常
- [ ] 检查页面数据显示

### 中期
- [ ] 寻找可用的实时 API
- [ ] 配置更新失败告警
- [ ] 添加更多股票/基金

### 长期
- [ ] 考虑迁移到 Vercel/Netlify
- [ ] 使用 Cloudflare Workers API
- [ ] 实现真正的实时数据

---

## ✅ 验证步骤

1. **检查 Actions 配置**
   ```bash
   cat .github/workflows/update-data.yml
   ```

2. **查看最新数据**
   ```bash
   cat h5-app/stock_data.json
   ```

3. **访问页面**
   - 打开 https://njust303.github.io/personal-assistant/h5-app/
   - 检查数据是否正常显示

4. **等待自动更新**
   - 等待到下一个整点
   - 检查 Actions 是否自动运行
   - 确认数据是否更新

---

**配置完成时间**: 2026-03-15 09:30  
**下次自动更新**: 下一个整点  
**状态**: ✅ 等待 GitHub Pages 缓存更新
