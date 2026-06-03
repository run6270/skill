#!/usr/bin/env bash
set -euo pipefail

DEFAULT_VAULT="/Users/mac/Documents/obsidian-demo"
DEFAULT_NOTEBOOK="AI笔记"
PLAYWRIGHT_CLI="/Users/mac/.codex/skills/playwright/scripts/playwright_cli.sh"
X_COOKIES_JSON="/Users/mac/Library/Application Support/baoyu-skills/x-to-markdown/cookies.json"

usage() {
  echo "Usage: clip_url_to_obsidian.sh <url> [vault_abs_path] [notebook_rel_path]" >&2
}

if [ "$#" -lt 1 ]; then
  usage
  exit 1
fi

URL="$1"
VAULT="${2:-$DEFAULT_VAULT}"
NOTEBOOK_REL="${3:-$DEFAULT_NOTEBOOK}"
TMP_HTML=""
PW_SESSION=""
SNAPSHOT_FILE=""

cleanup() {
  if [ -n "$TMP_HTML" ] && [ -f "$TMP_HTML" ]; then
    rm -f "$TMP_HTML"
  fi
  if [ -n "$SNAPSHOT_FILE" ] && [ -f "$SNAPSHOT_FILE" ]; then
    rm -f "$SNAPSHOT_FILE"
  fi
  if [ -n "$PW_SESSION" ]; then
    bash "$PLAYWRIGHT_CLI" --session "$PW_SESSION" close >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

json_unquote() {
  python3 - <<'PY'
import json, sys
raw = sys.stdin.read().strip()
if not raw or raw == 'null':
    print('')
else:
    try:
        value = json.loads(raw)
    except Exception:
        print(raw)
    else:
        if value is None:
            print('')
        else:
            print(value)
PY
}

find_fallback_vault() {
  python3 - "$NOTEBOOK_REL" <<'PY'
from pathlib import Path
import sys

desired = sys.argv[1]
home = Path.home()
search_roots = [home / 'Documents', home]
candidates = []

for root in search_roots:
    if not root.exists():
        continue
    for dot_obsidian in root.rglob('.obsidian'):
        if dot_obsidian.is_dir():
            vault = dot_obsidian.parent
            score = 0
            if (vault / desired).exists():
                score += 10
            if (vault / 'AI笔记').exists():
                score += 5
            candidates.append((score, str(vault)))

if not candidates:
    sys.exit(1)

candidates.sort(key=lambda item: (-item[0], item[1]))
print(candidates[0][1])
PY
}

resolve_vault() {
  if [ -d "$VAULT" ]; then
    return 0
  fi

  if fallback="$(find_fallback_vault 2>/dev/null)"; then
    VAULT="$fallback"
    return 0
  fi

  echo "Vault path not found: $VAULT" >&2
  exit 1
}

resolve_notebook_rel() {
  NOTEBOOK_REL="$(python3 - "$VAULT" "$NOTEBOOK_REL" <<'PY'
from pathlib import Path
import re
import sys

vault = Path(sys.argv[1])
desired = sys.argv[2].strip('/')
if not desired:
    print('AI笔记')
    raise SystemExit

if '/' in desired:
    print(desired)
    raise SystemExit


def norm(s: str) -> str:
    return re.sub(r'\s+', '', s)

for child in vault.iterdir():
    if child.is_dir() and norm(child.name) == norm(desired):
        print(child.name)
        raise SystemExit

print(desired)
PY
)"
}

sanitize_filename() {
  TITLE_RAW="$1" python3 - <<'PY'
import os
import re

title = os.environ['TITLE_RAW'].strip()
title = re.sub(r'[\\/:*?"<>|]', '-', title)
title = ''.join(ch for ch in title if ord(ch) >= 32)
title = re.sub(r'\s+', ' ', title).strip()
if not title:
    title = 'untitled'
print(title)
PY
}

next_target_path() {
  local out_dir="$1"
  local filename="$2"
  local target="$out_dir/$filename.md"
  if [ ! -e "$target" ]; then
    printf '%s\n' "$target"
    return 0
  fi
  local i=1
  while [ -e "$out_dir/$filename ($i).md" ]; do
    i=$((i + 1))
  done
  printf '%s\n' "$out_dir/$filename ($i).md"
}

normalize_markdown_images() {
  local markdown_file="$1"
  perl -0pi -e '
    s{
      !\[
      (.*?)
      \]
      \(
      ([^)]+)
      \)
    }{
      my $alt = $1;
      my $path = $2;
      $alt =~ s/\s+/ /g;
      $alt =~ s/^\s+|\s+$//g;
      "![$alt]($path)";
    }egsx;
  ' "$markdown_file"
}

localize_remote_images() {
  local markdown_file="$1"
  local out_dir="$2"
  local asset_dir_name="$3"
  local asset_dir="$out_dir/_assets/$asset_dir_name"
  local downloaded=0

  mkdir -p "$asset_dir"

  local image_urls=()
  while IFS= read -r line; do
    if [ -n "$line" ]; then
      image_urls+=("$line")
    fi
  done < <(perl -0ne 'while (/!\[.*?\]\((https?:\/\/[^)]+)\)/sg) { print "$1\n"; }' "$markdown_file" | awk '!seen[$0]++')

  if [ "${#image_urls[@]}" -eq 0 ]; then
    rmdir "$asset_dir" 2>/dev/null || true
    return 0
  fi

  for img_url in "${image_urls[@]}"; do
    local raw_name="${img_url##*/}"
    raw_name="${raw_name%%\?*}"
    if [ -z "$raw_name" ] || [ "$raw_name" = "$img_url" ]; then
      raw_name="image"
    fi

    local local_name
    local_name="$(printf '%s' "$raw_name" | perl -pe 's/[^A-Za-z0-9._-]+/_/g')"
    if [ -z "$local_name" ]; then
      local_name="image"
    fi

    local stem="$local_name"
    local ext=""
    if [[ "$local_name" == *.* ]]; then
      stem="${local_name%.*}"
      ext=".${local_name##*.}"
    fi

    local candidate="$local_name"
    local suffix=2
    while [ -e "$asset_dir/$candidate" ]; do
      candidate="${stem}-${suffix}${ext}"
      suffix=$((suffix + 1))
    done

    if curl -L --fail --silent --show-error "$img_url" -o "$asset_dir/$candidate"; then
      perl -0pi -e 's#\Q'"$img_url"'\E#<_assets/'"$asset_dir_name"'/'"$candidate"'>#g' "$markdown_file"
      downloaded=$((downloaded + 1))
    else
      rm -f "$asset_dir/$candidate"
    fi
  done

  if [ "$downloaded" -eq 0 ]; then
    rmdir "$asset_dir" 2>/dev/null || true
  fi
}

extract_title_from_html() {
  TMP_HTML="$1" python3 - <<'PY'
import html
import os
import re
from html.parser import HTMLParser

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_title = False
        self.title = ''
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'title':
            self._in_title = True
    def handle_endtag(self, tag):
        if tag.lower() == 'title':
            self._in_title = False
    def handle_data(self, data):
        if self._in_title:
            self.title += data

with open(os.environ['TMP_HTML'], 'r', encoding='utf-8', errors='ignore') as f:
    data = f.read()

parser = TitleParser()
parser.feed(data)
title = html.unescape(parser.title).strip()
title = re.sub(r'\s+', ' ', title)
print(title)
PY
}

pw() {
  bash "$PLAYWRIGHT_CLI" --session "$PW_SESSION" "$@"
}

load_x_cookies() {
  if [ ! -f "$X_COOKIES_JSON" ]; then
    return 0
  fi

  while IFS=$'\t' read -r name value; do
    [ -n "$name" ] || continue
    for domain in .x.com .twitter.com; do
      args=(cookie-set "$name" "$value" --domain "$domain" --path / --secure --sameSite Lax)
      if [ "$name" = "auth_token" ]; then
        args+=(--httpOnly)
      fi
      pw "${args[@]}" >/dev/null </dev/null
    done
  done < <(python3 - "$X_COOKIES_JSON" <<'PY'
import json
import sys

obj = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
for key, value in obj.get('cookieMap', {}).items():
    print(f"{key}\t{value}")
PY
)
}

render_x_markdown() {
  python3 - "$1" <<'PY'
import json
import re
import sys

body = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
lines = [line.strip() for line in body.splitlines()]
out = []
for line in lines:
    if not line:
        continue
    if re.match(r'^[一二三四五六七八九十]+、', line):
        out.append(f'## {line}')
    else:
        out.append(line)
    out.append('')
print('\n'.join(out).rstrip())
PY
}

clip_x_url() {
  require_cmd python3
  require_cmd npx

  if [ ! -f "$PLAYWRIGHT_CLI" ]; then
    echo "Playwright wrapper not found: $PLAYWRIGHT_CLI" >&2
    exit 1
  fi

  PW_SESSION="x${RANDOM}$$"
  local tmp_body_json
  tmp_body_json="$(mktemp -t obsidian_x_body_XXXXXX).json"

  pw open https://x.com >/dev/null
  pw cookie-clear >/dev/null
  load_x_cookies
  pw goto "$URL" >/dev/null

  local body=""
  local raw=""
  local title_raw=""
  local focus_url=""
  local author_line=""
  local published_at=""
  local i

  for i in 1 2 3 4 5 6 7 8; do
    raw="$(pw --raw eval 'document.querySelector(".public-DraftEditor-content > div")?.innerText || ""' 2>/dev/null || true)"
    body="$(printf '%s' "$raw" | json_unquote)"
    if [ -n "$body" ]; then
      break
    fi
    sleep 2
  done

  if [ -z "$body" ]; then
    echo "Failed to extract article body from X via Playwright: $URL" >&2
    exit 1
  fi

  title_raw="$(pw --raw eval '(() => { const t = document.title || ""; const m = t.match(/"([^"]+)"/); return (m && m[1]) ? m[1] : t.replace(/\s*\/ X$/, "").trim(); })()' 2>/dev/null | json_unquote)"
  if [ -z "$title_raw" ] || [ "$title_raw" = "X" ]; then
    title_raw="$(printf '%s\n' "$body" | sed -n '1p')"
  fi

  focus_url="$(pw --raw eval 'document.querySelector("a[href*=\"/article/\"]")?.href || ""' 2>/dev/null | json_unquote)"
  author_line="$(pw --raw eval 'document.querySelector("article a[href^=\"/\"] span")?.textContent || ""' 2>/dev/null | json_unquote)"
  published_at="$(pw --raw eval 'document.querySelector("time")?.textContent || ""' 2>/dev/null | json_unquote)"

  local filename
  filename="$(sanitize_filename "$title_raw")"
  local target
  target="$(next_target_path "$OUT_DIR" "$filename")"
  local note_stem
  note_stem="$(basename "$target" .md)"
  local asset_dir="$OUT_DIR/_assets/$note_stem"
  mkdir -p "$asset_dir"

  printf '%s' "$raw" > "$tmp_body_json"
  local body_md
  body_md="$(render_x_markdown "$tmp_body_json")"

  SNAPSHOT_FILE="$(mktemp -t obsidian_x_snapshot_XXXXXX.txt)"
  pw snapshot > "$SNAPSHOT_FILE" 2>/dev/null || true
  local image_ref=""
  image_ref="$(python3 - "$SNAPSHOT_FILE" <<'PY'
import re
import sys
text = open(sys.argv[1], 'r', encoding='utf-8', errors='ignore').read()
for pattern in [r'img "Image" \[ref=(e\d+)\]', r'link "Image" \[ref=(e\d+)\]']:
    m = re.search(pattern, text)
    if m:
        print(m.group(1))
        raise SystemExit
print('')
PY
)"

  local cover_md=""
  if [ -n "$image_ref" ]; then
    local screenshot_out
    screenshot_out="$(pw screenshot "$image_ref" 2>/dev/null || true)"
    local screenshot_path
    screenshot_path="$(printf '%s' "$screenshot_out" | python3 - <<'PY'
import re, sys
text = sys.stdin.read()
m = re.search(r'\[Screenshot of element\]\(([^)]+)\)', text)
print(m.group(1) if m else '')
PY
)"
    if [ -n "$screenshot_path" ] && [ -f "$screenshot_path" ]; then
      cp "$screenshot_path" "$asset_dir/cover.png"
      cover_md='![](<_assets/'"$note_stem"'/cover.png>)'
    fi
  fi

  cat > "$target" <<EOF_NOTE
---
source_url: "$URL"
article_title: "$title_raw"
article_author: "${author_line:-}"
article_published_at: "${published_at:-}"
focus_mode_url: "$focus_url"
saved_at: "$(date +%F)"
captured_via: "Playwright"
notes: "X 链接已优先通过 Playwright 抓取；若存在登录 cookie，则自动复用。"
---

# $title_raw

原始链接：<$URL>

EOF_NOTE

  if [ -n "$focus_url" ]; then
    cat >> "$target" <<EOF_NOTE
X Article：<$focus_url>

EOF_NOTE
  fi

  cat >> "$target" <<EOF_NOTE
抓取方式：Playwright 打开 X 页面并提取正文。

EOF_NOTE

  if [ -n "$cover_md" ]; then
    printf '%s\n\n' "$cover_md" >> "$target"
  fi

  cat >> "$target" <<EOF_NOTE
---

$body_md
EOF_NOTE

  rm -f "$tmp_body_json"
  echo "$target"
}

clip_generic_url() {
  require_cmd curl
  require_cmd pandoc

  TMP_HTML="$(mktemp -t obsidian_clip_XXXXXX).html"
  curl -L --fail --silent --show-error "$URL" -o "$TMP_HTML"

  local title_raw
  title_raw="$(extract_title_from_html "$TMP_HTML")"
  if [ -z "$title_raw" ]; then
    title_raw="untitled"
  fi

  local filename
  filename="$(sanitize_filename "$title_raw")"
  local target
  target="$(next_target_path "$OUT_DIR" "$filename")"

  pandoc "$TMP_HTML" -f html -t gfm -o "$target"
  normalize_markdown_images "$target"
  localize_remote_images "$target" "$OUT_DIR" "$filename"
  echo "$target"
}

resolve_vault
resolve_notebook_rel
OUT_DIR="$VAULT/$NOTEBOOK_REL"
mkdir -p "$OUT_DIR"

case "$URL" in
  https://x.com/*|http://x.com/*|https://twitter.com/*|http://twitter.com/*)
    clip_x_url
    ;;
  *)
    clip_generic_url
    ;;
esac
