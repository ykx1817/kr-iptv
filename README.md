# 📺 kr-iptv

精选韩国 IPTV 直播源与 EPG 节目单自动同步系统。

本项目通过 GitHub Actions 每 4 小时自动从上游数据源拉取最新流媒体地址与电子节目指南（EPG），智能对齐 `tvg-id` 与频道预告，专为 **APTV**、**TiviMate**、**PotPlayer**、**Emby/Jellyfin** 等播放器优化。

---

## 🚀 订阅链接

> 💡 **提示**：M3U 文件头部已内置 EPG 地址，导入支持的播放器（如 APTV）时会自动加载节目预告。

### 1. 国内直连加速源（⚡ 推荐，无需翻墙）
基于 jsDelivr 全球 CDN 加速，国内无需代理即可极速拉取并自动更新：
- **M3U 播放列表**：
  ```text
  https://cdn.jsdelivr.net/gh/ykx1817/kr-iptv@main/kr.m3u
  ```
- **EPG 节目单**：
  ```text
  https://cdn.jsdelivr.net/gh/ykx1817/kr-iptv@main/kr.xml
  ```

---

### 2. 国内镜像加速源（备用，无需翻墙）
基于 GitHub 镜像代理：
- **M3U 播放列表**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/ykx1817/kr-iptv/main/kr.m3u
  ```
- **EPG 节目单**：
  ```text
  https://ghfast.top/https://raw.githubusercontent.com/ykx1817/kr-iptv/main/kr.xml
  ```

---

### 3. GitHub 原生源（适合具备网络环境）
- **M3U 播放列表**：
  ```text
  https://raw.githubusercontent.com/ykx1817/kr-iptv/main/kr.m3u
  ```
- **EPG 节目单**：
  ```text
  https://raw.githubusercontent.com/ykx1817/kr-iptv/main/kr.xml
  ```

---

## ✨ 项目特色

1. **精准 EPG 频道匹配**：
   - 自动解析 XMLTV 中的 Channel ID，并在 M3U 的 `#EXTINF` 标签中注入对应的 `tvg-id`。
   - 彻底解决 APTV / TiviMate 等播放器中因频道名空格或别名导致“无节目信息”的问题。
2. **零依赖与极速同步**：
   - 使用 Python 原生标准库，GitHub Actions 定时自动更新，无缝推送到仓库。
3. **保留必要请求头**：
   - 自动注入 `#EXTVLCOPT:http-user-agent` 等必要 Header，提高部分流媒体的兼容性。

---

## 📱 使用指南

### APTV（iOS / iPadOS / macOS / tvOS）
1. 打开 APTV，点击右上角 **+** 号添加配置。
2. 选择 **添加链接**：
   - **名称**：`Korea TV`
   - **URL**：粘贴上述 **jsDelivr 播放列表链接**
3. 保存后进入播放列表设置，确认 EPG 节目单已自动识别并更新。

### TiviMate / IPTV Smarters (Android TV)
1. 添加 Playlist (M3U)。
2. 填入上述 M3U 订阅 URL。
3. 若需单独配置 EPG，在播放列表设置中的 EPG Sources 填入上述 **kr.xml** 链接即可。

---

## ⚠️ 免责声明
本仓库仅用于个人技术研究与自动化脚本分享，所有流媒体数据均收集同步自公开开源项目（如 kenpark76.github.io）。本项目不提供任何媒体存储或流媒体转码服务，版权归各原版权方所有。
