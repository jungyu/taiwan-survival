#!/usr/bin/env python3
"""
Markdown 格式修正腳本
用於修正營地管理指南中的格式錯誤
"""

import re
import sys

def fix_markdown_format(content):
    """修正 Markdown 格式錯誤"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i]
        
        # 檢查是否為標題行
        if current_line.startswith('#'):
            # 確保標題前有空行（除非是文件開頭）
            if i > 0 and fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            
            fixed_lines.append(current_line)
            
            # 確保標題後有空行（除非下一行也是標題或文件結尾）
            if i + 1 < len(lines) and lines[i + 1].strip() != '' and not lines[i + 1].startswith('#'):
                fixed_lines.append('')
        
        # 檢查是否為列表項
        elif current_line.strip().startswith(('- ', '* ', '+ ')) or re.match(r'^\s*\d+\.', current_line):
            # 如果前一行不是空行且不是列表項，添加空行
            if (fixed_lines and fixed_lines[-1].strip() != '' and 
                not (fixed_lines[-1].strip().startswith(('- ', '* ', '+ ')) or 
                     re.match(r'^\s*\d+\.', fixed_lines[-1]))):
                fixed_lines.append('')
            
            # 收集連續的列表項
            list_items = []
            while (i < len(lines) and 
                   (lines[i].strip().startswith(('- ', '* ', '+ ')) or 
                    re.match(r'^\s*\d+\.', lines[i]) or
                    lines[i].strip() == '')):
                if lines[i].strip() != '':
                    list_items.append(lines[i])
                i += 1
            
            # 添加列表項
            fixed_lines.extend(list_items)
            
            # 確保列表後有空行（除非下一行是空行或文件結尾）
            if i < len(lines) and lines[i].strip() != '':
                fixed_lines.append('')
            
            i -= 1  # 因為 while 循環會 i += 1
        
        # 檢查是否為代碼區塊開始
        elif current_line.strip().startswith('```'):
            # 確保代碼區塊前有空行
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            
            # 處理代碼區塊
            code_block = [current_line]
            
            # 如果代碼區塊沒有語言標記，添加適當的語言
            if current_line.strip() == '```':
                # 檢查下一行內容來推斷語言
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if any(keyword in next_line for keyword in ['□', '【', '】', '：']):
                        current_line = '```markdown'
                    elif any(keyword in next_line for keyword in ['def ', 'import ', 'class ']):
                        current_line = '```python'
                    elif any(keyword in next_line for keyword in ['function', 'var ', 'let ', 'const ']):
                        current_line = '```javascript'
                    else:
                        current_line = '```text'
                code_block[0] = current_line
            
            i += 1
            # 收集代碼區塊內容直到結束
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_block.append(lines[i])
                i += 1
            
            # 添加結束標記
            if i < len(lines):
                code_block.append(lines[i])
            
            fixed_lines.extend(code_block)
            
            # 確保代碼區塊後有空行
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                fixed_lines.append('')
        
        else:
            fixed_lines.append(current_line)
        
        i += 1
    
    return '\n'.join(fixed_lines)

def main():
    """主函數"""
    if len(sys.argv) != 2:
        print("用法: python utils/fix_markdown.py <markdown文件路徑>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        # 讀取檔案
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修正格式
        fixed_content = fix_markdown_format(content)
        
        # 寫回檔案
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"已成功修正 {file_path} 的格式")
        
    except Exception as e:
        print(f"錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
