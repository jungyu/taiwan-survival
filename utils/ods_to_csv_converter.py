#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODS 轉 CSV 轉換器
將 ODS 檔案轉換為 CSV 格式
"""

import pandas as pd
import os
import sys
from pathlib import Path
import argparse


def ods_to_csv(input_file, output_file=None, sheet_name=0, encoding='utf-8-sig', skip_rows=0):
    """
    將 ODS 檔案轉換為 CSV 檔案
    
    Args:
        input_file (str): 輸入的 ODS 檔案路徑
        output_file (str): 輸出的 CSV 檔案路徑，如果為 None 則自動生成
        sheet_name: 工作表名稱或索引，預設為第一個工作表
        encoding (str): CSV 檔案的編碼格式，預設為 utf-8-sig (支援中文)
        skip_rows (int): 要跳過的標題行數，預設為 0
    
    Returns:
        str: 輸出的 CSV 檔案路徑
    """
    try:
        # 檢查輸入檔案是否存在
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"找不到檔案: {input_file}")
        
        # 讀取 ODS 檔案
        print(f"正在讀取 ODS 檔案: {input_file}")
        df = pd.read_excel(input_file, sheet_name=sheet_name, engine='odf', skiprows=skip_rows)
        
        # 清理欄位名稱（移除 Unnamed 欄位）
        df.columns = [col if not str(col).startswith('Unnamed:') else f'Column_{i}' for i, col in enumerate(df.columns)]
        
        # 移除完全空白的行
        df = df.dropna(how='all')
        
        # 如果沒有指定輸出檔案名稱，則自動生成
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.with_suffix('.csv')
        
        # 將資料寫入 CSV 檔案
        print(f"正在寫入 CSV 檔案: {output_file}")
        df.to_csv(output_file, index=False, encoding=encoding)
        
        print(f"轉換完成！")
        print(f"輸入檔案: {input_file}")
        print(f"輸出檔案: {output_file}")
        print(f"資料行數: {len(df)}")
        print(f"資料欄數: {len(df.columns)}")
        
        return str(output_file)
        
    except Exception as e:
        print(f"轉換失敗: {str(e)}")
        return None


def batch_convert(input_directory, output_directory=None, pattern="*.ods"):
    """
    批次轉換目錄中的所有 ODS 檔案
    
    Args:
        input_directory (str): 輸入目錄路徑
        output_directory (str): 輸出目錄路徑，如果為 None 則使用輸入目錄
        pattern (str): 檔案匹配模式
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
    
    # 尋找所有符合模式的 ODS 檔案
    ods_files = list(input_path.glob(pattern))
    
    if not ods_files:
        print(f"在目錄 {input_directory} 中找不到 {pattern} 檔案")
        return
    
    print(f"找到 {len(ods_files)} 個 ODS 檔案")
    
    success_count = 0
    for ods_file in ods_files:
        print(f"\n處理檔案: {ods_file.name}")
        
        if output_directory:
            csv_file = output_path / ods_file.with_suffix('.csv').name
        else:
            csv_file = ods_file.with_suffix('.csv')
        
        result = ods_to_csv(str(ods_file), str(csv_file))
        if result:
            success_count += 1
    
    print(f"\n批次轉換完成！成功轉換 {success_count}/{len(ods_files)} 個檔案")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(description='將 ODS 檔案轉換為 CSV 格式')
    parser.add_argument('input', help='輸入的 ODS 檔案或目錄路徑')
    parser.add_argument('-o', '--output', help='輸出的 CSV 檔案路徑')
    parser.add_argument('-d', '--directory', help='輸出目錄路徑（用於批次轉換）')
    parser.add_argument('-s', '--sheet', default=0, help='工作表名稱或索引（預設: 0）')
    parser.add_argument('-e', '--encoding', default='utf-8-sig', help='CSV 編碼格式（預設: utf-8-sig）')
    parser.add_argument('-b', '--batch', action='store_true', help='批次轉換模式')
    parser.add_argument('-p', '--pattern', default='*.ods', help='檔案匹配模式（預設: *.ods）')
    parser.add_argument('--skip-rows', type=int, default=0, help='要跳過的標題行數（預設: 0）')
    
    args = parser.parse_args()
    
    # 檢查輸入路徑
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"錯誤: 路徑不存在 - {args.input}")
        sys.exit(1)
    
    if args.batch or input_path.is_dir():
        # 批次轉換模式
        batch_convert(str(input_path), args.directory, args.pattern)
    else:
        # 單一檔案轉換模式
        result = ods_to_csv(
            str(input_path), 
            args.output, 
            args.sheet, 
            args.encoding,
            args.skip_rows
        )
        
        if not result:
            sys.exit(1)


if __name__ == "__main__":
    # 如果沒有命令列參數，提供互動式介面
    if len(sys.argv) == 1:
        print("ODS 轉 CSV 轉換器")
        print("=" * 50)
        
        # 範例：轉換宗教團體查詢檔案
        input_file = "原始資料/宮廟、宗教/宗教團體查詢_一般寺廟.ods"
        
        if os.path.exists(input_file):
            print(f"發現範例檔案: {input_file}")
            choice = input("是否要轉換這個檔案？(y/n): ").lower().strip()
            
            if choice in ['y', 'yes', '是']:
                ods_to_csv(input_file)
            else:
                print("請使用命令列參數或修改程式碼來指定要轉換的檔案")
        else:
            print("請使用命令列參數來指定要轉換的檔案")
            print("\n使用範例:")
            print("  python ods_to_csv_converter.py 原始資料/宮廟、宗教/宗教團體查詢_一般寺廟.ods")
            print("  python ods_to_csv_converter.py 原始資料/宮廟、宗教/ -b")
    else:
        main() 