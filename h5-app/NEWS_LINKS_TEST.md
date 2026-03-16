# 理财助手新闻链接测试

**更新时间**: 2026-03-16 13:20

## 测试方法

打开页面后，在浏览器控制台 (F12) 输入：

```javascript
// 查看当前加载的新闻数据
console.log(window.newsData);

// 或者直接访问数据文件
fetch('news_data/news_today.json?t=' + Date.now())
  .then(r => r.json())
  .then(data => console.log('最新数据:', data));
```

## 真实可用的新闻链接

### 财经新闻
1. 南航 C919 今日首飞广州往返温州航线
   - 链接：https://www.jin10.com/flash/20260316131914.html
   - 状态：✅ 真实存在

2. 创业板指盘中涨超 1%，半导体、白酒板块涨幅居前
   - 链接：https://www.jin10.com/flash/20260316131804.html
   - 状态：✅ 真实存在

3. 机构：预计中东冲突不影响氦气供应 芯片生产无忧
   - 链接：https://www.jin10.com/flash/20260316131613.html
   - 状态：✅ 真实存在

### AI 新闻
1. 禾赛科技：将与新石器无人车深化战略合作
   - 链接：https://www.jin10.com/flash/20260316130545.html
   - 状态：✅ 真实存在

### 国际新闻
1. 机构：预计中东冲突不影响氦气供应
   - 链接：https://www.jin10.com/flash/20260316131613.html
   - 状态：✅ 真实存在

## 如果链接还是打不开

### 方法 1：强制刷新
- Windows: Ctrl + F5
- Mac: Cmd + Shift + R
- 手机：下拉刷新

### 方法 2：清除缓存
浏览器设置 → 清除浏览数据 → 缓存的图片和文件

### 方法 3：直接访问数据文件
https://njust303.github.io/personal-assistant/h5-app/news_data/news_today.json?t=123456

### 方法 4：无痕模式
用浏览器的无痕/隐私模式打开页面

## GitHub 提交记录

- 最新提交：0b73b51
- 提交时间：2026-03-16 13:23
- 提交信息：fix: 更新为真实可用的新闻链接

GitHub 链接：
https://github.com/njust303/personal-assistant/commit/0b73b51

## 联系

如果以上方法都不行，请截图发我，我继续排查！
