# OpenDTV

**海外华人娱乐入口** — 影视 | 电视 | APP | 设备

🌐 Live: https://123638.com/

## 项目介绍

OpenDTV 是一个为海外华人打造的娱乐导航站，提供：

- 🎬 **影视平台** — 全球主流流媒体平台导航
- 📺 **电视直播** — IPTV 华语及海外频道精选
- 📱 **TV 应用** — 电视盒子 App 推荐与下载
- 📦 **电视设备** — 设备横向评测与选购指南

## 技术栈

- 纯静态 HTML + CSS + JS（无框架依赖）
- GitHub Pages 部署
- 后续计划迁移至 Supabase 数据驱动

## 文件结构

```
opendtv-site/
├── index.html        # 首页（导航 + 热门推荐）
├── streaming.html    # 影视平台页（占位）
├── livetv.html       # 电视直播页（占位）
├── apps.html         # TV 应用页（占位）
├── devices.html      # 电视设备页（占位）
├── style.css         # 全站样式
├── script.js         # 数据 & 渲染逻辑（含 mock data）
└── .github/
    └── workflows/
        └── static.yml  # GitHub Pages 自动部署
```

## Mock Data 位置

`script.js` 顶部的 `featuredItems` 数组即为热门推荐数据源，后续可替换为 Supabase 查询。

## 后续扩展路线图

- [ ] 四大频道页内容填充
- [ ] Supabase 数据表接入
- [ ] IPTV 数据源集成
- [ ] 影视详情页
- [ ] APP 下载页（含 APK 链接）
- [ ] 设备对比表格
- [ ] SEO 关键词页面
