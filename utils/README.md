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

### csv_cleaner.py

**功能**：CSV 檔案清理器

**用途**：

- 清理 CSV 檔案中的空白字元、欄位名稱等問題
- 正規化全形空白與所有 unicode 空白
- 移除欄位名稱中的特殊字元
- 移除完全空白的行和欄位
- 批次處理多個 CSV 檔案

**使用方法**：

```bash
# 單一檔案清理
python utils/csv_cleaner.py <csv檔案路徑>

# 批次清理目錄中的所有 CSV 檔案
python utils/csv_cleaner.py <目錄路徑> -b

# 預覽檔案問題（不寫入檔案）
python utils/csv_cleaner.py <csv檔案路徑> --preview

# 覆蓋原始檔案
python utils/csv_cleaner.py <csv檔案路徑> --replace
```

**範例**：

```bash
# 清理單一檔案
python utils/csv_cleaner.py 原始資料/宮廟、宗教/宗教團體查詢_全國性.csv

# 批次清理所有 CSV 檔案
python utils/csv_cleaner.py 原始資料/ -b

# 預覽檔案問題
python utils/csv_cleaner.py 原始資料/宮廟、宗教/宗教團體查詢_全國性.csv --preview
```

### ods_to_csv_converter.py

**功能**：ODS 轉 CSV 轉換器

**用途**：

- 將 ODS 檔案轉換為 CSV 格式
- 支援批次轉換目錄中的所有 ODS 檔案
- 可指定工作表名稱或索引
- 可跳過標題行
- 自動清理欄位名稱（移除 Unnamed 欄位）

**使用方法**：

```bash
# 單一檔案轉換
python utils/ods_to_csv_converter.py <ods檔案路徑>

# 批次轉換目錄中的所有 ODS 檔案
python utils/ods_to_csv_converter.py <目錄路徑> -b

# 指定工作表
python utils/ods_to_csv_converter.py <ods檔案路徑> -s <工作表名稱或索引>

# 跳過標題行
python utils/ods_to_csv_converter.py <ods檔案路徑> --skip-rows <行數>
```

**範例**：

```bash
# 轉換單一檔案
python utils/ods_to_csv_converter.py 原始資料/宮廟、宗教/宗教團體查詢_一般寺廟.ods

# 批次轉換所有 ODS 檔案
python utils/ods_to_csv_converter.py 原始資料/宮廟、宗教/ -b

# 跳過 3 行標題
python utils/ods_to_csv_converter.py 原始資料/宮廟、宗教/宗教團體查詢_一般寺廟.ods --skip-rows 3
```

### quick_convert.py

**功能**：快速 ODS 轉 CSV 轉換器

**用途**：

- 提供簡單的選單介面
- 自動尋找所有 ODS 檔案
- 支援單一檔案轉換和批次轉換
- 自動嘗試不同的跳過行數設定

**使用方法**：

```bash
python utils/quick_convert.py
```

**功能特色**：

- 互動式選單介面
- 自動掃描 `原始資料/` 目錄中的所有 ODS 檔案
- 顯示檔案大小和路徑
- 支援批次轉換所有檔案
- 自動嘗試不同的標題行設定

### batch_clean_csv.py

**功能**：批次清理所有 CSV 檔案

**用途**：

- 批次清理專案中所有的 CSV 檔案
- 自動掃描 `原始資料/` 目錄
- 顯示清理前後的檔案資訊
- 統計清理結果

**使用方法**：

```bash
python utils/batch_clean_csv.py
```

**功能特色**：

- 自動尋找所有 CSV 檔案
- 顯示檔案路徑和大小
- 批次執行清理作業
- 顯示清理結果統計

### test_converter.py

**功能**：測試 ODS 轉 CSV 轉換器

**用途**：

- 測試轉換器的各種功能
- 顯示可用的 ODS 檔案
- 執行單一檔案和批次轉換測試
- 提供使用說明

**使用方法**：

```bash
python utils/test_converter.py
```

**測試內容**：

- 單一檔案轉換測試
- 批次轉換測試
- 顯示可用檔案清單
- 提供使用說明

### convert_camping_tags.py

**功能**：車泊地點標籤分析和分類工具

**用途**：

- 從車泊地點CSV檔案中解析括號內的服務和設施標籤
- 智能分類標籤為8大類別（設施服務、露營類型、優惠折扣等）
- 生成適用於離線地圖的標記資料
- 支援OpenStreetMap + Leaflet地圖整合
- 產生詳細的標籤統計和分析報告

**使用方法**：

```bash
# 分析車泊地點標籤
python utils/convert_camping_tags.py <CSV檔案路徑> [輸出目錄]

# 範例：分析車泊場地資料
python utils/convert_camping_tags.py 原始資料/車泊場地/全國車泊地點.csv camping_analysis
```

**輸出檔案**：

- `camping_analysis.json` - 完整分析結果
- `tag_categories.json` - 標籤分類對應表  
- `tag_statistics.json` - 標籤統計資料
- `leaflet_markers.json` - Leaflet地圖標記資料
- `camping_locations_clean.csv` - 清理後的地點資料
- `offline_map_example.html` - 離線地圖範例

**標籤分類系統**：

1. **設施服務** - 淋浴、住宿、用餐、民宿等基礎設施
2. **露營類型** - 車泊、搭帳、小帳、背包客等露營方式
3. **優惠折扣** - 憑卡優惠、九折、會員福利等價格優惠
4. **營業時間** - 特約平日、週日到週四等時間限制
5. **商品服務** - 農產品、戶外用品、保修等商品服務
6. **限制條件** - 僅特約、只收、無等使用限制
7. **聯絡資訊** - 申請、辦卡、預訂等聯絡方式
8. **其他** - 未分類的標籤（地名、人名等）

**範例**：

```bash
# 分析全國車泊地點
python utils/convert_camping_tags.py 原始資料/車泊場地/全國車泊地點.csv

# 指定輸出目錄
python utils/convert_camping_tags.py 原始資料/車泊場地/全國車泊地點.csv my_analysis

# 檢視分析結果
ls camping_analysis_output/
```

### kml_to_csv.py

**功能**：Google My Maps KML/KMZ 轉 CSV 轉換器

**用途**：

- 將 Google My Maps 的 KML 檔案轉換為 CSV 格式
- 支援直接從 Google My Maps URL 下載並轉換
- 自動解析地點標記的座標和詳細資訊
- 智能縣市名稱偵測和檔案命名
- 適用於警政署民防資料和其他地圖資料

**使用方法**：

```bash
# 轉換本地 KML 檔案
python utils/kml_to_csv.py <KML檔案路徑>

# 直接從 Google My Maps URL 下載並轉換
python utils/kml_to_csv.py <Google_My_Maps_URL>
```

**範例**：

```bash
# 轉換本地 KML 檔案
python utils/kml_to_csv.py 車泊天地.kml

# 從 Google My Maps 下載並轉換
python utils/kml_to_csv.py "https://www.google.com/maps/d/u/0/kml?mid=1Jdztdx0GIv_EwgYF2yxc1qtJQec"

# 轉換警政署民防資料
python utils/kml_to_csv.py "https://www.google.com/maps/d/u/0/kml?mid=1ceQ5gitm3HnFVXVwhzroV7uLM_obkDdd"
```

**功能特色**：

- 自動縣市名稱偵測（支援22個縣市）
- 智能檔案命名（加入警政署民防前綴）
- 座標資料驗證和格式化
- 支援多種欄位格式的相容性
- 錯誤處理和臨時檔案清理

## �️ 地圖資料處理工具

### 地圖資料工作流程

1. **下載地圖資料**：使用 `kml_to_csv.py` 從 Google My Maps 下載 KML 並轉換為 CSV
2. **標籤分析**：使用 `convert_camping_tags.py` 分析服務標籤並分類
3. **離線地圖**：使用生成的 JSON 檔案建立 Leaflet 離線地圖

### 建議處理順序

```bash
# 1. 下載並轉換 Google My Maps 資料
python utils/kml_to_csv.py "Google_My_Maps_URL"

# 2. 分析標籤並分類
python utils/convert_camping_tags.py 轉換後的CSV檔案.csv

# 3. 使用 leaflet_markers.json 建立離線地圖
# 參考 offline_map_example.html 範例
```

安裝所需的 Python 套件：

```bash
pip install -r utils/requirements.txt
```

**主要依賴套件**：

- `pandas>=1.5.0` - 資料處理
- `odfpy>=1.4.1` - ODS 檔案讀取
- `openpyxl>=3.0.0` - Excel 檔案支援
- `requests>=2.25.0` - HTTP 請求（用於下載 Google My Maps）
- `lxml>=4.6.0` - XML 解析（用於 KML 檔案）

**用途說明**：

- `pandas` - CSV/Excel 資料處理和清理
- `odfpy` - ODS 檔案格式支援
- `openpyxl` - Excel 檔案讀寫
- `requests` - 從 Google My Maps 下載 KML 檔案
- `lxml` - 解析 KML 格式的地圖資料

## 🛠️ 開發工具建議

### 批次處理所有 Markdown 檔案

如需批次修正所有 Markdown 檔案，可使用以下命令：

```bash
# macOS/Linux
find . -name "*.md" -not -path "./utils/*" -exec python utils/fix_markdown.py {} \;

# 或使用 xargs（效率更高）
find . -name "*.md" -not -path "./utils/*" | xargs -I {} python utils/fix_markdown.py {}
```

### 批次處理所有 CSV 檔案

```bash
# 批次清理所有 CSV 檔案
python utils/batch_clean_csv.py

# 或使用 csv_cleaner.py
python utils/csv_cleaner.py 原始資料/ -b
```

### 批次轉換所有 ODS 檔案

```bash
# 使用快速轉換器
python utils/quick_convert.py

# 或使用命令列工具
python utils/ods_to_csv_converter.py 原始資料/ -b
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

- 此資料夾的工具主要用於專案維護和資料處理
- 新增工具程式時請更新此 README
- 工具程式應該包含適當的錯誤處理和使用說明
- 建議為複雜的工具添加命令列參數支援
- 所有 Python 工具程式都統一放在此資料夾中

## 🔄 工具程式工作流程

### 資料處理流程

1. **ODS 檔案轉換**：使用 `ods_to_csv_converter.py` 或 `quick_convert.py` 將 ODS 檔案轉換為 CSV
2. **CSV 檔案清理**：使用 `csv_cleaner.py` 或 `batch_clean_csv.py` 清理 CSV 檔案
3. **格式檢查**：使用 `fix_markdown.py` 修正 Markdown 檔案格式

### 建議使用順序

```bash
# 1. 轉換 ODS 檔案
python utils/quick_convert.py

# 2. 清理 CSV 檔案
python utils/batch_clean_csv.py

# 3. 修正 Markdown 格式
find . -name "*.md" -not -path "./utils/*" | xargs -I {} python utils/fix_markdown.py {}
```

---

**最後更新**：2025年6月24日
