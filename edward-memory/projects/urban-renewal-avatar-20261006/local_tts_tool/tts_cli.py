from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import wave
from pathlib import Path

BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"
DEFAULT_MODEL = "zh_CN-huayan-medium"


def model_file_names(model_name: str) -> tuple[str, str]:
    return f"{model_name}.onnx", f"{model_name}.onnx.json"


def model_path_parts(model_name: str) -> tuple[str, str, str, str]:
    try:
        language, speaker, quality = model_name.split("-", 2)
    except ValueError as exc:
        raise ValueError(
            "Expected model name in the form <language>-<speaker>-<quality>, "
            f"for example '{DEFAULT_MODEL}'"
        ) from exc
    return language.split("_")[0], language, speaker, quality


def build_model_urls(model_name: str) -> tuple[str, str]:
    lang_group, language, speaker, quality = model_path_parts(model_name)
    onnx_name, json_name = model_file_names(model_name)
    base = f"{BASE_URL}/{lang_group}/{language}/{speaker}/{quality}"
    return f"{base}/{onnx_name}", f"{base}/{json_name}"


def normalize_text_for_filename(text: str) -> str:
    value = re.sub(r"\s+", "_", text.strip())
    value = re.sub(r"[^\w\u4e00-\u9fff_-]", "", value)
    value = value.strip("_") or "tts_output"
    return value[:24]


def build_default_output_path(output_dir: Path, text: str) -> Path:
    return output_dir / f"{normalize_text_for_filename(text)}.wav"


def download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as fh:
        fh.write(response.read())


def ensure_model(model_name: str, model_dir: Path) -> tuple[Path, Path]:
    onnx_name, json_name = model_file_names(model_name)
    onnx_path = model_dir / onnx_name
    json_path = model_dir / json_name
    onnx_url, json_url = build_model_urls(model_name)

    if not onnx_path.exists():
        print(f"[INFO] Downloading model: {onnx_url}")
        download_file(onnx_url, onnx_path)
    if not json_path.exists():
        print(f"[INFO] Downloading config: {json_url}")
        download_file(json_url, json_path)
    return onnx_path, json_path


def ensure_piper_installed() -> str:
    try:
        import piper  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "Cannot import 'piper'. Please install dependencies first: "
            "python -m pip install -r requirements.txt"
        ) from exc
    else:
        return sys.executable


def synthesize(text: str, model_path: Path, output_path: Path, noise_scale: float = 0.667, length_scale: float = 1.0) -> None:
    ensure_piper_installed()
    from piper import PiperVoice, SynthesisConfig
    from piper.phonemize_espeak import ESPEAK_DATA_DIR

    output_path.parent.mkdir(parents=True, exist_ok=True)
    voice = PiperVoice.load(model_path, espeak_data_dir=ESPEAK_DATA_DIR)
    config = SynthesisConfig(noise_scale=noise_scale, length_scale=length_scale)
    with wave.open(str(output_path), "wb") as wav_file:
        voice.synthesize_wav(text, wav_file, syn_config=config)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal local Chinese TTS tool using Piper.")
    parser.add_argument("text", nargs="?", help="Text to synthesize")
    parser.add_argument("--input-file", help="Read UTF-8 text from a file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Piper model name, default: zh_CN-huayan-medium")
    parser.add_argument("--project-dir", default=str(Path(__file__).resolve().parent), help="Project directory")
    parser.add_argument("--output", help="Output .wav path")
    parser.add_argument("--noise-scale", type=float, default=0.667)
    parser.add_argument("--length-scale", type=float, default=1.0)
    args = parser.parse_args(argv)

    if bool(args.text) == bool(args.input_file):
        parser.error("Provide exactly one of: positional text or --input-file")
    return args


def get_input_text(args: argparse.Namespace) -> str:
    if args.input_file:
        input_path = Path(args.input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        text = input_path.read_text(encoding="utf-8")
    else:
        text = args.text or ""

    if not text.strip():
        raise ValueError("Input text is empty after trimming whitespace")
    return text


def main() -> int:
    args = parse_args()
    text = get_input_text(args)
    project_dir = Path(args.project_dir).resolve()
    model_dir = project_dir / "models"
    output_dir = project_dir / "outputs"

    output_path = Path(args.output).resolve() if args.output else build_default_output_path(output_dir, text)
    onnx_path, json_path = ensure_model(args.model, model_dir)
    synthesize(text, onnx_path, output_path, args.noise_scale, args.length_scale)

    manifest = {
        "model": args.model,
        "model_path": str(onnx_path),
        "config_path": str(json_path),
        "output_path": str(output_path),
        "text": text,
        "input_file": str(Path(args.input_file).resolve()) if args.input_file else None,
    }
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
