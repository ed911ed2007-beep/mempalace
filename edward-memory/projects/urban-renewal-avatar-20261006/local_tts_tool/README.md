# Local Chinese TTS Tool

這是一個最小可用版的本機中文 TTS 小工具。

我替你選的引擎是：Piper

選 Piper 的原因：
1. 可離線執行
2. CPU 可跑，對本機要求相對低
3. 模型下載簡單
4. 很適合先做出一個可用版
5. 直接輸出 `.wav`，不用先依賴 ffmpeg

目前預設模型：`zh_CN-huayan-medium`

注意：
- 這是簡體中文語音模型，但一般中文句子都能念
- 如果你之後要更接近台灣中文口音，可以再換模型

## 目錄
- `tts_cli.py`：主程式
- `requirements.txt`：Python 依賴
- `setup_windows.ps1`：Windows 安裝腳本
- `speak_zh.ps1`：Windows 執行腳本
- `tests_test_tts_cli.py`：純 Python 單元測試
- `models/`：模型下載位置（首次執行自動建立）
- `outputs/`：語音輸出位置（首次執行自動建立）

## 安裝方式（Windows PowerShell）
建議在 Windows PowerShell 執行。

```powershell
Set-ExecutionPolicy -Scope Process Bypass
cd "D:\Edward的資料夾\h.EMBA\AI\local_tts_tool"
.\setup_windows.ps1
```

這會做：
1. 建立 `.venv`
2. 升級 pip
3. 安裝 `piper-tts`

## 第一次測試
```powershell
cd "D:\Edward的資料夾\h.EMBA\AI\local_tts_tool"
.\speak_zh.ps1 -Text "最近一直下雨，不知道什麼時候能放晴？"
```

## 指定輸出檔案
```powershell
.\speak_zh.ps1 -Text "最近一直下雨，不知道什麼時候能放晴？" -OutputPath "D:\Edward的資料夾\h.EMBA\AI\rain_test.wav"
```

## 直接用 Python 執行
```powershell
.\.venv\Scripts\python.exe .\tts_cli.py "最近一直下雨，不知道什麼時候能放晴？"
```

## 用文字檔轉語音
如果你已經有稿子，可以直接給 UTF-8 `.txt` 檔：

```powershell
.\.venv\Scripts\python.exe .\tts_cli.py --input-file .\demo.txt
```

或：

```powershell
.\speak_zh.ps1 -Text (Get-Content .\demo.txt -Raw)
```

## 工具行為
- CLI 輸入來源二選一：
  - 直接給文字參數
  - 或使用 `--input-file` 讀 UTF-8 文字檔
- 若 `--input-file` 指向不存在檔案，會明確報錯
- 若輸入內容是空白，會明確報錯
- 模型名稱格式需符合：`<language>-<speaker>-<quality>`
- 首次執行會自動下載：
  - `zh_CN-huayan-medium.onnx`
  - `zh_CN-huayan-medium.onnx.json`
- 下載來源：Hugging Face `rhasspy/piper-voices`
- 預設輸出資料夾：`outputs/`
- 預設輸出格式：`.wav`

## 已驗證項目
以下是我目前已經在這邊驗證過的：
1. 測試檔 `tests_test_tts_cli.py` 通過
2. 模型 URL 存在：
   - `zh_CN-huayan-medium.onnx`
   - `zh_CN-huayan-medium.onnx.json`

## 尚未在此環境直接完成的部分
目前這個 Hermes/WSL session 沒有可直接用的 Windows Python + pip 執行鏈，
所以我已完成：
- 工具實作
- 測試
- 模型 URL 驗證

但最終的 Windows 本機安裝與真正生成 `.wav`，需要你在 Windows PowerShell 跑一次。

## 建議下一步
1. 先執行 `setup_windows.ps1`
2. 再執行 `speak_zh.ps1`
3. 如果成功，我下一步可以再幫你做：
   - 批次念稿版
   - txt 檔轉語音
   - STT + LLM + TTS 串接版
   - GUI 小工具版
