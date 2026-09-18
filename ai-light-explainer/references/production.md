# 制作、迁移与交付

## 成套发布素材

按当前用户范围输出，可参考以下组织；文件命名不强制：

```text
episode/
  carousel/01-cover.png ...
  video/main.mp4
  video/cover.png
  copy.md
  sources.md
  source/
```

- 图文：标题、正文、可选少量相关标签、首评建议；以说明和回看价值为主。
- 视频：单独的标题、短正文和首评；强调能看见的过程。标题例子：“把 Jev 的决策过程做成动画，就好懂了”。
- 首评可以澄清一个误解或邀请讨论用途，不编造测试次数、观众反应、承诺或数据。
- 不自动继承某个发帖时间。图文先发、视频随后发可以作为一轮测试建议，不能承诺算法效果；未授权时只交付文案，不实际操作账号。
- 来源记录写明 URL、查阅日期、支撑的事实及示意内容。旧例子的发布热度、性能和开放状态不能直接当作新一期的当前事实。

## 复用代码

1. 将 `assets/reference-project/` 复制到本期 `source/`。
2. 在本期目录安装 `requirements.txt` 所需 Python 包。不要硬编码创作者电脑上的 Python 路径，也不把依赖库、缓存、凭证打进技能包。
3. 参考工程默认使用 macOS PingFang SC、SFNSMono。如果没有这些字体，设置以下环境变量为本地已安装字体的路径：
   - `AI_EXPLAINER_CN_FONT`：含简体中文的常规字体。
   - `AI_EXPLAINER_CN_BOLD_FONT`：对应中粗字体，可选。
   - `AI_EXPLAINER_MONO_FONT`：等宽字体。
   使用 Noto Sans CJK / Source Han Sans 等替代时，重新检视行宽、换行与字形，不能保证逐像素一致。不分发系统字体。
4. 先生成目标尺寸关键帧，检查后再输出视频。示例命令：

```sh
python3 -m pip install -r requirements.txt
python3 render.py --stills-only --output-dir ./preview --stills ./frames
python3 render.py --output-dir ./rendered --stills ./frames
```

这个示例会输出 Jev 视频与封面。新主题必须修改副本，不要把重跑示例冒称为完成新选题。它未提供通用多页图文渲染器；组图要复用字体、配色和窗口绘图函数，根据稿件新增页面。

## 搬到其他模型／agent

- 支持目录式 Skills：将完整 `ai-light-explainer/` 放入该工具规定的技能目录。不要只带走 `SKILL.md`，参考图、视频和相对链接都需要保留。
- 不支持自动 Skills：让 agent 先读取 `SKILL.md`，按里面的相对链接加载所需参考。`agents/openai.yaml` 可忽略。
- 没有视频渲染或图片查看能力：可先给出稿件和分镜，并明确缺少的能力；不能声称已经制作或验收成片。
- 本包能复用规范和资产，不能使不同模型的判断与审美完全一致；最终渲染检查仍不可省略。

## 已保留的参考

`reference-cover.png` 与 `reference-video.mp4` 是 Jev 第一期完成版，来源于用户本次对话确认的系列方向。属于概念动画，未调用 Jev API。参考图中“外网爆火”是该期标题，不是未来所有主题的默认前缀。

技术事实原始来源：https://docs.typesafe.ai/introduction 和 https://typesafe.ai/blog/introducing-system-one-models-and-jev 。2026-09-18 查阅时发布帖 https://news.ycombinator.com/item?id=49717558 为 1,866 points、491 comments，作为本期热度标题的背景记录，之后使用需重查。
