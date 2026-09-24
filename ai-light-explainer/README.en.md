[中文](README.md) | **English**

# AI Light Explainer

An AI Agent Skill that turns AI concepts into short-form Chinese explainers — illustrated carousels, animated videos, and publishing copy — in a fixed series visual style. Written for readers curious about AI who don't necessarily code: everyday examples, accurate mechanics, no hype.

## Visual style

Warm white background, dark gray text, terracotta-orange accents, thin-line windows. Carousels are 3:4, videos 9:16, no voiceover, light typing/transition sounds.

![Reference cover](assets/reference-cover.png)

![Reference video](assets/reference-video.mp4)

*Reference cover and video: episode 1, "What is Jev?" — concept animation, not real model output.*

## Layout

```text
ai-light-explainer/
├── SKILL.md                      # Skill entry: content principles, workflow, QA standards
├── references/
│   ├── visual-system.md          # Visual spec: colors, type sizes, motion grammar
│   └── production.md             # Production, migration, and delivery process
├── assets/
│   ├── reference-cover.png       # Reference cover
│   ├── reference-video.mp4       # Reference video (47 s)
│   └── reference-project/        # Editable render project (Python, fully local)
└── agents/openai.yaml            # Optional client metadata
```

## Install

```bash
npx skills@latest add voidning/skills --skill ai-light-explainer
```

Alternatively, drop the whole `ai-light-explainer/` directory into your tool's skills folder. No specific model or client required.

## Usage

After installing, tell your agent:

```text
Use this skill for the next episode on how agents work — both carousel and video.
```

The skill reuses the confirmed topic, audience, and style, and only asks about gaps that would change direction.

## Reference project

`assets/reference-project/render.py` reproduces the reference video's styling, typing animation, probability bars, and sounds (dependencies in `requirements.txt`, rendered fully locally, no API calls). It is a finished example, not a generic generation engine — copy it into your working directory and rewrite it for your topic.

## License

See the repo root [LICENSE](../LICENSE).
