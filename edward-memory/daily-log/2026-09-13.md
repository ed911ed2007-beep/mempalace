# 離題王交接：2026-09-13

## 專案位置

`D:\Edward-Laptop\PRJ\離題王`（WSL：`/mnt/d/Edward-Laptop/PRJ/離題王`）。此資料夾沒有 .git；共享庫只保存交接記憶，不代表專案程式已上傳 GitHub。

## 使用者確認的核心方向

圖片應有爆笑或爆點，不能只是精緻、嚴肅的原角色漫畫。使用者否定了正經神力女超人制服影印機版本，提出「大肥宅 cosplay 神力女超人，用套索進行滑稽行為」。核心為身分錯置、道具誤用、可見反噬、失敗仍耍帥；體型是人物特徵，笑點落在行為。宅男 cosplay 是本案例，不是所有題目的固定模板。

上一版未經創意總監確認，助手已承認。實際測試發現舊 creative_director 依火星／夜市／KPI 等關鍵字及固定模板評估，沒有模型看圖能力；關鍵字堆砌能得到較高新奇訊號，不能當成笑果驗證。

## 已完成

- TASK-033：human label ingestion＋evidence summary，6 個新增測試；當時副本全量 160 tests OK。
- TASK-034：image_comedy.py、image-comedy-review／export-image-comedy CLI、結構化喜劇 brief、引用證據、人工／模型來源區分、版本 hash 綁定、待審與匯出門檻。
- 欄位完整或模型評語不會自動核准；實際人工評語才可開啟試生圖匯出。此工具驗證審閱資料，不是自動理解笑點的新模型。
- V4 不再截斷 image subject 前 80 字，並標示 creative_review_status=needs_review。
- 舊通用圖片 endpoint 仍維持相容；新門檻涵蓋專用 CLI，不能聲稱所有圖片入口已審核。

## 驗證與回復

TASK-034 暫存副本全量 172 tests OK，回寫 17 檔逐檔 hash 一致，原專案再跑新增 12 tests OK。100 題 V4 benchmark 成功。API 測試在沙箱外開 localhost socket；有既有 HTTPError ResourceWarning。

原檔備份：`/tmp/litiwang-task034-originals`；暫存副本：`/tmp/litiwang-task034`。/tmp 非長期備份。

## 必讀交接

相對專案根目錄：
- `CLI_HANDOFF_NEXT_STEPS.md`
- `tasks.md`
- `docs/task-034-image-comedy-review.md`
- `prompts/image/comedy_briefs/lasso_cosplay.json`
- `reports/task-034-lasso-review-v1/candidate_for_review.md`
- `reports/task-034-lasso-review-v1/image_comedy_review.md`

## 下一步

目前宅男套索候選：想懶著拿洋芋片，套索先把自己綁在椅子上，還硬撐英雄表情。已有 Codex 助手文字評語，來源明確為 model，狀態 needs_review；沒有捏造 human pass。

待真實人工檢閱 review_template.json 副本，填寫 reviewer、引用及理由後，使用 export-image-comedy 匯出純 Gemini Markdown。之後比較舊版／靜態 cosplay／翻車版的實際圖片；尚未生成或看過這輪成品，不能宣稱圖片已更好笑。使用者目前未提供成品圖，舊版圖片問題來自使用者文字回報。

## GitHub 同步語意

「sync github」固定指 claude-config-sync、ai-collaboration-governance、mempalace 三庫，用於跨電腦 AI agents 同步；不是替離題王尋找 remote。
