---
name: task-completion
description: 任務完成後的標準流程
created: 2026-05-20
from: CLAUDE.md 工作規則
---

# 任務完成協議

## 規則

每次完成任務後，執行以下步驟：

1. 更新相關的 TODO.md 或專案追蹤檔
2. 發現新專案資訊時，更新 `~/.claude/projects/` 對應檔案
3. 學到的重要知識寫入 memory layer

## 為什麼

- 確保知識不會遺失
- 下次 session 可以接續
- 建立可追溯的工作記錄

## 怎麼套用

### 完成任務時

```bash
# 1. 更新專案追蹤檔
# 位置：~/.claude/projects/{project-name}.md

# 2. 重要發現寫入 memory
cd ~/ai-lab && source .venv/bin/activate
python -m memory.cli write "發現內容" --agent claude-code --tags "relevant,tags"
```

### Carryover（session 結束時）

如果任務未完成，在 daily-log 寫入：
- 目前進度
- 下一步行動
- 阻塞原因（如有）
