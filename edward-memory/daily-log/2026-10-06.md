# 都市更新 Avatar 影片保存點｜2026-10-06

## 已完成
- 原始逐字稿 1295 字（不含空白），拆成 19 段，逐段串接與原稿完全一致。
- FFmpeg／ffprobe 9.0.2 已安裝。原 Avatar：H.264、720×1280、25 fps；AAC、48 kHz、單聲道；19.605 秒。原片與副本 Hash 一致，完整解碼無錯誤。
- 5 秒測試 MP4 保存在 AI Media／土開_Avatar_5sec_test.mp4，解碼通過。
- 使用使用者指定 local_tts_tool 的 Piper 1.8.0、zh_CN-huayan-medium 一般合成聲音，未複製原片聲音。
- 建立獨立 WSL Python 3.12 環境 local_tts_tool/.venv-wsl；原 .venv 是 Windows 環境，WSL 無法使用。
- 19 段 WAV 與完整 WAV 皆通過解碼；完整旁白 258.693 秒（4 分 18.693 秒）。
- 完整試聽：/home/edward/Downloads/AI Media/01都市更新_旁白試聽_Piper.wav。
- 專案：/home/edward/Downloads/AI Media/avatar-video-project。

## 待確認與下一步
- 音檔為 DRAFT_PENDING_LISTENING_REVIEW；語速、發音、普通話口音待使用者試聽。
- 講師 xxx 保留原文，名稱待確認；原稿標題目前也有口播。
- Avatar 使用授權與生成路徑尚未確認；尚未生成新 Avatar 對嘴、B-roll、字幕或正式影片。
- 本次提示詞指定 16:9；原片直式 9:16。分段為估時草稿，正式生成前調整語意銜接。
- 原稿法律敘述保留來源，未做現行法規查核。
- 先核准 S001 低解析 PoC，再核准完整預覽，才能正式輸出。保留第三方標示。

## 保存與重跑
GitHub 保存逐字稿、提示詞、分段 JSON／CSV／MD、影音測試紀錄、19 段與完整 WAV、TTS 程式及生成腳本。來源 Avatar、5 秒 MP4、ONNX 模型、venv 留在原本機位置；模型與來源 Hash 已記錄。
SHA-256 清單：archive_sha256.json。生成腳本使用本機路徑且拒絕覆寫既有 WAV；跨電腦需依路徑重建環境，或調整 PROJECT／TOOL 位置。

GitHub 同步範圍：claude-config-sync、ai-collaboration-governance、mempalace。同步 Git 文件不等於套用各機器設定。
