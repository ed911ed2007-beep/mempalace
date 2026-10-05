# 土開 Avatar × 逐字稿影片製作｜Codex 接續執行規格

> 狀態：`WAITING_FOR_TRANSCRIPT`  
> 建立日期：2026-09-12  
> 執行角色：Codex CLI / Enterprise AI Copilot  
> 原則：保留來源、禁止臆造、不移除第三方浮水印、每階段可驗證與可回復。

## 1. 任務目標

收到使用者後續提供的繁體中文逐字稿後，使用既有「土開 Avatar」作為角色與視覺基準，產出可審核、可重跑、可批次合併的直式解說影片。

本文件是 Codex 的執行任務書。未收到逐字稿前，只能完成資產盤點與環境預檢，不得自行補寫講稿或產生正式成片。

## 2. 已知輸入

### 2.1 Avatar 來源

- 使用者上傳檔名：`土開 Avatar.mp4`
- 本次工作階段來源路徑：`upload/土開 Avatar.mp4`
- 影片：H.264、720 × 1280、25 fps、直式 9:16
- 音訊：AAC、48 kHz、單聲道
- 時長：19.605 秒
- 檔案大小：約 1.55 MiB
- 已觀察到：影片內含燒錄字幕及 Vidnoz 標示

### 2.2 待補輸入

將使用者後續提供的逐字稿保存為：

```text
input/transcript_zh-TW.txt
```

可選參數若使用者未指定，採以下預設：

```yaml
language: zh-TW
aspect_ratio: "9:16"
resolution: "720x1280"
fps: 25
subtitle: true
subtitle_style: clean_corporate
segment_target_seconds: 12-18
final_format: mp4
```

## 3. 重要限制與判斷

1. `土開 Avatar.mp4` 目前只能直接視為角色／服裝／構圖參考與品質基準。
2. 原片已有舊字幕，不能把原片直接循環後覆蓋新旁白，否則會出現舊字幕、新字幕與嘴型不同步。
3. 不得使用裁切、遮蓋或修補方式移除 Vidnoz 標示。若正式成片要求無標示，必須使用合法的無浮水印匯出方案或由使用者提供乾淨母片。
4. 若要讓同一 Avatar 朗讀新逐字稿，必須使用下列其中一條合法路徑：
   - 已授權的 Avatar 平台/API 專案；或
   - 使用者有權使用的乾淨 Avatar 素材，加上本機 lip-sync 流程；或
   - 靜態角色圖搭配旁白與字幕的降級方案。
5. 不得將影片中的聲音用於語音複製，除非使用者明確確認擁有該聲音及複製授權。
6. 所有逐字稿文字必須可追溯至使用者來源。只能修正明顯錯字、標點和口語停頓；涉及事實、金額、法規或同意比時不得自行改寫內容。

## 4. 建議目錄結構

```text
avatar-video-project/
├─ README.md
├─ input/
│  ├─ avatar_source.mp4
│  ├─ transcript_zh-TW.txt
│  └─ assets/
├─ work/
│  ├─ transcript_clean.md
│  ├─ segments.json
│  ├─ scene_manifest.csv
│  ├─ audio/
│  ├─ video/
│  └─ subtitles/
├─ output/
│  ├─ preview_lowres.mp4
│  ├─ final_720x1280.mp4
│  ├─ final_720x1280.srt
│  └─ qa_report.md
├─ logs/
└─ scripts/
```

複製來源時不得覆寫上傳原檔：

```bash
mkdir -p avatar-video-project/{input/assets,work/{audio,video,subtitles},output,logs,scripts}
cp "upload/土開 Avatar.mp4" "avatar-video-project/input/avatar_source.mp4"
sha256sum "upload/土開 Avatar.mp4" "avatar-video-project/input/avatar_source.mp4" \
  | tee "avatar-video-project/logs/source_sha256.txt"
```

## 5. Codex 執行工作流

### Gate 0｜輸入確認

必要條件：

- [ ] `input/avatar_source.mp4` 可讀
- [ ] `input/transcript_zh-TW.txt` 已收到且非空白
- [ ] 使用者確認 Avatar 與其聲音／平台資產的使用權
- [ ] 已確認採用哪一條生成路徑：平台/API、本機 lip-sync、靜態降級

若逐字稿缺少，輸出：

```text
STATUS=WAITING_FOR_TRANSCRIPT
NEXT_ACTION=請提供完整逐字稿；Codex 不自行補寫內容。
```

不得進入 Gate 1。

### Gate 1｜逐字稿正規化

1. 保留原始逐字稿，不直接改寫來源檔。
2. 產生 `work/transcript_clean.md`，僅處理：
   - 全形／半形標點一致化；
   - 明顯錯字；
   - 過長句斷句；
   - 數字、英文縮寫與專有名詞的發音註記。
3. 有疑義的內容以 `[待確認：...]` 標示，不猜測。
4. 產生修改摘要，列出所有非標點變更。

驗收：清理稿與原稿逐段可對照，內容零遺漏。

### Gate 2｜分段與場景表

依語意分段，以每段 12–18 秒為目標；避免在專有名詞、數字、法規名稱中間切斷。建立 `work/segments.json`：

```json
{
  "project": "land-development-avatar",
  "language": "zh-TW",
  "segments": [
    {
      "id": "S001",
      "text": "逐字稿第一段",
      "estimated_seconds": 15,
      "visual": "avatar",
      "status": "pending"
    }
  ]
}
```

同步建立 `work/scene_manifest.csv`：

```csv
segment_id,text,estimated_seconds,audio_path,video_path,subtitle_path,status,notes
S001,"逐字稿第一段",15,work/audio/S001.wav,work/video/S001.mp4,work/subtitles/S001.srt,pending,
```

驗收：段落串接後必須與 `transcript_clean.md` 完整一致。

### Gate 3｜旁白與 Avatar 生成

#### 路徑 A：已授權 Avatar 平台/API（優先）

1. 從環境變數讀取憑證；禁止把 API Key 寫入程式碼、Markdown、JSON 或 Git。
2. 以 S001、S002…逐段送出，保存 request ID、狀態與輸出路徑。
3. API 失敗採指數退避，單段最多重試 3 次；仍失敗則停止合併並記錄。
4. 使用合法匯出設定；若方案會產生標示，成片必須保留。

#### 路徑 B：本機 lip-sync

只有在使用者提供可合法重製的乾淨母片或角色圖後才能執行。模型與權重需記錄版本及授權；先用 S001 製作低解析 PoC，人工核准後才批次生成。

#### 路徑 C：靜態降級方案

若沒有 Avatar API 或可用 lip-sync 環境，從已授權角色素材製作靜態講者畫面，配旁白、字幕與簡單縮放。此路徑不得宣稱已完成嘴型同步。

### Gate 4｜字幕

1. 字幕文字直接取自分段逐字稿，不以 ASR 重新猜詞作為主稿。
2. 每行建議不超過 18 個全形中文字，最多兩行。
3. 字幕不得遮住嘴部、下巴或重要視覺；保留手機安全邊界。
4. 同時輸出外掛 `.srt` 與燒錄字幕預覽。
5. 字體需具繁體中文字形；正式執行前以 `fc-match "Noto Sans CJK TC"` 檢查。

### Gate 5｜規格正規化與合併

所有分段先正規化成相同規格再合併：

```bash
ffmpeg -i work/video/S001.mp4 \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25" \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 20 \
  -c:a aac -ar 48000 -ac 1 -b:a 128k \
  work/video/S001_normalized.mp4
```

將已核准段落依 `segments.json` 順序建立 concat 清單後合併。禁止以檔名字典排序取代 manifest 順序。

### Gate 6｜低解析預覽與人工核准

先產出 `output/preview_lowres.mp4`。正式輸出前，由使用者核對：

- [ ] Avatar 外觀與角色一致
- [ ] 嘴型與語音無明顯錯位
- [ ] 專有名詞、數字、地名、法規名唸法正確
- [ ] 字幕沒有錯字、切斷或超出安全區
- [ ] 段落順序正確，無重複或遺漏
- [ ] 音量一致，沒有爆音、底噪或段落忽大忽小
- [ ] 第三方標示及素材授權符合預期

未取得人工核准，狀態只能是 `CONDITIONAL_PASS`，不可標記完成。

### Gate 7｜正式輸出與 QA

產出：

- `output/final_720x1280.mp4`
- `output/final_720x1280.srt`
- `output/qa_report.md`

最低技術檢查：

```bash
ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels \
  -of json output/final_720x1280.mp4 \
  > logs/final_ffprobe.json

ffmpeg -v error -i output/final_720x1280.mp4 -f null - \
  2> logs/final_decode_errors.log
```

`qa_report.md` 至少包含：來源 Hash、逐字稿版本、分段數、生成路徑、模型／平台版本、成片時長、影音規格、失敗與重試紀錄、人工核准狀態、已知限制。

## 6. 狀態碼

| 狀態 | 意義 | 是否可繼續 |
|---|---|---|
| `WAITING_FOR_TRANSCRIPT` | 尚未收到逐字稿 | 否 |
| `READY_FOR_SEGMENTATION` | 逐字稿已收到且完成正規化 | 是 |
| `BLOCKED_ASSET_RIGHTS` | Avatar／聲音授權不明 | 否 |
| `BLOCKED_GENERATOR` | 無可用 Avatar API 或本機生成環境 | 可改採靜態降級 |
| `PREVIEW_READY` | 預覽已完成，等待人工核准 | 否 |
| `CONDITIONAL_PASS` | 技術檢查通過，尚待人工內容確認 | 否 |
| `PASS` | 技術與人工核准皆完成 | 完成 |
| `FAIL` | 關鍵輸入、影音或內容驗證失敗 | 修正後重跑 |

## 7. Acceptance Criteria

- [ ] 上傳原檔未被覆寫，來源 Hash 已保存
- [ ] 逐字稿內容零遺漏，疑義未被 AI 擅自補寫
- [ ] 每段都有唯一 ID，音訊、影片、字幕可追溯
- [ ] 正式輸出為 720×1280、25 fps、H.264/AAC、可正常解碼
- [ ] 字幕為繁體中文，與旁白及畫面同步
- [ ] 無舊字幕與新字幕重疊
- [ ] 未使用技術手段移除第三方標示
- [ ] API Key、個資、地主資料未出現在 Repo、Log 或成片中
- [ ] 先有預覽與人工核准，再產出正式版
- [ ] `qa_report.md` 可重現本次製作條件與結果

## 8. Codex 收到逐字稿後的第一個回覆格式

```markdown
## 執行摘要

- 狀態：READY_FOR_SEGMENTATION
- 逐字稿字數：<數字>
- 預估片長：<分:秒>
- 預計分段：<數字>
- 生成路徑：<A/B/C 或待確認>
- 阻擋事項：<無／項目>
- 下一步：產生 transcript_clean.md、segments.json 與 scene_manifest.csv
```

## 9. 給 Codex CLI 的直接指令

```text
請依本文件逐 Gate 執行。先驗證 Avatar 來源與 transcript_zh-TW.txt；若逐字稿尚未存在，回報 WAITING_FOR_TRANSCRIPT 後停止。若已存在，保留原稿並產出清理稿、segments.json、scene_manifest.csv。所有事實與專有名詞不得自行補寫。確認生成路徑與素材授權後，只先完成 S001 低解析 PoC；通過人工核准才批次生成、合併、字幕化與輸出 QA 報告。
```

