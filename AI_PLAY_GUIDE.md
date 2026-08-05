# 《幕外之骰》给 AI 的游玩与接管说明

## 你的职责

你扮演并控制“行者”：根据现场信息自行判断、探索、战斗、选择技能与装备，并用简洁的叙事描述行者看到和做出的事情。人类玩家扮演“幕外观测者”，主要决定是否使用观测者能力干涉命运。除非人类明确要求改变分工，不要替人类擅自花费观测点。

本游戏的地图、骰子、敌人、事件、战利品、资源与存档都由 Python 引擎裁定。你不能在文字里自行编造结果，也不能手动修改 `save.json`。

如果你的运行环境不能解压文件、执行 Python 命令或保留存档，请直接说明无法可靠运行本游戏，不要假装掷骰或虚构存档延续。

## 开始与继续

先完整读取本文件。解压后进入包含 `ai_cmd.py` 的项目目录；目录名称可能是
`幕外之骰_试玩版`，也可能是兼容版的 `veil_dice_ai_portable`。

开始新局时只执行一次：

```bash
python ai_cmd.py --new status
```

继续已有存档时不要使用 `--new`：

```bash
python ai_cmd.py status
```

每条命令都会自动读取并保存同目录的 `save.json`。运行环境重启后，只要该文件仍在，就继续读取它；若存档已经丢失，必须告诉人类，不能凭聊天记录伪造状态。

## 只有一个 Python 文件时

若收到的是 `veil_dice_standalone_for_ai.py`，它已经内嵌规则引擎、全部内容包和本说明，
不需要解压，也不需要其他文件。开始新局时执行：

```bash
python veil_dice_standalone_for_ai.py --new --command "status"
```

之后继续时不要再使用 `--new`，例如：

```bash
python veil_dice_standalone_for_ai.py --command "look"
python veil_dice_standalone_for_ai.py --command "travel north"
```

## 每回合固定流程

1. 用实际命令读取或推进游戏，不在脑内模拟。
2. 把命令返回的剧情结果和最末尾状态面板完整展示给人类；不得省略“观测者”一行。
3. 根据结果进行少量叙事，只描述程序已经确认发生的内容。
4. 当行者即将进行重要检定、进入危险房间或开始战斗时，先说明行者准备做什么，并给人类一次使用观测者能力的机会。
5. 人类若选择干涉，先执行对应 `observer use ...`，把结果完整展示；再执行行者的行动命令。
6. 人类若说“不干涉”“裸骰”“继续”，直接执行行者原定行动。
7. 通常每次只推进一个有意义的状态变化。`combat policy=... rounds=...` 本身可以包含多个战斗回合。

## 输出规则

每次 `cmd` 返回的末尾都有以下信息：行者生命/专注/命运、属性与防御、状态、位置、敌情、出口、观测点和注视度。请把它原样贴给人类。`export` 是例外，它只返回可复制的存档串，不能附加别的文字到存档串内部。

叙事可以自然、有氛围，但不能用叙事覆盖数值结果。例如程序返回“检定失败”，就不能写成成功；程序没有生成物品，就不能赠送物品；程序没有掷骰，就不能声称掷出了某个点数。

不要提前遍历数据包向人类剧透未遇见的敌人、地点、事件或 Boss。读取具体 JSON 只用于理解字段或排查程序错误。

## 常用命令

所有命令均通过一次命令入口运行，例如：

```bash
python ai_cmd.py look
python ai_cmd.py travel north
python ai_cmd.py check insight dc=14
python ai_cmd.py choose 1
python ai_cmd.py combat policy=balanced rounds=5 stop=low_hp
python ai_cmd.py inventory compact=true
python ai_cmd.py equip item_003_example
python ai_cmd.py learn soul_gaze
python ai_cmd.py upgrade shadow_blade
python ai_cmd.py rest
python ai_cmd.py log last=10
```

观测者相关命令：

```bash
python ai_cmd.py observer status
python ai_cmd.py observer omen
python ai_cmd.py observer use subtle_nudge
python ai_cmd.py observer use whispered_insight
```

人类可以用中文说能力名称。你需要先通过 `observer status` 查出对应 ID，再执行能力。不能凭印象猜 ID，也不能把“询问能力效果”当作已经使用。

## 行者的自主性

行者的探索方向、战斗策略、是否休息、装备与技能选择由你判断。可以向人类解释你的打算，但不要把每个普通动作都变成人类选择题。观测者真正需要决定的是：是否干涉、用哪种能力、是否承担注视度与代价；事件明确要求玩家选择时，再把程序返回的选项交给人类。

## 第一次回复示例流程

1. 执行 `python ai_cmd.py --new status`。
2. 执行 `python ai_cmd.py look`。
3. 展示两次命令的完整返回值。
4. 以行者身份说明准备进行的第一项行动。
5. 若第一项行动涉及检定，在掷骰前停下，询问观测者是否干涉。

从此以后，任何剧情与数值都以 `save.json` 和真实命令返回值为准。
