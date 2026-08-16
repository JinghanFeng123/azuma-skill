# Azuma Skill — 碧蓝航线「吾妻」知识库与角色扮演 Skill

一个为 Codex（及其他支持 skill 的 AI 助手）打造的碧蓝航线舰船「吾妻」（猉 / IJN Azuma / B-65 超甲型巡洋舰）专用 skill。既可以当作完整的舰船资料库使用，也可以让 AI 以吾妻温柔、淑女的口吻进行对话和角色扮演。

## 功能特性

- **完整图鉴资料**：属性数据、技能效果、开发加成、天运拟合、装备槽位、强度评价与配装推荐
- **台词全集**：默认台词、三套皮肤台词（细语春霞 / 【誓约】纯洁憧憬 / 心向何方的指导课）、历年情人节礼物
- **历史考据**：B-65 超甲型巡洋舰原型、大型巡洋舰定位、与阿拉斯加级的比较、战舰世界相关资料
- **角色扮演模式**：内置吾妻风格指南，AI 可按设定以“指挥官”称呼用户，用温柔淑女的语气回复，并保证数据准确
- **语音播放脚本**：播放内置的吾妻语音（好感度失望 / 好感度陌生），支持列出、校验与批量播放
- **数据刷新脚本**：一键从碧蓝海事局 WIKI 拉取吾妻页面最新源码
- **图片资源**：默认立绘、三套皮肤立绘、SD 动图与头像，可直接用于角色卡、Wiki 条目与同人创作配图

## 目录结构

```text
azuma-skill/
├── SKILL.md                    # Skill 主文档（触发说明与使用方式）
├── agents/
│   └── openai.yaml             # UI 元数据（显示名称、简介、默认提示词）
├── references/
│   ├── character.md            # 舰船档案：属性、技能、装备、配装、强度评价
│   ├── lines.md                # 台词全集与情人节礼物
│   ├── history.md              # 历史考据、角色设定、更新日志与资料来源
│   └── persona.md              # 吾妻角色扮演风格指南
├── scripts/
│   ├── fetch_wiki.py           # 从 WIKI 拉取最新资料
│   └── play_voice.py           # 播放内置语音
└── assets/
    ├── azuma-avatar.jpg        # 头像
    ├── azuma-default.jpg       # 默认立绘
    ├── azuma-skin-*.jpg        # 三套皮肤立绘
    ├── azuma-sd.gif            # SD 动图
    └── 好感度*.mp3             # 语音文件
```

## 安装方法

1. 将 `azuma-skill` 文件夹放入 Codex 的技能目录：
   - Windows：`C:\Users\<你的用户名>\.codex\skills\`
   - macOS / Linux：`~/.codex/skills/`
2. 重新打开或新建一个对话，即可自动识别。
3. 也可在对话中显式调用：`Use $azuma-skill 来查询吾妻的资料`。

## 使用示例

```text
# 查询资料
吾妻的技能「怒火连峰」具体效果是什么？

# 角色扮演
用吾妻的风格和我聊天吧~

# 播放语音（Windows）
python scripts/play_voice.py 好感度陌生

# 校验语音文件
python scripts/play_voice.py --check

# 刷新 WIKI 数据
python scripts/fetch_wiki.py --save references/wikitext_latest.txt
```

## 环境要求

- 运行 skill 本身无需额外依赖，AI 助手可直接读取 Markdown 文档。
- 更新脚本与语音播放脚本需要 Python 3（仅使用标准库，无需安装第三方包）。
- 语音播放脚本基于 Windows MCI 接口；macOS / Linux 会自动尝试 `afplay`、`paplay`、`aplay` 或 `ffplay`。

## 数据来源与版权声明

- 舰船数据、台词与历史考据整理自[碧蓝海事局 WIKI](https://wiki.biligame.com/blhx/%E5%90%BE%E5%A6%BB)（页面更新于 2026-07-06），如有出入以 WIKI 最新内容为准。
- 历史资料另参考《战舰世界》官网《Armada：Azuma》与战舰世界 WIKI。
- 立绘、皮肤与语音等图片音频资源版权归游戏官方及画师所有，本仓库仅用于个人学习与创作整理，请勿用于商业用途。

## 致谢

- [碧蓝海事局 WIKI](https://wiki.biligame.com/blhx/)
- [《Armada：Azuma》- 战舰世界官网](https://worldofwarships.asia/zh-tw/news/history/armada-azuma/)
- 画师 木shiyo+、CV 安野希世乃
