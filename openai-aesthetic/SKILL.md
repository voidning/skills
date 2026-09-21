---
name: openai-aesthetic
description: Apply the OpenAI visual design language to web pages, UI components, and documents. Use when asked to "make it look like OpenAI", "apply OpenAI design", "OpenAI style", or similar.
metadata:
  author: agent
  version: "1.2.0"
  sources:
    - https://styles.refero.design/style/dc541737-8bf2-4b31-b729-0352f696e82f
    - https://styles.refero.design/style/5c94c49f-0612-4261-842c-e1d501f3e13d
    - https://developers.openai.com
    - https://openai.com/zh-Hans-CN/brand/
  related-skills:
    - test-guide-html
---

# OpenAI Aesthetic

Apply the OpenAI visual design language. This is a monochrome-first, editorial, restrained system. Trust whitespace and typography; avoid decoration. One muted accent color is permitted — use it sparingly.

## When to Use

Use this skill when the user asks for:
- "make it look like OpenAI"
- "OpenAI style"
- "OpenAI design"
- "apply OpenAI aesthetic"
- Clean, research-lab, documentation-style UI

## Application Workflow

When triggered:

1. Determine the surface: **consumer/marketing** (openai.com) or **developers/docs/report** (developers.openai.com).
   - Consumer: larger display type, 6px card radius, full-bleed imagery, 1200px max-width.
   - Developers/docs: smaller compressed scale, 8px card radius, #f9f9f9 cards, 900–1200px max-width.
2. Apply the color tokens and type scale below.
3. Build components using the prescribed radii and borders.
4. Use at most one accent color (see Accent & Graphics). Never introduce gradients or heavy shadows.
5. Output the result (CSS snippet, HTML file, or component code) and mention that it follows OpenAI aesthetic.

## Design Philosophy

- **Minimalism:** pure white canvas, near-black type, at most one accent color.
- **Restraint:** the only filled black element is the single primary button.
- **Editorial Canvas:** typography and whitespace do the work.
- **Geometric signature:** pills (9999px radius) for interactive elements; 6–8px radius for cards.

## Color Tokens

Use these exact values. Do not introduce colors beyond the single accent below.

| Name | Value | Role |
|------|-------|------|
| Obsidian | `#000000` | filled primary button only |
| Carbon | `#181818` | primary text, section headings |
| Graphite | `#282828` | nav text, links, icons |
| Ash Gray | `#5d5d5d` | secondary body text |
| Smoke | `#8f8f8f` | tertiary text, placeholders |
| Paper | `#ffffff` | page canvas |
| Fog White | `#f9f9f9` | card backgrounds |
| Linen | `#f3f3f3` | hover states |
| Mist Gray | `#ededed` | borders, dividers |
| Hairline | `rgba(0,0,0,0.12)` | all borders |
| Whisper | `rgba(0,0,0,0.04)` | hover tints |
| Accent Blue | `#3b5bdb` | links, focus rings, small monoline icons — the only color allowed |
| Accent Tint | `rgba(59,91,219,0.06)` | rare subtle highlight background (e.g., active link) |

## Accent & Graphics

The base stays monochrome. Color and graphics are seasoning, not the dish.

- Exactly **one** accent color: `#3b5bdb`. Use it only for text links, focus rings, small monoline icons, and tiny status dots.
- Never use the accent as a large-area fill, on the primary button (stays black), or for headings.
- Graphics are limited to thin monoline icons and simple geometric marks (dots, rings, hairline rules).
- **Never** reproduce OpenAI's wordmark, the Blossom icon, or anything that imitates them.
- No gradients, no decorative photos or illustrations.

## Typography

- **Font stack:** `"OpenAI Sans", Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", sans-serif`
  - **Note:** "OpenAI Sans" is OpenAI's custom typeface. Use it only if the project already has it loaded; otherwise fall back to Inter/system fonts.
- **Weights:** 400 (body), 500 (nav/labels/subheads), 600 (section headings). Never 700/800.

### Type Scale

| Role | Size | Weight | Line Height | Letter Spacing | Use |
|------|------|--------|-------------|----------------|-----|
| display | 48px | 500 | 1.16 | -1.44px | hero headline only |
| heading | 28px | 600 | 1.21 | 0.31px | section headings |
| subheading | 22px | 500 | 1.26 | -0.22px | card titles, subsection heads |
| body-lg | 18px | 400 | 1.32 | -0.18px | hero subtitle |
| body | 16px | 400 | 1.6 | -0.01em | body copy |
| label | 14px | 500 | 1.5 | — | nav, tags, buttons |
| caption | 13px | 500 | 1.51 | -0.13px | metadata, footnotes |

## Spacing & Shapes

- **Base unit:** 4px
- **Page max-width:** 1200px (consumer/marketing), 800–900px (docs/reports)
- **Section gap:** 32–64px
- **Card radius:** 8px (developers/docs), 6px (consumer)
- **Pill/button/input radius:** 9999px
- **Link radius:** 4px
- **Border:** 1px solid `rgba(0,0,0,0.12)` — semi-transparent black, not gray hex
- **Shadows:** avoid. If absolutely needed: `rgba(0,0,0,0.08) 0px 1px 2px -1px`

## Components

### Filled Primary Button
```css
background: #000000;
color: #ffffff;
font-size: 14px;
font-weight: 500;
border-radius: 9999px;
padding: 10px 16px;
```
Use sparingly. The only filled element on the page.

### Outlined Pill / Tag
```css
background: transparent;
border: 1px solid rgba(0,0,0,0.12);
color: #000000;
font-size: 14px;
font-weight: 500;
border-radius: 9999px;
padding: 8px 16px;
```

### Card
```css
background: #f9f9f9;
border-radius: 8px;
padding: 24px;
```
No shadow. Structure comes from surface and whitespace.

### Callout / Note
```css
background: #f9f9f9;
border-radius: 8px;
padding: 16px 20px;
font-size: 15px;
```
No colored left border. Use a light surface or a subtle hairline border.

## Do's and Don'ts

### Do
- Use `#000000` **only** for the filled primary button.
- Use `#181818` for primary text and section headings.
- Use `rgba(0,0,0,0.12)` for all borders.
- Use 9999px radius for pills, tags, buttons, inputs.
- Use 8px radius for cards (6px only for consumer marketing cards).
- Use `#3b5bdb` only for links, focus rings, and small monoline icons.
- Use weight changes for hierarchy.
- Trust whitespace over dividers.

### Don't
- Don't introduce a second accent color, and never use gradients.
- Don't use the accent as large-area fills or on the primary button.
- Don't reproduce OpenAI's wordmark or the Blossom icon.
- Don't use shadows on cards.
- Don't use weight 700/800.
- Don't use colored left borders for alerts.
- Don't use lifestyle illustrations; keep it text-first.

## Example Prompts

1. **Hero section:** white background, centered. Headline 48px weight 500 #181818, letter-spacing -1.44px. Subtitle 18px weight 400 #5d5d5d, 16px gap. Below: row of outlined pill tags spaced 8px.

2. **Feature card grid:** 3 columns, 20px gap. Card #f9f9f9, 8px radius, 24px padding. 20px monoline icon #282828 top-left, 16px gap to 16px weight 500 #181818 title, 8px gap to 14px weight 400 #5d5d5d body.

3. **Report page:** max-width 800px, white canvas. Section headings 22px weight 600 #181818 with bottom hairline border. Body 16px weight 400 #181818. Callouts use #f9f9f9 surface, no left border.
