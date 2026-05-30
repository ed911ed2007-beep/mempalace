# 記憶存檔規則

> 觸發詞：存檔、記憶、save

## 存檔流程（必須全部執行）

1. **ChromaDB 寫入** - Session summary 寫入 memory layer
2. **Daily-log 更新** - 更新 `memory/daily-log/{date}.md`
3. **Mempalace 同步** - `cp -r memory/* mempalace/edward-memory/`
4. **GitHub 推送** - 自動推送，不需詢問艾德華大人

## 規則來源

- 2026-05-30：艾德華大人指示「未來不再問，同時在 ai lab 存檔」
