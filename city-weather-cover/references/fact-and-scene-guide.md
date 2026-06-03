# Fact And Scene Guide

## Minimum Verified Facts

Before generation, verify:

- city name spelling
- exact current date
- exact local time
- weather summary for the current period
- temperature range or current-band temperature
- wind if available
- sunrise / sunset if lighting is near dawn or dusk

## Anchor Selection Heuristics

Choose the anchor with the strongest combination of:

- local recognizability
- visual richness
- compatibility with the current weather
- compatibility with the current time of day

Good examples:

- mountains, rivers, gates, walls, pagodas, bridges, temple complexes, observatories
- historic streets, old towns, memorial halls, museums, plazas
- local statues, former residences, or scholarly settings for a city-defining historical figure

Weak examples:

- generic skyline with no local identifiers
- random park with no city linkage
- historical figure portrait with no city-specific setting

## Historical Figure Rule

Use a historical figure only when at least one of these is true:

- the city is widely identified with that person
- the city contains a famous memorial, former residence, tomb, academy, or statue related to that person
- the user explicitly asks for a people-centered version

When using a historical figure, keep the composition plausible:

- outdoor statue or memorial under the current sky
- former residence courtyard with present weather conditions
- museum or study reconstruction with visible time-of-day lighting through windows

## Time-To-Lighting Cheatsheet

- `05:00-07:00`: dawn, cool blue light, low sun if clear
- `07:00-10:00`: fresh morning light
- `10:00-16:00`: day scene
- `16:00-18:00`: late afternoon
- `18:00-20:00`: dusk / blue hour depending on season and sunset
- `20:00-05:00`: night

If sunset has passed, bias strongly toward dusk or night. Use practical lights sparingly and realistically.

## Weather-To-Surface Cheatsheet

- rain: wet stone, reflective pavement, damp air, umbrellas only if composition benefits
- after rain: clean air, reflective ground, clouds breaking
- snow: snow accumulation, cold air clarity or snowfall haze
- fog: softened distance, limited horizon detail
- clear: high visibility, sharper edges, stronger tonal separation

## Chinese Text Pattern

Default layout pattern:

- main title: `CITY_NAME天气预报`
- subtitle: `YYYY年M月D日  天气摘要`
- info line: `当前时间 HH:MM  温度范围`
- corner line: `风向 风力`

Keep the typography restrained and editorial. Avoid loud ad-like slogans.
