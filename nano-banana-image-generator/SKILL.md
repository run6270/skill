---
name: nano-banana-image-generator
description: Use this skill to generate images using Nano Banana Pro (Gemini image generation). This skill should be used when the user asks to create, generate, or make an image, illustration, artwork, or visual content. The generated images are automatically saved to the public images folder.
---

# Nano Banana Image Generator

## Overview

This skill enables AI-powered image generation using Nano Banana Pro (powered by Gemini). Generated images are automatically saved to the user's public images folder for easy access.

## When to Use

- User asks to "generate an image of..."
- User asks to "create a picture of..."
- User asks to "make an illustration of..."
- User wants visual content created from a text description
- User mentions "Nano Banana" for image generation

## Workflow

### Step 1: Generate the Image

Use the Composio/Rube MCP tools to generate the image:

1. Call `RUBE_SEARCH_TOOLS` with the query "generate images using nano banana" to get session ID
2. Call `RUBE_MULTI_EXECUTE_TOOL` with tool_slug `GEMINI_GENERATE_IMAGE`

**Tool Parameters:**
- `prompt` (required): The text description of the image to generate
- `model`: Use `gemini-3-pro-image-preview` for Nano Banana Pro (default, best quality with 4K support)
- `aspect_ratio`: Options include `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, etc.
- `image_size`: For Nano Banana Pro, options are `1K`, `2K`, or `4K`

**Example execution:**
```
RUBE_MULTI_EXECUTE_TOOL with:
  tool_slug: "GEMINI_GENERATE_IMAGE"
  arguments: {
    "prompt": "A cute cat wearing sunglasses on a beach",
    "model": "gemini-3-pro-image-preview",
    "aspect_ratio": "16:9",
    "image_size": "2K"
  }
```

The tool returns a public S3 URL with the generated image.

### Step 2: Download and Save to Public Folder

After receiving the image URL from the generation tool:

1. Download the image using `curl` or `wget`
2. Save it to the public images folder: `/Users/mac/Public/images/`
3. Use a descriptive filename based on the prompt (e.g., `cat-sunglasses-beach.png`)

**Example:**
```bash
curl -o "/Users/mac/Public/images/cat-sunglasses-beach.png" "<generated-image-url>"
```

### Step 3: Confirm to User

After saving:
1. Confirm the image was generated and saved
2. Provide the local file path
3. Optionally display the image if in a supported environment

## Important Notes

- Always set `sync_response_to_workbench: false` when calling `RUBE_MULTI_EXECUTE_TOOL` for image generation
- The public images folder is `/Users/mac/Public/images/` - create it if it doesn't exist
- Use descriptive, kebab-case filenames derived from the prompt
- The Gemini connection is already active and ready to use
