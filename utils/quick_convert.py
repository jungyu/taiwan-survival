#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速 ODS 轉 CSV 轉換器
提供簡單的選單介面
"""

from .ods_to_csv_converter import ods_to_csv, batch_convert
import os
import glob

def find_ods_files():
    """尋找所有 ODS 檔案"""
    ods_files = []
    
    # 搜尋所有目錄中的 ODS 檔案
    for root, dirs, files in os.walk("原始資料"):
        for file in files:
            if file.endswith('.ods'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path)
                file_size = os.path.getsize(full_path)
                ods_files.append((rel_path, file_size))
    
    return ods_files

def show_menu():
    """顯示選單"""
    print("\n" + "="*60)
    print("ODS 轉 CSV 快速轉換器")
    print("="*60)
    
    ods_files = find_ods_files()
    
    if not ods_files:
        print("❌ 沒有找到任何 ODS 檔案")
        return
    
    print(f"📁 找到 {len(ods_files)} 個 ODS 檔案:")
    print("-" * 60)
    
    for i, (file_path, file_size) in enumerate(ods_files, 1):
        size_mb = file_size / (1024 * 1024)
        print(f"{i:2d}. {file_path} ({size_mb:.1f} MB)")
    
    print("-" * 60)
    print("選項:")
    print(" 0. 批次轉換所有檔案")
    print(" 1-{}. 轉換單一檔案".format(len(ods_files)))
    print(" q. 退出")
    
    return ods_files

def convert_single_file(file_path):
    """轉換單一檔案"""
    print(f"\n🔄 正在轉換: {file_path}")
    
    # 嘗試不同的跳過行數
    skip_options = [0, 1, 2, 3, 4]
    
    for skip_rows in skip_options:
        try:
            result = ods_to_csv(file_path, skip_rows=skip_rows)
            if result:
                print(f"✅ 轉換成功！跳過 {skip_rows} 行標題")
                return True
        except Exception as e:
            continue
    
    print("❌ 轉換失敗")
    return False

def convert_all_files():
    """批次轉換所有檔案"""
    print("\n🔄 正在批次轉換所有 ODS 檔案...")
    
    # 按目錄分組轉換
    directories = set()
    for root, dirs, files in os.walk("原始資料"):
        for file in files:
            if file.endswith('.ods'):
                directories.add(root)
                break
    
    total_success = 0
    total_files = 0
    
    for directory in sorted(directories):
        ods_files = glob.glob(os.path.join(directory, "*.ods"))
        if ods_files:
            print(f"\n📁 處理目錄: {directory}")
            success_count = 0
            for ods_file in ods_files:
                try:
                    result = ods_to_csv(ods_file, skip_rows=3)
                    if result:
                        success_count += 1
                except Exception as e:
                    print(f"❌ 轉換失敗: {os.path.basename(ods_file)}")
            
            total_success += success_count
            total_files += len(ods_files)
            print(f"✅ 目錄完成: {success_count}/{len(ods_files)} 個檔案")
    
    print(f"\n🎉 批次轉換完成！總計: {total_success}/{total_files} 個檔案")

def main():
    """主程式"""
    while True:
        ods_files = show_menu()
        
        if not ods_files:
            break
        
        choice = input("\n請選擇選項: ").strip().lower()
        
        if choice == 'q':
            print("👋 再見！")
            break
        elif choice == '0':
            convert_all_files()
        elif choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(ods_files):
                file_path = ods_files[index][0]
                convert_single_file(file_path)
            else:
                print("❌ 無效的選項")
        else:
            print("❌ 無效的選項")

if __name__ == "__main__":
    main() 