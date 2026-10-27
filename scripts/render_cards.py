#!/usr/bin/env python3
"""Render exact-text consultation cards in a Swiss grid visual system."""
import argparse
import html
import json
import subprocess
from pathlib import Path


def e(value):
    return html.escape(str(value), quote=True).replace("\n", "<br>")


def chrome_path():
    for path in ("C:/Program Files/Google/Chrome/Application/chrome.exe", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", "C:/Program Files/Microsoft/Edge/Application/msedge.exe"):
        if Path(path).exists():
            return path
    raise RuntimeError("Chrome or Edge is required")


CSS = """
*{box-sizing:border-box}html,body{margin:0;width:1672px;height:940px;overflow:hidden}
body{font-family:'Microsoft YaHei','PingFang SC',sans-serif;color:#111;background:#f8f8f4}
body:before{content:'';position:absolute;inset:46px;border:2px solid #171717;pointer-events:none}
body:after{content:'';position:absolute;left:46px;top:46px;width:28px;height:28px;background:#f3d72f}
.head{position:absolute;left:112px;top:105px;right:112px}.eyebrow{font:700 17px Consolas,monospace;color:#555;letter-spacing:2.5px}
h1{font-size:58px;line-height:1.12;letter-spacing:1px;margin:14px 0 13px;font-weight:900}.subtitle{font-size:25px;line-height:1.35;color:#3c3c3c}
.annotation{position:absolute;border:1.5px solid #111;color:#111;font:700 16px Consolas,monospace;letter-spacing:1px;padding:10px 13px;background:#f3d72f}
.annotation.top{top:112px;right:112px}.annotation.bottom{bottom:100px;right:112px;background:#fff}
.fig-line{position:absolute;left:112px;top:301px;width:1448px;border-top:2px solid #111}
.foot{position:absolute;left:112px;bottom:103px;color:#333;font-size:21px;max-width:1020px}
.flow{position:absolute;left:112px;top:326px;width:1448px;border-top:1px solid #111}
.row{height:160px;border-bottom:1px solid #111;display:grid;grid-template-columns:112px 865px 1fr;align-items:center}
.num{font:700 34px Consolas,monospace;color:#111;align-self:start;padding-top:28px}
.main{padding-right:35px}.main h2{margin:0 0 9px;font-size:32px}.main p{margin:0;font-size:24px;line-height:1.45;color:#303030}
.out{border-left:2px solid #111;background:#f3d72f;padding:18px 20px;min-height:101px}
.out small{display:block;font:700 15px Consolas,monospace;color:#333;letter-spacing:1.5px;margin-bottom:7px}.out strong{font-size:23px;line-height:1.28}
.cards{position:absolute;left:112px;top:328px;display:grid;grid-template-columns:704px 704px;gap:40px}
.case{height:467px;background:#fff;border:2px solid #111;position:relative;padding:32px 35px 24px}
.corner{position:absolute;right:27px;top:27px;font:700 15px Consolas,monospace;color:#111;border:1.5px solid #111;padding:8px 10px;background:#f3d72f}
.case h2{margin:0;font-size:34px;padding-right:130px}.meta{margin-top:12px;font-size:23px;color:#444}
.rule{height:1px;background:#111;margin:22px 0 17px}.role{font-size:27px;font-weight:800;line-height:1.35}
.company{font-size:22px;color:#404040;margin-top:7px}.salary{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:20px;border:1px solid #111}
.salary>div{padding:11px 12px}.salary>div+div{border-left:1px solid #111}.salary small{display:block;font-size:16px;color:#555;margin-bottom:5px}
.salary b{font-size:23px;white-space:nowrap}.salary.single{grid-template-columns:1fr}.growth{position:absolute;bottom:24px;left:35px;right:35px;background:#f3d72f;border-top:2px solid #111;padding:11px 14px;font-size:23px;font-weight:800}
.purple-line{display:none}
"""


def page(title, subtitle, eyebrow, content, footer):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="head"><div class="eyebrow">{e(eyebrow)}</div><h1>{e(title)}</h1><div class="subtitle">{e(subtitle)}</div></div><div class="fig-line"></div><div class="annotation top">CONSULTATION / 01</div>{content}<div class="foot">{e(footer)}</div></body></html>'''


def action(data):
    if len(data["steps"]) != 3:
        raise ValueError("Action card requires exactly 3 stages")
    rows = ""
    for i, step in enumerate(data["steps"], 1):
        rows += f'<div class="row"><div class="num">{i:02d}</div><div class="main"><h2>{e(step["phase"])}</h2><p>{e(step["actions"])}</p></div><div class="out"><small>OUTPUT / {i:02d}</small><strong>{e(step["output"])}</strong></div></div>'
    content = f'<div class="flow">{rows}</div><div class="annotation bottom">03 / ACTION</div>'
    return page(data["title"], data["subtitle"], "LEARNING / ACTION", content, data["footer"])


def cases(data):
    if not 1 <= len(data["cases"]) <= 2:
        raise ValueError("Case card supports 1 or 2 cases")
    cards = ""
    for i, case in enumerate(data["cases"], 1):
        lines = case["course_and_role"].splitlines()
        company = " · ".join(lines[1:])
        if case.get("before"):
            salary = f'<div class="salary"><div><small>{e(case.get("before_label", "转行前月薪"))}</small><b>{e(case["before"])}</b></div><div><small>{e(case.get("after_label", "录用月薪"))}</small><b>{e(case["after"])}</b></div></div>'
        else:
            salary = f'<div class="salary single"><div><small>{e(case.get("after_label", "实习日薪"))}</small><b>{e(case["after"])}</b></div></div>'
        growth = f'<div class="growth">{e(case.get("growth_label", "最高薪资涨幅"))}  {e(case["growth"])}</div>' if case.get("growth") else ""
        cards += f'''<section class="case"><span class="corner">CASE / {i:02d}</span><h2>{e(case["label"])}</h2><div class="meta">{e(case["background"])}</div><div class="rule"></div><div class="role">{e(lines[0])}</div><div class="company">{e(company)}</div>{salary}{growth}</section>'''
    content = f'<div class="cards">{cards}</div><div class="annotation bottom">02 / CASES</div>'
    return page(data["title"], data["subtitle"], "MATCHED / CASES", content, data["footer"])


def render(chrome, html_path, png_path, content):
    html_path.write_text(content, encoding="utf-8")
    subprocess.run([str(chrome), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1672,940", f"--screenshot={png_path.resolve()}", html_path.resolve().as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--slug", default="consultation")
    args = p.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    chrome = chrome_path()
    result = {}
    for name, maker, key in (("action", action, "action"), ("case", cases, "cases")):
        html_path = output / f"{args.slug}-{name}-card.html"
        png_path = output / f"{args.slug}-{name}-card.png"
        render(chrome, html_path, png_path, maker(data[key]))
        result[name] = {"html": str(html_path.resolve()), "png": str(png_path.resolve())}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
