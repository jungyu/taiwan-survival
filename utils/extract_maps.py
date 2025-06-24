#!/usr/bin/env python3
"""
從 Google Maps 短連結提取露營場地資料並轉換為 CSV

這個腳本會：
1. 解析 Google Maps 短連結
2. 提取地圖中的地點資料
3. 轉換為 CSV 格式
"""

import requests
import csv
import re
import time
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import json

# Google Maps 短連結列表
GOOGLE_MAPS_LINKS = [
    {"name": "雨棚主題露營區清單", "url": "https://goo.gl/maps/LPeF64hoG1dzQDdn8"},
    {"name": "雲海主題露營區google地圖清單", "url": "https://goo.gl/maps/pioA9sjczkV3hyff9"},
    {"name": "露營區google地圖清單1~500", "url": "https://goo.gl/maps/trwRYT8giNdQ1XFG9"},
    {"name": "露營區google地圖清單501~999", "url": "https://goo.gl/maps/ScRptYLYeaPGkdvb6"},
    {"name": "野營泊點google地圖清單1~500", "url": "https://goo.gl/maps/ZpieCz1KC7ynWooe7"},
    {"name": "野營泊點google地圖清單501~999", "url": "https://goo.gl/maps/QiFbKZTRxqyTmkev9"},
    {"name": "真車宿阿翔-車宿泊點地圖", "url": "https://goo.gl/maps/wYMpRZteqsGUnihs5"}
]

def resolve_short_url(short_url):
    """解析短連結，獲取實際的 Google Maps URL"""
    try:
        response = requests.get(short_url, allow_redirects=True)
        return response.url
    except Exception as e:
        print(f"解析短連結失敗 {short_url}: {e}")
        return None

def extract_place_data_from_html(html_content):
    """從 HTML 內容中提取地點資料"""
    places = []
    
    try:
        # 尋找 JSON 資料
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 嘗試從各種可能的 script 標籤中提取資料
        scripts = soup.find_all('script')
        
        for script in scripts:
            if script.string and 'window.APP_INITIALIZATION_STATE' in script.string:
                # 解析 Google Maps 的初始化資料
                content = script.string
                # 這裡需要進一步解析 Google Maps 的內部資料結構
                # 由於 Google Maps 的資料結構複雜，我們使用簡化的方法
                pass
        
        # 備用方法：尋找地點名稱和座標的模式
        # 這是一個簡化的實作，實際上 Google Maps 的資料結構更複雜
        
    except Exception as e:
        print(f"解析 HTML 內容失敗: {e}")
    
    return places

def download_and_parse_map(map_info):
    """下載並解析單個地圖"""
    print(f"處理: {map_info['name']}")
    
    # 解析短連結
    real_url = resolve_short_url(map_info['url'])
    if not real_url:
        return []
    
    print(f"實際 URL: {real_url}")
    
    # 下載頁面內容
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(real_url, headers=headers)
        response.raise_for_status()
        
        # 儲存原始 HTML 用於除錯
        with open(f"debug_{map_info['name'].replace(' ', '_')}.html", 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # 提取地點資料
        places = extract_place_data_from_html(response.text)
        
        return places
        
    except Exception as e:
        print(f"下載地圖失敗 {real_url}: {e}")
        return []

def save_to_csv(all_places, filename):
    """將所有地點資料儲存為 CSV"""
    if not all_places:
        print("沒有找到任何地點資料")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['名稱', '地址', '緯度', '經度', '類型', '來源地圖']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for place in all_places:
            writer.writerow(place)
    
    print(f"已儲存 {len(all_places)} 個地點到 {filename}")

def main():
    """主函數"""
    print("開始下載和解析 Google Maps 資料...")
    
    all_places = []
    
    for map_info in GOOGLE_MAPS_LINKS:
        places = download_and_parse_map(map_info)
        
        # 為每個地點添加來源資訊
        for place in places:
            place['來源地圖'] = map_info['name']
        
        all_places.extend(places)
        
        # 避免過於頻繁的請求
        time.sleep(2)
    
    # 儲存為 CSV
    save_to_csv(all_places, 'camping_locations.csv')
    
    print("處理完成！")

if __name__ == "__main__":
    main()
