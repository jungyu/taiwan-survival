#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 ODS 轉 CSV 轉換器
"""

from .ods_to_csv_converter import ods_to_csv, batch_convert
import os

def test_single_file_conversion():
    """測試單一檔案轉換"""
    print("=== 測試單一檔案轉換 ===")
    
    input_file = "原始資料/宮廟、宗教/宗教團體查詢_全國性.ods"
    
    if os.path.exists(input_file):
        # 基本轉換
        print("1. 基本轉換（跳過 3 行標題）")
        result = ods_to_csv(input_file, skip_rows=3)
        print(f"結果: {result}\n")
        
        # 指定輸出檔案
        print("2. 指定輸出檔案")
        result = ods_to_csv(input_file, "test_output.csv", skip_rows=3)
        print(f"結果: {result}\n")
        
        # 清理測試檔案
        if os.path.exists("test_output.csv"):
            os.remove("test_output.csv")
            print("已清理測試檔案\n")
    else:
        print(f"測試檔案不存在: {input_file}\n")

def test_batch_conversion():
    """測試批次轉換"""
    print("=== 測試批次轉換 ===")
    
    input_dir = "原始資料/宮廟、宗教/"
    
    if os.path.exists(input_dir):
        print("批次轉換宮廟、宗教目錄中的 ODS 檔案")
        batch_convert(input_dir, pattern="*.ods")
        print()
    else:
        print(f"測試目錄不存在: {input_dir}\n")

def show_available_files():
    """顯示可用的 ODS 檔案"""
    print("=== 可用的 ODS 檔案 ===")
    
    religious_dir = "原始資料/宮廟、宗教/"
    if os.path.exists(religious_dir):
        ods_files = [f for f in os.listdir(religious_dir) if f.endswith('.ods')]
        print(f"在 {religious_dir} 中找到的 ODS 檔案:")
        for i, file in enumerate(ods_files, 1):
            file_path = os.path.join(religious_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"{i}. {file} ({file_size:,} bytes)")
        print()
    
    # 檢查其他目錄
    other_dirs = ["原始資料/防空疏散避難設施/", "原始資料/露營場地/", "原始資料/車泊/"]
    for dir_path in other_dirs:
        if os.path.exists(dir_path):
            ods_files = [f for f in os.listdir(dir_path) if f.endswith('.ods')]
            if ods_files:
                print(f"在 {dir_path} 中找到的 ODS 檔案:")
                for i, file in enumerate(ods_files, 1):
                    file_path = os.path.join(dir_path, file)
                    file_size = os.path.getsize(file_path)
                    print(f"{i}. {file} ({file_size:,} bytes)")
                print()

def main():
    """主測試函數"""
    print("ODS 轉 CSV 轉換器測試")
    print("=" * 50)
    
    # 顯示可用檔案
    show_available_files()
    
    # 測試單一檔案轉換
    test_single_file_conversion()
    
    # 測試批次轉換
    test_batch_conversion()
    
    print("測試完成！")
    print("\n使用說明:")
    print("1. 單一檔案轉換: python ods_to_csv_converter.py <檔案路徑>")
    print("2. 批次轉換: python ods_to_csv_converter.py <目錄路徑> -b")
    print("3. 跳過標題行: python ods_to_csv_converter.py <檔案路徑> --skip-rows <行數>")

if __name__ == "__main__":
    main() 