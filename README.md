# Skills

个人维护的 AI Agent 技能集合，涵盖独立评审、项目约定整理、中文网页排版、AI 轻科普内容制作、OpenAI 视觉风格应用和测试指南 HTML 生成。

## 技能目录

| 技能 | 用途 |
| --- | --- |
| [blind-review](blind-review/SKILL.md) | **盲审**：由未参与制作的 Agent 独立评审，隔离制作讨论和作者自评。 |
| [distill-agents-md](distill-agents-md/SKILL.md) | **规则提炼**：筛选长期约定，去重后提出 `AGENTS.md` 修改建议。 |
| [chinese-web-typography](chinese-web-typography/SKILL.md) | **中文排版**：按内容选择排版策略，检查不同屏幕下的实际渲染。 |
| [ai-light-explainer](ai-light-explainer/SKILL.md) | **AI 轻科普**：复用暖白橙色线框风格，制作中文图文、动画与各自发布文案，包含可编辑工程和完整参考素材。 |
| [openai-aesthetic](openai-aesthetic/SKILL.md) | **OpenAI 风格**：应用 OpenAI  monochrome-first 视觉语言到网页、组件和文档。 |
| [test-guide-html](test-guide-html/SKILL.md) | **测试指南生成**：生成单文件 HTML 测试指南，默认 OpenAI 风格、中文输出。 |

## 安装

需要 [Node.js](https://nodejs.org/)。在目标项目目录运行，按提示选择技能和 Agent：

```bash
npx skills@latest add voidning/skills
```

默认安装到当前项目，添加 `-g` 可全局安装。也可指定技能和 Agent，例如安装中文排版技能到个人 Codex：

```bash
npx skills@latest add voidning/skills --skill chinese-web-typography -a codex -g
```

查看可安装的技能：

```bash
npx skills@latest add voidning/skills --list
```

更新已安装的技能：

```bash
npx skills@latest update
```

更新范围不限于本仓库。更多选项见 [Skills CLI 文档](https://github.com/vercel-labs/skills)。

## 使用

安装后，在 Agent 中指定技能并说明任务。例如在 Codex 中：

```text
使用 $chinese-web-typography 检查这个页面的中文排版，
保留文案和风格，修复问题并验证手机与桌面效果。
```

具体要求见各技能的 `SKILL.md`。涉及子 Agent 或独立任务的技能，需要客户端支持相应能力。

## 说明与测试

- [中文网页排版：使用说明](docs/chinese-web-typography.md)
- [中文网页排版：测试案例、结果与复测方法](tests/chinese-web-typography/TEST_REPORT.md)

测试代码和依赖位于 `tests/`，不会随技能安装。只有运行浏览器测试时才需要 Playwright。

## 添加技能

每个技能放在根目录的独立文件夹中，以 `SKILL.md` 定义名称、用途和执行规则。参考资料、脚本和素材按需添加；开发测试放在 `tests/<skill-name>/`。

新增后，更新上方目录并验证文件、链接和实际使用效果。

## 反馈

通过 [Issues](https://github.com/voidning/skills/issues) 提交建议或问题，请附上技能名称、使用场景、预期结果与实际表现。
