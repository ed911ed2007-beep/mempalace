"""Generate reproducible draft narration using the user's local TTS tool."""
from pathlib import Path
import csv
import hashlib
import importlib.metadata
import json
import subprocess
import sys
import wave

PROJECT = Path(__file__).resolve().parents[1]
TOOL = PROJECT.parent / "local_tts_tool"
sys.path.insert(0, str(TOOL))
from tts_cli import ensure_model, synthesize


def main():
    manifest = json.loads((PROJECT / "work/segments_draft.json").read_text())
    model, config = ensure_model("zh_CN-huayan-medium", TOOL / "models")
    output = PROJECT / "work/audio/piper_draft"
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "DRAFT_PENDING_LISTENING_REVIEW",
        "model": model.name,
        "model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
        "config_sha256": hashlib.sha256(config.read_bytes()).hexdigest(),
        "piper_version": importlib.metadata.version("piper-tts"),
        "length_scale": 1.0,
        "noise_scale": 0.667,
        "notes": ["Original text preserved, including xxx", "Mandarin zh_CN voice; no voice cloning"],
        "segments": [],
    }
    combined = None
    try:
        for segment in manifest["segments"]:
            path = output / (segment["id"] + ".wav")
            if path.exists():
                raise FileExistsError(f"Refusing to overwrite {path}")
            synthesize(segment["text"], model, path)
            with wave.open(str(path), "rb") as audio:
                params = audio.getparams()
                frames = audio.readframes(audio.getnframes())
                seconds = audio.getnframes() / audio.getframerate()
                if combined is None:
                    full = PROJECT.parent / "01都市更新_旁白試聽_Piper.wav"
                    if full.exists():
                        raise FileExistsError(f"Refusing to overwrite {full}")
                    combined = wave.open(str(full), "wb")
                    combined.setparams(params)
                assert (params.nchannels, params.sampwidth, params.framerate) == (combined.getnchannels(), combined.getsampwidth(), combined.getframerate())
                combined.writeframes(frames)
            check = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "null", "-"], capture_output=True, text=True)
            if check.returncode or check.stderr:
                raise RuntimeError(check.stderr)
            item = {"id": segment["id"], "text": segment["text"], "path": str(path), "duration_seconds": round(seconds, 3), "sample_rate": params.framerate, "channels": params.nchannels, "decode": "PASS"}
            report["segments"].append(item)
            (PROJECT / "logs/piper_narration_draft.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
            print(f"{segment['id']}: {seconds:.2f} sec PASS", flush=True)
    finally:
        if combined:
            combined.close()
    report["total_seconds"] = round(sum(s["duration_seconds"] for s in report["segments"]), 3)
    report["combined_audio"] = str(full)
    check = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(full), "-f", "null", "-"], capture_output=True, text=True)
    assert check.returncode == 0 and not check.stderr, check.stderr
    report["combined_decode"] = "PASS"
    (PROJECT / "logs/piper_narration_draft.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    with (PROJECT / "work/narration_manifest_draft.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(report["segments"][0]))
        writer.writeheader()
        writer.writerows(report["segments"])
    print(json.dumps({"segments": len(report["segments"]), "seconds": report["total_seconds"], "combined": str(full)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
