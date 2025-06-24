#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批次清理所有 CSV 檔案
"""

from .csv_cleaner import batch_clean_csv
import os

def main():
    """批次清理所有 CSV 檔案"""
    print("CSV 檔案批次清理器")
    print("=" * 50)
    
    # 尋找所有 CSV 檔案
    csv_files = []
    for root, dirs, files in os.walk("原始資料"):
        for file in files:
            if file.endswith('.csv'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path)
                file_size = os.path.getsize(full_path)
                csv_files.append((rel_path, file_size))
    
    if not csv_files:
        print("❌ 沒有找到任何 CSV 檔案")
        return
    
    print(f"找到 {len(csv_files)} 個 CSV 檔案:")
    for i, (file_path, file_size) in enumerate(csv_files, 1):
        print(f"{i:2d}. {file_path} ({file_size:,} bytes)")
    
    print("\n開始批次清理...")
    print("-" * 50)
    
    # 執行批次清理
    batch_clean_csv("原始資料/", pattern="*.csv")
    
    print("\n✅ 批次清理完成！")
    print("\n清理後的檔案:")
    print("-" * 30)
    
    # 顯示清理後的檔案
    cleaned_files = []
    for root, dirs, files in os.walk("原始資料"):
        for file in files:
            if file.endswith('_cleaned.csv'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path)
                file_size = os.path.getsize(full_path)
                cleaned_files.append((rel_path, file_size))
    
    for i, (file_path, file_size) in enumerate(cleaned_files, 1):
        print(f"{i:2d}. {file_path} ({file_size:,} bytes)")

if __name__ == "__main__":
    main() 