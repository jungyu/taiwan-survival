#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV 檔案清理器
清理 CSV 檔案中的空白字元、欄位名稱等問題
"""

import pandas as pd
import os
import sys
import re
from pathlib import Path
import argparse
import unicodedata


def strip_and_normalize_whitespace(val):
    if pd.isna(val):
        return val
    s = str(val)
    # 正規化全形空白與所有 unicode 空白
    s = unicodedata.normalize('NFKC', s)
    # 將所有 unicode 空白（包含全形、tab、zero-width、換行等）都轉成半形空白
    s = re.sub(r'[\s\u3000\u00A0\u2000-\u200B\u202F\u205F\u3000]+', ' ', s)
    # 去除前後空白
    s = s.strip()
    # 將多個空白合併為一個
    s = re.sub(r' +', ' ', s)
    return s


def clean_csv_data(input_file, output_file=None, encoding='utf-8-sig'):
    """
    清理 CSV 檔案中的空白字元
    
    Args:
        input_file (str): 輸入的 CSV 檔案路徑
        output_file (str): 輸出的 CSV 檔案路徑，如果為 None 則自動生成
        encoding (str): CSV 檔案的編碼格式
    
    Returns:
        str: 輸出的 CSV 檔案路徑
    """
    try:
        # 檢查輸入檔案是否存在
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"找不到檔案: {input_file}")
        
        print(f"正在讀取 CSV 檔案: {input_file}")
        
        # 讀取 CSV 檔案
        df = pd.read_csv(input_file, encoding=encoding)
        
        print(f"原始資料: {len(df)} 行, {len(df.columns)} 欄")
        
        # 清理欄位名稱
        print("正在清理欄位名稱...")
        original_columns = df.columns.tolist()
        
        # 徹底正規化所有空白
        df.columns = [strip_and_normalize_whitespace(col) if isinstance(col, str) else str(col).strip() for col in df.columns]
        
        # 移除欄位名稱中的特殊字元
        df.columns = [re.sub(r'[^\w\s\u4e00-\u9fff]', '', col) for col in df.columns]
        
        # 如果欄位名稱為空，給予預設名稱
        for i, col in enumerate(df.columns):
            if not col or col.isspace():
                df.columns.values[i] = f'Column_{i+1}'
        
        print("欄位名稱清理完成")
        
        # 清理資料內容
        print("正在清理資料內容...")
        
        # 對所有字串欄位進行清理
        for col in df.columns:
            if df[col].dtype == 'object':  # 字串欄位
                # 徹底正規化所有空白
                df[col] = df[col].apply(strip_and_normalize_whitespace)
                # 將 'nan' 字串替換為空值
                df[col] = df[col].replace('nan', '')
                df[col] = df[col].replace('None', '')
                # 將空字串替換為空值
                df[col] = df[col].replace('', pd.NA)
        
        # 移除完全空白的行
        df = df.dropna(how='all')
        
        # 移除完全空白的欄位
        df = df.dropna(axis=1, how='all')
        
        print("資料內容清理完成")
        
        # 如果沒有指定輸出檔案名稱，則自動生成
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.with_name(f"{input_path.stem}_cleaned.csv")
        
        # 將清理後的資料寫入 CSV 檔案
        print(f"正在寫入清理後的 CSV 檔案: {output_file}")
        df.to_csv(output_file, index=False, encoding=encoding)
        
        print(f"清理完成！")
        print(f"輸入檔案: {input_file}")
        print(f"輸出檔案: {output_file}")
        print(f"清理後資料: {len(df)} 行, {len(df.columns)} 欄")
        
        # 顯示欄位名稱對比
        print("\n欄位名稱對比:")
        print("-" * 80)
        for i, (orig, new) in enumerate(zip(original_columns, df.columns)):
            if orig != new:
                print(f"{i+1:2d}. '{orig}' → '{new}'")
        
        return str(output_file)
        
    except Exception as e:
        print(f"清理失敗: {str(e)}")
        return None


def batch_clean_csv(input_directory, output_directory=None, pattern="*.csv", replace=False):
    """
    批次清理目錄中的所有 CSV 檔案
    
    Args:
        input_directory (str): 輸入目錄路徑
        output_directory (str): 輸出目錄路徑，如果為 None 則使用輸入目錄
        pattern (str): 檔案匹配模式
        replace (bool): 是否將 *_cleaned.csv 覆蓋原始 .csv，並將原始檔案改名為 *_raw.csv
    """
    input_path = Path(input_directory)
    
    if not input_path.exists():
        print(f"目錄不存在: {input_directory}")
        return
    
    if output_directory:
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
    
    # 遞迴尋找所有符合模式的 CSV 檔案
    csv_files = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith('.csv') and not file.endswith('_cleaned.csv'):
                csv_files.append(Path(root) / file)
    
    if not csv_files:
        print(f"在目錄 {input_directory} 中找不到 CSV 檔案")
        return
    
    print(f"找到 {len(csv_files)} 個 CSV 檔案")
    
    success_count = 0
    for csv_file in csv_files:
        print(f"\n處理檔案: {csv_file.name}")
        
        if output_directory:
            cleaned_file = output_path / f"{csv_file.stem}_cleaned.csv"
        else:
            cleaned_file = csv_file.with_name(f"{csv_file.stem}_cleaned.csv")
        
        result = clean_csv_data(str(csv_file), str(cleaned_file))
        if result:
            success_count += 1
            if replace and result:
                import shutil
                raw = str(csv_file).replace('.csv', '_raw.csv')
                shutil.move(str(csv_file), raw)
                shutil.copy(result, str(csv_file))
                print(f"已用 {result} 覆蓋 {csv_file}，原始檔案改名為 {raw}")
    
    print(f"\n批次清理完成！成功清理 {success_count}/{len(csv_files)} 個檔案")


def preview_csv_issues(input_file, encoding='utf-8-sig'):
    """
    預覽 CSV 檔案的問題
    
    Args:
        input_file (str): 輸入的 CSV 檔案路徑
        encoding (str): CSV 檔案的編碼格式
    """
    try:
        if not os.path.exists(input_file):
            print(f"檔案不存在: {input_file}")
            return
        
        print(f"預覽檔案: {input_file}")
        print("=" * 60)
        
        # 讀取 CSV 檔案
        df = pd.read_csv(input_file, encoding=encoding)
        
        print(f"檔案大小: {len(df)} 行, {len(df.columns)} 欄")
        print()
        
        # 檢查欄位名稱問題
        print("欄位名稱問題:")
        print("-" * 40)
        for i, col in enumerate(df.columns):
            original_col = col
            if isinstance(col, str):
                stripped_col = col.strip()
                if col != stripped_col:
                    print(f"欄位 {i+1}: 前後有空白字元")
                    print(f"  原始: '{col}'")
                    print(f"  清理後: '{stripped_col}'")
                    print()
        
        # 檢查資料內容問題
        print("資料內容問題:")
        print("-" * 40)
        
        # 檢查空白行
        empty_rows = df.isna().all(axis=1).sum()
        if empty_rows > 0:
            print(f"發現 {empty_rows} 個完全空白的行")
        
        # 檢查空白欄位
        empty_cols = df.isna().all(axis=0).sum()
        if empty_cols > 0:
            print(f"發現 {empty_cols} 個完全空白的欄位")
        
        # 檢查多餘空白字元
        whitespace_count = 0
        for col in df.columns:
            if df[col].dtype == 'object':
                # 檢查前後空白
                has_leading_trailing = df[col].astype(str).str.match(r'^\s+|\s+$').sum()
                if has_leading_trailing > 0:
                    print(f"欄位 '{col}': {has_leading_trailing} 個值有前後空白")
                    whitespace_count += has_leading_trailing
                
                # 檢查多個連續空白
                has_multiple_spaces = df[col].astype(str).str.contains(r'\s{2,}').sum()
                if has_multiple_spaces > 0:
                    print(f"欄位 '{col}': {has_multiple_spaces} 個值有多個連續空白")
                    whitespace_count += has_multiple_spaces
        
        if whitespace_count == 0:
            print("未發現空白字元問題")
        
        print()
        print("建議執行清理程式來修復這些問題")
        
    except Exception as e:
        print(f"預覽失敗: {str(e)}")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(description='CSV 檔案清理器')
    parser.add_argument('input', help='輸入的 CSV 檔案或目錄路徑')
    parser.add_argument('-o', '--output', help='輸出的 CSV 檔案路徑')
    parser.add_argument('-d', '--directory', help='輸出目錄路徑（用於批次清理）')
    parser.add_argument('-e', '--encoding', default='utf-8-sig', help='CSV 編碼格式')
    parser.add_argument('-b', '--batch', action='store_true', help='批次清理模式')
    parser.add_argument('-p', '--pattern', default='*.csv', help='檔案匹配模式（預設: *.csv）')
    parser.add_argument('--preview', action='store_true', help='預覽清理效果，不寫入檔案')
    parser.add_argument('--replace', action='store_true', help='將 *_cleaned.csv 覆蓋原始 .csv，並將原始檔案改名為 *_raw.csv')
    
    args = parser.parse_args()
    
    # 檢查輸入路徑
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"錯誤: 路徑不存在 - {args.input}")
        sys.exit(1)
    
    if args.preview:
        # 預覽模式
        if input_path.is_file():
            preview_csv_issues(str(input_path), args.encoding)
        else:
            print("預覽模式僅支援單一檔案")
    elif args.batch or input_path.is_dir():
        # 批次清理模式
        batch_clean_csv(str(input_path), args.directory, args.pattern, args.replace)
    else:
        # 單一檔案清理模式
        output_file = args.output
        cleaned_path = clean_csv_data(str(input_path), output_file=output_file, encoding=args.encoding)
        if args.replace and cleaned_path:
            import shutil
            orig = str(input_path)
            raw = orig.replace('.csv', '_raw.csv')
            shutil.move(orig, raw)
            shutil.copy(cleaned_path, orig)
            print(f"已用 {cleaned_path} 覆蓋 {orig}，原始檔案改名為 {raw}")


if __name__ == "__main__":
    # 如果沒有命令列參數，提供互動式介面
    if len(sys.argv) == 1:
        print("CSV 檔案清理器")
        print("=" * 50)
        
        # 範例：清理宗教團體查詢檔案
        input_file = "原始資料/宮廟、宗教/宗教團體查詢_全國性.csv"
        
        if os.path.exists(input_file):
            print(f"發現範例檔案: {input_file}")
            print("\n選項:")
            print("1. 預覽檔案問題")
            print("2. 清理檔案")
            print("3. 批次清理所有 CSV 檔案")
            
            choice = input("\n請選擇選項 (1-3): ").strip()
            
            if choice == '1':
                preview_csv_issues(input_file)
            elif choice == '2':
                clean_csv_data(input_file)
            elif choice == '3':
                batch_clean_csv("原始資料/", pattern="*.csv")
            else:
                print("無效選項")
        else:
            print("請使用命令列參數來指定要清理的檔案")
            print("\n使用範例:")
            print("  python csv_cleaner.py 原始資料/宮廟、宗教/宗教團體查詢_全國性.csv")
            print("  python csv_cleaner.py 原始資料/宮廟、宗教/宗教團體查詢_全國性.csv --preview")
            print("  python csv_cleaner.py 原始資料/ -b")
    else:
        main() 