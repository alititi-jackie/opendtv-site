# OpenDTV

**海外华人娱乐入口** — 影视 | 电视 | APP | 设备

🌐 Live: https://opendtv.com/

## 项目介绍

OpenDTV 是一个为海外华人打造的娱乐导航站，提供：

- 🎬 **影视平台** — 全球主流流媒体 + 华语视频平台导航（Netflix、Disney+、抖音、哔哩哔哩、腾讯视频 WeTV、优酷国际版、芒果TV国际版等）
- 📺 **电视直播** — 合法网络电视与免费频道平台
- 📱 **TV 应用** — 播放器、媒体库、投屏与官方 TV 应用
- 📦 **电视设备** — 流媒体盒子、智能电视选购指南
- 📖 **使用指南** — 4 篇实用指南（设备选购、免费看电视、安全装应用、卡顿排查）

只收录公开、合法、可核验的平台和官方入口，不提供盗版资源。

## 技术栈

- 纯静态 HTML + CSS + JS（无框架依赖）
- Vercel 部署（vercel.json 管理跳转与安全头）
- PWA：manifest.webmanifest + sw.js（可安装、离线可用）
- 导航数据：`app-v2.js` 顶部的 `items` 数组（搜索、首页推荐、目录页共用）；频道页另有硬编码卡片，新增条目时两处都要加

## 文件结构

```
opendtv-site/
├── index.html        # 首页（导航 + 热门推荐 + 站内搜索）
├── streaming.html    # 影视平台页
├── livetv.html       # 电视服务页
├── apps.html         # TV 应用页
├── devices.html      # 电视设备页
├── catalog.html      # 可筛选的全部内容目录（?type=streaming|livetv|apps|devices）
├── guides.html       # 指南索引
├── guides/           # 4 篇指南文章
├── app-v2.js         # 数据 & 渲染逻辑
├── style-v2.css      # 全站样式
├── manifest.webmanifest
├── sw.js             # Service Worker
├── sitemap.xml
├── robots.txt
├── vercel.json       # 跳转与安全头
└── .github/workflows/static.yml  # 历史遗留（当前主部署为 Vercel）
```

## 部署说明

- 主部署：Vercel（推送到 main 自动部署）
- `.github/workflows/static.yml` 为历史 GitHub Pages 配置，当前未启用，如确认不再需要可删除
- 域名策略：以裸域 https://opendtv.com/ 为主，www 做 301 跳转到裸域（Vercel 控制台配置）

## 后续扩展路线图

- [x] 四大频道页内容填充
- [ ] Supabase 数据表接入
- [ ] 影视详情页
- [ ] 设备对比表格
- [ ] 更多指南文章（SEO）
