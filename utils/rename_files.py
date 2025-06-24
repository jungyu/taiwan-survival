#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import re
from pathlib import Path

def get_location_from_csv(file_path):
    """從CSV檔案中提取縣市資訊"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # 讀取標題行
            for i, row in enumerate(reader):
                if i > 5:  # 只檢查前5行數據
                    break
                
                # 檢查地址欄位
                for cell in row:
                    if '縣' in cell or '市' in cell:
                        # 提取縣市名稱
                        match = re.search(r'(台北市|新北市|桃園市|台中市|台南市|高雄市|基隆市|新竹市|嘉義市|新竹縣|苗栗縣|彰化縣|南投縣|雲林縣|嘉義縣|屏東縣|宜蘭縣|花蓮縣|台東縣|澎湖縣|金門縣|連江縣|臺北市|臺中市|臺南市|臺東縣)', cell)
                        if match:
                            county = match.group(1)
                            # 標準化縣市名稱
                            county = county.replace('台', '臺')
                            
                            # 檢查是否有區域資訊
                            area_match = re.search(r'(臺北市|新北市|桃園市|臺中市|臺南市|高雄市|基隆市|新竹市|嘉義市)([^縣市區]+區)', cell)
                            if area_match:
                                return f"{area_match.group(1)}{area_match.group(2)}"
                            
                            return county
                
                # 檢查轄管分局欄位
                if len(row) > 8 and '分局' in str(row[8]):
                    station = str(row[8])
                    # 根據分局名稱推斷縣市
                    if '鼓山分局' in station or '鹽埕分局' in station or '岡山分局' in station or '楠梓分局' in station or '六龜分局' in station:
                        return "高雄市"
                    elif '花蓮分局' in station:
                        return "花蓮縣"
                    elif '臺東分局' in station:
                        return "臺東縣"
                    # 可以繼續添加更多分局對應關係
        
        return None
    except Exception:
        return None

def main():
    folder_path = Path(".")
    
    # 需要重新命名的檔案清單（GUID格式的檔案）
    guid_files = [f for f in os.listdir(folder_path) if re.match(r'^[a-f0-9-]{36}\.csv$', f)]
    
    for file_name in guid_files:
        file_path = folder_path / file_name
        location = get_location_from_csv(file_path)
        
        if location:
            new_name = f"{location}_防空疏散避難設施.csv"
            new_path = folder_path / new_name
            
            # 避免檔案名稱衝突
            counter = 1
            while new_path.exists():
                new_name = f"{location}_{counter}_防空疏散避難設施.csv"
                new_path = folder_path / new_name
                counter += 1
            
            print(f"重新命名: {file_name} -> {new_name}")
            file_path.rename(new_path)
        else:
            print(f"無法識別地區: {file_name}")

if __name__ == "__main__":
    main()
