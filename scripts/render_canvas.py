"""Render a career lean canvas in a Swiss grid visual system."""

import argparse
import html
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "career-canvas-template.html"


def esc(value):
    return html.escape(str(value), quote=True)


def marked(value):
    escaped = esc(value)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)


def chrome_path():
    for path in (
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ):
        if path.exists():
            return path
    raise FileNotFoundError("Chrome or Edge is required for PNG rendering")


def render(data):
    blocks = data["blocks"]
    if len(blocks) != 9:
        raise ValueError("The career lean canvas requires exactly nine blocks")
    header = (
        f'<div class="eyebrow">{esc(data.get("eyebrow", "CAREER CANVAS"))}</div>'
        f'<div class="title"><h1>{esc(data.get("title", "职业规划画布"))}</h1>'
        f'<span class="tag">{esc(data["tag"])}</span></div>'
        f'<div class="sub">{esc(data["subtitle"])}</div>'
    )
    cells = ""
    for i, block in enumerate(blocks, 1):
        lines = "".join(f"<div>{marked(line)}</div>" for line in block["lines"])
        cells += (
            f'<article class="cell"><div class="head"><span class="no">{i:02d}</span>'
            f'<span class="name">{esc(block["heading"])}</span></div>'
            f'<div class="body">{lines}</div></article>'
        )
    footer = (
        f'<span>{esc(data["source_note"])}</span>'
        f'<strong><span class="circle">{esc(data["footer_phrase"])}</span></strong>'
    )
    source = TEMPLATE.read_text(encoding="utf-8")
    for token, value in (
        ("{{HEADER}}", header),
        ("{{CELLS}}", cells),
        ("{{FOOTER}}", footer),
    ):
        source = source.replace(token, value)
    if "{{" in source:
        raise ValueError("Unfilled canvas template token")
    return source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="UTF-8 JSON with a canvas object")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--slug", default="consultation")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))["canvas"]
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    html_path = output / f"{args.slug}-career-canvas.html"
    png_path = output / f"{args.slug}-career-canvas.png"
    html_path.write_text(render(data), encoding="utf-8")
    subprocess.run(
        [str(chrome_path()), "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--window-size=2000,1125",
         f"--screenshot={png_path.resolve()}", html_path.resolve().as_uri()],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(json.dumps({"html": str(html_path.resolve()), "png": str(png_path.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
