#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont


def ensure_background(path: Path | None, url: str | None, download_to: Path | None) -> Path:
    if path:
        return path
    if not url or not download_to:
        raise SystemExit("Provide either --background-path or both --background-url and --download-to")
    download_to.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url, timeout=120) as response:
        download_to.write_bytes(response.read())
    return download_to


def draw_poster(
    background: Path,
    output: Path,
    *,
    city_name: str,
    date_text: str,
    weather_summary: str,
    local_time: str,
    temp_range: str,
    wind: str,
    caption: str,
    font_path: str,
) -> None:
    img = Image.open(background).convert("RGBA")
    w, h = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    panel_x = int(w * 0.065)
    panel_y = int(h * 0.06)
    panel_w = int(w * 0.42)
    panel_h = int(h * 0.24)
    od.rounded_rectangle(
        (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
        radius=34,
        fill=(7, 16, 28, 138),
    )
    od.rounded_rectangle(
        (panel_x + 22, panel_y + 26, panel_x + 38, panel_y + 124),
        radius=8,
        fill=(188, 25, 46, 235),
    )
    od.rounded_rectangle(
        (int(w * 0.07), int(h * 0.885), int(w * 0.72), int(h * 0.955)),
        radius=24,
        fill=(7, 16, 28, 120),
    )

    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(font_path, size=int(h * 0.032))
    date_font = ImageFont.truetype(font_path, size=int(h * 0.017))
    weather_font = ImageFont.truetype(font_path, size=int(h * 0.056))
    info_font = ImageFont.truetype(font_path, size=int(h * 0.022))
    caption_font = ImageFont.truetype(font_path, size=int(h * 0.020))

    white = (247, 248, 250, 255)
    soft = (224, 228, 233, 255)
    accent = (255, 205, 92, 255)

    x = panel_x + 64
    y = panel_y + 28

    d.text((x, y), f"{city_name}天气预报", font=title_font, fill=white)
    y += int(h * 0.058)
    d.text((x, y), date_text, font=date_font, fill=soft)
    y += int(h * 0.040)
    d.text((x, y), weather_summary, font=weather_font, fill=accent)
    y += int(h * 0.078)
    d.text((x, y), f"当前时间  {local_time}", font=info_font, fill=white)
    y += int(h * 0.045)
    d.text((x, y), f"温度范围  {temp_range}", font=info_font, fill=white)
    y += int(h * 0.045)
    d.text((x, y), f"风力      {wind}", font=info_font, fill=white)

    d.text((int(w * 0.10), int(h * 0.905)), caption, font=caption_font, fill=white)

    output.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output, quality=95)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose a city weather poster from a background image.")
    parser.add_argument("--background-path")
    parser.add_argument("--background-url")
    parser.add_argument("--download-to")
    parser.add_argument("--output", required=True)
    parser.add_argument("--city-name", required=True)
    parser.add_argument("--date-text", required=True)
    parser.add_argument("--weather-summary", required=True)
    parser.add_argument("--local-time", required=True)
    parser.add_argument("--temp-range", required=True)
    parser.add_argument("--wind", required=True)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--font-path", default="/System/Library/Fonts/Hiragino Sans GB.ttc")
    args = parser.parse_args()

    background = ensure_background(
        Path(args.background_path) if args.background_path else None,
        args.background_url,
        Path(args.download_to) if args.download_to else None,
    )
    draw_poster(
        background,
        Path(args.output),
        city_name=args.city_name,
        date_text=args.date_text,
        weather_summary=args.weather_summary,
        local_time=args.local_time,
        temp_range=args.temp_range,
        wind=args.wind,
        caption=args.caption,
        font_path=args.font_path,
    )
    print(Path(args.output).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
