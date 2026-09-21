---
name: test-guide-html
description: Generate a clean, OpenAI-styled single-file HTML test guide for QA testers. Use when the user asks for a test guide, test plan HTML, testing instructions document, or QA verification guide in Chinese.
metadata:
  author: agent
  version: "1.1.0"
  language: zh-CN
  related-skills:
    - openai-aesthetic
---

# Test Guide HTML Generator

Generate a single-file HTML test guide that QA testers can read in a browser or print. The guide should be concise, actionable, and visually clean in the OpenAI aesthetic.

## When to Use

Use this skill when the user asks for:
- "生成测试指南 HTML"
- "给测试写个测试说明"
- "QA 测试指南"
- "测试计划 HTML"
- "验证步骤文档"

Default output language is **Chinese (zh-CN)** unless the user explicitly asks for English.

## Output Format

Always output a single self-contained `.html` file with:
- Embedded CSS (no external dependencies)
- No JavaScript required
- Printable layout (`@media print` should remove horizontal padding)
- Responsive for desktop and mobile

## Styling

1. First, apply the `openai-aesthetic` skill.
2. Then apply these report-specific conventions:
   - Page max-width: **800px**
   - H1 (page title): 28px / weight 600 / color #181818
   - H2 (section): 22px / weight 600 / color #181818 / bottom hairline border
   - H3 (subsection): 16px / weight 600 / color #181818
   - Body: 16px / weight 400 / line-height 1.6 / color #181818
   - Meta label: 13px / weight 500 / uppercase / color #8f8f8f
   - Font stack: `"OpenAI Sans", Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif`
   - Cards/callouts: #f9f9f9 background, 8px radius, 16–20px padding
   - Tables: hairline borders, hover state #f9f9f9
   - Checklists: `☐` prefix, no native checkbox inputs

If `openai-aesthetic` is not available, fall back to the tokens above.

## Required Sections

1. **Header**
   - Document type label: "Test Guide"
   - Title
   - One-line subtitle describing the scope

2. **测试范围 / Scope**
   - 1–2 sentences explaining what is being tested.
   - Any critical environment note (e.g., "do not use localhost").

3. **前置条件 / Prerequisites**
   - Use a checkbox-style list (`☐`).
   - Keep items short and checkable.

4. **测试场景 / Test Scenarios**
   - One section per major scenario.
   - Each scenario contains:
     - **操作步骤**: numbered list of actions
     - **预期结果**: a highlighted callout box
     - **验证要点**: bullet list of things to verify

5. **常见异常处理 / Common Issues**
   - Use a table: 报错 / 原因 / 处理.
   - Keep rows short.

6. **边界场景 / Edge Cases**
   - Checkbox list of additional scenarios to verify.

## What to Avoid

- Do not ask testers to fill in URLs, dates, names, or pass/fail columns.
- Do not include technical implementation details (code paths, Redis commands, etc.).
- Do not make it look like a Jira ticket or Excel sheet.
- Do not use localhost-specific URLs unless explicitly requested.
- Do not use colored left borders on callouts.

## Worked Mini-Example

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>示例测试指南</title>
  <style>
    body {
      font-family: Inter, system-ui, "Microsoft YaHei", sans-serif;
      font-size: 16px;
      line-height: 1.6;
      color: #181818;
      max-width: 800px;
      margin: 0 auto;
      padding: 72px 32px;
    }
    h1 { font-size: 28px; font-weight: 600; }
    h2 { font-size: 22px; font-weight: 600; border-bottom: 1px solid #ededed; padding-bottom: 10px; }
    .callout { background: #f9f9f9; border-radius: 8px; padding: 16px 20px; }
    .checklist { list-style: none; margin-left: 0; }
    .checklist li { padding-left: 28px; position: relative; }
    .checklist li::before { content: "☐"; position: absolute; left: 0; color: #8f8f8f; }
  </style>
</head>
<body>
  <h1>示例测试指南</h1>
  <h2>1. 测试范围</h2>
  <p>...</p>
  <h2>2. 前置条件</h2>
  <ul class="checklist"><li>账号已注册</li></ul>
  <h2>3. 操作步骤</h2>
  <ol><li>打开页面</li></ol>
  <h3>预期结果</h3>
  <div class="callout">页面正常加载。</div>
</body>
</html>
```

## Generation Workflow

1. Identify the system/feature being tested from the user's request.
2. Ask for the scope only if unclear: "这个指南要覆盖哪个功能或系统？"
3. Draft the guide using the structure above.
4. Apply the OpenAI aesthetic and report-specific conventions.
5. Save as a single `.html` file and tell the user the path.
