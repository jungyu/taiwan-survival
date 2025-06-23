# 工具程式 Utils

這個資料夾包含專案維護和開發時使用的工具程式。

## 📁 檔案說明

### fix_markdown.py

**功能**：Markdown 格式修正腳本

**用途**：

- 修正 Markdown 檔案的格式錯誤
- 確保標題前後有適當的空行
- 修正列表格式問題
- 為代碼區塊添加適當的語言標記
- 統一格式風格以符合 Markdown lint 規則

**使用方法**：

```bash
python utils/fix_markdown.py <markdown檔案路徑>
```

**範例**：

```bash
# 修正單個檔案
python utils/fix_markdown.py README.md

# 修正特定路徑的檔案
python utils/fix_markdown.py 01_生存必需/01_01_人身安全與威脅應對/戰時生存經驗指南.md
```

**支援功能**：

- 自動檢測並修正標題周圍的空行
- 修正列表項目的格式
- 為空的代碼區塊添加適當的語言標記
- 確保代碼區塊前後有空行
- 處理中文內容的格式問題

## 🛠️ 開發工具建議

### 批次處理所有 Markdown 檔案

如需批次修正所有 Markdown 檔案，可使用以下命令：

```bash
# macOS/Linux
find . -name "*.md" -not -path "./utils/*" -exec python utils/fix_markdown.py {} \;

# 或使用 xargs（效率更高）
find . -name "*.md" -not -path "./utils/*" | xargs -I {} python utils/fix_markdown.py {}
```

### 檢查格式

建議使用 markdownlint 檢查格式：

```bash
# 安裝 markdownlint-cli
npm install -g markdownlint-cli

# 檢查所有 Markdown 檔案
markdownlint **/*.md

# 檢查特定檔案
markdownlint README.md
```

## 📝 維護說明

- 此資料夾的工具主要用於專案維護
- 新增工具程式時請更新此 README
- 工具程式應該包含適當的錯誤處理和使用說明
- 建議為複雜的工具添加命令列參數支援

---

**最後更新**：2025年6月23日
