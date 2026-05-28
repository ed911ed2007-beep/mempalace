# Memory Index (L5 規則層索引)

> 最後更新：2026-05-20
> 此檔案為規則層的索引，啟動時載入

## 索引說明

- 每條規則對應 `rules/` 目錄下的一個 markdown 檔案
- 格式：`規則名稱` → `檔案路徑` → `簡述`
- 超過 200 行時需要修剪

---

## 工作規則

| 規則 | 檔案 | 說明 |
|------|------|------|
| 強目標格式 | `rules/strong-goals.md` | 目標必須可驗證 |
| 任務完成協議 | `rules/task-completion.md` | 完成後更新追蹤檔 |
| 記憶存檔觸發 | `rules/memory-save.md` | 存檔/記憶/save 時寫入 |

## 技術規則

| 規則 | 檔案 | 說明 |
|------|------|------|
| 繁體中文優先 | `rules/traditional-chinese.md` | 輸出預設繁體 |
| Markdown 表格 | `rules/markdown-tables.md` | 結構化資料用表格 |

## 糾正記錄

| 日期 | 規則 | 來源 |
|------|------|------|
| 2026-05-20 | 四層記憶架構 | YouTube 影片學習 |

---

## ChromaDB 記憶層

位置：`~/ai-lab/memory/`
查詢：`python -m memory.cli search "query"`
統計：34 條記憶
