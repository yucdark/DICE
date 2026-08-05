# 幕外之骰 · 试玩版 0.1.0

这是一个不需要 API、联网或第三方依赖的命令行规则原型。它会读取 `data/`
中的 JSON 内容包，生成一张 10 房间地图，并处理检定、事件、装备、技能、
战斗、战利品、观测者能力与存档。

如果准备把游戏交给另一个 AI 运行，请让它先完整阅读
[`给AI的游玩与接管说明.md`](给AI的游玩与接管说明.md)，并优先使用 `ai_cmd.py`。

如果对方不能正确解压 ZIP，直接发送 `veil_dice_standalone_for_ai.py`。这是一个纯
UTF-8 单文件版本，已内嵌引擎、全部内容包和 AI 说明；它不依赖 `data/` 目录。

## 运行

在本目录执行：

```bash
python 幕外之骰试玩版.py --seed 42
```

想继续上次存档：

```bash
python 幕外之骰试玩版.py --load
```

默认存档是同目录的 `save.json`。固定 `--seed` 会得到可复现的地图和骰子序列。

给 AI 的一次一命令入口：

```bash
python ai_cmd.py --new status
python ai_cmd.py look
python ai_cmd.py travel north
```

之后继续游戏时不要再加 `--new`。`ai_cmd.py` 会自动读取和保存 `save.json`，
而且每条返回都会附带可直接展示给玩家的状态面板。

## 常用命令

```text
status
look
travel north
combat policy=balanced rounds=5
inventory compact=true
check insight dc=14
choose 1
observer status
observer use subtle_nudge
rest
export
log last=10
```

也可以作为 Python 模块调用：

```python
from veil_dice_engine import boot, cmd

boot(seed=42)
print(cmd("status"))
print(cmd("look"))
```

## 说明

这是“能完整跑一局”的核心原型，不是最终 UI。内容包仍然是普通 JSON，后续
可以在不改规则引擎的情况下继续增加敌人、地点、事件、装备和风味文本。
