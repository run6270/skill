#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TERMINAL_STATUSES = {"SUCCEEDED", "FAILED", "VIOLATION"}


class ApiError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


@dataclass
class Session:
    base_url: str | None = None
    token: str | None = None


def normalize_base_url(base_url: str) -> str:
    value = base_url.strip().rstrip("/")
    return value if value.endswith("/api") else f"{value}/api"


def load_json_file(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text("utf-8"))
    except FileNotFoundError:
        return None


def load_session(auth_file: str | None) -> Session:
    candidates: list[Path] = []
    if auth_file:
        candidates.append(Path(auth_file).expanduser())
    candidates.append(Path.cwd() / ".genimage" / "session.json")
    candidates.append(Path.home() / ".genimage" / "session.json")

    for candidate in candidates:
        data = load_json_file(candidate)
        if data:
            return Session(
                base_url=data.get("baseUrl") or data.get("base_url"),
                token=data.get("token"),
            )
    return Session()


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = 60,
) -> Any:
    request_headers = dict(headers or {})
    payload = None
    if body is not None:
        request_headers["Content-Type"] = "application/json"
        payload = json.dumps(body).encode("utf-8")

    request = Request(url, data=payload, headers=request_headers, method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8")
            return json.loads(text) if text else None
    except HTTPError as error:
        text = error.read().decode("utf-8", "ignore")
        body_json = None
        try:
            body_json = json.loads(text)
        except Exception:
            body_json = text or None
        message = None
        if isinstance(body_json, dict):
            message = body_json.get("msg") or body_json.get("message")
        raise ApiError(message or f"HTTP {error.code}", status=error.code, body=body_json) from error
    except URLError as error:
        raise ApiError(f"Network error: {error.reason}") from error


def login(base_url: str, username: str, password: str) -> tuple[str, dict[str, Any]]:
    envelope = http_json(
        f"{base_url}/auth/login",
        method="POST",
        body={"username": username, "password": password},
    )
    token = envelope.get("data", {}).get("token")
    if not token:
        raise ApiError("Login succeeded but no token was returned.", body=envelope)
    return token, envelope


def request_authed(base_url: str, token: str, path: str, *, method: str = "GET", body: dict[str, Any] | None = None) -> Any:
    return http_json(
        f"{base_url}{path}",
        method=method,
        headers={"Authorization": f"Bearer {token}"},
        body=body,
    )


def infer_time_bucket(local_time: str | None) -> str:
    if not local_time:
        return "当前时段"
    try:
        hour = int(local_time.split(":", 1)[0])
    except Exception:
        return "当前时段"
    if 5 <= hour < 7:
        return "黎明时分"
    if 7 <= hour < 10:
        return "上午时段"
    if 10 <= hour < 16:
        return "日间时段"
    if 16 <= hour < 18:
        return "傍晚前段"
    if 18 <= hour < 20:
        return "傍晚蓝调时刻"
    if 20 <= hour <= 23:
        return "夜间时段"
    return "凌晨或深夜"


def infer_light_phrase(local_time: str | None) -> str:
    bucket = infer_time_bucket(local_time)
    mapping = {
        "黎明时分": "接近日出前后的冷色自然光，天空微亮",
        "上午时段": "清晨到上午的自然光，光线方向明确但不过曝",
        "日间时段": "日间自然光，能见度高，层次清晰",
        "傍晚前段": "下午转傍晚的自然光，光线逐渐降低",
        "傍晚蓝调时刻": "已接近日落后或刚过日落的蓝调暮光，绝不是正午强光",
        "夜间时段": "夜间环境光与少量人工照明并存，天空较暗",
        "凌晨或深夜": "深夜或黎明前的低照度环境，天空较暗",
    }
    return mapping.get(bucket, "符合当前本地时段的自然光线")


def infer_weather_phrase(summary: str) -> str:
    text = summary or ""
    clauses: list[str] = []
    if "雨" in text:
        clauses.append("地面或石阶可见雨后湿润反光，空气略有潮润感")
    if "雪" in text:
        clauses.append("场景体现降雪或积雪后的寒冷质感")
    if "雾" in text or "霾" in text:
        clauses.append("远景能见度下降，空气中有明显朦胧感")
    if "多云" in text:
        clauses.append("天空保留明显云层结构")
    if "阴" in text:
        clauses.append("整体以漫射光为主，阴天感明确")
    if "晴" in text:
        clauses.append("云层正在散开或已经放晴，空气通透")
    if not clauses:
        clauses.append("场景必须符合当前天气摘要，不能是通用明信片式天气")
    return "，".join(clauses)


def build_subject_clause(subject: str, subject_type: str) -> str:
    if not subject:
        return "以与当地高度相关的地标、历史场所、自然景观或城市人物场景为主体"
    if subject_type == "person":
        return f"以{subject}这一与当地高度相关的历史人物为核心形象，并置于具有城市识别度的纪念空间、塑像场景或历史环境中"
    return f"以{subject}这一与当地高度相关的真实场景为主体"


def build_text_blocks(args: argparse.Namespace) -> tuple[str, str, str, str]:
    title = args.title or f"{args.city_name}天气预报"
    subtitle = args.subtitle or f"{args.date}  {args.weather_summary}"
    info_bits = []
    if args.local_time:
        info_bits.append(f"当前时间 {args.local_time}")
    if args.temp_range:
        info_bits.append(args.temp_range)
    info_line = args.info_line or "  ".join(info_bits)
    corner = args.corner_text or (args.wind or "")
    return title, subtitle, info_line, corner


def build_prompt(args: argparse.Namespace) -> str:
    if args.prompt_mode == "background":
        return build_background_prompt(args)

    return build_full_poster_prompt(args)


def build_full_poster_prompt(args: argparse.Namespace) -> str:
    time_bucket = infer_time_bucket(args.local_time)
    light_phrase = infer_light_phrase(args.local_time)
    weather_phrase = infer_weather_phrase(args.weather_summary)
    subject_clause = build_subject_clause(args.subject, args.subject_type)
    title, subtitle, info_line, corner = build_text_blocks(args)

    text_requirements = [
        f"主标题“{title}”",
        f"副标题“{subtitle}”",
    ]
    if info_line:
        text_requirements.append(f"说明文字“{info_line}”")
    if corner:
        text_requirements.append(f"角落小字“{corner}”")

    return (
        f"{subject_clause}，为{args.city_name}制作天气预报封面。"
        f"时间设定为{args.date} {args.local_time or '当前本地时间'}，属于{time_bucket}。"
        f"天气摘要为“{args.weather_summary}”，{weather_phrase}。"
        f"画面光线要求：{light_phrase}。"
        f"整体风格为高端自然地理纪实杂志封面风格，但不要出现任何真实杂志名称或 logo。"
        f"必须是真实摄影质感、写实、超高细节、构图克制、颜色自然、层次清晰，背景内容要体现{args.city_name}的地方身份，不能像通用旅游海报。"
        f"如果主体是人物，人物造型要庄重可信，并与城市历史语境一致。"
        f"画面加入清晰可读的中文排版文字：{'，'.join(text_requirements)}。"
        f"中文排版要高级、简洁、有信息设计感，留出封面排版空间，竖版封面构图，{args.resolution.upper()}，比例 {args.ratio}。"
    )


def build_background_prompt(args: argparse.Namespace) -> str:
    time_bucket = infer_time_bucket(args.local_time)
    light_phrase = infer_light_phrase(args.local_time)
    weather_phrase = infer_weather_phrase(args.weather_summary)
    subject_clause = build_subject_clause(args.subject, args.subject_type)
    return (
        f"{subject_clause}，服务于{args.city_name}天气预报封面的背景图。"
        f"时间设定为{args.date} {args.local_time or '当前本地时间'}，属于{time_bucket}。"
        f"天气摘要为“{args.weather_summary}”，{weather_phrase}。"
        f"画面光线要求：{light_phrase}。"
        f"只生成背景画面，不要出现任何文字、字母、logo、水印、标题或排版元素。"
        f"整体为高端自然地理纪实杂志封面风格，真实摄影质感，写实，超高细节，构图克制，颜色自然，层次清晰，突出{args.city_name}地方身份。"
        f"竖版封面背景图，比例 {args.ratio}，{args.resolution.upper()}。"
    )


def ensure_ready_for_submit(args: argparse.Namespace) -> None:
    missing = []
    for field in ["date", "weather_summary", "subject"]:
        if not getattr(args, field):
            missing.append(field)
    if missing:
        raise SystemExit(f"--submit requires these fields to be provided: {', '.join(missing)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and optionally submit a city weather cover image prompt.")
    parser.add_argument("city_name", help="City name to appear in the cover.")
    parser.add_argument("--date", help="Exact local date, e.g. 2026年4月3日 or 2026-04-03")
    parser.add_argument("--local-time", help="Exact local time, e.g. 19:17")
    parser.add_argument("--weather-summary", help="Verified weather summary for the current period.")
    parser.add_argument("--temp-range", help="Verified temperature range, e.g. 12℃~16℃")
    parser.add_argument("--wind", help="Verified wind text, e.g. 南风 3-4级")
    parser.add_argument("--subject", help="Local landmark, landscape, heritage site, or historical figure.")
    parser.add_argument("--subject-type", choices=["landmark", "landscape", "heritage", "person"], default="landmark")
    parser.add_argument("--title", help="Override main Chinese title.")
    parser.add_argument("--subtitle", help="Override subtitle.")
    parser.add_argument("--info-line", help="Override info line.")
    parser.add_argument("--corner-text", help="Override corner text.")
    parser.add_argument("--prompt-mode", choices=["full", "background"], default="full")
    parser.add_argument("--ratio", default="3:4")
    parser.add_argument("--resolution", default="4k")
    parser.add_argument("--base-url", help="Image API host, with or without /api.")
    parser.add_argument("--token", help="Bearer token.")
    parser.add_argument("--username", help="Username for login fallback.")
    parser.add_argument("--password", help="Password for login fallback.")
    parser.add_argument("--auth-file", help="Session file path.")
    parser.add_argument("--submit", action="store_true", help="Submit the generation task.")
    parser.add_argument("--wait", action="store_true", help="Poll until the task reaches a terminal state.")
    parser.add_argument("--poll-interval", type=float, default=10.0, help="Polling interval in seconds.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt = build_prompt(args)
    result: dict[str, Any] = {
        "city_name": args.city_name,
        "date": args.date,
        "local_time": args.local_time,
        "weather_summary": args.weather_summary,
        "temp_range": args.temp_range,
        "wind": args.wind,
        "subject": args.subject,
        "subject_type": args.subject_type,
        "ratio": args.ratio,
        "resolution": args.resolution,
        "prompt": prompt,
    }

    if not args.submit:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    ensure_ready_for_submit(args)

    session = load_session(args.auth_file or os.getenv("GENIMAGE_AUTH_FILE"))
    base_url = args.base_url or os.getenv("GENIMAGE_BASE_URL") or session.base_url
    if not base_url:
        raise SystemExit("Missing image API base URL. Pass --base-url or set GENIMAGE_BASE_URL.")
    base_url = normalize_base_url(base_url)

    token = args.token or os.getenv("GENIMAGE_TOKEN") or session.token
    username = args.username or os.getenv("GENIMAGE_USERNAME")
    password = args.password or os.getenv("GENIMAGE_PASSWORD")

    login_envelope = None
    if not token:
        if not username or not password:
            raise SystemExit("Missing token and no username/password fallback is available.")
        token, login_envelope = login(base_url, username, password)

    if login_envelope:
        result["login"] = login_envelope

    create_envelope = request_authed(
        base_url,
        token,
        "/tasks/generate",
        method="POST",
        body={
            "prompt": prompt,
            "ratio": args.ratio,
            "resolution": args.resolution,
        },
    )
    result["task_create"] = create_envelope

    task_data = create_envelope.get("data", {})
    task_id = task_data.get("id")
    if not args.wait or not task_id:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    while True:
        poll_envelope = request_authed(base_url, token, f"/tasks/{task_id}/poll", method="POST")
        result["task_poll"] = poll_envelope
        status = poll_envelope.get("data", {}).get("status")
        if status in TERMINAL_STATUSES:
            break
        time.sleep(args.poll_interval)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ApiError as error:
        payload = {"error": str(error), "status": error.status, "body": error.body}
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit(1)
