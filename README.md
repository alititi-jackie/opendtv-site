# OpenDTV · 全球精选视频与电视门户

静态中文站点 [opendtv.com](https://opendtv.com/)。Python 标准库在构建时生成 HTML、搜索索引和站点地图。浏览器使用原生 JavaScript。GitHub Pages 仅部署 dist 目录。站内不存储视频，不需要数据库、用户系统或付费翻译服务。

## 开发与预览

从 main 建立开发分支，在仓库根目录运行以下命令。

```sh
python scripts/build.py
python scripts/check.py
node --check portal/site.js
python -m http.server 8000 -d dist
```

浏览 http://localhost:8000/ 。原有根目录 HTML 和 guides/*.html 是历史文章与介绍的构建输入。不要直接发布仓库根目录。编辑旧文章正文后重新构建。旧的 catalog.html?type=apps 等链接继续支持。同名目录与 .html 地址分别有实体页面，未使用服务端重定向。

## 编辑与审核

1. 从版权方官网、发布者原始页面或官方频道确认归属。记录原片 ID、频道标识、原始发布日期、时长及官方封面。仅使用发布者允许的官方嵌入。不要使用搬运频道或抓取的媒体流。
2. 在 data/channels/sources.json 登记来源。YouTube 使用实际 UC 频道 ID 和频道默认分类，Vimeo 使用 vimeo- 加数字用户 ID。已支持播放器仅限 YouTube、Vimeo 和 NPS。接入新播放器时需要同步修改 scripts/model.py、portal/site.js 与浏览器验播脚本。
3. 新分类在 data/categories.json 增加永久英文键和中文名称。已有分类键与 stableId 均应长期保留。
4. 参照 data/videos/od00018.json 填写一条 JSON。stableId 是独立站内编号。使用原发布页核对中文简介和署名。用实际浏览器在嵌入环境内播放，确认画面解码且时间推进。核对授权、原标题、频道、封面、地区限制和时长后记录 playbackCheckedAt。只有源站可播时可设置 embeddable 为 false 并保留原片入口。
5. 运行下列命令。import 先写入审核状态；approve 根据已复核的单条文件发布。分支构建通过后合并。长期不能用的记录设置 status 为 archived，保留提示页并移出搜索和 Sitemap。第三方要求删除资料时同时清理记录中该平台的元数据。
6. featured 控制编辑精选，featuredOrder 较小的条目优先。首页首位使用原视频封面。最新视频按原片发布时间排序。新增一条记录即可更新详情、分类、相关推荐、搜索及 Sitemap。

```sh
python scripts/catalog_ops.py import /path/to/one-video.json
python scripts/catalog_ops.py approve /path/to/one-video.json
python scripts/build.py
python scripts/check.py
```

## 自动发现与配额

在 GitHub 仓库 Settings → Secrets and variables → Actions → New repository secret 中设置 YOUTUBE_API_KEY。仅启用 YouTube Data API v3，限制密钥可调用的 API，使用免费项目并设置日配额。不要把密钥写入代码、表单、Issue 或浏览器。没有密钥时每日来源检查、静态部署和手动审核仍可运行。采集日志明确标记 SKIPPED。

每日 06:21 UTC 的 GitHub Actions 读取白名单，最多检查 10 个 YouTube 频道。每频道至多一次 channels.list、一次 playlistItems.list、一次 videos.list，使用 uploads 播放列表，无 search.list，不分页。每天最多输出 10 条未收录候选。下载当次运行的 editorial-review 工件，查看 candidates.json。候选只保存 7 天，按平台和视频编号对照已入库内容去重。候选可能在两天的工件里重复，不能当作新增发布数。编辑从数组中取单条，补上中文介绍、站内编号、收录日期和验播结果，再按上述流程审核。没有自动翻译、自动发布或付费 API。

## 失效处理与直播维护

data/live/channels.json 每项包含固定频道键、中文名、类别、官方入口、核对标识和核验日期。在官网确认是该频道的观看页，注明可能的地域、时段或订阅要求。站内入口不标记虚构的直播状态。

每日检查直播官方页面；普通视频和目录链接每七天复查。检查报告区分 ok、review、missing、unavailable、external。单次网络故障或 403 保留待复核；相隔两天的 404/410 触发隐藏。对于目录中原有平台，报告交给编辑复核并修正链接。YouTube API 明确不可用时停止展示，禁止嵌入时改为官方入口。已发布 YouTube 元数据在构建时用官方 API 刷新，超过 30 天未成功刷新的条目退出公开列表；不把 API 返回的候选工件提交到公开仓库。对 API 删除要求应及时清理源数据。

播放器检查通过 Chromium 点击本站加载控件，确认第三方播放器内出现实际解码画面。每天最多复查 32 条，优先较久未查的条目；遇到故障次日重试，连续两次失败暂停公开推荐。恢复后重新展示。播放器可能有地域限制，失败应结合人工复查，不表示全球下架。报告及历史保存在 Actions 工件和短期缓存，缓存失效后从源数据重新核验。原平台入口、直播入口访问和站内实播分开统计。不同平台的播放事件不统一，用户界面记录“最近打开的播放器”。

## 发布、暂停与恢复

PR 自动构建并验证旧 URL、内部链接、锚点、H1、canonical、索引与 Sitemap。合并 main 后部署 dist。Actions → Build and deploy OpenDTV 可查看 build、deploy 和 github-pages 环境地址。手动 Run workflow 可执行外部核验、候选获取与重新部署。在线检查首页、/videos/、/search/?q=上海 与任一详情页。

只暂停采集时移除 YOUTUBE_API_KEY 或停用 Collect pending videos 步骤。只暂停每日任务时从工作流移除 schedule，保留 push。回退时用 git revert 回退有问题的合并提交并重新构建，通过 PR 发布，不改写历史。若单片失效，优先归档单条记录。

## 托管与平台条款

独立编辑型门户使用 GitHub Pages。GitHub Pages 对发布体积、带宽和以商业交易为主要目的的站点有限制，若未来加入收费业务需重新评估。仅加载官方播放器，不覆盖控件、广告或品牌。上线新来源前核对其条款、嵌入方式和地域限制。

- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- https://developers.google.com/youtube/terms/developer-policies
- https://developers.google.com/youtube/v3/determine_quota_cost
- https://vimeo.com/terms
