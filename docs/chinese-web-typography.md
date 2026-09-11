# 中文网页排版 · Chinese Web Typography

一个面向中文及中英混排网页的 Agent Skill，帮助 AI 把文字排得自然、完整，并在真实内容和不同屏幕下验证效果。

适合创建中文页面，以及修复标题断行、长文本溢出、标点位置、字体回退和组件文字裁切。保留已有文案、事实与设计风格，不要求所有网页使用同一套字号或布局。

## 安装

使用 [Skills CLI](https://github.com/vercel-labs/skills) 从 GitHub 安装，无需发布 npm 包：

```sh
npx skills@latest add voidning/skills --skill chinese-web-typography
```

按照提示选择要安装的技能、Agent 和安装范围。只安装到个人 Codex：

```sh
npx skills@latest add voidning/skills --skill chinese-web-typography -a codex -g
```

`npx` 需要本机有 Node.js/npm。它运行的是技能安装工具；**使用技能本身不需要安装 Playwright，也不会自动运行本仓库的 JavaScript 测试。** 技能单独放在 `chinese-web-typography/`，测试项目留在 `tests/chinese-web-typography/`。

安装后，在新的 Codex 任务中调用：

```text
使用 $chinese-web-typography 检查并修复这个页面的中文排版。
保留文案和现有风格，用手机、桌面及长短内容验证效果。
```

<details>
<summary>不使用 npx：手动安装到 Codex</summary>

克隆本仓库后，在仓库根目录运行。目标已存在时脚本会停止：

```sh
(
  skill_target="${CODEX_HOME:-$HOME/.codex}/skills/chinese-web-typography"
  if [ -e "$skill_target" ]; then
    printf '目标目录已存在：%s\n' "$skill_target"
    exit 1
  fi
  mkdir -p "$(dirname "$skill_target")"
  cp -R chinese-web-typography "$skill_target"
)
```

</details>

## 它处理什么

| 场景 | 关注的问题 |
| --- | --- |
| 中文标题 | 生硬分行、孤字、过窄容器、装饰性硬换行、动态标题 |
| 正文与混排 | 标点禁则、中英文间距、长英文、URL、字体与字形回退 |
| 数字与单位 | 金额、日期、百分比、缺失值、对齐与局部不拆分 |
| 组件文字 | 商品名、按钮、表单错误、导航、表格、弹窗中的换行与完整展示 |
| 响应式 | 小屏幕、文字放大、内容长度变化、固定高度裁切和整页溢出 |

技能按问题加载参考规则：先定位容器和样式约束，再选择最小修复，最后查看实际渲染。`text-wrap: balance` 不是中文语义分词器；无溢出也不代表断行自然。

它不负责通篇文案改写、品牌视觉重设计或印刷排版，也不承诺消除所有孤字或让所有浏览器产生完全相同的行序。

## 使用示例

**新页面**

> 使用 $chinese-web-typography 完成这个中文介绍页的排版，保留当前设计风格，检查中文标题、正文混排和移动端文字展示。

**已有页面**

> 使用 $chinese-web-typography 检查商品卡片的长标题、价格和按钮；不要改写商品文案，修复后用常见长度与超长内容复测。

**先检查再修改**

> 使用 $chinese-web-typography 审查这个页面，先列出有渲染证据的问题及原因，暂不修改代码。

## 技能与测试分开存放

```text
.
├── README.md
├── chinese-web-typography/          # 技能安装内容，不含测试依赖
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── docs/chinese-web-typography.md   # 本说明
└── tests/chinese-web-typography/    # 可选测试项目
    ├── package.json
    ├── package-lock.json
    ├── TEST_REPORT.md
    ├── typography-lab/
    │   ├── before.html
    │   ├── index.html
    │   └── verify.cjs
    ├── evidence/                   # 保存的测试结果与截图
    └── artifacts/                  # 本地复测输出，Git 忽略
```

查看 [技能入口](../chinese-web-typography/SKILL.md)、[中文文字规则](../chinese-web-typography/references/text-rules.md) 和 [测试报告](../tests/chinese-web-typography/TEST_REPORT.md)。

## 测试案例与效果

用六类业务场景的模拟内容测试：标题、混排正文、商品卡片、订单表格、表单和配送说明。`before.html` 是构造的故障对照，不是生产站点源码。测试含长短标题、长 URL/订单号、大金额、缺失值、繁体和生僻字。

实测中发现并补充了两条重要规则：短标题仅设置 `balance` 仍可能在不自然的位置分行；普通正文里的长英文也可能在文字放大后溢出。

![320px 窄屏下的标题分行](../tests/chinese-web-typography/evidence/screenshots/after-320-hero.png)

保存的测试记录覆盖 **9 组修复后配置**：320、390、768、1440px，根字号 200%、系统衬线字体替换及长短动态内容。86 项适用断言通过，故障对照仍检出预期问题。浏览器版本、具体检查与局限见 [测试报告](../tests/chinese-web-typography/TEST_REPORT.md)。

### 自己运行测试（可选）

只使用技能可跳过本节。开发或复测需要 Node.js 20+：

```sh
git clone https://github.com/voidning/skills.git
cd skills/tests/chinese-web-typography
npm ci
npx playwright install chromium
npm test
```

仅运行故障对照：

```sh
npm run test:baseline
```

新结果写入 `tests/chinese-web-typography/artifacts/`，不会覆盖 `tests/chinese-web-typography/evidence/` 中保存的历史证据。两个 HTML 文件也可以直接用浏览器打开。

### 验证边界

- 自动化实测使用 macOS / Chromium，不代表 Safari、Firefox、真实手机或完整无障碍合规。
- 根字号 200% 是 rem 驱动文字放大的近似测试，不等于真实浏览器缩放。
- 系统字体替换不是网络字体加载/失败测试；操作系统和字体差异会影响断行。
- 自动化能发现部分溢出、裁切与数据保真问题；语义停顿、字形和阅读感仍需查看实际渲染。
- 技能包含更多组件策略，但本次实测只覆盖上述六类场景。新增规则应来自真实失败与复测，不应把一次修复扩展成全局限制。

## 参考

规则参考 [W3C《中文排版需求》](https://www.w3.org/TR/clreq/) 与 MDN 的 CSS/HTML 文档。参考链接集中在 [文字规则](../chinese-web-typography/references/text-rules.md) 中；依赖新 CSS 特性时，应核对目标浏览器的当前支持情况。
