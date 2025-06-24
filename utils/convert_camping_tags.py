#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
車泊地點標籤分析和分類工具
從車泊地點CSV檔案中解析括號內的服務和設施標籤，
並將其分類以便於建立離線地圖的標記系統。
"""

import csv
import re
import json
from collections import defaultdict, Counter
from pathlib import Path


class CampingTagAnalyzer:
    """車泊地點標籤分析器"""
    
    def __init__(self):
        # 定義標籤分類規則
        self.tag_categories = {
            'facilities': {  # 設施類
                'name': '設施服務',
                'keywords': ['淋浴', '住宿', '用餐', '民宿', '雅房', '棧點', '澡點'],
                'tags': set()
            },
            'camping_types': {  # 露營類型
                'name': '露營類型',
                'keywords': ['車泊', '搭帳', '小帳', '帳', '搭小帳', '背包客'],
                'tags': set()
            },
            'business_hours': {  # 營業時間
                'name': '營業時間',
                'keywords': ['特約平日', '週日到週四', '週日到週五', '全年', '無季節'],
                'tags': set()
            },
            'discounts': {  # 優惠折扣
                'name': '優惠折扣',
                'keywords': ['憑卡', '九折', '9折', '優惠', '折扣', '送', '免費'],
                'tags': set()
            },
            'products': {  # 商品服務
                'name': '商品服務',
                'keywords': ['農產品', '漁產品', '伴手禮', '食材', '戶外用品', '保修'],
                'tags': set()
            },
            'restrictions': {  # 限制條件
                'name': '限制條件',
                'keywords': ['僅', '只收', '無', '限'],
                'tags': set()
            },
            'contact': {  # 聯絡資訊
                'name': '聯絡資訊',
                'keywords': ['申請', '辦卡', '預訂', '團卡'],
                'tags': set()
            },
            'other': {  # 其他
                'name': '其他',
                'keywords': [],
                'tags': set()
            }
        }
        
        # 標籤統計
        self.tag_stats = Counter()
        self.all_tags = set()
        
    def extract_tags_from_text(self, text):
        """從文字中提取括號內的標籤"""
        if not text:
            return []
        
        # 尋找所有括號內容
        pattern = r'\(([^)]*)\)'
        matches = re.findall(pattern, text)
        
        tags = []
        for match in matches:
            # 分割逗號分隔的標籤
            tag_list = [tag.strip() for tag in match.split(',') if tag.strip()]
            tags.extend(tag_list)
        
        return tags
    
    def categorize_tag(self, tag):
        """將標籤分類到對應類別"""
        tag_lower = tag.lower()
        
        for category_id, category_info in self.tag_categories.items():
            for keyword in category_info['keywords']:
                if keyword in tag_lower:
                    return category_id
        
        return 'other'
    
    def analyze_csv(self, csv_file_path):
        """分析CSV檔案中的標籤"""
        results = []
        
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_idx, row in enumerate(reader, 1):
                name = row.get('名稱', '').strip()
                lat = row.get('緯度', '').strip()
                lon = row.get('經度', '').strip()
                
                # 從名稱中提取標籤
                tags = self.extract_tags_from_text(name)
                
                if tags:
                    # 統計標籤出現次數
                    for tag in tags:
                        self.tag_stats[tag] += 1
                        self.all_tags.add(tag)
                    
                    # 分類標籤
                    categorized_tags = defaultdict(list)
                    for tag in tags:
                        category = self.categorize_tag(tag)
                        categorized_tags[category].append(tag)
                        self.tag_categories[category]['tags'].add(tag)
                    
                    # 清理地點名稱（移除括號內容）
                    clean_name = re.sub(r'\([^)]*\)', '', name).strip()
                    
                    result = {
                        'id': row_idx,
                        'name': clean_name,
                        'original_name': name,
                        'latitude': lat,
                        'longitude': lon,
                        'raw_tags': tags,
                        'categorized_tags': dict(categorized_tags),
                        'category_count': len(categorized_tags)
                    }
                    
                    results.append(result)
        
        return results
    
    def generate_tag_mapping(self):
        """生成標籤對應表"""
        mapping = {}
        
        for category_id, category_info in self.tag_categories.items():
            if category_info['tags']:
                mapping[category_id] = {
                    'name': category_info['name'],
                    'tags': sorted(list(category_info['tags']))
                }
        
        return mapping
    
    def generate_leaflet_markers(self, analyzed_data):
        """生成 Leaflet 地圖標記配置"""
        markers = []
        
        # 定義分類顏色
        category_colors = {
            'facilities': '#2E8B57',      # 海綠色 - 設施服務
            'camping_types': '#FF6347',   # 番茄紅 - 露營類型
            'business_hours': '#4682B4',  # 鋼藍色 - 營業時間
            'discounts': '#FFD700',       # 金色 - 優惠折扣
            'products': '#9370DB',        # 中紫色 - 商品服務
            'restrictions': '#DC143C',    # 深紅色 - 限制條件
            'contact': '#20B2AA',         # 淺海綠 - 聯絡資訊
            'other': '#708090'            # 石板灰 - 其他
        }
        
        for item in analyzed_data:
            if not item['latitude'] or not item['longitude']:
                continue
                
            try:
                lat = float(item['latitude'])
                lon = float(item['longitude'])
            except (ValueError, TypeError):
                continue
            
            # 決定主要分類（取標籤最多的分類）
            main_category = 'other'
            max_tags = 0
            
            for category, tags in item['categorized_tags'].items():
                if len(tags) > max_tags:
                    max_tags = len(tags)
                    main_category = category
            
            # 生成標記
            marker = {
                'id': item['id'],
                'name': item['name'],
                'lat': lat,
                'lng': lon,
                'category': main_category,
                'color': category_colors.get(main_category, '#708090'),
                'tags': item['raw_tags'],
                'categorized_tags': item['categorized_tags'],
                'popup_content': self.generate_popup_content(item)
            }
            
            markers.append(marker)
        
        return markers
    
    def generate_popup_content(self, item):
        """生成地圖彈出視窗內容"""
        content = f"<b>{item['name']}</b><br>"
        
        if item['categorized_tags']:
            content += "<br><b>服務設施：</b><br>"
            for category, tags in item['categorized_tags'].items():
                if tags:
                    category_name = self.tag_categories[category]['name']
                    content += f"• {category_name}: {', '.join(tags)}<br>"
        
        return content
    
    def save_results(self, analyzed_data, output_dir='output'):
        """儲存分析結果"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 1. 詳細分析結果
        with open(output_path / 'camping_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analyzed_data, f, ensure_ascii=False, indent=2)
        
        # 2. 標籤分類對應表
        tag_mapping = self.generate_tag_mapping()
        with open(output_path / 'tag_categories.json', 'w', encoding='utf-8') as f:
            json.dump(tag_mapping, f, ensure_ascii=False, indent=2)
        
        # 3. 標籤統計
        tag_statistics = {
            'total_unique_tags': len(self.all_tags),
            'most_common_tags': dict(self.tag_stats.most_common(50)),
            'category_distribution': {
                cat_id: len(cat_info['tags']) 
                for cat_id, cat_info in self.tag_categories.items() 
                if cat_info['tags']
            }
        }
        
        with open(output_path / 'tag_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(tag_statistics, f, ensure_ascii=False, indent=2)
        
        # 4. Leaflet 地圖標記
        markers = self.generate_leaflet_markers(analyzed_data)
        with open(output_path / 'leaflet_markers.json', 'w', encoding='utf-8') as f:
            json.dump(markers, f, ensure_ascii=False, indent=2)
        
        # 5. 清理後的CSV（移除標籤，加入分類）
        with open(output_path / 'camping_locations_clean.csv', 'w', newline='', encoding='utf-8') as f:
            if analyzed_data:
                fieldnames = ['id', 'name', 'latitude', 'longitude', 'main_category', 'tags', 'facilities', 'camping_types', 'discounts']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in analyzed_data:
                    # 決定主要分類
                    main_category = 'other'
                    max_tags = 0
                    for category, tags in item['categorized_tags'].items():
                        if len(tags) > max_tags:
                            max_tags = len(tags)
                            main_category = category
                    
                    writer.writerow({
                        'id': item['id'],
                        'name': item['name'],
                        'latitude': item['latitude'],
                        'longitude': item['longitude'],
                        'main_category': main_category,
                        'tags': '|'.join(item['raw_tags']),
                        'facilities': '|'.join(item['categorized_tags'].get('facilities', [])),
                        'camping_types': '|'.join(item['categorized_tags'].get('camping_types', [])),
                        'discounts': '|'.join(item['categorized_tags'].get('discounts', []))
                    })
        
        return output_path


def main():
    """主程式"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python3 convert_camping_tags.py <CSV檔案路徑> [輸出目錄]")
        print("範例: python3 convert_camping_tags.py ../原始資料/車泊場地/全國車泊地點.csv")
        return
    
    csv_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'camping_analysis_output'
    
    if not Path(csv_file).exists():
        print(f"錯誤: 找不到檔案 {csv_file}")
        return
    
    print(f"開始分析車泊地點標籤: {csv_file}")
    
    # 創建分析器
    analyzer = CampingTagAnalyzer()
    
    # 分析CSV檔案
    print("正在分析標籤...")
    analyzed_data = analyzer.analyze_csv(csv_file)
    
    # 儲存結果
    print(f"正在儲存結果到: {output_dir}")
    output_path = analyzer.save_results(analyzed_data, output_dir)
    
    # 顯示統計資訊
    print(f"\n=== 分析完成 ===")
    print(f"處理地點數量: {len(analyzed_data)}")
    print(f"發現標籤總數: {len(analyzer.all_tags)}")
    print(f"輸出檔案位置: {output_path}")
    
    print(f"\n=== 標籤分類統計 ===")
    for cat_id, cat_info in analyzer.tag_categories.items():
        if cat_info['tags']:
            print(f"{cat_info['name']}: {len(cat_info['tags'])} 個標籤")
    
    print(f"\n=== 最常見標籤 (前10名) ===")
    for tag, count in analyzer.tag_stats.most_common(10):
        print(f"{tag}: {count} 次")
    
    print(f"\n生成的檔案:")
    print(f"• camping_analysis.json - 詳細分析結果")
    print(f"• tag_categories.json - 標籤分類對應表")
    print(f"• tag_statistics.json - 標籤統計資料")
    print(f"• leaflet_markers.json - Leaflet地圖標記資料")
    print(f"• camping_locations_clean.csv - 清理後的地點資料")


if __name__ == "__main__":
    main()
