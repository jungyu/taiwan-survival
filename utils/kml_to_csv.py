#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將 Google My Maps 的 KML 檔案轉換為 CSV 格式
"""

import xml.etree.ElementTree as ET
import csv
import re
import requests
import tempfile
import os

def parse_kml_to_csv(kml_source, csv_file):
    """解析 KML 檔案並轉換為 CSV
    kml_source: KML 檔案路徑或 URL
    """
    
    kml_file = None
    temp_file = False
    
    try:
        # 判斷是 URL 還是檔案路徑
        if kml_source.startswith('http'):
            # 下載 KML 檔案
            print(f"正在下載 KML 檔案: {kml_source}")
            response = requests.get(kml_source)
            response.raise_for_status()
            
            # 建立臨時檔案
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.kml', delete=False, encoding='utf-8') as tmp_file:
                tmp_file.write(response.text)
                kml_file = tmp_file.name
                temp_file = True
        else:
            kml_file = kml_source
        
        # 解析 KML 檔案
        tree = ET.parse(kml_file)
        root = tree.getroot()
        
        # KML 命名空間
        ns = {'kml': 'http://www.opengis.net/kml/2.2'}
        
        # 準備 CSV 資料
        csv_data = []
        headers = ['名稱', '地址', '電腦編號', '建築物名稱', '里別', '緯度', '經度', '避難樓層', '容量', '轄管分局', '備註']
        
        # 找到所有地點標記
        placemarks = root.findall('.//kml:Placemark', ns)
        
        print(f"找到 {len(placemarks)} 個地點標記")
        
        for placemark in placemarks:
            # 取得名稱
            name_elem = placemark.find('kml:name', ns)
            name = name_elem.text if name_elem is not None else ''
            
            # 取得座標
            coord_elem = placemark.find('.//kml:coordinates', ns)
            lat, lon = '', ''
            if coord_elem is not None:
                coords = coord_elem.text.strip().split(',')
                if len(coords) >= 2:
                    lon = coords[0]
                    lat = coords[1]
            
            # 取得詳細資料
            extended_data = {}
            extended_data_elem = placemark.find('kml:ExtendedData', ns)
            if extended_data_elem is not None:
                for data in extended_data_elem.findall('kml:Data', ns):
                    name_attr = data.get('name')
                    value_elem = data.find('kml:value', ns)
                    if name_attr and value_elem is not None:
                        extended_data[name_attr] = value_elem.text if value_elem.text else ''
            
            # 如果沒有 ExtendedData，嘗試從描述中解析
            if not extended_data:
                desc_elem = placemark.find('kml:description', ns)
                if desc_elem is not None and desc_elem.text:
                    # 解析描述中的表格或鍵值對
                    desc_text = desc_elem.text
                    
                    # 嘗試匹配常見的格式
                    patterns = [
                        r'地址[：:]\s*([^\n<]+)',
                        r'電腦編號[：:]\s*([^\n<]+)',
                        r'建築物名稱[：:]\s*([^\n<]+)',
                        r'里別[：:]\s*([^\n<]+)',
                        r'避難樓層[：:]\s*([^\n<]+)',
                        r'地下樓層數[：:]\s*([^\n<]+)',
                        r'容量[：:]\s*([^\n<]+)',
                        r'可容納人數[：:]\s*([^\n<]+)',
                        r'轄管分局[：:]\s*([^\n<]+)',
                        r'備註[：:]\s*([^\n<]+)'
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, desc_text)
                        if match:
                            key = pattern.split('[')[0]
                            extended_data[key] = match.group(1).strip()
            
            # 建立 CSV 行
            row = [
                name,
                extended_data.get('地址', ''),
                extended_data.get('電腦編號', ''),
                extended_data.get('建築物名稱', ''),
                extended_data.get('里別', ''),
                lat,
                lon,
                extended_data.get('避難樓層', extended_data.get('地下樓層數', '')),  # 處理不同的欄位名稱
                extended_data.get('容量', extended_data.get('可容納人數', '')),  # 處理不同的欄位名稱
                extended_data.get('轄管分局', ''),
                extended_data.get('備註', '')
            ]
            
            csv_data.append(row)
        
        # 寫入 CSV 檔案
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(csv_data)
        
        print(f"已將 {len(csv_data)} 筆資料寫入 {csv_file}")
        
    finally:
        # 清理臨時檔案
        if temp_file and kml_file and os.path.exists(kml_file):
            os.unlink(kml_file)

def detect_city_from_url_or_content(url_or_content):
    """從 URL 或內容中偵測縣市名稱"""
    cities = ['基隆市', '台北市', '新北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', 
              '台中市', '彰化縣', '南投縣', '雲林縣', '嘉義市', '嘉義縣', '台南市', 
              '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣', '金門縣', '連江縣']
    
    # 先嘗試從 URL 偵測
    for city in cities:
        if city in url_or_content:
            return city
    
    return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 如果有參數，使用參數作為輸入檔案或 URL
        input_source = sys.argv[1]
        
        # 偵測縣市名稱
        city = detect_city_from_url_or_content(input_source)
        
        if city:
            output_file = f'警政署民防_{city}_防空疏散避難設施.csv'
        else:
            # 如果無法偵測縣市，使用預設名稱
            output_file = '警政署民防_未知縣市_防空疏散避難設施.csv'
        
        # 如果檔案已存在，加上數字後綴
        base_name = output_file.replace('.csv', '')
        counter = 2
        while os.path.exists(output_file):
            output_file = f'{base_name}{counter}_防空疏散避難設施.csv'
            counter += 1
        
        parse_kml_to_csv(input_source, output_file)
    else:
        print("使用方式: python3 kml_to_csv.py <KML檔案路徑或URL>")
