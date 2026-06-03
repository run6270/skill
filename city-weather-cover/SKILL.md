---
name: city-weather-cover
description: Generate a natural-geography-style city weather cover image from a city name. Use when the user gives a city and wants a weather poster, weather cover, 天气预报图, 城市封面图, or similar output that must match the city's current local weather and time of day, use Chinese text, and feature a locally resonant landmark, landscape, heritage site, or historically significant figure.
---

# City Weather Cover

Turn one city name into a finished weather cover image with no user back-and-forth in the normal path.

## Default Behavior

When this skill triggers, do the work end-to-end. Do not stop to ask the user to confirm ordinary choices such as source selection, subject selection, prompt wording, or whether to retry with a simpler generation path.

The user should be able to say only:

- `给我做一个临汾的天气预报图片`
- `做一个南京天气预报封面`
- `做一个西安天气海报`

Then return the final image directly.

## Zero-Confirmation Workflow

1. Verify the city's current local weather and local time.
2. Pick the strongest local anchor automatically.
3. Build a Chinese poster prompt automatically.
4. Try a direct poster generation once.
5. If the image API rejects the poster prompt, automatically switch to the fallback path:
   - generate a clean background-only image
   - download the background
   - compose the Chinese weather poster locally with `scripts/compose_weather_poster.py`
6. Return the final poster image, not the intermediate steps.

If the normal path works, do not mention the fallback. If the fallback was needed, mention it briefly only after delivering the result.

## Fact Gathering

Always browse for up-to-date facts. Do not guess today's weather, today's wind, or the current local time.

Prefer this source order:

- China: official or primary weather pages such as `weather.com.cn` `weather1d` pages, then local meteorological or tourism sites if needed.
- Other countries: official meteorological services first, then major weather providers if an official source is unavailable.
- Visual identity: official tourism sites, museum pages, local government pages, encyclopedic references, or multiple corroborating reputable sources.

Collect these facts:

- Exact date
- Local time in the target city
- Weather summary for the current period, not only the day-level forecast
- Temperature range for the current period or day
- Wind direction / force if available
- Sunrise / sunset when lighting is sensitive
- One strong local visual anchor

Also capture one or two sources that can support the final answer.

## Visual Anchor Rules

Prefer, in order:

1. A landmark or landscape strongly associated with the city
2. A historic district, old street, riverfront, mountain, temple, bridge, gate, memorial, or museum with strong local identity
3. A historically significant local figure only when that person is central to the city's identity

Pick automatically. Do not ask the user to choose unless they explicitly request a specific subject.

If using a historical figure:

- Place the figure inside a city-specific environment, memorial, statue, mural, study, or heritage context
- Still make the sky, lighting, and atmosphere match the verified current weather and time
- Avoid generic portrait backdrops with no city identity

## Weather Fidelity Rules

The background must reflect the verified current period, not a generic daytime postcard.

Translate facts into visible cues:

- `晴`: direct light, clearer air, stronger contrast
- `多云`: visible cloud structure, softer direct light
- `阴`: diffuse light, flatter shadows, cooler sky
- `小雨` or `雨后`: wet ground, puddle reflections, haze or low cloud, softened contrast
- `雾` or `霾`: reduced distance clarity, atmospheric depth loss
- `雪`: snow cover, cold diffuse light, winter surface cues

Translate time into visible cues:

- Before sunrise: dim pre-dawn blue light
- Morning: low-angle warm or cool sunlight depending on cloud cover
- Midday / afternoon: higher light angle, brighter surfaces
- Around sunset: warm side light if clear enough
- After sunset: blue-hour or early-night ambience, practical lights visible where appropriate
- Night: artificial lighting, darker sky, realistic visibility limits

If the current local time is after sunset, do not generate a bright daytime scene.

## Prompt And Generation

Use `scripts/city_weather_cover.py` to generate the prompt text.

Use `scripts/genimage_task.mjs` for live task submission because this API path has been more reliable than direct Python requests.

Direct poster attempt:

```bash
python3 scripts/city_weather_cover.py "CITY_NAME" \
  --date "2026-04-03" \
  --local-time "19:17" \
  --weather-summary "多云转晴" \
  --temp-range "12℃~16℃" \
  --wind "南风 3-4级" \
  --subject "牛山国家森林公园" \
  --subject-type landmark \
  > /tmp/city-cover-prompt.json

node scripts/genimage_task.mjs generate \
  --base-url "$GENIMAGE_BASE_URL" \
  --prompt "$(jq -r .prompt /tmp/city-cover-prompt.json)" \
  --ratio 3:4 \
  --resolution 4k \
  --wait
```

If direct poster generation fails or the model produces poor text rendering, immediately switch to background-only mode:

```bash
python3 scripts/city_weather_cover.py "CITY_NAME" \
  --prompt-mode background \
  --date "2026-04-03" \
  --local-time "19:17" \
  --weather-summary "多云转晴" \
  --temp-range "12℃~16℃" \
  --wind "南风 3-4级" \
  --subject "牛山国家森林公园" \
  --subject-type landmark \
  > /tmp/city-cover-background.json

node scripts/genimage_task.mjs generate \
  --base-url "$GENIMAGE_BASE_URL" \
  --prompt "$(jq -r .prompt /tmp/city-cover-background.json)" \
  --ratio 3:4 \
  --resolution 4k \
  --wait
```

Then compose the final poster locally:

```bash
python3 scripts/compose_weather_poster.py \
  --background-url "BACKGROUND_IMAGE_URL" \
  --download-to "output/city-weather/city-bg.png" \
  --output "output/city-weather/city-poster.png" \
  --city-name "CITY_NAME" \
  --date-text "2026年4月3日" \
  --weather-summary "多云转晴" \
  --local-time "19:17" \
  --temp-range "12℃~16℃" \
  --wind "南风 3-4级" \
  --caption "CITY_NAME · SUBJECT"
```

`city_weather_cover.py`:

- Builds a Chinese prompt in natural-geography magazine style
- Forces weather/time fidelity into the scene description
- Supports `--prompt-mode full` and `--prompt-mode background`

`compose_weather_poster.py`:

- Downloads the background image if needed
- Draws a clean editorial weather panel with Chinese text
- Produces a final PNG poster automatically

## API Configuration

`genimage_task.mjs` supports these inputs for the image API:

- `GENIMAGE_BASE_URL`
- `GENIMAGE_TOKEN`
- `GENIMAGE_USERNAME`
- `GENIMAGE_PASSWORD`
- `GENIMAGE_AUTH_FILE`

Token lookup order:

1. `--token`
2. `GENIMAGE_TOKEN`
3. Saved session file from `GENIMAGE_AUTH_FILE`
4. `./.genimage/session.json`
5. `~/.genimage/session.json`

If no token is available but username and password are present, the script logs in first and saves the session.

## Runtime Dependencies

Local composition uses Pillow.

If Pillow is missing, create a workspace-local venv and install it automatically rather than asking first:

```bash
python3 -m venv .skill-venv
.skill-venv/bin/pip install Pillow PyYAML
```

Use that venv for local composition and validation.

## Output Requirements

Return:

- The final image first
- The verified weather facts
- The chosen local anchor
- The source links

Prefer delivering the finished poster directly. Keep process notes brief.

If the first image uses the wrong lighting or weather mood, retry automatically with a stricter background prompt rather than asking the user what to do next.

## References

- Read `references/fact-and-scene-guide.md` when choosing anchors or mapping weather/time into imagery.
- Use `scripts/city_weather_cover.py --help`, `node scripts/genimage_task.mjs`, and `python3 scripts/compose_weather_poster.py --help` to inspect the automation surface.
