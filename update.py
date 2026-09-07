#!/usr/bin/env python3
"""
kr-iptv 数据同步与格式转换脚本
数据源：
- 播放源：https://raw.githubusercontent.com/kenpark76/kenpark76.github.io/main/koreatv.json
- EPG 源：https://raw.githubusercontent.com/kenpark76/kenpark76.github.io/main/koreatvEPG.xml
生成文件：
- kr.m3u：包含 tvg-id、tvg-logo、分组与播放链接的 M3U8 播放列表
- kr.xml：同步最新节目单 EPG
- version.json：版本与更新统计元数据
"""

import json
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

SOURCE_JSON_URL = "https://raw.githubusercontent.com/kenpark76/kenpark76.github.io/main/koreatv.json"
SOURCE_EPG_URL = "https://raw.githubusercontent.com/kenpark76/kenpark76.github.io/main/koreatvEPG.xml"

OUTPUT_M3U_FILE = "kr.m3u"
OUTPUT_XML_FILE = "kr.xml"
OUTPUT_VERSION_FILE = "version.json"

GITHUB_USER = "ykx1817"
GITHUB_REPO = "kr-iptv"
EPG_JSDELIVR_URL = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{GITHUB_REPO}@main/{OUTPUT_XML_FILE}"
EPG_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/{OUTPUT_XML_FILE}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_url(url: str) -> bytes:
    """拉取远程 URL 数据，带超时和请求头"""
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def sync_epg() -> dict:
    """下载并保存 kr.xml，同时解析频道 ID 映射表"""
    print(f"[*] 正在拉取 EPG 数据: {SOURCE_EPG_URL}")
    epg_data = fetch_url(SOURCE_EPG_URL)

    with open(OUTPUT_XML_FILE, "wb") as f:
        f.write(epg_data)
    print(f"[+] EPG 已保存至: {OUTPUT_XML_FILE} ({len(epg_data)} 字节)")

    name_to_id = {}
    try:
        root = ET.fromstring(epg_data)
        for channel in root.findall("channel"):
            channel_id = channel.get("id")
            for display_name in channel.findall("display-name"):
                if display_name.text and channel_id:
                    name_clean = display_name.text.strip()
                    name_to_id[name_clean] = channel_id
                    name_to_id[name_clean.lower().replace(" ", "")] = channel_id
        print(f"[+] 成功从 EPG 中解析出 {len(name_to_id)} 个频道映射条目")
    except Exception as e:
        print(f"[!] 解析 EPG 映射时出现非致命警告: {e}")

    return name_to_id


def generate_m3u(name_to_id: dict):
    """拉取 JSON 并生成 kr.m3u"""
    print(f"[*] 正在拉取频道 JSON 数据: {SOURCE_JSON_URL}")
    raw_json = fetch_url(SOURCE_JSON_URL).decode("utf-8")
    channels = json.loads(raw_json)

    m3u_lines = [
        f'#EXTM3U url-tvg="{EPG_JSDELIVR_URL}" x-tvg-url="{EPG_JSDELIVR_URL}"'
    ]

    matched_count = 0
    total_channels = 0

    for ch in channels:
        name = ch.get("name", "").strip()
        uris = ch.get("uris", [])
        if not name or not uris:
            continue

        url = uris[0].strip()
        logo = ch.get("logo", "").strip()
        group = ch.get("group", "한국-기타").strip()
        headers = ch.get("headers", {})

        # 匹配 EPG channel id
        tvg_id = name_to_id.get(name) or name_to_id.get(name.lower().replace(" ", "")) or name
        if tvg_id != name:
            matched_count += 1

        extinf_parts = [
            f'#EXTINF:-1 tvg-id="{tvg_id}"',
            f'tvg-name="{name}"',
        ]
        if logo:
            extinf_parts.append(f'tvg-logo="{logo}"')
        if group:
            extinf_parts.append(f'group-title="{group}"')

        extinf_line = " ".join(extinf_parts) + f",{name}"
        m3u_lines.append(extinf_line)

        # 携带请求头选项以增强播放器兼容性
        ua = headers.get("user-agent") or headers.get("User-Agent")
        if ua:
            m3u_lines.append(f"#EXTVLCOPT:http-user-agent={ua}")

        m3u_lines.append(url)
        total_channels += 1

    m3u_content = "\n".join(m3u_lines) + "\n"
    with open(OUTPUT_M3U_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"[+] M3U 播放列表已生成: {OUTPUT_M3U_FILE}")
    print(f"[+] 总频道数: {total_channels}，精准匹配 EPG ID 数: {matched_count}")

    # 更新 version.json
    version_info = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "timestamp": int(time.time()),
        "channel_count": total_channels,
        "epg_matched_count": matched_count,
        "source_json": SOURCE_JSON_URL,
        "source_epg": SOURCE_EPG_URL
    }
    with open(OUTPUT_VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(version_info, f, ensure_ascii=False, indent=2)
    print(f"[+] 版本记录已写入: {OUTPUT_VERSION_FILE}")


def main():
    try:
        name_to_id = sync_epg()
        generate_m3u(name_to_id)
        print("\n✅ 所有数据同步完成！")
    except Exception as e:
        print(f"\n❌ 同步失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
