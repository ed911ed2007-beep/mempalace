# GitHub 同步範圍

使用者於 2026-09-12 明確指定：「sync github／同步 github／同步 GitHub 資料」預設指同步 `ed911ed2007-beep` 帳號的三個儲存庫：

1. `claude-config-sync`：AI agents 共用設定、角色、技能與記憶。
2. `ai-collaboration-governance`：協作規則、任務、交接與驗證。
3. `mempalace`：共享記憶及其專案。

目的是同步不同電腦 AI agents 之間的差異。若同時指定專案路徑，先同步三庫，再接續該專案；不要將兩件事混為尋找該專案的 GitHub remote。

保留本機差異，檢閱後合併與推送；不得盲目覆寫機器專用設定或上傳憑證。回報應區分 Git 同步、設定套用與索引重新載入。
