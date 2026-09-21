---
name: test-handoff-guide
description: 生成「工程师 → 测试」交接测试指南，输出为 Anthropic 美学风格的单文件 HTML。当工程师完成开发需要把功能/修复/变更交给测试人员验收时使用。触发词：测试指南、测试交接、提测、handoff、QA 指南、验收文档。
---

# Test Handoff Guide

把工程师脑中的上下文翻译成测试人员可以直接执行的一页纸指南。核心原则：**测试人员不需要读代码，照着指南就能测完。**

## 工作流程

1. **收集上下文**（按可用性，缺什么问什么，最多追问一轮）：
   - 变更内容：改了什么功能 / 修了哪个 bug（一句话即可）
   - 变更范围：涉及的页面、接口、模块
   - 测试重点：工程师最担心出问题的地方
   - 环境信息：测试环境地址、账号、前置数据
2. **判断变更类型**，套用对应结构（见下）。
3. **生成单文件 HTML**，所有样式内联，不依赖网络。文件名建议：`test-guide-<功能名>-<YYYYMMDD>.html`。
4. 生成后自查清单（必须全部通过才交付）：
   - [ ] 测试人员不读代码、不找工程师，能否独立完成测试？
   - [ ] 每个测试点都有「操作步骤 + 预期结果」两要素？
   - [ ] 全文读一遍不超过 3 分钟？（超出就删，把细节挪进折叠区）
   - [ ] 环境 URL 可点击打开，账号/密码/前置数据可复制？
   - [ ] 所有 `{{...}}` 占位符是否已全部替换？（信息缺失时在报告中标注「待工程师补充」，不得漏出占位符）
   - [ ] 验收标准和 bug 提交通道是否都写明了？

## 报告内容结构（精炼、易懂）

按此顺序组织，**每节一句话说清，能列表就不写段落**：

1. **TL;DR**（顶部一句话）：本次要测什么 + 预计耗时，例如「验证登录页新增验证码，约 15 分钟」。
2. **背景**：为什么改、改了什么。3 行以内。
3. **测试环境**：URL、账号密码、依赖数据。用可复制的代码样式呈现。**只允许写内部测试环境凭据，禁止生产凭据**；报告含明文账号，不外发、不提交公网仓库。
4. **测试点**：核心部分。每条 = 编号 + 操作步骤 + 预期结果 + 优先级（P0 必测 / P1 应测 / P2 有空测）。正常路径在前，边界与异常在后。
5. **回归范围**：本次变更可能影响的旧功能，列 1-3 条快速 smoke 项。
6. **已知问题 / 不测项**：明确告诉测试「这些不用报 bug」，避免无效工单。
7. **验收标准**：怎样算通过，例如「全部 P0 通过即验收通过；P1 遗留 ≤2 项可带病上线」。同时写明测试结果在哪回填。
8. **缺陷反馈**：发现 bug 提到哪（工单系统链接），以及提单必附信息：复现步骤、截图/录屏、测试账号、发生时间。

省略规则：没有回归影响就删掉第 5 节；没有已知问题就删掉第 6 节。不要为凑结构保留空节。第 7、8 节是验收必备，不可省略。

## 视觉规范（Anthropic 美学）

这套美学 = 高级编辑部/研究机构的安静感，不是科技公司的霓虹感。

**配色**（暖纸底 + 珊瑚点缀，禁用冷蓝、渐变、阴影堆叠）：

| 用途 | 值 |
|---|---|
| 画布背景 | `#faf9f5` |
| 卡片/表面 | `#f5f0e8`（或白 `#ffffff` 配发丝边框） |
| 正文墨色 | `#141413` / 次级 `#3d3d3a` / 弱化 `#6c6a64` |
| 品牌强调（CTA、编号、重点） | `#cc785c`，hover `#a9583e` |
| 发丝边框 | `#e6dfd8` |
| 深表面（代码块、页脚） | `#141413`，其上文字 `#f5f0e8` |
| 语义色（少用） | 成功/通过 `#5e7d5a` / 失败 `#b4543f` / 警告 `#a97f2f` |

注意小字对比度：12-13px 文字需 ≥4.5:1。步骤编号圆点底用深色 `#a9583e`（白字约 4.6:1）；警告徽章文字用 `#7d5a1e` 而非 `#a97f2f`。

**字体**：标题用衬线（`Georgia, "Songti SC", "Noto Serif CJK SC", "Source Han Serif SC", "STSong", SimSun, serif`）；正文和 UI 用无衬线（`-apple-system, "Helvetica Neue", "PingFang SC", "Microsoft YaHei", sans-serif`）；代码用 `ui-monospace, "SF Mono", Menlo, monospace`。

**排版规则**：
- 大量留白：页面 max-width 720px 居中，章节间距 ≥ 48px，行高 1.7。
- 标题层级靠字号和字重区分，不用下划线和彩色标题。
- 编号、标签、步骤前的圆点用品牌珊瑚色，克制使用——除优先级徽章和步骤编号外，珊瑚色强调一屏不超过 3 处。
- 卡片圆角 12px，边框 1px 发丝色，无投影或仅极浅投影。
- 禁止：emoji 图标、渐变色、彩色大面积背景、斜体正文、全大写中文标题。

## HTML 模板

生成时以此骨架为基础填充。`{{...}}` 为占位符。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{功能名}} · 测试指南</title>
<style>
  :root {
    --canvas:#faf9f5; --surface:#ffffff; --surface-soft:#f5f0e8;
    --ink:#141413; --body:#3d3d3a; --muted:#6c6a64;
    --accent:#cc785c; --accent-active:#a9583e; --hairline:#e6dfd8;
    --ok:#5e7d5a; --fail:#b4543f; --warn:#a97f2f;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background:var(--canvas); color:var(--body);
    font:16px/1.7 -apple-system,"Helvetica Neue","PingFang SC","Microsoft YaHei",sans-serif;
    -webkit-font-smoothing:antialiased;
  }
  .page { max-width:720px; margin:0 auto; padding:64px 24px 96px; }
  h1,h2 { font-family:Georgia,"Songti SC","Noto Serif CJK SC","Source Han Serif SC","STSong",SimSun,serif; color:var(--ink); font-weight:600; }
  h1 { font-size:32px; line-height:1.25; }
  h2 { font-size:20px; margin:48px 0 16px; }
  .tldr {
    margin:24px 0 0; padding:16px 20px; background:var(--surface-soft);
    border-left:3px solid var(--accent); border-radius:0 12px 12px 0;
    color:var(--ink); font-size:15px;
  }
  .meta { margin-top:12px; color:var(--muted); font-size:13px; }
  .card {
    background:var(--surface); border:1px solid var(--hairline);
    border-radius:12px; padding:20px 24px; margin-top:16px;
  }
  code, .env-val {
    font-family:ui-monospace,"SF Mono",Menlo,monospace; font-size:13.5px;
    background:var(--surface-soft); border-radius:6px; padding:2px 8px; color:var(--ink);
  }
  pre {
    background:var(--ink); color:#f5f0e8; border-radius:12px;
    padding:16px 20px; overflow-x:auto; font-size:13.5px; line-height:1.6; margin-top:12px;
  }
  pre code { background:none; padding:0; color:inherit; }
  ol.steps { list-style:none; counter-reset:s; }
  ol.steps > li { counter-increment:s; padding-left:36px; position:relative; margin:10px 0; }
  ol.steps > li::before {
    content:counter(s); position:absolute; left:0; top:2px;
    width:24px; height:24px; border-radius:50%;
    background:var(--accent-active); color:#fff; font-size:13px;
    display:flex; align-items:center; justify-content:center;
  }
  table { width:100%; border-collapse:collapse; margin-top:12px; font-size:14.5px; }
  th { text-align:left; color:var(--muted); font-weight:500; font-size:13px;
       border-bottom:1px solid var(--hairline); padding:8px 12px 8px 0; }
  td { padding:12px 12px 12px 0; border-bottom:1px solid var(--hairline); vertical-align:top; }
  .pri { font-size:12px; font-weight:600; padding:2px 8px; border-radius:6px; white-space:nowrap; }
  .p0 { color:var(--fail); background:#f7ebe7; }
  .p1 { color:#7d5a1e; background:#f5efe0; }
  .p2 { color:var(--muted); background:var(--surface-soft); }
  .expect { color:var(--ok); }
  details { margin-top:12px; }
  summary { cursor:pointer; color:var(--muted); font-size:14px; }
  summary::marker { color:var(--accent); }
  footer {
    margin-top:72px; padding-top:24px; border-top:1px solid var(--hairline);
    color:var(--muted); font-size:13px; display:flex; justify-content:space-between;
    flex-wrap:wrap; gap:8px;
  }
</style>
</head>
<body>
<div class="page">
  <h1>{{功能名}}测试指南</h1>
  <div class="tldr">{{一句话：测什么 + 预计耗时}}</div>
  <div class="meta">{{提交人}} → 测试 · {{日期}} · 版本/分支：{{branch}}</div>

  <h2>背景</h2>
  <p>{{为什么改、改了什么，3 行以内}}</p>

  <h2>测试环境</h2>
  <div class="card">
    <table>
      <tr><td style="width:96px;color:var(--muted)">地址</td><td><a href="{{URL}}" style="color:var(--accent)"><code>{{URL}}</code></a></td></tr>
      <tr><td style="color:var(--muted)">账号</td><td><code>{{账号}}</code> / <code>{{密码}}</code></td></tr>
      <tr><td style="color:var(--muted)">前置数据</td><td>{{如需造数，给出入口或脚本}}</td></tr>
    </table>
  </div>

  <h2>测试点</h2>
  <div class="card">
    <table>
      <tr><th style="width:44px">#</th><th>操作步骤</th><th>预期结果</th><th style="width:56px">优先级</th></tr>
      <tr>
        <td>1</td>
        <td>{{步骤，可嵌 ol.steps 多步}}</td>
        <td class="expect">{{预期}}</td>
        <td><span class="pri p0">P0</span></td>
      </tr>
      <!-- 更多行：正常路径在前，边界/异常在后 -->
    </table>
  </div>

  <!-- 回归 Smoke：无回归影响时整节删除，见"省略规则"；禁止留空节或填"无" -->
  <h2>回归 Smoke</h2>
  <div class="card">
    <ol class="steps">
      <li>{{旧功能快速验证 1}}</li>
      <li>{{旧功能快速验证 2}}</li>
    </ol>
  </div>

  <!-- 已知问题 / 不测项：没有时整节删除，见"省略规则" -->
  <h2>已知问题 / 不测项</h2>
  <div class="card">
    <ul style="padding-left:20px">
      <li>{{明确不用报 bug 的现象}}</li>
    </ul>
  </div>

  <h2>验收标准</h2>
  <div class="card">
    <p>{{通过条件，例如：全部 P0 通过即验收通过；P1 遗留 ≤2 项可带病上线。}}</p>
    <p style="margin-top:8px;color:var(--muted);font-size:14px">测试结果请回填至：{{回填位置，如共享表格链接}}</p>
  </div>

  <h2>缺陷反馈</h2>
  <div class="card">
    <p>发现 bug 请提交至 <a href="{{工单系统链接}}" style="color:var(--accent)"><code>{{工单系统链接}}</code></a>，提单必附：</p>
    <ul style="padding-left:20px;margin-top:8px">
      <li>复现步骤（从打开页面开始写）</li>
      <li>截图或录屏</li>
      <li>测试账号 + 发生时间</li>
    </ul>
  </div>

  <details>
    <summary>补充细节（接口报文、数据准备脚本等）</summary>
    <pre><code>{{可选：curl / SQL / 报文示例}}</code></pre>
  </details>

  <footer>
    <span>有疑问找 {{提交人}}</span>
    <span>{{日期}}</span>
  </footer>
</div>
</body>
</html>
```

## 语气

写给同事看的，不是写给领导看的：直接、具体、不客套。说「输入 11 位手机号」，不说「输入合法手机号」。说「应弹出 toast：发送成功」，不说「应有相应提示」。
