# -*- coding: utf-8 -*-
# VEIL DICE - STANDALONE AI EDITION
# This is plain UTF-8 source code, not a ZIP archive. Read the guide below first.
# New game: python veil_dice_standalone_for_ai.py --new --command "status"
# Continue: python veil_dice_standalone_for_ai.py --command "look"
# ================= AI PLAY GUIDE =================
# # 《幕外之骰》给 AI 的游玩与接管说明
#
# ## 你的职责
#
# 你扮演并控制“行者”：根据现场信息自行判断、探索、战斗、选择技能与装备，并用简洁的叙事描述行者看到和做出的事情。人类玩家扮演“幕外观测者”，主要决定是否使用观测者能力干涉命运。除非人类明确要求改变分工，不要替人类擅自花费观测点。
#
# 本游戏的地图、骰子、敌人、事件、战利品、资源与存档都由 Python 引擎裁定。你不能在文字里自行编造结果，也不能手动修改 `save.json`。
#
# 如果你的运行环境不能解压文件、执行 Python 命令或保留存档，请直接说明无法可靠运行本游戏，不要假装掷骰或虚构存档延续。
#
# ## 开始与继续
#
# 先完整读取本文件。解压后进入包含 `ai_cmd.py` 的项目目录；目录名称可能是
# `幕外之骰_试玩版`，也可能是兼容版的 `veil_dice_ai_portable`。
#
# 开始新局时只执行一次：
#
# ```bash
# python ai_cmd.py --new status
# ```
#
# 继续已有存档时不要使用 `--new`：
#
# ```bash
# python ai_cmd.py status
# ```
#
# 每条命令都会自动读取并保存同目录的 `save.json`。运行环境重启后，只要该文件仍在，就继续读取它；若存档已经丢失，必须告诉人类，不能凭聊天记录伪造状态。
#
# ## 只有一个 Python 文件时
#
# 若收到的是 `veil_dice_standalone_for_ai.py`，它已经内嵌规则引擎、全部内容包和本说明，
# 不需要解压，也不需要其他文件。开始新局时执行：
#
# ```bash
# python veil_dice_standalone_for_ai.py --new --command "status"
# ```
#
# 之后继续时不要再使用 `--new`，例如：
#
# ```bash
# python veil_dice_standalone_for_ai.py --command "look"
# python veil_dice_standalone_for_ai.py --command "travel north"
# ```
#
# ## 每回合固定流程
#
# 1. 用实际命令读取或推进游戏，不在脑内模拟。
# 2. 把命令返回的剧情结果和最末尾状态面板完整展示给人类；不得省略“观测者”一行。
# 3. 根据结果进行少量叙事，只描述程序已经确认发生的内容。
# 4. 当行者即将进行重要检定、进入危险房间或开始战斗时，先说明行者准备做什么，并给人类一次使用观测者能力的机会。
# 5. 人类若选择干涉，先执行对应 `observer use ...`，把结果完整展示；再执行行者的行动命令。
# 6. 人类若说“不干涉”“裸骰”“继续”，直接执行行者原定行动。
# 7. 通常每次只推进一个有意义的状态变化。`combat policy=... rounds=...` 本身可以包含多个战斗回合。
#
# ## 输出规则
#
# 每次 `cmd` 返回的末尾都有以下信息：行者生命/专注/命运、属性与防御、状态、位置、敌情、出口、观测点和注视度。请把它原样贴给人类。`export` 是例外，它只返回可复制的存档串，不能附加别的文字到存档串内部。
#
# 叙事可以自然、有氛围，但不能用叙事覆盖数值结果。例如程序返回“检定失败”，就不能写成成功；程序没有生成物品，就不能赠送物品；程序没有掷骰，就不能声称掷出了某个点数。
#
# 不要提前遍历数据包向人类剧透未遇见的敌人、地点、事件或 Boss。读取具体 JSON 只用于理解字段或排查程序错误。
#
# ## 常用命令
#
# 所有命令均通过一次命令入口运行，例如：
#
# ```bash
# python ai_cmd.py look
# python ai_cmd.py travel north
# python ai_cmd.py check insight dc=14
# python ai_cmd.py choose 1
# python ai_cmd.py combat policy=balanced rounds=5 stop=low_hp
# python ai_cmd.py inventory compact=true
# python ai_cmd.py equip item_003_example
# python ai_cmd.py learn soul_gaze
# python ai_cmd.py upgrade shadow_blade
# python ai_cmd.py rest
# python ai_cmd.py log last=10
# ```
#
# 观测者相关命令：
#
# ```bash
# python ai_cmd.py observer status
# python ai_cmd.py observer omen
# python ai_cmd.py observer use subtle_nudge
# python ai_cmd.py observer use whispered_insight
# ```
#
# 人类可以用中文说能力名称。你需要先通过 `observer status` 查出对应 ID，再执行能力。不能凭印象猜 ID，也不能把“询问能力效果”当作已经使用。
#
# ## 行者的自主性
#
# 行者的探索方向、战斗策略、是否休息、装备与技能选择由你判断。可以向人类解释你的打算，但不要把每个普通动作都变成人类选择题。观测者真正需要决定的是：是否干涉、用哪种能力、是否承担注视度与代价；事件明确要求玩家选择时，再把程序返回的选项交给人类。
#
# ## 第一次回复示例流程
#
# 1. 执行 `python ai_cmd.py --new status`。
# 2. 执行 `python ai_cmd.py look`。
# 3. 展示两次命令的完整返回值。
# 4. 以行者身份说明准备进行的第一项行动。
# 5. 若第一项行动涉及检定，在掷骰前停下，询问观测者是否干涉。
#
# 从此以后，任何剧情与数值都以 `save.json` 和真实命令返回值为准。
# ================= END GUIDE =================

#!/usr/bin/env python3
"""幕外之骰：无 API、纯 Python 的可运行规则原型。

这个模块故意只依赖 Python 标准库。内容（装备、材质、词缀、技能、敌人、
事件、地点、观测者能力、风味文本）从同目录的 data/*.json 读取；规则和状态
则保存在 Game 中。既可直接运行 REPL，也可在 Python 中：

    from veil_dice_engine import boot, cmd
    boot(seed=42)
    print(cmd("status"))

命令写法与试玩版设计书一致，状态改变后会自动写入 save.json。
"""

from __future__ import annotations

import argparse
import ast
import base64
import copy
import json
import pickle
import random
import re
import shlex
import sys
import textwrap
from pathlib import Path
from typing import Any, Iterable


DICE_RE = re.compile(r"^(?P<count>[1-9][0-9]*)d(?P<sides>4|6|8|10|12|20|100)(?P<bonus>[+-][0-9]+)?$")
DICE_SIZES = [4, 6, 8, 10, 12, 20, 100]
STATUS_NAMES = {"bleed", "poison", "burn", "stagger", "fear", "ward", "mark"}
READ_ONLY = {"status", "look", "inventory", "log", "map", "help", "export"}


def now_copy(value: Any) -> Any:
    return copy.deepcopy(value)


def parse_dice(expr: str) -> tuple[int, int, int]:
    match = DICE_RE.match(str(expr).strip())
    if not match:
        raise ValueError(f"不支持的骰式：{expr}")
    return int(match.group("count")), int(match.group("sides")), int(match.group("bonus") or 0)


def roll_dice(rng: random.Random, expr: str) -> tuple[int, list[int]]:
    count, sides, bonus = parse_dice(expr)
    rolls = [rng.randint(1, sides) for _ in range(count)]
    return sum(rolls) + bonus, rolls


def dice_step(expr: str, step: int) -> str:
    """按内容包的 damage_die_step 推进骰子。

    2d6 也保留为一个合法台阶；超出范围时钳制到两端。
    """
    count, sides, bonus = parse_dice(expr)
    # 常用武器骰的顺序；多骰武器在自己的档位附近移动。
    order = [(1, 4), (1, 6), (1, 8), (1, 10), (1, 12), (2, 6), (2, 8), (2, 10), (2, 12)]
    try:
        idx = order.index((count, sides))
    except ValueError:
        idx = min(range(len(order)), key=lambda i: abs(order[i][0] * order[i][1] - count * sides))
    idx = max(0, min(len(order) - 1, idx + int(step)))
    c, s = order[idx]
    return f"{c}d{s}" + (f"{bonus:+d}" if bonus else "")


def b64_pickle(value: Any) -> str:
    return base64.b64encode(pickle.dumps(value, protocol=4)).decode("ascii")


def unpickle_b64(value: str) -> Any:
    return pickle.loads(base64.b64decode(value.encode("ascii")))


class ContentStore:
    """读取并按 ID 合并内容包。最后加载的同 ID 条目覆盖前者。"""

    ARRAY_NAMES = (
        "equipment_bases",
        "materials",
        "affixes",
        "skills",
        "enemies",
        "events",
        "locations",
        "observer_actions",
        "flavor_text",
    )

    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"找不到内容目录：{self.data_dir}")
        self.data: dict[str, list[dict[str, Any]]] = {name: [] for name in self.ARRAY_NAMES}
        for path in sorted(self.data_dir.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for name in self.ARRAY_NAMES:
                rows = payload.get(name, [])
                if isinstance(rows, list):
                    self.data[name].extend(x for x in rows if isinstance(x, dict))
        self.maps = {name: {row.get("id"): row for row in rows if row.get("id")} for name, rows in self.data.items()}

    def all(self, name: str) -> list[dict[str, Any]]:
        return self.data.get(name, [])

    def get(self, name: str, item_id: str) -> dict[str, Any] | None:
        return self.maps.get(name, {}).get(item_id)


class Game:
    VERSION = "0.1.0"

    def __init__(self, data_dir: str | Path, save_path: str | Path | None = None, seed: int | None = None,
                 state: dict[str, Any] | None = None):
        self.store = ContentStore(data_dir)
        self.save_path = Path(save_path) if save_path else None
        self.rng = random.Random(seed)
        self.state: dict[str, Any] = {}
        self.dirty = False
        if state is not None:
            self._load_state(state)
        else:
            self._new_state(seed)

    @classmethod
    def new(cls, data_dir: str | Path, save_path: str | Path | None = None, seed: int | None = None) -> "Game":
        return cls(data_dir, save_path=save_path, seed=seed)

    @classmethod
    def load(cls, data_dir: str | Path, save_path: str | Path) -> "Game":
        path = Path(save_path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(data_dir, save_path=path, state=payload)

    def _new_state(self, seed: int | None) -> None:
        self.state = {
            "version": self.VERSION,
            "seed": seed,
            "turn": 0,
            "phase": "exploration",
            "end_state": None,
            "attention": 0,
            "observer_points": 5,
            "flags": {},
            "rooms": [],
            "current_room": 0,
            "visited": [],
            "pending_event": None,
            "pending_observer": {"before_check": [], "before_room": [], "combat_start": []},
            "combat": None,
            "inventory": [],
            "item_serial": 0,
            "equipped": {"main_hand": None, "off_hand": None, "body": None, "trinket_1": None, "trinket_2": None},
            "learned_skills": {},
            "cooldowns": {},
            "audit": [],
            "player": {
                "name": "无名行者",
                "stats": {"might": 1, "finesse": 1, "insight": 1, "will": 1},
                "hp": 21,
                "max_hp": 21,
                "focus": 3,
                "max_focus": 5,
                "fate": 2,
                "fate_cap": 3,
                "shield": 0,
                "statuses": {},
                "temp_mods": {},
            },
        }
        self._build_map()
        self._add_starting_loadout()
        self._enter_room(0, initial=True)
        self.dirty = True

    def _load_state(self, state: dict[str, Any]) -> None:
        self.state = now_copy(state)
        rng_blob = self.state.pop("_rng_state", None)
        if rng_blob:
            self.rng.setstate(unpickle_b64(rng_blob))
        else:
            self.rng.seed(self.state.get("seed"))
        # 兼容中途扩展字段。
        self.state.setdefault("pending_observer", {"before_check": [], "before_room": [], "combat_start": []})
        self.state.setdefault("cooldowns", {})
        self.state.setdefault("item_serial", len(self.state.get("inventory", [])))
        self.state.setdefault("audit", [])
        self.state.setdefault("attention", 0)
        self.state.setdefault("observer_points", 5)
        self.state.setdefault("end_state", None)
        self.dirty = False

    def save(self, path: str | Path | None = None) -> Path:
        target = Path(path or self.save_path or "save.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = now_copy(self.state)
        payload["_rng_state"] = b64_pickle(self.rng.getstate())
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        self.save_path = target
        self.dirty = False
        return target

    def export_string(self) -> str:
        payload = now_copy(self.state)
        payload["_rng_state"] = b64_pickle(self.rng.getstate())
        raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return "VEIL-DICE-0.1:" + base64.b64encode(raw).decode("ascii")

    def import_string(self, token: str) -> str:
        if token.startswith("VEIL-DICE-0.1:"):
            token = token.split(":", 1)[1]
        payload = json.loads(base64.b64decode(token.encode("ascii")).decode("utf-8"))
        self._load_state(payload)
        self.dirty = True
        return "已导入存档。"

    # ---------- 地图与房间 ----------

    def _weighted_choice(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        if not rows:
            raise ValueError("内容包没有可用条目")
        weights = [max(1, int(row.get("weight", 1))) for row in rows]
        return now_copy(self.rng.choices(rows, weights=weights, k=1)[0])

    def _build_map(self) -> None:
        locations = self.store.all("locations")
        by_type: dict[str, list[dict[str, Any]]] = {}
        for loc in locations:
            by_type.setdefault(loc.get("room_type", "exploration"), []).append(loc)
        sequence = ["entrance", "exploration", "exploration", "exploration", "exploration",
                    "combat", "combat", "event", "elite", "boss"]
        rooms: list[dict[str, Any]] = []
        used: set[str] = set()
        for index, kind in enumerate(sequence):
            source_type = "exploration" if kind == "entrance" else kind
            candidates = [x for x in by_type.get(source_type, []) if x.get("id") not in used] or by_type.get(source_type, [])
            if not candidates:
                # 兼容缺少某类房间的外部包：用 exploration 填位，但保留目标房间类型。
                candidates = [x for x in locations if x.get("room_type") == "exploration"]
            loc = self._weighted_choice(candidates)
            used.add(loc.get("id", ""))
            room = {
                "index": index,
                "location_id": loc.get("id"),
                "name": loc.get("name", "未知房间"),
                "room_type": kind,
                "description": loc.get("description", "雾幕遮住了房间。"),
                "tags": list(loc.get("tags", [])),
                "danger": int(loc.get("danger", 0)),
                "enemy_tags_any": list(loc.get("enemy_tags_any", [])),
                "event_tags_any": list(loc.get("event_tags_any", [])),
                "entry_effects": list(loc.get("entry_effects", [])),
                "exits": {},
                "revealed": False,
                "cleared": False,
            }
            rooms.append(room)
        for i, room in enumerate(rooms):
            if i + 1 < len(rooms):
                room["exits"]["north"] = i + 1
            if i > 0:
                room["exits"]["south"] = i - 1
            # 轻微分支：不会让线性主路断开，也不会令 boss 不可达。
            if i in (1, 3, 5, 7) and i + 2 < len(rooms):
                room["exits"]["east"] = i + 2
        self.state["rooms"] = rooms

    def _room(self, index: int | None = None) -> dict[str, Any]:
        return self.state["rooms"][self.state["current_room"] if index is None else index]

    def _enter_room(self, index: int, initial: bool = False) -> str:
        self.state["current_room"] = index
        if index not in self.state["visited"]:
            self.state["visited"].append(index)
        room = self._room()
        self.state["phase"] = "exploration"
        self.state["pending_event"] = None
        if not initial:
            self._apply_pending_observer("before_room", room=room)
        self._apply_effect_list(room.get("entry_effects", []), self.state["player"], None,
                                {"room": room, "tags": set(room.get("tags", []))}, source="room")
        enter_context = {"room": room, "tags": set(room.get("tags", [])) | self._player_tags()}
        self._dispatch("on_enter_room", self.state["player"], None, enter_context,
                       set(enter_context["tags"]))
        if room["room_type"] in {"combat", "elite", "boss"} and not room.get("cleared"):
            self.state["phase"] = "combat_pending"
        elif room["room_type"] in {"event", "npc"} and not room.get("cleared"):
            self._prepare_event(room)
        return self._room_text(room, entered=True)

    def _room_text(self, room: dict[str, Any], entered: bool = False) -> str:
        exits = ", ".join(f"{direction}->{target}" for direction, target in room.get("exits", {}).items())
        lines = [f"[{room['index']}] {room['name']} · {room['room_type']} · 危险{room.get('danger', 0)}",
                 room.get("description", "")]
        if exits:
            lines.append(f"出口：{exits}")
        if room["room_type"] in {"combat", "elite", "boss"} and not room.get("cleared"):
            lines.append("这里的敌意已经凝成实体；输入 combat 开始战斗。")
        if self.state.get("pending_event"):
            event = self.store.get("events", self.state["pending_event"]) or {}
            lines.append(f"事件：{event.get('name', '未知事件')}（输入 choose 1/2/...）")
        if entered:
            flavor = self._flavor("room_enter", room.get("tags", []))
            if flavor:
                lines.append(flavor)
        return "\n".join(lines)

    def _prepare_event(self, room: dict[str, Any]) -> None:
        events = []
        for event in self.store.all("events"):
            if event.get("unique") and self.state["flags"].get(f"event_done:{event.get('id')}"):
                continue
            tags = set(room.get("tags", [])) | set(room.get("event_tags_any", []))
            required = set(event.get("room_tags_any", []))
            if not required or tags.intersection(required):
                events.append(event)
        if events:
            self.state["pending_event"] = self._weighted_choice(events).get("id")

    # ---------- 装备、属性与技能 ----------

    def _add_starting_loadout(self) -> None:
        main = self._make_item(base_id="stiletto_needle", material_id="cold_iron", affix_ids=[])
        body = self._make_item(base_id="patched_armor", material_id="ash_leather", affix_ids=[])
        self._add_item(main, equip_slot="main_hand")
        self._add_item(body, equip_slot="body")
        for skill_id in ("crushing_blow", "shadow_blade", "iron_prayer", "keen_scout"):
            if self.store.get("skills", skill_id):
                self.state["learned_skills"][skill_id] = {"level": 0}

    def _add_item(self, item: dict[str, Any], equip_slot: str | None = None) -> None:
        self.state["inventory"].append(item)
        if equip_slot:
            self.state["equipped"][equip_slot] = item["id"]

    def _choose_material(self, base: dict[str, Any], material_id: str | None = None) -> dict[str, Any] | None:
        if material_id:
            material = self.store.get("materials", material_id)
            if material and base.get("category") in material.get("allowed_categories", []):
                return material
        options = [m for m in self.store.all("materials") if base.get("category") in m.get("allowed_categories", [])]
        return self._weighted_choice(options) if options else None

    def _choose_affixes(self, base: dict[str, Any], affix_ids: list[str] | None, quality: str | None = None) -> list[dict[str, Any]]:
        if affix_ids is not None:
            rows = []
            for affix_id in affix_ids:
                row = self.store.get("affixes", affix_id)
                if row and base.get("category") in row.get("allowed_categories", []):
                    rows.append(row)
            return rows
        quality = quality or self._roll_quality()
        normal = [a for a in self.store.all("affixes") if a.get("position") in ("prefix", "suffix")
                  and base.get("category") in a.get("allowed_categories", [])]
        special = [a for a in self.store.all("affixes") if a.get("position") in ("curse", "miracle")
                   and base.get("category") in a.get("allowed_categories", [])]
        count = {"common": 0, "uncommon": 1, "rare": 1, "epic": 2, "relic": 2}.get(quality, 0)
        rows = []
        if normal and count:
            rows = self.rng.sample(normal, min(count, len(normal)))
        if special and quality in {"rare", "epic", "relic"} and self.rng.randint(1, 100) <= 18:
            rows.append(self._weighted_choice(special))
        return rows

    def _roll_quality(self) -> str:
        roll = self.rng.randint(1, 100)
        if roll <= 2:
            return "relic"
        if roll <= 7:
            return "epic"
        if roll <= 20:
            return "rare"
        if roll <= 50:
            return "uncommon"
        return "common"

    def _make_item(self, base_id: str | None = None, material_id: str | None = None,
                   affix_ids: list[str] | None = None, quality: str | None = None,
                   reward_tags: Iterable[str] | None = None) -> dict[str, Any]:
        bases = self.store.all("equipment_bases")
        if reward_tags:
            wanted = set(reward_tags)
            tagged = [b for b in bases if wanted.intersection(b.get("tags", []))]
            base = self._weighted_choice(tagged or bases)
        else:
            base = self.store.get("equipment_bases", base_id) if base_id else self._weighted_choice(bases)
        if not base:
            raise ValueError("装备基础包为空或找不到指定装备")
        material = self._choose_material(base, material_id)
        affixes = self._choose_affixes(base, affix_ids, quality)
        tags = set(base.get("tags", []))
        if material:
            tags.update(material.get("tags", []))
        for affix in affixes:
            tags.update(affix.get("tags", []))
        self.state["item_serial"] = int(self.state.get("item_serial", 0)) + 1
        row: dict[str, Any] = {
            "id": f"item_{self.state['item_serial']:03d}_{base.get('id')}",
            "base_id": base.get("id"),
            "material_id": material.get("id") if material else None,
            "affix_ids": [a.get("id") for a in affixes],
            "name": base.get("name", "无名装备"),
            "slot": base.get("slot", "trinket"),
            "category": base.get("category", "accessory"),
            "tags": sorted(tags),
            "guard": int(base.get("guard", 0)),
            "damage_reduction": int(base.get("damage_reduction", 0)),
            "weight": int(base.get("weight", 0)),
            "damage_die": base.get("damage_die"),
            "attack_stat": base.get("attack_stat"),
            "effects": [],
        }
        name_prefix: list[str] = []
        name_suffix: list[str] = []
        if material:
            row["guard"] += int(material.get("guard_mod", material.get("stat_modifiers", {}).get("guard", 0)))
            row["damage_reduction"] += int(material.get("damage_reduction_mod", material.get("stat_modifiers", {}).get("damage_reduction", 0)))
            row["weight"] += int(material.get("weight_mod", material.get("stat_modifiers", {}).get("weight", 0)))
            if material.get("damage_die_step"):
                row["damage_die"] = dice_step(row["damage_die"], int(material["damage_die_step"])) if row.get("damage_die") else None
            row["effects"].extend(material.get("effects", []))
            name_prefix.append(material.get("name", ""))
        for affix in affixes:
            row["guard"] += int(affix.get("guard_mod", 0))
            row["damage_reduction"] += int(affix.get("damage_reduction_mod", 0))
            row["weight"] += int(affix.get("weight_mod", 0))
            if row.get("damage_die") and affix.get("damage_die_step"):
                row["damage_die"] = dice_step(row["damage_die"], int(affix["damage_die_step"]))
            row["effects"].extend(affix.get("effects", []))
            if affix.get("position") == "prefix":
                name_prefix.append(affix.get("name", ""))
            else:
                name_suffix.append(affix.get("name", ""))
        row["name"] = "·".join([x for x in name_prefix + [row["name"]] + name_suffix if x])
        row["guard"] = max(0, row["guard"])
        row["damage_reduction"] = max(0, row["damage_reduction"])
        row["weight"] = max(0, row["weight"])
        row["quality"] = quality or self._quality_from_affixes(affixes)
        return row

    @staticmethod
    def _quality_from_affixes(affixes: list[dict[str, Any]]) -> str:
        ranks = {"common": 0, "uncommon": 1, "rare": 2, "epic": 3, "relic": 4}
        if not affixes:
            return "common"
        return max(affixes, key=lambda x: ranks.get(x.get("rarity", "common"), 0)).get("rarity", "common")

    def _item_by_id(self, item_id: str) -> dict[str, Any] | None:
        return next((item for item in self.state["inventory"] if item.get("id") == item_id), None)

    def _equipped_items(self) -> list[dict[str, Any]]:
        return [item for item_id in self.state["equipped"].values() if item_id and (item := self._item_by_id(item_id))]

    def _passive_effects(self) -> list[dict[str, Any]]:
        effects: list[dict[str, Any]] = []
        for item in self._equipped_items():
            effects.extend(e for e in item.get("effects", []) if e.get("trigger") == "passive")
        for skill_id, info in self.state["learned_skills"].items():
            skill = self.store.get("skills", skill_id)
            if skill and skill.get("kind") == "passive":
                effects.extend(skill.get("effects", []))
        return effects

    def _player_stat(self, stat: str) -> int:
        value = int(self.state["player"]["stats"].get(stat, 0))
        value += int(self.state["player"].get("temp_mods", {}).get(stat, 0))
        for effect in self._passive_effects():
            if effect.get("operation") == "stat_mod" and effect.get("stat") == stat:
                value += int(effect.get("value", 0))
        return value

    def _player_guard(self) -> int:
        return 10 + self._player_stat("finesse") + sum(i.get("guard", 0) for i in self._equipped_items())

    def _player_dr(self) -> int:
        value = sum(i.get("damage_reduction", 0) for i in self._equipped_items())
        for effect in self._passive_effects():
            if effect.get("operation") == "damage_reduction":
                value += int(effect.get("value", 0))
        return max(0, value)

    def _player_tags(self) -> set[str]:
        tags: set[str] = set()
        for item in self._equipped_items():
            tags.update(item.get("tags", []))
        for skill_id in self.state["learned_skills"]:
            skill = self.store.get("skills", skill_id)
            if skill:
                tags.update(skill.get("tags", []))
        return tags

    # ---------- 效果与状态 ----------

    def _condition_ok(self, effect: dict[str, Any], tags: set[str]) -> bool:
        any_tags = set(effect.get("condition_tags_any", []))
        all_tags = set(effect.get("condition_tags", []))
        if any_tags and not tags.intersection(any_tags):
            return False
        if all_tags and not all_tags.issubset(tags):
            return False
        chance = effect.get("chance")
        if chance is not None and self.rng.randint(1, 100) > int(chance):
            return False
        return True

    def _resolve_target(self, target: str | None, actor: Any, target_obj: Any, context: dict[str, Any]) -> Any:
        if target == "self" or target is None:
            return actor
        if target == "enemy":
            return target_obj
        if target == "attacker":
            return context.get("attacker", target_obj)
        if target == "random_enemy":
            enemies = [e for e in (self.state.get("combat") or {}).get("enemies", []) if e.get("hp", 0) > 0]
            return self.rng.choice(enemies) if enemies else target_obj
        return target_obj

    def _apply_status(self, target: Any, status: str, stacks: int = 1, duration: int = 1) -> None:
        if target is None or status not in STATUS_NAMES:
            return
        statuses = target.setdefault("statuses", {})
        old = statuses.get(status, {"stacks": 0, "duration": 0})
        statuses[status] = {"stacks": int(old.get("stacks", 0)) + int(stacks),
                            "duration": max(int(old.get("duration", 0)), int(duration))}

    def _remove_status(self, target: Any, status: str) -> None:
        if target is not None:
            target.setdefault("statuses", {}).pop(status, None)

    def _heal(self, target: Any, value: int) -> None:
        if not isinstance(target, dict):
            return
        if "max_hp" in target:
            target["hp"] = min(int(target.get("max_hp", 0)), int(target.get("hp", 0)) + int(value))
        elif target is self.state["player"]:
            target["hp"] = min(target["max_hp"], target["hp"] + int(value))

    def _damage(self, target: Any, value: int, tags: set[str] | None = None, ignore_dr: bool = False) -> int:
        if not isinstance(target, dict):
            return 0
        amount = max(0, int(value))
        tags = tags or set()
        resist = set(target.get("resistances", []))
        weak = set(target.get("weaknesses", []))
        if tags.intersection(weak):
            amount += 2
        if tags.intersection(resist):
            amount = max(1, amount // 2)
        if target is self.state["player"]:
            if not ignore_dr:
                amount = max(1, amount - self._player_dr()) if amount > 0 else 0
            ward = target.setdefault("statuses", {}).get("ward")
            if ward:
                absorb = min(amount, int(ward.get("stacks", 0)) * 2)
                amount -= absorb
                ward["stacks"] -= (1 if absorb else 0)
                if ward["stacks"] <= 0:
                    target["statuses"].pop("ward", None)
            shield = min(amount, int(target.get("shield", 0)))
            target["shield"] = int(target.get("shield", 0)) - shield
            amount -= shield
        else:
            dr = int(target.get("damage_reduction", 0))
            if not ignore_dr:
                amount = max(1, amount - dr) if amount > 0 else 0
            shield = min(amount, int(target.get("shield", 0)))
            target["shield"] = int(target.get("shield", 0)) - shield
            amount -= shield
        target["hp"] = max(0, int(target.get("hp", 0)) - amount)
        if target is self.state["player"] and target["hp"] > 0 and target["hp"] <= target["max_hp"] // 3 \
                and not self.state["flags"].get("low_hp_triggered"):
            self.state["flags"]["low_hp_triggered"] = True
            self._dispatch("on_low_hp", target, None, {"tags": self._player_tags(), "room": self._room()}, self._player_tags())
        self.dirty = True
        return amount

    def _apply_effect(self, effect: dict[str, Any], actor: Any, target_obj: Any, context: dict[str, Any], tags: set[str]) -> None:
        if not self._condition_ok(effect, tags):
            return
        operation = effect.get("operation")
        target = self._resolve_target(effect.get("target"), actor, target_obj, context)
        value = int(effect.get("value", 0))
        if operation == "stat_mod" and isinstance(target, dict):
            target.setdefault("temp_mods", {})[effect.get("stat", "might")] = target.setdefault("temp_mods", {}).get(effect.get("stat", "might"), 0) + value
        elif operation == "guard_mod" and isinstance(target, dict):
            target["guard_current"] = int(target.get("guard_current", target.get("guard", 0))) + value
        elif operation == "damage_reduction" and isinstance(target, dict):
            target["damage_reduction"] = int(target.get("damage_reduction", 0)) + value
        elif operation == "weight_mod":
            context["weight_mod"] = context.get("weight_mod", 0) + value
        elif operation == "damage_die_step":
            context["damage_die_step"] = context.get("damage_die_step", 0) + value
        elif operation == "bonus_die":
            die = effect.get("die", "1d4")
            if effect.get("target") == "current_check":
                context.setdefault("check_bonus_dice", []).append(die)
            else:
                context.setdefault("bonus_damage_dice", []).append(die)
        elif operation == "reroll":
            context["reroll"] = int(context.get("reroll", 0)) + max(1, value)
        elif operation == "advantage":
            context["advantage"] = True
        elif operation == "disadvantage":
            context["disadvantage"] = True
        elif operation == "modify_dc":
            context["dc_mod"] = int(context.get("dc_mod", 0)) + value
        elif operation == "apply_status":
            self._apply_status(target, effect.get("status", "mark"), int(effect.get("stacks", 1)), int(effect.get("duration", 1)))
        elif operation == "remove_status":
            self._remove_status(target, effect.get("status", "fear"))
        elif operation == "heal":
            self._heal(target, value)
        elif operation == "damage":
            self._damage(target, value, tags=tags)
        elif operation == "shield" and isinstance(target, dict):
            target["shield"] = int(target.get("shield", 0)) + value
        elif operation == "resource_gain":
            resource = effect.get("resource", "focus")
            if resource == "attention":
                self.state["attention"] += value
            elif resource == "observer_point":
                self.state["observer_points"] += value
            elif resource in self.state["player"]:
                p = self.state["player"]
                cap = p.get(f"{resource}_cap", p.get(f"max_{resource}", 999))
                p[resource] = min(cap, p.get(resource, 0) + value)
            elif resource == "hp":
                self._heal(self.state["player"], value)
        elif operation == "resource_loss":
            resource = effect.get("resource", "focus")
            if resource == "attention":
                self.state["attention"] = max(0, self.state["attention"] - value)
            elif resource == "observer_point":
                self.state["observer_points"] = max(0, self.state["observer_points"] - value)
            elif resource in self.state["player"]:
                self.state["player"][resource] = max(0, self.state["player"].get(resource, 0) - value)
        elif operation == "reveal":
            room = context.get("room") or self._room()
            room["revealed"] = True
        elif operation == "spawn":
            if self.state.get("combat") is not None:
                self._spawn_enemy_for_combat(self._room())
            else:
                self._room()["spawn_pending"] = int(self._room().get("spawn_pending", 0)) + max(1, value)
        elif operation == "counterattack":
            attacker = context.get("attacker") or target_obj
            if attacker:
                self._damage(attacker, value, tags=tags)
        self.dirty = True

    def _apply_effect_list(self, effects: Iterable[dict[str, Any]], actor: Any, target_obj: Any,
                           context: dict[str, Any], source: str = "event", tags: set[str] | None = None) -> None:
        tags = set(tags or context.get("tags", set()))
        for effect in effects:
            self._apply_effect(effect, actor, target_obj, context, tags)

    def _dispatch(self, trigger: str, actor: Any, target_obj: Any, context: dict[str, Any],
                  tags: set[str], extra_effects: Iterable[dict[str, Any]] = ()) -> None:
        effects: list[dict[str, Any]] = []
        if actor is self.state["player"]:
            for item in self._equipped_items():
                effects.extend(e for e in item.get("effects", []) if e.get("trigger") == trigger)
            # on_skill_use 只属于这次选中的主动技能；其余事件则遍历已学技能的
            # 对应触发器，避免普通攻击意外触发铁血祷告等技能。
            if trigger != "on_skill_use":
                for skill_id in self.state["learned_skills"]:
                    skill = self.store.get("skills", skill_id)
                    if skill:
                        level = self.state["learned_skills"][skill_id].get("level", 0)
                        effects.extend(e for e in skill.get("effects", []) if e.get("trigger") == trigger)
                        for upgrade in skill.get("upgrades", [])[:level]:
                            effects.extend(e for e in upgrade.get("effects", []) if e.get("trigger") == trigger)
        effects.extend(e for e in extra_effects if e.get("trigger") == trigger)
        self._apply_effect_list(effects, actor, target_obj, context, source=trigger, tags=tags)

    def _tick_statuses(self, target: dict[str, Any], is_player: bool) -> list[str]:
        messages: list[str] = []
        statuses = target.setdefault("statuses", {})
        for status, info in list(statuses.items()):
            stacks = int(info.get("stacks", 1))
            if status == "bleed":
                dealt = self._damage(target, stacks, ignore_dr=True)
                messages.append(f"流血-{dealt}")
            elif status == "poison":
                dealt = self._damage(target, stacks, ignore_dr=False, tags={"poison"})
                messages.append(f"中毒-{dealt}")
            elif status == "burn":
                dealt = self._damage(target, max(1, stacks), ignore_dr=True, tags={"fire"})
                messages.append(f"燃烧-{dealt}")
            info["duration"] = int(info.get("duration", 1)) - 1
            if info["duration"] <= 0:
                statuses.pop(status, None)
        return messages

    # ---------- 检定 ----------

    def _apply_pending_observer(self, timing: str, context: dict[str, Any] | None = None, room: dict[str, Any] | None = None) -> None:
        pending = self.state.get("pending_observer", {}).get(timing, [])
        if not pending:
            return
        ctx = context or {"room": room or self._room(), "tags": set((room or self._room()).get("tags", []))}
        for action in pending:
            self._apply_effect_list(action.get("effects", []), self.state["player"], None, ctx, source="observer",
                                    tags=set(ctx.get("tags", set())) | self._player_tags())
        self.state["pending_observer"][timing] = []

    def _check(self, stat: str, dc: int, tags: set[str] | None = None, label: str = "检定",
               context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {"tags": set(tags or set())}
        self._apply_pending_observer("before_check", context=context)
        context.setdefault("tags", set(tags or set()))
        check_extra = context.get("_check_extra_effects", [])
        self._dispatch("on_check", self.state["player"], context.get("enemy"), context,
                       set(context.get("tags", set())), extra_effects=check_extra)
        mode = "normal"
        if context.get("advantage") and not context.get("disadvantage"):
            mode = "advantage"
        elif context.get("disadvantage") and not context.get("advantage"):
            mode = "disadvantage"
        rolls = [self.rng.randint(1, 20)]
        if mode != "normal":
            rolls.append(self.rng.randint(1, 20))
        raw = max(rolls) if mode == "advantage" else min(rolls) if mode == "disadvantage" else rolls[0]
        bonus = self._player_stat(stat) + 2 + int(context.get("check_bonus", 0))
        for die in context.get("check_bonus_dice", []):
            extra, _ = roll_dice(self.rng, die)
            bonus += extra
        total = raw + bonus
        target_dc = int(dc) + int(context.get("dc_mod", 0))
        result = "critical_success" if raw == 20 else "critical_failure" if raw == 1 else "success" if total >= target_dc else "failure"
        self.state["audit"].append({"type": "roll", "label": label, "raw": raw, "rolls": rolls, "bonus": bonus,
                                     "dc": target_dc, "result": result})
        if result in {"failure", "critical_failure"}:
            self._dispatch("on_check_fail", self.state["player"], context.get("enemy"), context,
                           set(context.get("tags", set())), extra_effects=check_extra)
            if context.get("reroll", 0) and not context.get("_rerolled"):
                context["_rerolled"] = True
                return self._check(stat, dc, tags=tags, label=label, context=context)
        else:
            self._dispatch("on_check_success", self.state["player"], context.get("enemy"), context,
                           set(context.get("tags", set())), extra_effects=check_extra)
        return {"raw": raw, "rolls": rolls, "bonus": bonus, "total": total, "dc": target_dc, "result": result,
                "context": context}

    # ---------- 战斗 ----------

    def _select_enemy_template(self, room: dict[str, Any], rank: str) -> dict[str, Any] | None:
        candidates = [e for e in self.store.all("enemies") if e.get("rank") == rank]
        room_tags = set(room.get("tags", [])) | set(room.get("enemy_tags_any", []))
        matched = [e for e in candidates if not room.get("enemy_tags_any") or room_tags.intersection(e.get("tags", []))]
        return now_copy(self._weighted_choice(matched or candidates)) if (matched or candidates) else None

    def _spawn_enemy_for_combat(self, room: dict[str, Any], rank: str | None = None) -> dict[str, Any] | None:
        combat = self.state.get("combat")
        if combat is None:
            return None
        rank = rank or ("boss" if room.get("room_type") == "boss" else "elite" if room.get("room_type") == "elite" else "normal")
        template = self._select_enemy_template(room, rank)
        if not template:
            # 若内容包没有精确 rank，降级到任意敌人。
            template = now_copy(self._weighted_choice(self.store.all("enemies")))
        enemy = {
            "runtime_id": f"{template.get('id')}_{len(combat['enemies']) + 1}",
            "template_id": template.get("id"),
            "name": template.get("name", "未知敌人"),
            "rank": template.get("rank", rank),
            "hp": int(template.get("hp", 8)),
            "max_hp": int(template.get("hp", 8)),
            "guard": int(template.get("guard", 10)),
            "guard_current": int(template.get("guard", 10)),
            "will_defense": int(template.get("will_defense", 10)),
            "damage_reduction": int(template.get("damage_reduction", 0)),
            "tags": list(template.get("tags", [])),
            "weaknesses": list(template.get("weaknesses", [])),
            "resistances": list(template.get("resistances", [])),
            "actions": list(template.get("actions", [])),
            "loot_tags": list(template.get("loot_tags", [])),
            "statuses": {},
            "shield": 0,
        }
        combat["enemies"].append(enemy)
        return enemy

    def _start_combat(self) -> str:
        room = self._room()
        if self.state.get("combat"):
            return "战斗已经在进行。"
        self.state["phase"] = "combat"
        self.state["combat"] = {"round": 1, "enemies": [], "target": 0, "log": []}
        self._spawn_enemy_for_combat(room)
        if room.get("room_type") == "combat" and self.rng.randint(1, 100) <= 35:
            self._spawn_enemy_for_combat(room, rank="normal")
        if room.get("spawn_pending"):
            for _ in range(int(room.pop("spawn_pending"))):
                self._spawn_enemy_for_combat(room, rank="normal")
        combat_ctx = {"tags": self._player_tags(), "room": room}
        self._dispatch("on_combat_start", self.state["player"], self._current_enemy(), combat_ctx, self._player_tags())
        self._apply_pending_observer("combat_start", context=combat_ctx)
        names = ", ".join(e["name"] for e in self.state["combat"]["enemies"])
        return f"战斗开始：{names}。输入 combat policy=balanced rounds=5，或 fight。"

    def _current_enemy(self) -> dict[str, Any] | None:
        combat = self.state.get("combat")
        if not combat:
            return None
        living = [e for e in combat["enemies"] if e.get("hp", 0) > 0]
        if not living:
            return None
        idx = min(int(combat.get("target", 0)), len(living) - 1)
        return living[idx]

    def _skill_ready(self, skill_id: str) -> bool:
        return skill_id in self.state["learned_skills"] and int(self.state["cooldowns"].get(skill_id, 0)) <= 0

    def _use_skill_cost(self, skill_id: str, skill: dict[str, Any]) -> bool:
        focus = int(skill.get("focus_cost", 0))
        hp_cost = int(skill.get("hp_cost", 0))
        player = self.state["player"]
        if player["focus"] < focus or player["hp"] <= hp_cost:
            return False
        player["focus"] -= focus
        player["hp"] -= hp_cost
        self.state["cooldowns"][skill_id] = int(skill.get("cooldown", 0))
        return True

    def _player_attack(self, skill_id: str | None = None) -> str:
        enemy = self._current_enemy()
        if not enemy:
            return "没有可攻击的敌人。"
        skill = self.store.get("skills", skill_id) if skill_id else None
        if skill:
            if skill.get("kind") not in {"active", "reaction"} or not self._skill_ready(skill_id):
                return f"技能不可用：{skill_id}。"
            if not self._use_skill_cost(skill_id, skill):
                return f"资源不足，无法使用 {skill.get('name')}。"
        tags = self._player_tags() | set(skill.get("tags", [])) if skill else self._player_tags()
        extra = skill.get("effects", []) if skill else []
        context: dict[str, Any] = {"tags": tags, "enemy": enemy, "room": self._room(), "bonus_damage_dice": [],
                                   "_check_extra_effects": extra}
        if skill:
            self._dispatch("on_skill_use", self.state["player"], enemy, context, tags, extra_effects=extra)
        weapon = self._item_by_id(self.state["equipped"].get("main_hand", ""))
        attack_stat = (weapon or {}).get("attack_stat") or ("might" if "might" in tags else "finesse")
        check = self._check(attack_stat, int(enemy.get("guard_current", enemy.get("guard", 10))), tags=tags,
                            label=f"攻击:{skill.get('name') if skill else '普通攻击'}", context=context)
        if check["result"] in {"failure", "critical_failure"}:
            if check["result"] == "critical_failure":
                self._apply_status(self.state["player"], "stagger", 1, 1)
            return f"你对 {enemy['name']} 的攻击{('大失败' if check['result']=='critical_failure' else '未命中')}（{check['total']} vs {check['dc']}）。"
        # 先结算命中/暴击词缀，把 bonus_die 等效果纳入本次伤害。
        self._dispatch("on_hit", self.state["player"], enemy, context, tags, extra_effects=extra)
        if check["result"] == "critical_success":
            self._dispatch("on_crit", self.state["player"], enemy, context, tags, extra_effects=extra)
        die = (weapon or {}).get("damage_die") or "1d4"
        if context.get("damage_die_step"):
            die = dice_step(die, context["damage_die_step"])
        damage, rolls = roll_dice(self.rng, die)
        damage += self._player_stat(attack_stat)
        if check["result"] == "critical_success":
            crit, _ = roll_dice(self.rng, die)
            damage += crit
        for bonus_die in context.get("bonus_damage_dice", []):
            bonus, _ = roll_dice(self.rng, bonus_die)
            damage += bonus
        dealt = self._damage(enemy, max(1, damage), tags=tags)
        if enemy["hp"] <= 0:
            self._dispatch("on_kill", self.state["player"], enemy, context, tags, extra_effects=extra)
        return f"你攻击 {enemy['name']}：{check['result']}，掷 {die}{rolls}，造成 {dealt} 伤害（剩余 {enemy['hp']}）。"

    def _enemy_turn(self) -> str:
        enemy = self._current_enemy()
        if not enemy:
            return "敌方回合：没有存活敌人。"
        actions = enemy.get("actions") or [{"id": "strike", "name": "撕咬", "weight": 1, "damage_die": "1d4", "effects": []}]
        action = self._weighted_choice(actions)
        context = {"tags": set(enemy.get("tags", [])), "attacker": enemy, "room": self._room()}
        die = action.get("damage_die")
        lines = [f"{enemy['name']} 使用 {action.get('name', '未知招式')}。"]
        action_effects = list(action.get("effects", []))
        self._apply_effect_list([e for e in action_effects if e.get("trigger") == "on_skill_use"],
                                enemy, self.state["player"], context, source="enemy_skill",
                                tags=set(enemy.get("tags", [])))
        hit = False
        if die:
            attack = self.rng.randint(1, 20)
            bonus = int(action.get("attack_bonus", 0))
            total = attack + bonus
            if attack == 20 or (attack != 1 and total >= self._player_guard()):
                hit = True
                damage, rolls = roll_dice(self.rng, die)
                rank_bonus = {"minion": 0, "normal": 1, "elite": 2, "boss": 3}.get(enemy.get("rank"), 1)
                dealt = self._damage(self.state["player"], damage + rank_bonus, tags=set(enemy.get("tags", [])))
                self._dispatch("on_damaged", self.state["player"], enemy, context, set(enemy.get("tags", [])))
                lines.append(f"命中（{attack}+{bonus} vs {self._player_guard()}），造成 {dealt}，你的生命 {self.state['player']['hp']}/{self.state['player']['max_hp']}。")
                if self.state["player"]["hp"] <= 0:
                    self.state["end_state"] = "death"
            else:
                lines.append(f"未命中（{attack}+{bonus} vs {self._player_guard()}）。")
        # 命中效果不能在未命中时生效。
        if hit:
            self._apply_effect_list([e for e in action_effects if e.get("trigger") == "on_hit"],
                                    enemy, self.state["player"], context, source="enemy_hit",
                                    tags=set(enemy.get("tags", [])))
        return " ".join(lines)

    def _combat_round(self, policy: str = "balanced") -> list[str]:
        combat = self.state.get("combat")
        if not combat:
            return [self._start_combat()]
        lines: list[str] = [f"— 第 {combat['round']} 回合 —"]
        living = [e for e in combat["enemies"] if e.get("hp", 0) > 0]
        if not living:
            return lines
        target = self._current_enemy()
        skill_id = None
        available = [sid for sid, info in self.state["learned_skills"].items()
                     if self.store.get("skills", sid) and self.store.get("skills", sid).get("kind") == "active" and self._skill_ready(sid)]
        if policy == "aggressive":
            skill_id = next((sid for sid in available if "attack" in self.store.get("skills", sid).get("tags", [])), None)
        elif policy == "defensive":
            skill_id = next((sid for sid in available if "ward" in self.store.get("skills", sid).get("tags", [])), None)
        else:
            skill_id = available[combat["round"] % len(available)] if available and combat["round"] % 2 == 0 else None
        lines.append(self._player_attack(skill_id))
        if not any(e.get("hp", 0) > 0 for e in combat["enemies"]):
            lines.append(self._finish_combat(victory=True))
            return lines
        lines.append(self._enemy_turn())
        # 回合末状态和冷却。
        status_lines = self._tick_statuses(self.state["player"], is_player=True)
        for enemy in combat["enemies"]:
            status_lines.extend(f"{enemy['name']}:{x}" for x in self._tick_statuses(enemy, is_player=False))
        if status_lines:
            lines.append("状态：" + "，".join(status_lines))
        for sid in list(self.state["cooldowns"]):
            self.state["cooldowns"][sid] = max(0, int(self.state["cooldowns"][sid]) - 1)
        combat["round"] += 1
        self.state["turn"] += 1
        if self.state["player"]["hp"] <= 0:
            self.state["end_state"] = "death"
        return lines

    def _finish_combat(self, victory: bool) -> str:
        room = self._room()
        if victory:
            room["cleared"] = True
            combat = self.state.get("combat") or {"enemies": []}
            loot_tags: set[str] = set()
            for enemy in combat.get("enemies", []):
                loot_tags.update(enemy.get("loot_tags", []))
            item = self._make_item(reward_tags=loot_tags)
            self._add_item(item)
            self.state["combat"] = None
            self.state["phase"] = "exploration"
            self._dispatch("on_combat_end", self.state["player"], None, {"tags": self._player_tags(), "room": room}, self._player_tags())
            flavor = self._flavor("victory", room.get("tags", []))
            return f"战斗胜利。获得战利品：{item['name']}（{item['quality']}）。" + (f" {flavor}" if flavor else "")
        self.state["combat"] = None
        self.state["phase"] = "exploration"
        return "战斗结束。"

    # ---------- 事件、观测者与奖励 ----------

    def _has_requirement(self, requirement: str) -> bool:
        if requirement in self.state["flags"]:
            return bool(self.state["flags"][requirement])
        if requirement in self._player_tags():
            return True
        return any(requirement in item.get("tags", []) for item in self.state["inventory"])

    def _grant_reward(self, reward_tags: Iterable[str]) -> list[str]:
        tags = list(reward_tags)
        if not tags:
            return []
        item = self._make_item(reward_tags=tags)
        self._add_item(item)
        return [item["name"]]

    def _choose_event(self, index: int) -> str:
        event_id = self.state.get("pending_event")
        if not event_id:
            return "这里没有待选择的事件。"
        event = self.store.get("events", event_id)
        if not event:
            self.state["pending_event"] = None
            return "事件数据已失效。"
        choices = event.get("choices", [])
        if index < 1 or index > len(choices):
            return f"请选择 1-{len(choices)}。"
        choice = choices[index - 1]
        reqs = choice.get("requirements_all", [])
        missing = [r for r in reqs if not self._has_requirement(r)]
        if missing:
            return "条件不足：" + ", ".join(missing)
        self._apply_effect_list(choice.get("cost_effects", []), self.state["player"], None,
                                {"room": self._room(), "tags": self._player_tags()}, source="event_cost", tags=self._player_tags())
        check = choice.get("check")
        if check:
            stat = check.get("stat", "insight")
            result = self._check(stat, int(check.get("dc", 10)), tags=self._player_tags(), label=f"事件:{event.get('name')}")
            outcome_key = result["result"]
        else:
            outcome_key = "automatic"
        outcomes = choice.get("outcomes", [])
        candidates = [o for o in outcomes if o.get("result") == outcome_key]
        if not candidates:
            fallback = "success" if outcome_key == "critical_success" else "failure" if outcome_key == "critical_failure" else outcome_key
            candidates = [o for o in outcomes if o.get("result") == fallback] or outcomes
        outcome = self._weighted_choice(candidates) if candidates else {"text": "什么也没有发生。"}
        self._apply_effect_list(outcome.get("effects", []), self.state["player"], None,
                                {"room": self._room(), "tags": self._player_tags()}, source="event_outcome", tags=self._player_tags())
        for flag in outcome.get("set_flags", []):
            self.state["flags"][flag] = True
        rewards = self._grant_reward(outcome.get("reward_tags", []))
        self.state["pending_event"] = None
        if event.get("unique"):
            self.state["flags"][f"event_done:{event.get('id')}"] = True
        self._room()["cleared"] = True
        text = outcome.get("text", "")
        if rewards:
            text += " 获得：" + ", ".join(rewards)
        return f"{event.get('name')} · 选项{index}：{text}"

    def _use_observer(self, action_id: str) -> str:
        action = self.store.get("observer_actions", action_id)
        if not action:
            return f"找不到观测者能力：{action_id}。"
        cost = int(action.get("cost", 0))
        if cost > 0 and self.state["observer_points"] < cost:
            return "观测点不足。"
        self.state["observer_points"] -= cost
        self.state["attention"] += int(action.get("attention", 0))
        timing = action.get("timing", "before_check")
        if timing in self.state["pending_observer"]:
            self.state["pending_observer"][timing].append(action)
            if timing == "turn_start":
                self._apply_effect_list(action.get("effects", []), self.state["player"], None,
                                        {"room": self._room(), "tags": self._player_tags()}, source="observer", tags=self._player_tags())
            return f"已启用观测者能力：{action.get('name')}（消耗 {cost}，注视度 +{action.get('attention', 0)}）。"
        self._apply_effect_list(action.get("effects", []), self.state["player"], self._current_enemy(),
                                {"room": self._room(), "tags": self._player_tags()}, source="observer", tags=self._player_tags())
        return f"已启用观测者能力：{action.get('name')}。"

    # ---------- 展示、命令与入口 ----------

    def _flavor(self, category: str, tags: Iterable[str]) -> str:
        rows = [x for x in self.store.all("flavor_text") if x.get("category") == category]
        tagset = set(tags)
        matched = [x for x in rows if not x.get("tags") or tagset.intersection(x.get("tags", []))]
        return self._weighted_choice(matched or rows).get("text", "") if (matched or rows) else ""

    def status_text(self) -> str:
        return self.panel_text()

    def panel_text(self) -> str:
        """每条命令末尾附带、可以原样展示给玩家的紧凑状态面板。"""
        p = self.state["player"]
        room = self._room()
        statuses = "、".join(
            f"{name}×{info.get('stacks', 1)}({info.get('duration', 1)})"
            for name, info in p.get("statuses", {}).items()
        ) or "无"
        phase_names = {
            "exploration": "探索",
            "combat_pending": "遭遇待处理",
            "combat": "战斗",
        }
        exits = "、".join(f"{direction}→{target}" for direction, target in room.get("exits", {}).items()) or "无"
        combat = self.state.get("combat")
        enemy_text = "无"
        if combat:
            living = [f"{e['name']} {e['hp']}/{e['max_hp']}" for e in combat["enemies"] if e["hp"] > 0]
            enemy_text = "、".join(living) or "已清除"
        pending = ""
        if self.state.get("pending_event"):
            event = self.store.get("events", self.state["pending_event"]) or {}
            pending = f"｜事件 {event.get('name', self.state['pending_event'])}"
        end_text = f"｜结局 {self.state['end_state']}" if self.state.get("end_state") else ""
        return (
            f"╭─《幕外之骰》· 回合 {self.state['turn']} ─╮\n"
            f"│ 行者｜HP {p['hp']}/{p['max_hp']}｜专注 {p['focus']}/{p['max_focus']}｜命运 {p['fate']}/{p['fate_cap']}｜护盾 {p.get('shield', 0)}\n"
            f"│ 属性｜M{self._player_stat('might')} F{self._player_stat('finesse')} I{self._player_stat('insight')} W{self._player_stat('will')}｜防御 {self._player_guard()}｜减伤 {self._player_dr()}\n"
            f"│ 状态｜{statuses}\n"
            f"│ 地点｜[{room['index']}] {room['name']}｜{phase_names.get(self.state['phase'], self.state['phase'])}{pending}{end_text}\n"
            f"│ 敌情｜{enemy_text}\n"
            f"│ 出口｜{exits}\n"
            f"│ 观测者｜观测点 {self.state['observer_points']}｜注视度 {self.state['attention']}\n"
            f"╰────────────────────╯"
        )

    def inventory_text(self, compact: bool = False) -> str:
        lines = [f"背包 {len(self.state['inventory'])} 件："]
        for item in self.state["inventory"]:
            equipped = " · 已装备" if item["id"] in self.state["equipped"].values() else ""
            if compact:
                lines.append(f"{item['id']} {item['name']} [{item['slot']}] {item['quality']}{equipped}")
            else:
                lines.append(f"{item['id']} {item['name']} · {item['quality']} · 防{item['guard']} 减伤{item['damage_reduction']} 重{item['weight']}{equipped}")
        return "\n".join(lines)

    def help_text(self) -> str:
        return textwrap.dedent("""
        基础命令：status / look / map / travel north|south|east / inventory [compact]
        探索：check insight dc=14 / choose 1 / rest
        战斗：combat policy=balanced rounds=5 / fight / target 1
        成长：equip item_id / learn skill_id / upgrade skill_id
        观测者：observer status / observer use action_id / observer omen
        存档：save / export / import <token> / log last=10
        退出：quit
        """).strip()

    def map_text(self) -> str:
        rows = []
        for room in self.state["rooms"]:
            mark = "@" if room["index"] == self.state["current_room"] else "✓" if room.get("cleared") else "·"
            rows.append(f"{mark} [{room['index']}] {room['name']} ({room['room_type']})")
        return "\n".join(rows)

    def cmd(self, command: str) -> str:
        raw = command.strip()
        if raw.startswith("cmd(") and raw.endswith(")"):
            try:
                raw = ast.literal_eval(raw[4:-1])
            except Exception:
                raw = raw[4:-1].strip("'\"")
        if not raw:
            return self.help_text()
        try:
            parts = shlex.split(raw)
        except ValueError as exc:
            return f"命令解析失败：{exc}"
        op = parts[0].lower()
        args = parts[1:]
        try:
            if op in {"help", "?"}:
                result = self.help_text()
            elif op == "status":
                result = self.status_text()
            elif op == "look":
                result = self._room_text(self._room())
            elif op == "map":
                result = self.map_text()
            elif op == "inventory":
                result = self.inventory_text(compact=("compact=true" in args or "compact" in args))
            elif op == "travel":
                result = self._travel(args[0] if args else "north")
            elif op in {"combat", "fight"}:
                result = self._combat_command(args)
            elif op == "target":
                self.state["combat"]["target"] = max(0, int(args[0]) - 1)
                result = "已切换攻击目标。"
            elif op == "choose":
                result = self._choose_event(int(args[0]))
            elif op == "check":
                result = self._check_command(args)
            elif op == "rest":
                result = self._rest()
            elif op == "equip":
                result = self._equip(args[0] if args else "")
            elif op == "learn":
                result = self._learn(args[0] if args else "")
            elif op == "upgrade":
                result = self._upgrade(args[0] if args else "")
            elif op == "observer":
                result = self._observer_command(args)
            elif op == "save":
                path = self.save()
                result = f"已保存：{path}"
            elif op == "export":
                result = self.export_string()
            elif op == "import":
                result = self.import_string(" ".join(args))
            elif op == "log":
                last = 10
                for arg in args:
                    if arg.startswith("last="):
                        last = max(1, int(arg.split("=", 1)[1]))
                result = json.dumps(self.state["audit"][-last:], ensure_ascii=False, indent=2)
            elif op in {"quit", "exit"}:
                result = "再见。"
            else:
                result = f"未知命令：{op}。输入 help 查看命令。"
        except (ValueError, IndexError, KeyError) as exc:
            result = f"命令执行失败：{exc}"
        if self.dirty and self.save_path:
            self.save()
        # export 必须保持为可直接复制的纯存档串；退出命令也无需再附面板。
        if op in {"export", "quit", "exit"}:
            return result
        if op == "status":
            return self.panel_text()
        return f"{result}\n\n{self.panel_text()}"

    def _travel(self, direction: str) -> str:
        room = self._room()
        if self.state.get("combat"):
            return "战斗中不能移动。"
        if self.state.get("pending_event"):
            return "先处理当前事件。"
        if direction not in room.get("exits", {}):
            return f"没有通往 {direction} 的出口。可选：{', '.join(room.get('exits', {}))}"
        return self._enter_room(int(room["exits"][direction]))

    def _combat_command(self, args: list[str]) -> str:
        if not self.state.get("combat"):
            start = self._start_combat()
        else:
            start = ""
        policy = "balanced"
        rounds = 1 if args == [] or args == ["fight"] else 5
        for arg in args:
            if arg.startswith("policy="):
                policy = arg.split("=", 1)[1]
            if arg.startswith("rounds="):
                rounds = max(1, min(20, int(arg.split("=", 1)[1])))
        lines = [start] if start else []
        for _ in range(rounds):
            if not self.state.get("combat") or self.state.get("end_state"):
                break
            lines.extend(self._combat_round(policy=policy))
            if not self.state.get("combat") or self.state.get("end_state"):
                break
            if self.state["player"]["hp"] <= max(1, self.state["player"]["max_hp"] // 5):
                if "stop=low_hp" in args:
                    lines.append("按 stop=low_hp 停止。")
                    break
        return "\n".join(lines)

    def _check_command(self, args: list[str]) -> str:
        stat = args[0] if args else "insight"
        dc = 10
        for arg in args[1:]:
            if arg.startswith("dc="):
                dc = int(arg.split("=", 1)[1])
        result = self._check(stat, dc, tags=self._player_tags(), label=f"自由检定:{stat}")
        return f"{stat} 检定：{result['result']}，{result['total']} vs {result['dc']}（原骰 {result['raw']}）。"

    def _rest(self) -> str:
        if self.state.get("combat"):
            return "战斗中不能休息。"
        p = self.state["player"]
        p["hp"] = min(p["max_hp"], p["hp"] + 5)
        p["focus"] = min(p["max_focus"], p["focus"] + 2)
        self.state["turn"] += 1
        return "你在阴影里短暂休息：恢复 5 生命与 2 专注。"

    def _equip(self, item_id: str) -> str:
        item = self._item_by_id(item_id)
        if not item:
            return f"背包里没有 {item_id}。"
        slot = item.get("slot", "trinket")
        if slot == "trinket":
            slot = "trinket_1" if not self.state["equipped"].get("trinket_1") else "trinket_2"
        self.state["equipped"][slot] = item["id"]
        return f"已装备：{item['name']}。"

    def _learn(self, skill_id: str) -> str:
        skill = self.store.get("skills", skill_id)
        if not skill:
            return f"找不到技能：{skill_id}。"
        if skill_id in self.state["learned_skills"]:
            return "已经学会了。"
        if self.state["player"]["fate"] <= 0:
            return "命运碎片不足。"
        self.state["player"]["fate"] -= 1
        self.state["learned_skills"][skill_id] = {"level": 0}
        return f"学会：{skill.get('name')}。"

    def _upgrade(self, skill_id: str) -> str:
        skill = self.store.get("skills", skill_id)
        info = self.state["learned_skills"].get(skill_id)
        if not skill or info is None:
            return "尚未学会该技能。"
        level = int(info.get("level", 0))
        if level >= len(skill.get("upgrades", [])):
            return "该技能已达到最高等级。"
        cost = level + 1
        if self.state["player"]["fate"] < cost:
            return f"需要 {cost} 个命运碎片。"
        self.state["player"]["fate"] -= cost
        info["level"] = level + 1
        return f"{skill.get('name')} 升至 {info['level']} 级。"

    def _observer_command(self, args: list[str]) -> str:
        if not args or args[0] == "status":
            abilities = self.store.all("observer_actions")
            return f"观测点 {self.state['observer_points']} · 注视度 {self.state['attention']}\n" + "\n".join(
                f"{a.get('id')}：{a.get('name')}（cost {a.get('cost', 0)}, attention +{a.get('attention', 0)}）" for a in abilities)
        if args[0] == "use" and len(args) > 1:
            return self._use_observer(args[1])
        if args[0] == "omen":
            room = self._room()
            room["revealed"] = True
            return f"幕角落照：你看见了 {room['name']} 的结构；危险等级 {room.get('danger', 0)}。"
        return "observer status | observer use <action_id> | observer omen"


_ACTIVE_GAME: Game | None = None


def boot(data_dir: str | Path | None = None, save_path: str | Path | None = None,
         seed: int | None = None, load: bool = False) -> Game:
    """启动一个全局游戏对象，供 `cmd()`/`observer()` 调用。"""
    global _ACTIVE_GAME
    here = Path(__file__).resolve().parent
    data_dir = Path(data_dir or here / "data")
    save_path = Path(save_path or here / "save.json")
    if load and save_path.exists():
        _ACTIVE_GAME = Game.load(data_dir, save_path)
    else:
        _ACTIVE_GAME = Game.new(data_dir, save_path, seed=seed)
        _ACTIVE_GAME.save(save_path)
    return _ACTIVE_GAME


def cmd(command: str) -> str:
    if _ACTIVE_GAME is None:
        boot()
    assert _ACTIVE_GAME is not None
    return _ACTIVE_GAME.cmd(command)


def observer(command: str) -> str:
    return cmd("observer " + command)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="幕外之骰试玩版")
    parser.add_argument("--data-dir", default=str(Path(__file__).resolve().parent / "data"))
    parser.add_argument("--save", default=str(Path(__file__).resolve().parent / "save.json"))
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--load", action="store_true")
    parser.add_argument("--new", action="store_true", help="明确开始新局，不读取已有存档")
    parser.add_argument("--command", default=None, help="执行单条命令后退出，例如 --command 'look'")
    args = parser.parse_args(argv)
    should_load = args.load or (Path(args.save).exists() and not args.new)
    game = boot(args.data_dir, args.save, seed=args.seed, load=should_load)
    if args.command:
        print(game.cmd(args.command))
        game.save(args.save)
        return 0
    print(game.cmd("status"))
    print("输入 help 查看命令；输入 quit 退出。")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        output = game.cmd(line)
        print(output)
        if line.lower() in {"quit", "exit"}:
            break
    game.save(args.save)
    return 0




# 单文件版本：忽略 data_dir，直接读取下方嵌入内容。
_EMBEDDED_CONTENT = json.loads(r'''{
  "equipment_bases": [
    {
      "id": "stiletto_needle",
      "name": "刺针",
      "slot": "main_hand",
      "category": "light_weapon",
      "description": "剑身狭长呈三棱锥状，专为穿透铠甲缝隙与关节连接处设计。",
      "hands_required": 1,
      "damage_die": "1d6",
      "attack_stat": "finesse",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "blade",
        "thrust"
      ]
    },
    {
      "id": "hunting_whip",
      "name": "猎鞭",
      "slot": "main_hand",
      "category": "light_weapon",
      "description": "编织多股绳缆与细小钩刺而成的长鞭，擅长在中距离牵制敌人。",
      "hands_required": 1,
      "damage_die": "1d4",
      "attack_stat": "finesse",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "whip",
        "reach"
      ]
    },
    {
      "id": "sleeve_dagger",
      "name": "袖藏短刃",
      "slot": "main_hand",
      "category": "light_weapon",
      "description": "形制窄薄，护手极小，可以贴着前臂藏进袖口或绑带。",
      "hands_required": 1,
      "damage_die": "1d6",
      "attack_stat": "finesse",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "blade",
        "concealable"
      ]
    },
    {
      "id": "hooked_sickle",
      "name": "弯钩短镰",
      "slot": "main_hand",
      "category": "light_weapon",
      "description": "弧度极大的内弯短刃，尾端带有配重环，便于钩拉与近身割切。",
      "hands_required": 1,
      "damage_die": "1d6",
      "attack_stat": "finesse",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "blade",
        "hook"
      ]
    },
    {
      "id": "executioner_sword",
      "name": "斩首大剑",
      "slot": "main_hand",
      "category": "heavy_weapon",
      "description": "剑端平宽无尖头，重心极度靠前，依靠强大的惯性完成斩切。",
      "hands_required": 2,
      "damage_die": "2d6",
      "attack_stat": "might",
      "guard": 1,
      "damage_reduction": 0,
      "weight": 3,
      "tags": [
        "blade",
        "cleave",
        "heavy"
      ]
    },
    {
      "id": "incense_flail",
      "name": "香炉连枷",
      "slot": "main_hand",
      "category": "heavy_weapon",
      "description": "长链末端连接着多孔的重型镂空锤球，摆动时散发阵阵烟气。",
      "hands_required": 1,
      "damage_die": "1d8",
      "attack_stat": "might",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 2,
      "tags": [
        "blunt",
        "chain",
        "incense"
      ]
    },
    {
      "id": "war_pick",
      "name": "破甲战镐",
      "slot": "main_hand",
      "category": "heavy_weapon",
      "description": "头部呈长角状喙刺，专门用来击穿厚重铠甲与板材。",
      "hands_required": 1,
      "damage_die": "1d8",
      "attack_stat": "might",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 2,
      "tags": [
        "piercing",
        "heavy"
      ]
    },
    {
      "id": "hanging_censer",
      "name": "悬吊手炉",
      "slot": "main_hand",
      "category": "focus",
      "description": "带有锁链配重的握持式手炉，炉身刻满祈祷纹路，用于引导精神专注。",
      "hands_required": 1,
      "damage_die": "1d4",
      "attack_stat": "will",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "holy",
        "ritual"
      ]
    },
    {
      "id": "carved_tome",
      "name": "刻印典籍",
      "slot": "main_hand",
      "category": "focus",
      "description": "页脚带有硬质包角的大型仪式典籍，记载着复杂的符文排列。",
      "hands_required": 2,
      "damage_die": "1d6",
      "attack_stat": "insight",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 2,
      "tags": [
        "occult",
        "book"
      ]
    },
    {
      "id": "divining_rod",
      "name": "占卜杖",
      "slot": "main_hand",
      "category": "focus",
      "description": "分叉顶端留有固定占卜媒介的爪座，长柄便于沿地面与墙壁缓慢探查。",
      "hands_required": 1,
      "damage_die": "1d4",
      "attack_stat": "insight",
      "guard": 0,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "divination",
        "staff"
      ]
    },
    {
      "id": "tower_shield",
      "name": "塔盾",
      "slot": "off_hand",
      "category": "shield",
      "description": "高度几乎遮蔽全身的直立大盾，底端带有用于锚定地面的排齿。",
      "hands_required": 1,
      "guard": 3,
      "damage_reduction": 1,
      "weight": 3,
      "tags": [
        "shield",
        "heavy"
      ]
    },
    {
      "id": "buckler",
      "name": "小圆盾",
      "slot": "off_hand",
      "category": "shield",
      "description": "抓握于手掌中心的小型凸面圆盾，便于快速格挡与弹开刺击。",
      "hands_required": 1,
      "guard": 1,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "shield",
        "parry"
      ]
    },
    {
      "id": "patched_armor",
      "name": "拼接胸甲",
      "slot": "body",
      "category": "light_armor",
      "description": "由多块经过硬化处理的衬板缝合而成的护甲，兼顾灵活性与基础防护。",
      "hands_required": 0,
      "guard": 1,
      "damage_reduction": 1,
      "weight": 1,
      "tags": [
        "flexible",
        "armor"
      ]
    },
    {
      "id": "studded_armor",
      "name": "钉板胸甲",
      "slot": "body",
      "category": "light_armor",
      "description": "关键部位排布着密集的加固凸钉，肩肘仍保留足够的活动余量。",
      "hands_required": 0,
      "guard": 2,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "studded",
        "armor"
      ]
    },
    {
      "id": "half_plate_armor",
      "name": "半身重甲",
      "slot": "body",
      "category": "heavy_armor",
      "description": "覆盖胸腹与肩部的重型甲板，搭配带扣固定，提供稳固的正面防护。",
      "hands_required": 0,
      "guard": 3,
      "damage_reduction": 2,
      "weight": 3,
      "tags": [
        "plate",
        "heavy"
      ]
    },
    {
      "id": "brigandine_armor",
      "name": "叠层胸甲",
      "slot": "body",
      "category": "heavy_armor",
      "description": "外层包裹结实衬面，内侧重叠铆接许多小块硬质防护片的复合重甲。",
      "hands_required": 0,
      "guard": 2,
      "damage_reduction": 2,
      "weight": 2,
      "tags": [
        "plate",
        "brigandine"
      ]
    },
    {
      "id": "traveler_cloak",
      "name": "旅人斗篷",
      "slot": "body",
      "category": "garment",
      "description": "宽大的加厚面料斗篷，带有兜帽，能遮挡风雨并掩盖身体轮廓。",
      "hands_required": 0,
      "guard": 1,
      "damage_reduction": 0,
      "weight": 1,
      "tags": [
        "cloth",
        "cloak"
      ]
    },
    {
      "id": "ascetic_robe",
      "name": "苦修长袍",
      "slot": "body",
      "category": "garment",
      "description": "裁剪简单的粗布长袍，束腰固定，不提供实体护甲却便于施展动作。",
      "hands_required": 0,
      "guard": 0,
      "damage_reduction": 0,
      "weight": 0,
      "tags": [
        "cloth",
        "robe"
      ]
    },
    {
      "id": "pendant_amulet",
      "name": "路祷坠符",
      "slot": "trinket",
      "category": "accessory",
      "description": "悬挂于胸前的雕花护身符，刻有古老的路途祷文。",
      "hands_required": 0,
      "guard": 0,
      "damage_reduction": 0,
      "weight": 0,
      "tags": [
        "amulet",
        "holy"
      ]
    },
    {
      "id": "signet_ring",
      "name": "印章戒指",
      "slot": "trinket",
      "category": "accessory",
      "description": "戒面刻有未知家族徽记的重型戒指，可用于盖印或作为标志。",
      "hands_required": 0,
      "guard": 0,
      "damage_reduction": 0,
      "weight": 0,
      "tags": [
        "ring",
        "signet"
      ]
    }
  ],
  "materials": [
    {
      "id": "cold_iron",
      "name": "冷铁",
      "rarity": "common",
      "power_budget": 0,
      "description": "低温锤打锻造的粗糙铁材，对异质气息有天然的排斥。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon",
        "shield",
        "heavy_armor"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": 0,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "metal",
        "cold"
      ]
    },
    {
      "id": "grave_silver",
      "name": "墓银",
      "rarity": "uncommon",
      "power_budget": 1,
      "description": "从古老墓穴殉葬品中熔炼出的暗沉白银，质地韧软且传导灵性。",
      "allowed_categories": [
        "light_weapon",
        "focus",
        "accessory"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": -1,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "metal",
        "holy"
      ]
    },
    {
      "id": "bone_ash_steel",
      "name": "骨灰钢",
      "rarity": "rare",
      "power_budget": 3,
      "description": "折叠锻打时掺入兽骨细粉的坚硬钢材，淬火后呈灰白纹理。",
      "allowed_categories": [
        "heavy_weapon",
        "heavy_armor",
        "shield"
      ],
      "guard_mod": 1,
      "damage_reduction_mod": 0,
      "weight_mod": 1,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "metal",
        "bone"
      ]
    },
    {
      "id": "mourning_silk",
      "name": "悼亡丝",
      "rarity": "common",
      "power_budget": 1,
      "description": "使用黑蚕吐出的暗色丝线纺织成的面料，触感冰凉且不吸水分。",
      "allowed_categories": [
        "garment",
        "focus"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": -1,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "cloth",
        "soft"
      ]
    },
    {
      "id": "ash_leather",
      "name": "灰烬皮革",
      "rarity": "uncommon",
      "power_budget": 1,
      "description": "浸泡在植物灰碱水中反复鞣制的厚重皮革，耐磨损且防水。",
      "allowed_categories": [
        "light_armor",
        "garment",
        "shield"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 1,
      "weight_mod": 0,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "leather",
        "tough"
      ]
    },
    {
      "id": "bog_oak",
      "name": "沼泽黑橡",
      "rarity": "uncommon",
      "power_budget": 1,
      "description": "在淤泥深处沉淀百年的炭化橡木，质地如石般坚硬且不易腐朽。",
      "allowed_categories": [
        "focus",
        "shield",
        "light_weapon"
      ],
      "guard_mod": 1,
      "damage_reduction_mod": 0,
      "weight_mod": 0,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "wood",
        "dense"
      ]
    },
    {
      "id": "bleached_bone",
      "name": "漂白兽骨",
      "rarity": "common",
      "power_budget": 0,
      "description": "经日光与盐水风干剥离的坚硬骨骼，表面刻有天然的微小孔隙。",
      "allowed_categories": [
        "light_weapon",
        "focus",
        "accessory"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": 0,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "bone",
        "light"
      ]
    },
    {
      "id": "dusk_brass",
      "name": "黄昏黄铜",
      "rarity": "uncommon",
      "power_budget": 1,
      "description": "色泽黯淡的暗金铜合金，击打时发出的声音沉闷而传之甚远。",
      "allowed_categories": [
        "focus",
        "accessory",
        "heavy_weapon"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": 1,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "metal",
        "sound"
      ]
    },
    {
      "id": "obsidian_glass",
      "name": "黑曜玻璃",
      "rarity": "rare",
      "power_budget": 4,
      "description": "火山熔岩急速凝固形成的黑玻璃，断口极其锋利但耐受力较差。",
      "allowed_categories": [
        "light_weapon",
        "focus",
        "accessory"
      ],
      "guard_mod": -1,
      "damage_reduction_mod": 0,
      "weight_mod": 0,
      "damage_die_step": 2,
      "effects": [],
      "tags": [
        "glass",
        "sharp"
      ]
    },
    {
      "id": "plague_copper",
      "name": "疫病青铜",
      "rarity": "common",
      "power_budget": 0,
      "description": "表面生成厚重铜绿的古老青铜，散发着陈腐的金属气味。",
      "allowed_categories": [
        "heavy_weapon",
        "heavy_armor",
        "shield"
      ],
      "guard_mod": 1,
      "damage_reduction_mod": 0,
      "weight_mod": 1,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "metal",
        "ancient"
      ]
    },
    {
      "id": "whitetail_sinew",
      "name": "白尾兽筋",
      "rarity": "common",
      "power_budget": 0,
      "description": "经过浸油与抽拉处理的野兽大筋，拥有惊人的拉伸韧性。",
      "allowed_categories": [
        "light_weapon",
        "garment"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": 0,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "organ",
        "flexible"
      ]
    },
    {
      "id": "meteorite_ore",
      "name": "陨星铁矿",
      "rarity": "rare",
      "power_budget": 4,
      "description": "坠落天外熔岩残余的黑陨铁，极其沉重且能吸收外界撞击。",
      "allowed_categories": [
        "heavy_weapon",
        "heavy_armor"
      ],
      "guard_mod": 1,
      "damage_reduction_mod": 1,
      "weight_mod": 2,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "metal",
        "rare"
      ]
    },
    {
      "id": "hallowed_amber",
      "name": "圣化琥珀",
      "rarity": "epic",
      "power_budget": 7,
      "description": "包裹着古代孢子与昆虫的透明琥珀，摸上去永远带着微温。",
      "allowed_categories": [
        "focus",
        "accessory"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": -1,
      "damage_die_step": 0,
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "advantage",
          "target": "current_check",
          "condition_tags_any": [
            "holy"
          ]
        },
        {
          "trigger": "on_hit",
          "operation": "heal",
          "target": "self",
          "value": 1,
          "condition_tags_any": [
            "holy"
          ]
        }
      ],
      "tags": [
        "gem",
        "holy"
      ]
    },
    {
      "id": "shadow_weave_felt",
      "name": "影织毡毛",
      "rarity": "uncommon",
      "power_budget": 1,
      "description": "使用深山野羊粗毛压制而成的厚毛毡，能有效吸收摩擦声响。",
      "allowed_categories": [
        "garment",
        "light_armor"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 1,
      "weight_mod": 0,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "cloth",
        "stealth"
      ]
    },
    {
      "id": "lead_alloy",
      "name": "铅锡合金",
      "rarity": "uncommon",
      "power_budget": 1,
      "description": "高密度的软质重金属合金，常用于配重或吸收强烈振动。",
      "allowed_categories": [
        "heavy_weapon",
        "shield",
        "heavy_armor"
      ],
      "guard_mod": 1,
      "damage_reduction_mod": 0,
      "weight_mod": 2,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "metal",
        "heavy"
      ]
    },
    {
      "id": "raven_feather_cloth",
      "name": "乌鸦羽布",
      "rarity": "epic",
      "power_budget": 6,
      "description": "将漆黑羽毛交织编入布匹中的特殊织物，轻盈且随风飘甩。",
      "allowed_categories": [
        "garment",
        "accessory"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": -1,
      "damage_die_step": 0,
      "effects": [
        {
          "trigger": "on_check",
          "operation": "advantage",
          "target": "current_check",
          "condition_tags_any": [
            "light"
          ]
        },
        {
          "trigger": "passive",
          "operation": "stat_mod",
          "target": "self",
          "stat": "finesse",
          "value": 1,
          "condition_tags_any": [
            "feather"
          ]
        }
      ],
      "tags": [
        "feather",
        "light"
      ]
    },
    {
      "id": "blood_vein_stone",
      "name": "血脉矿石",
      "rarity": "epic",
      "power_budget": 7,
      "description": "内部布满红色网状纹理的原石，对体液与温度变化十分敏感。",
      "allowed_categories": [
        "focus",
        "accessory",
        "light_weapon"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": 0,
      "damage_die_step": 1,
      "effects": [
        {
          "trigger": "on_hit",
          "operation": "heal",
          "target": "self",
          "value": 2,
          "condition_tags_any": [
            "occult"
          ]
        },
        {
          "trigger": "on_kill",
          "operation": "resource_gain",
          "target": "self",
          "resource": "focus",
          "value": 1,
          "condition_tags_any": [
            "occult"
          ]
        }
      ],
      "tags": [
        "mineral",
        "occult"
      ]
    },
    {
      "id": "thorn_vine_wood",
      "name": "荆棘藤木",
      "rarity": "common",
      "power_budget": 0,
      "description": "干瘪交错的硬质藤木，表皮带有些许未褪去的坚硬刺角。",
      "allowed_categories": [
        "light_weapon",
        "focus",
        "shield"
      ],
      "guard_mod": 0,
      "damage_reduction_mod": 0,
      "weight_mod": 0,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "wood",
        "thorny"
      ]
    },
    {
      "id": "phantom_thread",
      "name": "幻影蛛丝",
      "rarity": "rare",
      "power_budget": 4,
      "description": "来自深渊巨蛛的韧性单丝，透明细瘦却难以用普通手段割断。",
      "allowed_categories": [
        "garment",
        "light_armor"
      ],
      "guard_mod": 1,
      "damage_reduction_mod": 1,
      "weight_mod": -1,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "silk",
        "rare"
      ]
    },
    {
      "id": "chitin_shell",
      "name": "黑甲壳",
      "rarity": "rare",
      "power_budget": 3,
      "description": "剥离自巨型害虫的硬质外壳，兼具弧形偏斜力与绝佳防腐性。",
      "allowed_categories": [
        "light_armor",
        "heavy_armor",
        "shield"
      ],
      "guard_mod": 1,
      "damage_reduction_mod": 1,
      "weight_mod": 0,
      "damage_die_step": 0,
      "effects": [],
      "tags": [
        "chitin",
        "sturdy"
      ]
    }
  ],
  "affixes": [
    {
      "id": "prefix_keen",
      "name": "锐利的",
      "rarity": "common",
      "power_budget": 1,
      "description": "经过精细打磨，边缘极其锋利。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon"
      ],
      "tags": [
        "sharp",
        "offense"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "prefix_sturdy",
      "name": "坚固的",
      "rarity": "common",
      "power_budget": 1,
      "description": "结构强化，能有效招架外部冲击。",
      "allowed_categories": [
        "shield",
        "heavy_armor",
        "light_armor"
      ],
      "tags": [
        "defense",
        "sturdy"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "prefix_heavy",
      "name": "沉重的",
      "rarity": "common",
      "power_budget": 0,
      "description": "用料扎实额外加重，虽然不易挥舞但招架性能卓越。",
      "allowed_categories": [
        "heavy_weapon",
        "heavy_armor",
        "shield"
      ],
      "tags": [
        "heavy",
        "metal"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "passive",
          "operation": "weight_mod",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "prefix_light",
      "name": "轻巧的",
      "rarity": "common",
      "power_budget": 1,
      "description": "削减多余重量，穿戴和挥舞时更加灵活。",
      "allowed_categories": [
        "light_weapon",
        "garment",
        "light_armor"
      ],
      "tags": [
        "light",
        "agility"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "weight_mod",
          "target": "self",
          "value": -1
        }
      ]
    },
    {
      "id": "prefix_rusted",
      "name": "斑驳的",
      "rarity": "uncommon",
      "power_budget": 1,
      "description": "表面带有岁月的锈蚀或剥落纹理，质地反而更加紧实。",
      "allowed_categories": [
        "heavy_armor",
        "shield"
      ],
      "tags": [
        "ancient",
        "tough"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "prefix_blessed",
      "name": "受赐福的",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "浸润过圣水与祷告，在施放圣洁术式时能带来加成。",
      "allowed_categories": [
        "focus",
        "accessory"
      ],
      "tags": [
        "holy",
        "magic"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d4",
          "condition_tags_any": [
            "holy"
          ]
        }
      ]
    },
    {
      "id": "prefix_jagged",
      "name": "锯齿的",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "边缘呈不规则的锯齿状，牺牲了防御换取极高的撕裂威力。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon"
      ],
      "tags": [
        "sharp",
        "vicious"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": -1
        },
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "on_hit",
          "operation": "damage",
          "target": "enemy",
          "value": 1,
          "condition_tags_any": [
            "sharp"
          ]
        }
      ]
    },
    {
      "id": "prefix_padded",
      "name": "加衬的",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "内侧缝入厚实软垫，大幅缓冲受到的直接冲击。",
      "allowed_categories": [
        "light_armor",
        "garment",
        "heavy_armor"
      ],
      "tags": [
        "defense",
        "soft"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "prefix_swift",
      "name": "疾风的",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "附着轻盈的风之气息，闪避后获得短暂的战斗优势。",
      "allowed_categories": [
        "garment",
        "accessory",
        "light_weapon"
      ],
      "tags": [
        "speed",
        "wind"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "weight_mod",
          "target": "self",
          "value": -1
        },
        {
          "trigger": "on_check_success",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d4",
          "condition_tags_any": [
            "agility"
          ]
        }
      ]
    },
    {
      "id": "prefix_vampiric",
      "name": "汲血的",
      "rarity": "rare",
      "power_budget": 4,
      "description": "散发着令人不适的血腥味，命中时可汲取敌人的生机。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon",
        "focus"
      ],
      "tags": [
        "blood",
        "occult"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "on_hit",
          "operation": "heal",
          "target": "self",
          "value": 1,
          "condition_tags_any": [
            "occult"
          ]
        }
      ]
    },
    {
      "id": "prefix_fortified",
      "name": "堡垒的",
      "rarity": "rare",
      "power_budget": 4,
      "description": "重型防卫技术的集大成者，提供极高的防护与招架能力。",
      "allowed_categories": [
        "heavy_armor",
        "shield"
      ],
      "tags": [
        "defense",
        "fortress"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 2
        },
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "passive",
          "operation": "weight_mod",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "prefix_runic",
      "name": "刻符的",
      "rarity": "rare",
      "power_budget": 4,
      "description": "表面刻满了微光的秘法符文，显著提升攻击和施法威力。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon",
        "focus"
      ],
      "tags": [
        "rune",
        "magic"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "on_skill_use",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d4",
          "condition_tags_any": [
            "magic"
          ]
        }
      ]
    },
    {
      "id": "prefix_dread",
      "name": "恐惧的",
      "rarity": "rare",
      "power_budget": 5,
      "description": "裹挟着死亡与绝望的冷意，命中时能震撼敌人的心智。",
      "allowed_categories": [
        "heavy_weapon",
        "focus",
        "accessory"
      ],
      "tags": [
        "dark",
        "fear"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "on_hit",
          "operation": "damage",
          "target": "enemy",
          "value": 2,
          "condition_tags_any": [
            "dark"
          ]
        }
      ]
    },
    {
      "id": "prefix_celestial",
      "name": "星穹的",
      "rarity": "epic",
      "power_budget": 7,
      "description": "引动天体轨道的神秘律动，回合开始时为你注满星辉之力。",
      "allowed_categories": [
        "focus",
        "accessory",
        "garment"
      ],
      "tags": [
        "celestial",
        "holy"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "weight_mod",
          "target": "self",
          "value": -1
        },
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "turn_start",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d6",
          "condition_tags_any": [
            "holy"
          ]
        }
      ]
    },
    {
      "id": "prefix_abyssal",
      "name": "深渊的",
      "rarity": "epic",
      "power_budget": 7,
      "description": "自地底最黑暗的缝隙中淬炼而成，击杀敌人后能反噬敌人的灵魂治疗自身。",
      "allowed_categories": [
        "heavy_weapon",
        "light_weapon",
        "focus"
      ],
      "tags": [
        "dark",
        "abyssal"
      ],
      "position": "prefix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 2
        },
        {
          "trigger": "on_kill",
          "operation": "heal",
          "target": "self",
          "value": 3,
          "condition_tags_any": [
            "dark"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_protection",
      "name": "庇护之",
      "rarity": "common",
      "power_budget": 1,
      "description": "赋予佩戴者基础的防伤害效果。",
      "allowed_categories": [
        "light_armor",
        "heavy_armor",
        "garment",
        "shield"
      ],
      "tags": [
        "defense",
        "ward"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "suffix_of_impact",
      "name": "冲击之",
      "rarity": "common",
      "power_budget": 1,
      "description": "增强武器或攻击媒介的力道与穿透性。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon"
      ],
      "tags": [
        "offense",
        "impact"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "suffix_of_balance",
      "name": "平衡之",
      "rarity": "common",
      "power_budget": 0,
      "description": "优化重心分布，略微降低装备的负重感。",
      "allowed_categories": [
        "heavy_weapon",
        "shield",
        "heavy_armor"
      ],
      "tags": [
        "utility",
        "balance"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "weight_mod",
          "target": "self",
          "value": -1
        }
      ]
    },
    {
      "id": "suffix_of_guarding",
      "name": "招架之",
      "rarity": "common",
      "power_budget": 1,
      "description": "侧重于格挡与架势维持的结构设计。",
      "allowed_categories": [
        "shield",
        "heavy_weapon",
        "light_weapon"
      ],
      "tags": [
        "guard",
        "parry"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "suffix_of_warding",
      "name": "辟邪之",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "兼具物理与灵性阻隔，稳定提升综合防御性能。",
      "allowed_categories": [
        "shield",
        "heavy_armor",
        "accessory"
      ],
      "tags": [
        "ward",
        "holy"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 1
        }
      ]
    },
    {
      "id": "suffix_of_venom",
      "name": "毒液之",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "附着剧毒痕迹，命中敌人时附加额外的毒性侵蚀。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon",
        "focus"
      ],
      "tags": [
        "poison",
        "dot"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "on_hit",
          "operation": "damage",
          "target": "enemy",
          "value": 1,
          "condition_tags_any": [
            "poison"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_flame",
      "name": "烈焰之",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "带有灼热余温，攻击时能撕裂目标并造成燃烧效益。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon",
        "focus"
      ],
      "tags": [
        "fire",
        "elemental"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "on_hit",
          "operation": "damage",
          "target": "enemy",
          "value": 1,
          "condition_tags_any": [
            "fire"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_frost",
      "name": "寒霜之",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "凝结着不化的霜雪，受创时能激发冰晶反制与护盾。",
      "allowed_categories": [
        "shield",
        "light_armor",
        "accessory"
      ],
      "tags": [
        "ice",
        "defense"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "on_damaged",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d4",
          "condition_tags_any": [
            "ice"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_echoes",
      "name": "回响之",
      "rarity": "uncommon",
      "power_budget": 2,
      "description": "施法时能引发低沉震荡，强化后续法术表现。",
      "allowed_categories": [
        "focus",
        "accessory"
      ],
      "tags": [
        "sound",
        "magic"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d4",
          "condition_tags_any": [
            "sound"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_slaughter",
      "name": "屠戮之",
      "rarity": "rare",
      "power_budget": 4,
      "description": "为了纯粹的杀戮而打造，击杀敌人后激发更为狂暴的攻势。",
      "allowed_categories": [
        "heavy_weapon",
        "light_weapon"
      ],
      "tags": [
        "offense",
        "ferocity"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 2
        },
        {
          "trigger": "on_kill",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d6",
          "condition_tags_any": [
            "offense"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_immortality",
      "name": "不朽之",
      "rarity": "rare",
      "power_budget": 5,
      "description": "蕴含永恒不灭的生机，在回合开始时为你提供持续回复。",
      "allowed_categories": [
        "heavy_armor",
        "garment",
        "accessory"
      ],
      "tags": [
        "life",
        "immortal"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 2
        },
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "turn_start",
          "operation": "heal",
          "target": "self",
          "value": 1,
          "condition_tags_any": [
            "life"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_the_void",
      "name": "虚空之",
      "rarity": "rare",
      "power_budget": 4,
      "description": "连接着不可见的无底虚空，在攻击时蚕食敌方的灵性并反哺使用者。",
      "allowed_categories": [
        "focus",
        "light_weapon",
        "accessory"
      ],
      "tags": [
        "void",
        "occult"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "weight_mod",
          "target": "self",
          "value": -1
        },
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "on_hit",
          "operation": "heal",
          "target": "self",
          "value": 1,
          "condition_tags_any": [
            "void"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_shadows",
      "name": "影子之",
      "rarity": "rare",
      "power_budget": 4,
      "description": "将使用者融于阴影之中，大幅降低存在感并提供闪避增益。",
      "allowed_categories": [
        "garment",
        "light_armor",
        "accessory"
      ],
      "tags": [
        "shadow",
        "stealth"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "weight_mod",
          "target": "self",
          "value": -2
        },
        {
          "trigger": "on_check_success",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d6",
          "condition_tags_any": [
            "stealth"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_bloodshed",
      "name": "血祭之",
      "rarity": "epic",
      "power_budget": 7,
      "description": "渴望鲜血的残暴力量，命中生命时疯狂汲取生命，击杀时恢复巨额气血。",
      "allowed_categories": [
        "heavy_weapon",
        "light_weapon",
        "focus"
      ],
      "tags": [
        "blood",
        "occult"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_die_step",
          "target": "self",
          "value": 2
        },
        {
          "trigger": "on_hit",
          "operation": "heal",
          "target": "self",
          "value": 2,
          "condition_tags_any": [
            "blood"
          ]
        },
        {
          "trigger": "on_kill",
          "operation": "heal",
          "target": "self",
          "value": 2,
          "condition_tags_any": [
            "blood"
          ]
        }
      ]
    },
    {
      "id": "suffix_of_the_titans",
      "name": "泰坦之",
      "rarity": "epic",
      "power_budget": 6,
      "description": "如远古山岳般不可动摇，承受打击时激起巍峨的反制威能。",
      "allowed_categories": [
        "heavy_armor",
        "shield"
      ],
      "tags": [
        "titan",
        "heavy"
      ],
      "position": "suffix",
      "effects": [
        {
          "trigger": "passive",
          "operation": "guard_mod",
          "target": "self",
          "value": 3
        },
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 2
        },
        {
          "trigger": "on_damaged",
          "operation": "bonus_die",
          "target": "current_check",
          "die": "1d6",
          "condition_tags_any": [
            "heavy"
          ]
        }
      ]
    },
    {
      "id": "curse_blood_offering",
      "name": "渴血",
      "position": "curse",
      "rarity": "rare",
      "description": "攻击命中时追加额外伤害，但使用者每次命中都会因伤口撕裂而陷入流血。",
      "allowed_categories": [
        "light_weapon",
        "heavy_weapon"
      ],
      "effects": [
        {
          "trigger": "on_hit",
          "operation": "bonus_die",
          "target": "enemy",
          "die": "1d6"
        },
        {
          "trigger": "on_hit",
          "operation": "apply_status",
          "target": "self",
          "status": "bleed",
          "stacks": 1,
          "duration": 2
        }
      ],
      "tags": [
        "blood",
        "curse",
        "weapon"
      ],
      "power_budget": 3
    },
    {
      "id": "curse_soul_drain",
      "name": "噬魂",
      "position": "curse",
      "rarity": "epic",
      "description": "使用技能时恢复专注点，但灵魂损耗会导致有几率失去命运碎片。",
      "allowed_categories": [
        "focus",
        "accessory"
      ],
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "resource_gain",
          "target": "self",
          "resource": "focus",
          "value": 1
        },
        {
          "trigger": "on_skill_use",
          "operation": "resource_loss",
          "target": "self",
          "resource": "fate",
          "value": 1,
          "chance": 50
        }
      ],
      "tags": [
        "soul",
        "curse",
        "resource"
      ],
      "power_budget": 4
    },
    {
      "id": "curse_eye_of_the_watcher",
      "name": "窥天",
      "position": "curse",
      "rarity": "rare",
      "description": "进入新房间时揭示内部威胁，但频繁的窥探会吸引幕外观测者的注视。",
      "allowed_categories": [
        "accessory"
      ],
      "effects": [
        {
          "trigger": "on_enter_room",
          "operation": "reveal",
          "target": "current_room",
          "value": 1
        },
        {
          "trigger": "on_enter_room",
          "operation": "resource_gain",
          "target": "world",
          "resource": "attention",
          "value": 1
        }
      ],
      "tags": [
        "vision",
        "curse",
        "observer"
      ],
      "power_budget": 2
    },
    {
      "id": "curse_mad_whisper",
      "name": "狂语",
      "position": "curse",
      "rarity": "rare",
      "description": "极大提升洞察力，但脑海中残留的耳语有概率在每回合开始时引发恐惧。",
      "allowed_categories": [
        "garment",
        "accessory"
      ],
      "effects": [
        {
          "trigger": "passive",
          "operation": "stat_mod",
          "target": "self",
          "stat": "insight",
          "value": 2
        },
        {
          "trigger": "turn_start",
          "operation": "apply_status",
          "target": "self",
          "status": "fear",
          "stacks": 1,
          "duration": 1,
          "chance": 30
        }
      ],
      "tags": [
        "mind",
        "curse",
        "stat"
      ],
      "power_budget": 3
    },
    {
      "id": "curse_bell_of_summoning",
      "name": "招魂",
      "position": "curse",
      "rarity": "epic",
      "description": "战斗开始时生成坚固护盾，但沉重的祷告声会立刻吸引新的敌人赶来。",
      "allowed_categories": [
        "accessory"
      ],
      "effects": [
        {
          "trigger": "on_combat_start",
          "operation": "shield",
          "target": "self",
          "value": 8
        },
        {
          "trigger": "on_combat_start",
          "operation": "spawn",
          "target": "current_room",
          "value": 1
        }
      ],
      "tags": [
        "summon",
        "curse",
        "shield"
      ],
      "power_budget": 5
    },
    {
      "id": "curse_shackles_of_might",
      "name": "蛮暴",
      "position": "curse",
      "rarity": "uncommon",
      "description": "大幅提高力量基础，但笨重僵硬的体态会导致灵巧降低。",
      "allowed_categories": [
        "heavy_armor",
        "heavy_weapon"
      ],
      "effects": [
        {
          "trigger": "passive",
          "operation": "stat_mod",
          "target": "self",
          "stat": "might",
          "value": 2
        },
        {
          "trigger": "passive",
          "operation": "stat_mod",
          "target": "self",
          "stat": "finesse",
          "value": -1
        }
      ],
      "tags": [
        "might",
        "curse",
        "stat"
      ],
      "power_budget": 1
    },
    {
      "id": "curse_shattered_shield",
      "name": "蚀骨",
      "position": "curse",
      "rarity": "rare",
      "description": "提供稳定的伤害减免，但受到伤害时容易因冲击陷入失衡状态。",
      "allowed_categories": [
        "heavy_armor",
        "light_armor"
      ],
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 3
        },
        {
          "trigger": "on_damaged",
          "operation": "apply_status",
          "target": "self",
          "status": "stagger",
          "stacks": 1,
          "duration": 1
        }
      ],
      "tags": [
        "defense",
        "curse",
        "armor"
      ],
      "power_budget": 3
    },
    {
      "id": "curse_greedy_pact",
      "name": "贪婪",
      "position": "curse",
      "rarity": "epic",
      "description": "击杀敌人可获得命运碎片，但沾染的血腥味会使自身立刻被标记。",
      "allowed_categories": [
        "accessory"
      ],
      "effects": [
        {
          "trigger": "on_kill",
          "operation": "resource_gain",
          "target": "self",
          "resource": "fate",
          "value": 1
        },
        {
          "trigger": "on_kill",
          "operation": "apply_status",
          "target": "self",
          "status": "mark",
          "stacks": 1,
          "duration": 2
        }
      ],
      "tags": [
        "greed",
        "curse",
        "fate"
      ],
      "power_budget": 4
    },
    {
      "id": "curse_witch_flame",
      "name": "巫火",
      "position": "curse",
      "rarity": "rare",
      "description": "暴击时能对敌人施加剧烈燃烧，但余火同时也会反噬自身。",
      "allowed_categories": [
        "focus"
      ],
      "effects": [
        {
          "trigger": "on_crit",
          "operation": "apply_status",
          "target": "enemy",
          "status": "burn",
          "stacks": 2,
          "duration": 2
        },
        {
          "trigger": "on_crit",
          "operation": "apply_status",
          "target": "self",
          "status": "burn",
          "stacks": 1,
          "duration": 2
        }
      ],
      "tags": [
        "fire",
        "curse",
        "elemental"
      ],
      "power_budget": 2
    },
    {
      "id": "curse_decayed_crown",
      "name": "朽冠",
      "position": "curse",
      "rarity": "relic",
      "description": "回合开始时恢复生命值，但头戴诅咒冠冕会使所有技能检定陷入劣势。",
      "allowed_categories": [
        "accessory"
      ],
      "effects": [
        {
          "trigger": "turn_start",
          "operation": "heal",
          "target": "self",
          "value": 3
        },
        {
          "trigger": "on_check",
          "operation": "disadvantage",
          "target": "current_check"
        }
      ],
      "tags": [
        "relic",
        "curse",
        "heal"
      ],
      "power_budget": 6
    },
    {
      "id": "curse_bone_whistle",
      "name": "骨笛",
      "position": "curse",
      "rarity": "uncommon",
      "description": "战斗开始时获得短暂护佑，但笛声止息后会因精神透支失去专注。",
      "allowed_categories": [
        "accessory",
        "focus"
      ],
      "effects": [
        {
          "trigger": "on_combat_start",
          "operation": "apply_status",
          "target": "self",
          "status": "ward",
          "stacks": 1,
          "duration": 2
        },
        {
          "trigger": "on_combat_end",
          "operation": "resource_loss",
          "target": "self",
          "resource": "focus",
          "value": 1
        }
      ],
      "tags": [
        "sound",
        "curse",
        "ward"
      ],
      "power_budget": 1
    },
    {
      "id": "curse_poison_spike",
      "name": "毒刺",
      "position": "curse",
      "rarity": "rare",
      "description": "格挡成功后反击敌人，但带毒的刺棘同样会使自身陷入中毒状态。",
      "allowed_categories": [
        "shield",
        "light_armor"
      ],
      "effects": [
        {
          "trigger": "on_block",
          "operation": "counterattack",
          "target": "attacker",
          "value": 4
        },
        {
          "trigger": "on_block",
          "operation": "apply_status",
          "target": "self",
          "status": "poison",
          "stacks": 1,
          "duration": 2
        }
      ],
      "tags": [
        "poison",
        "curse",
        "counter"
      ],
      "power_budget": 3
    },
    {
      "id": "miracle_martyr_grace",
      "name": "殉道之恩",
      "position": "miracle",
      "rarity": "epic",
      "description": "在生命值极低时触发强力护盾与护佑，但强行催动力量会消耗专注点。",
      "allowed_categories": [
        "garment",
        "accessory"
      ],
      "effects": [
        {
          "trigger": "on_low_hp",
          "operation": "shield",
          "target": "self",
          "value": 12
        },
        {
          "trigger": "on_low_hp",
          "operation": "apply_status",
          "target": "self",
          "status": "ward",
          "stacks": 2,
          "duration": 2
        },
        {
          "trigger": "on_low_hp",
          "operation": "resource_loss",
          "target": "self",
          "resource": "focus",
          "value": 2
        }
      ],
      "tags": [
        "holy",
        "miracle",
        "crisis"
      ],
      "power_budget": 6
    },
    {
      "id": "miracle_radiant_verdict",
      "name": "光芒裁决",
      "position": "miracle",
      "rarity": "relic",
      "description": "暴击时对敌人降下光芒裁决追加巨额伤害，但每次裁决都需要消耗专注点。",
      "allowed_categories": [
        "heavy_weapon",
        "focus"
      ],
      "effects": [
        {
          "trigger": "on_crit",
          "operation": "bonus_die",
          "target": "enemy",
          "die": "2d6"
        },
        {
          "trigger": "on_crit",
          "operation": "resource_loss",
          "target": "self",
          "resource": "focus",
          "value": 1
        }
      ],
      "tags": [
        "holy",
        "miracle",
        "crit"
      ],
      "power_budget": 8
    },
    {
      "id": "miracle_divine_barrier",
      "name": "天降圣障",
      "position": "miracle",
      "rarity": "epic",
      "description": "战斗开始时获得强力护佑保护，但圣障凝聚的瞬间会使自身陷入短暂失衡。",
      "allowed_categories": [
        "shield",
        "heavy_armor"
      ],
      "effects": [
        {
          "trigger": "on_combat_start",
          "operation": "apply_status",
          "target": "self",
          "status": "ward",
          "stacks": 3,
          "duration": 2
        },
        {
          "trigger": "on_combat_start",
          "operation": "apply_status",
          "target": "self",
          "status": "stagger",
          "stacks": 1,
          "duration": 1
        }
      ],
      "tags": [
        "holy",
        "miracle",
        "ward"
      ],
      "power_budget": 5
    },
    {
      "id": "miracle_second_wind",
      "name": "绝地逆风",
      "position": "miracle",
      "rarity": "rare",
      "description": "检定失败时可以获得一次重掷，但重新尝试必定消耗专注点。",
      "allowed_categories": [
        "garment",
        "accessory"
      ],
      "effects": [
        {
          "trigger": "on_check_fail",
          "operation": "reroll",
          "target": "current_check",
          "value": 1
        },
        {
          "trigger": "on_check_fail",
          "operation": "resource_loss",
          "target": "self",
          "resource": "focus",
          "value": 1
        }
      ],
      "tags": [
        "reroll",
        "miracle",
        "check"
      ],
      "power_budget": 4
    },
    {
      "id": "miracle_executioner_blessing",
      "name": "处刑洗礼",
      "position": "miracle",
      "rarity": "epic",
      "description": "击杀敌人后恢复自身生命值，并借死者余威对随机敌人施加恐惧。",
      "allowed_categories": [
        "heavy_weapon",
        "light_weapon"
      ],
      "effects": [
        {
          "trigger": "on_kill",
          "operation": "heal",
          "target": "self",
          "value": 5
        },
        {
          "trigger": "on_kill",
          "operation": "apply_status",
          "target": "random_enemy",
          "status": "fear",
          "stacks": 1,
          "duration": 1
        }
      ],
      "tags": [
        "kill",
        "miracle",
        "heal"
      ],
      "power_budget": 6
    },
    {
      "id": "miracle_observer_sanctuary",
      "name": "观照圣所",
      "position": "miracle",
      "rarity": "relic",
      "description": "战斗结束时能借圣所之力恢复生命，但异象会使世界注视度上升。",
      "allowed_categories": [
        "accessory"
      ],
      "effects": [
        {
          "trigger": "on_combat_end",
          "operation": "heal",
          "target": "self",
          "value": 4
        },
        {
          "trigger": "on_combat_end",
          "operation": "resource_gain",
          "target": "world",
          "resource": "attention",
          "value": 1
        }
      ],
      "tags": [
        "relic",
        "miracle",
        "heal"
      ],
      "power_budget": 7
    },
    {
      "id": "miracle_iron_resolve",
      "name": "钢铁执念",
      "position": "miracle",
      "rarity": "rare",
      "description": "每回合开始时获得一层短暂护佑，但维持专注姿态有概率消耗专注点。",
      "allowed_categories": [
        "heavy_armor",
        "shield"
      ],
      "effects": [
        {
          "trigger": "turn_start",
          "operation": "apply_status",
          "target": "self",
          "status": "ward",
          "stacks": 1,
          "duration": 1
        },
        {
          "trigger": "turn_start",
          "operation": "resource_loss",
          "target": "self",
          "resource": "focus",
          "value": 1,
          "chance": 40
        }
      ],
      "tags": [
        "defense",
        "miracle",
        "ward"
      ],
      "power_budget": 4
    },
    {
      "id": "miracle_epiphany_light",
      "name": "顿悟之光",
      "position": "miracle",
      "rarity": "epic",
      "description": "检定成功时获得额外专注点，但顿悟瞬间会暴露自身并使自身被标记。",
      "allowed_categories": [
        "focus",
        "accessory"
      ],
      "effects": [
        {
          "trigger": "on_check_success",
          "operation": "resource_gain",
          "target": "self",
          "resource": "focus",
          "value": 1
        },
        {
          "trigger": "on_check_success",
          "operation": "apply_status",
          "target": "self",
          "status": "mark",
          "stacks": 1,
          "duration": 1
        }
      ],
      "tags": [
        "focus",
        "miracle",
        "check"
      ],
      "power_budget": 5
    }
  ],
  "skills": [
    {
      "id": "crushing_blow",
      "name": "重碾重击",
      "kind": "active",
      "action_cost": "main",
      "focus_cost": 1,
      "hp_cost": 0,
      "cooldown": 2,
      "tags": [
        "might",
        "heavy",
        "attack"
      ],
      "description": "凝聚全身力气进行摧枯拉朽的猛击，对敌人造成重创并概率使其失衡。",
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "bonus_die",
          "target": "enemy",
          "die": "1d8"
        },
        {
          "trigger": "on_hit",
          "operation": "apply_status",
          "target": "enemy",
          "status": "stagger",
          "stacks": 1,
          "duration": 1,
          "chance": 60
        }
      ],
      "upgrades": [
        {
          "id": "crushing_blow_armor_break",
          "name": "破甲摧骨",
          "description": "在使敌人失衡之外进一步破坏护甲，短暂降低目标的防御能力。",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "guard_mod",
              "target": "enemy",
              "value": -2,
              "duration": 2
            }
          ]
        },
        {
          "id": "crushing_blow_reckless",
          "name": "孤注一掷",
          "description": "大幅提升伤害上限，但攻击时若未命中会导致自身失衡。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "bonus_die",
              "target": "enemy",
              "die": "1d6"
            },
            {
              "trigger": "on_check_fail",
              "operation": "apply_status",
              "target": "self",
              "status": "stagger",
              "stacks": 1,
              "duration": 1
            }
          ]
        }
      ]
    },
    {
      "id": "shadow_blade",
      "name": "影袭刺击",
      "kind": "active",
      "action_cost": "quick",
      "focus_cost": 1,
      "hp_cost": 0,
      "cooldown": 1,
      "tags": [
        "finesse",
        "stealth",
        "blade"
      ],
      "description": "利用快速的身法刺向敌人要害，若目标已被标记则造成额外出血。",
      "effects": [
        {
          "trigger": "on_hit",
          "operation": "bonus_die",
          "target": "enemy",
          "die": "1d6"
        },
        {
          "trigger": "on_hit",
          "operation": "apply_status",
          "target": "enemy",
          "status": "bleed",
          "stacks": 1,
          "duration": 2,
          "condition_tags_any": [
            "mark"
          ]
        }
      ],
      "upgrades": [
        {
          "id": "shadow_blade_poison",
          "name": "淬毒影刃",
          "description": "刺击附加剧毒，转为持续伤害控制。",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "poison",
              "stacks": 1,
              "duration": 3
            }
          ]
        },
        {
          "id": "shadow_blade_vanish",
          "name": "击退隐匿",
          "description": "命中后直接清除自身受到的标记与不利暴露。",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "remove_status",
              "target": "self",
              "status": "mark"
            }
          ]
        }
      ]
    },
    {
      "id": "soul_gaze",
      "name": "灵魂凝视",
      "kind": "active",
      "action_cost": "main",
      "focus_cost": 2,
      "hp_cost": 0,
      "cooldown": 3,
      "tags": [
        "insight",
        "occult",
        "mind"
      ],
      "description": "直视敌人的灵魂裂隙，使其暴露弱点并陷入恐惧，但对无心智单位效果有限。",
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "apply_status",
          "target": "enemy",
          "status": "mark",
          "stacks": 1,
          "duration": 2
        },
        {
          "trigger": "on_skill_use",
          "operation": "apply_status",
          "target": "enemy",
          "status": "fear",
          "stacks": 1,
          "duration": 2,
          "chance": 70
        }
      ],
      "upgrades": [
        {
          "id": "soul_gaze_break_will",
          "name": "意志瓦解",
          "description": "凝视同时瓦解目标的防备，短暂降低其防御能力，方便物理追击。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "guard_mod",
              "target": "enemy",
              "value": -3,
              "duration": 2
            }
          ]
        },
        {
          "id": "soul_gaze_mind_feed",
          "name": "心智抽吸",
          "description": "若目标成功陷入恐惧，则自身恢复专注点。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "resource_gain",
              "target": "self",
              "resource": "focus",
              "value": 1,
              "chance": 70
            }
          ]
        }
      ]
    },
    {
      "id": "iron_prayer",
      "name": "铁血祷告",
      "kind": "active",
      "action_cost": "quick",
      "focus_cost": 1,
      "hp_cost": 2,
      "cooldown": 2,
      "tags": [
        "will",
        "holy",
        "ward"
      ],
      "description": "以少许鲜血为代价吟诵坚定祷词，为自身凝聚临时护佑与护盾。",
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "shield",
          "target": "self",
          "value": 6
        },
        {
          "trigger": "on_skill_use",
          "operation": "apply_status",
          "target": "self",
          "status": "ward",
          "stacks": 1,
          "duration": 2
        }
      ],
      "upgrades": [
        {
          "id": "iron_prayer_purity",
          "name": "纯洁圣光",
          "description": "施放时顺便净化自身受到的流血影响。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "remove_status",
              "target": "self",
              "status": "bleed"
            }
          ]
        },
        {
          "id": "iron_prayer_martyr",
          "name": "殉道反誓",
          "description": "换取更厚的护盾与防御屏障。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "shield",
              "target": "self",
              "value": 6
            }
          ]
        }
      ]
    },
    {
      "id": "whirlwind_slash",
      "name": "狂风斩",
      "kind": "active",
      "action_cost": "main",
      "focus_cost": 1,
      "hp_cost": 0,
      "cooldown": 2,
      "tags": [
        "might",
        "finesse",
        "blade",
        "cross_attribute"
      ],
      "description": "结合力量与灵巧的迅捷旋风斩击，对敌人造成伤害并尝试打破其架势。",
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "bonus_die",
          "target": "enemy",
          "die": "1d6"
        },
        {
          "trigger": "on_hit",
          "operation": "apply_status",
          "target": "enemy",
          "status": "stagger",
          "stacks": 1,
          "duration": 1,
          "chance": 50
        }
      ],
      "upgrades": [
        {
          "id": "whirlwind_slash_gash",
          "name": "撕裂风暴",
          "description": "牺牲架势破坏，改为施加撕裂流血效果。",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "bleed",
              "stacks": 2,
              "duration": 2
            }
          ]
        },
        {
          "id": "whirlwind_slash_parry_step",
          "name": "旋风偏斜",
          "description": "斩击后顺势调整身位，获得一层持续到下回合的短暂护佑。",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "self",
              "status": "ward",
              "stacks": 1,
              "duration": 1
            }
          ]
        }
      ]
    },
    {
      "id": "astral_curse",
      "name": "星芒咒缚",
      "kind": "active",
      "action_cost": "main",
      "focus_cost": 2,
      "hp_cost": 0,
      "cooldown": 3,
      "tags": [
        "insight",
        "will",
        "occult",
        "cross_attribute"
      ],
      "description": "结合洞察与意志施放诅咒，使目标陷入灼烧与标记。",
      "effects": [
        {
          "trigger": "on_skill_use",
          "operation": "apply_status",
          "target": "enemy",
          "status": "burn",
          "stacks": 1,
          "duration": 2
        },
        {
          "trigger": "on_skill_use",
          "operation": "apply_status",
          "target": "enemy",
          "status": "mark",
          "stacks": 1,
          "duration": 2
        }
      ],
      "upgrades": [
        {
          "id": "astral_curse_spreading",
          "name": "蔓延阴火",
          "description": "在原有阴火之外额外施加一层灼烧，强化持续伤害效果。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "apply_status",
              "target": "enemy",
              "status": "burn",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "astral_curse_siphon",
          "name": "诅咒虹吸",
          "description": "若诅咒施加成功，从敌人身上汲取生命值。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "heal",
              "target": "self",
              "value": 3
            }
          ]
        }
      ]
    },
    {
      "id": "thick_hide",
      "name": "硬化皮质",
      "kind": "passive",
      "action_cost": "none",
      "focus_cost": 0,
      "hp_cost": 0,
      "cooldown": 0,
      "tags": [
        "might",
        "defense",
        "body"
      ],
      "description": "坚韧的肉体能天然抵挡伤害，但过于笨重会略微降低灵巧优势。",
      "effects": [
        {
          "trigger": "passive",
          "operation": "damage_reduction",
          "target": "self",
          "value": 1
        },
        {
          "trigger": "passive",
          "operation": "stat_mod",
          "target": "self",
          "stat": "finesse",
          "value": -1
        }
      ],
      "upgrades": [
        {
          "id": "thick_hide_iron_wall",
          "name": "铁壁高耸",
          "description": "进一步提升固定减伤能力，适合对抗多段轻微伤害。",
          "effects": [
            {
              "trigger": "passive",
              "operation": "damage_reduction",
              "target": "self",
              "value": 1
            }
          ]
        },
        {
          "id": "thick_hide_spikes",
          "name": "荆棘反骨",
          "description": "受到伤害时有几率对攻击者造成反击伤害。",
          "effects": [
            {
              "trigger": "on_damaged",
              "operation": "counterattack",
              "target": "attacker",
              "value": 2,
              "chance": 50
            }
          ]
        }
      ]
    },
    {
      "id": "nimble_footwork",
      "name": "灵动步法",
      "kind": "passive",
      "action_cost": "none",
      "focus_cost": 0,
      "hp_cost": 0,
      "cooldown": 0,
      "tags": [
        "finesse",
        "movement",
        "evasion"
      ],
      "description": "轻盈的身法让你在战斗开始时更容易占据主动位置。",
      "effects": [
        {
          "trigger": "on_combat_start",
          "operation": "advantage",
          "target": "current_check",
          "note": "仅作用于先攻检定"
        }
      ],
      "upgrades": [
        {
          "id": "nimble_footwork_elusive",
          "name": "难抓难寻",
          "description": "成功完成灵巧或闪避检定后自动获得短暂护佑。",
          "effects": [
            {
              "trigger": "on_check_success",
              "operation": "apply_status",
              "target": "self",
              "status": "ward",
              "stacks": 1,
              "duration": 1,
              "condition_tags_any": [
                "finesse",
                "evasion"
              ]
            }
          ]
        },
        {
          "id": "nimble_footwork_first_strike",
          "name": "先发制人",
          "description": "战斗开始时抢占视线，随机标记一名敌人以准备首轮集火。",
          "effects": [
            {
              "trigger": "on_combat_start",
              "operation": "apply_status",
              "target": "random_enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ]
    },
    {
      "id": "keen_scout",
      "name": "敏锐斥候",
      "kind": "passive",
      "action_cost": "none",
      "focus_cost": 0,
      "hp_cost": 0,
      "cooldown": 0,
      "tags": [
        "finesse",
        "insight",
        "scout",
        "cross_attribute"
      ],
      "description": "结合灵巧与洞察，在进入新房间时预先感知危险。",
      "effects": [
        {
          "trigger": "on_enter_room",
          "operation": "reveal",
          "target": "current_room",
          "value": 1
        }
      ],
      "upgrades": [
        {
          "id": "keen_scout_ambush",
          "name": "伏击埋伏",
          "description": "进入房间遇到战斗时，自动对随机敌人施加标记。",
          "effects": [
            {
              "trigger": "on_combat_start",
              "operation": "apply_status",
              "target": "random_enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "keen_scout_prepared",
          "name": "预先备战",
          "description": "揭示房间同时恢复1点专注点，为战斗做准备。",
          "effects": [
            {
              "trigger": "on_enter_room",
              "operation": "resource_gain",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ]
        }
      ]
    },
    {
      "id": "shield_block",
      "name": "招架盾击",
      "kind": "reaction",
      "action_cost": "reaction",
      "focus_cost": 1,
      "hp_cost": 0,
      "cooldown": 1,
      "tags": [
        "might",
        "shield",
        "defense"
      ],
      "description": "受到攻击时用武器或盾牌强行招架，成功后获得一层临时护盾。",
      "effects": [
        {
          "trigger": "on_block",
          "operation": "shield",
          "target": "self",
          "value": 3
        }
      ],
      "upgrades": [
        {
          "id": "shield_block_counter",
          "name": "反击盾顶",
          "description": "招架成功时顺势反击攻击者，造成固定物理伤害。",
          "effects": [
            {
              "trigger": "on_block",
              "operation": "counterattack",
              "target": "attacker",
              "value": 3
            }
          ]
        },
        {
          "id": "shield_block_unshakable",
          "name": "岿然不动",
          "description": "招架成功时获得护盾，吸收后续伤害。",
          "effects": [
            {
              "trigger": "on_block",
              "operation": "shield",
              "target": "self",
              "value": 5
            }
          ]
        }
      ]
    },
    {
      "id": "riposte_step",
      "name": "绝境偏转",
      "kind": "reaction",
      "action_cost": "reaction",
      "focus_cost": 1,
      "hp_cost": 0,
      "cooldown": 1,
      "tags": [
        "finesse",
        "blade",
        "parry"
      ],
      "description": "在受到伤害时迅速偏转攻击，使攻击者陷入失衡。",
      "effects": [
        {
          "trigger": "on_damaged",
          "operation": "apply_status",
          "target": "attacker",
          "status": "stagger",
          "stacks": 1,
          "duration": 1
        }
      ],
      "upgrades": [
        {
          "id": "riposte_step_bleed",
          "name": "血之偏转",
          "description": "偏转的同时划伤攻击者，施加流血状态。",
          "effects": [
            {
              "trigger": "on_damaged",
              "operation": "apply_status",
              "target": "attacker",
              "status": "bleed",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "riposte_step_disengage",
          "name": "脱身撤离",
          "description": "受到伤害后获得护佑，防止连续受创。",
          "effects": [
            {
              "trigger": "on_damaged",
              "operation": "apply_status",
              "target": "self",
              "status": "ward",
              "stacks": 1,
              "duration": 1
            }
          ]
        }
      ]
    },
    {
      "id": "mind_fortress",
      "name": "心智堡垒",
      "kind": "reaction",
      "action_cost": "reaction",
      "focus_cost": 1,
      "hp_cost": 0,
      "cooldown": 2,
      "tags": [
        "will",
        "mind",
        "defense"
      ],
      "description": "当受到攻击或精神冲击时，凭顽强意志抵御恐惧并清除负面状态。",
      "effects": [
        {
          "trigger": "on_damaged",
          "operation": "remove_status",
          "target": "self",
          "status": "fear"
        }
      ],
      "upgrades": [
        {
          "id": "mind_fortress_retaliate",
          "name": "意志反噬",
          "description": "成功抵御后反向对攻击者施加恐惧。",
          "effects": [
            {
              "trigger": "on_damaged",
              "operation": "apply_status",
              "target": "attacker",
              "status": "fear",
              "stacks": 1,
              "duration": 1
            }
          ]
        },
        {
          "id": "mind_fortress_second_wind",
          "name": "逆境回神",
          "description": "成功抵御后恢复少许生命值，稳住战局。",
          "effects": [
            {
              "trigger": "on_damaged",
              "operation": "heal",
              "target": "self",
              "value": 3
            }
          ]
        }
      ]
    }
  ],
  "enemies": [
    {
      "id": "hollow_cinder_sprite",
      "name": "虚空灰烬妖",
      "rank": "minion",
      "description": "依靠残留的热感感知生灵，以低空飘忽的弧线向前猛冲，撞击后自身易陷入失衡。",
      "hp": 10,
      "guard": 8,
      "will_defense": 7,
      "damage_reduction": 0,
      "tags": [
        "elemental",
        "fire",
        "minion"
      ],
      "resistances": [
        "fire"
      ],
      "weaknesses": [
        "water",
        "frost"
      ],
      "actions": [
        {
          "id": "cinder_sprite_burst",
          "name": "星火灼喷",
          "weight": 70,
          "description": "向前方喷吐残留的余烬火星。",
          "attack_bonus": 2,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "burn",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "cinder_sprite_flicker",
          "name": "忽明忽暗",
          "weight": 30,
          "description": "灰烬体剧烈闪烁并短暂凝聚防护层。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "shield",
              "target": "self",
              "value": 3
            }
          ]
        }
      ],
      "loot_tags": [
        "ash",
        "fire_essence"
      ]
    },
    {
      "id": "brass_clockwork_spider",
      "name": "黄铜齿轮蛛",
      "rank": "minion",
      "description": "顺着墙壁缝隙急速爬行，通过金属震动锁定敌人位置，攻击前关节会发出高亢鸣响。",
      "hp": 12,
      "guard": 10,
      "will_defense": 8,
      "damage_reduction": 0,
      "tags": [
        "construct",
        "clockwork",
        "mechanical"
      ],
      "resistances": [
        "poison",
        "bleed"
      ],
      "weaknesses": [
        "blunt",
        "lightning"
      ],
      "actions": [
        {
          "id": "clockwork_spider_stab",
          "name": "发条刺扎",
          "weight": 60,
          "description": "用尖锐的黄铜前肢刺向目标。",
          "attack_bonus": 3,
          "damage_die": "1d4+1",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "clockwork_spider_wound",
          "name": "齿轮割裂",
          "weight": 40,
          "description": "高速旋转肢体上的小型齿轮划伤敌人。",
          "attack_bonus": 2,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "bleed",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "clockwork",
        "scrap_metal"
      ]
    },
    {
      "id": "sprout_strangler",
      "name": "绞杀幼芽",
      "rank": "minion",
      "description": "沿潮湿泥土贴地潜行，专挑落单者的脚踝缠绕，根须暴露于阳光下时行动明显迟缓。",
      "hp": 14,
      "guard": 9,
      "will_defense": 9,
      "damage_reduction": 0,
      "tags": [
        "plant",
        "organic"
      ],
      "resistances": [
        "stagger"
      ],
      "weaknesses": [
        "fire",
        "blade"
      ],
      "actions": [
        {
          "id": "sprout_strangler_vine",
          "name": "藤蔓绊倒",
          "weight": 65,
          "description": "伸展幼嫩的藤蔓缠绕目标的双腿。",
          "attack_bonus": 2,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "stagger",
              "stacks": 1,
              "duration": 1
            }
          ]
        },
        {
          "id": "sprout_strangler_drain",
          "name": "根须汲润",
          "weight": 35,
          "description": "刺入皮肤吸取体液恢复生命。",
          "attack_bonus": 1,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "heal",
              "target": "self",
              "value": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "plant_seed",
        "vine"
      ]
    },
    {
      "id": "tattered_choir_page",
      "name": "破烂唱诗童",
      "rank": "minion",
      "description": "双脚悬空漂浮，依据求救声的方位盲目靠近，每次高声合唱前都会短暂停顿整理残缺袍服。",
      "hp": 11,
      "guard": 9,
      "will_defense": 10,
      "damage_reduction": 0,
      "tags": [
        "undead",
        "holy",
        "relic"
      ],
      "resistances": [
        "fear"
      ],
      "weaknesses": [
        "dark",
        "curse"
      ],
      "actions": [
        {
          "id": "choir_page_hymn",
          "name": "刺耳合唱",
          "weight": 70,
          "description": "发出尖锐无序的赞美诗呐喊。",
          "attack_bonus": 2,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "fear",
              "stacks": 1,
              "duration": 1
            }
          ]
        },
        {
          "id": "choir_page_prayer",
          "name": "遗缺祷告",
          "weight": 30,
          "description": "低头诵读残破的经文页。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "apply_status",
              "target": "self",
              "status": "ward",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "parchment",
        "sacred_dust"
      ]
    },
    {
      "id": "porcelain_ballerina",
      "name": "裁缝瓷偶",
      "rank": "normal",
      "description": "踏着固定机械舞步沿直线旋转移动，凭借镜面眼眶反射的光线捕捉目标，转向时关节极其僵硬。",
      "hp": 22,
      "guard": 13,
      "will_defense": 11,
      "damage_reduction": 1,
      "tags": [
        "construct",
        "toy",
        "gothic"
      ],
      "resistances": [
        "bleed",
        "poison"
      ],
      "weaknesses": [
        "blunt",
        "heavy_impact"
      ],
      "actions": [
        {
          "id": "ballerina_pirouette",
          "name": "高速旋转",
          "weight": 60,
          "description": "展开锋利的瓷质裙摆进行快速旋转切割。",
          "attack_bonus": 4,
          "damage_die": "1d6+2",
          "effects": [
            {
              "trigger": "on_crit",
              "operation": "bonus_die",
              "target": "enemy",
              "die": "1d4"
            }
          ]
        },
        {
          "id": "ballerina_puncture",
          "name": "缝纫针刺",
          "weight": 40,
          "description": "用长针手臂精准刺入目标缝隙。",
          "attack_bonus": 3,
          "damage_die": "1d6",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "bleed",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "porcelain",
        "sharp_needle"
      ]
    },
    {
      "id": "wax_crying_priest",
      "name": "蜡化哭泣祭司",
      "rank": "normal",
      "description": "托着庞大烛台蹒跚缓行，优先攻击持有亮光或发出巨大噪音的单位，蜡质融化时防护大幅下降。",
      "hp": 26,
      "guard": 12,
      "will_defense": 14,
      "damage_reduction": 0,
      "tags": [
        "humanoid",
        "cultist",
        "wax"
      ],
      "resistances": [
        "fear",
        "stagger"
      ],
      "weaknesses": [
        "fire",
        "heat"
      ],
      "actions": [
        {
          "id": "crying_priest_tear",
          "name": "熔蜡泼洒",
          "weight": 50,
          "description": "倾斜手中烛台泼洒滚烫的炽热熔蜡。",
          "attack_bonus": 3,
          "damage_die": "1d6+1",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "burn",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "crying_priest_sob",
          "name": "忏悔恸哭",
          "weight": 30,
          "description": "发出令人心神崩溃的哀号声。",
          "attack_bonus": 2,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "fear",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "crying_priest_guard",
          "name": "蜡封姿态",
          "weight": 20,
          "description": "用冷却凝固的硬蜡覆盖身体抵抗伤害。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "shield",
              "target": "self",
              "value": 5
            }
          ]
        }
      ],
      "loot_tags": [
        "candle_wax",
        "holy_relic"
      ]
    },
    {
      "id": "iron_ironing_maid",
      "name": "铁熨斗侍女",
      "rank": "normal",
      "description": "举着烧红的巨型铁斗在废墟间来回巡视，通过地表温度变化追踪生灵，起手摆臂幅度过大。",
      "hp": 28,
      "guard": 14,
      "will_defense": 12,
      "damage_reduction": 1,
      "tags": [
        "construct",
        "servant",
        "metal"
      ],
      "resistances": [
        "burn",
        "poison"
      ],
      "weaknesses": [
        "cold",
        "rust"
      ],
      "actions": [
        {
          "id": "ironing_maid_press",
          "name": "熨斗重压",
          "weight": 65,
          "description": "将炽热的铁熨斗重重砸向目标。",
          "attack_bonus": 4,
          "damage_die": "1d8+1",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "burn",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "ironing_maid_steam",
          "name": "灼热蒸汽",
          "weight": 35,
          "description": "喷射高压蒸汽使敌人无法立足。",
          "attack_bonus": 2,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "stagger",
              "stacks": 1,
              "duration": 1
            }
          ]
        }
      ],
      "loot_tags": [
        "iron_ingot",
        "coal"
      ]
    },
    {
      "id": "brier_knight_statue",
      "name": "荆棘骑士雕像",
      "rank": "normal",
      "description": "拖着沉重的藤蔓铠甲跨步逼近，依据金属碰撞声识别敌意，每次挥剑后胸口核心会短暂暴露。",
      "hp": 30,
      "guard": 15,
      "will_defense": 10,
      "damage_reduction": 1,
      "tags": [
        "construct",
        "plant",
        "knight"
      ],
      "resistances": [
        "bleed",
        "fear"
      ],
      "weaknesses": [
        "fire",
        "acid"
      ],
      "actions": [
        {
          "id": "brier_knight_cleave",
          "name": "荆棘斩击",
          "weight": 50,
          "description": "挥动缠满刺棘的石质巨剑劈砍。",
          "attack_bonus": 4,
          "damage_die": "1d8+2",
          "effects": []
        },
        {
          "id": "brier_knight_entangle",
          "name": "刺藤抽打",
          "weight": 30,
          "description": "伸长手臂上的藤蔓锁定并缠绕敌人。",
          "attack_bonus": 3,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "brier_knight_shield",
          "name": "石构防御",
          "weight": 20,
          "description": "举起石盾收拢全身藤蔓防御。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "guard_mod",
              "target": "self",
              "value": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "stone_fragment",
        "thorny_vine"
      ]
    },
    {
      "id": "mirror_glass_herald",
      "name": "镜片使者",
      "rank": "normal",
      "description": "折射光影折跃移动，专注追踪身上有标记的目标，受击后镜面裂痕会暴露真身方向。",
      "hp": 20,
      "guard": 12,
      "will_defense": 13,
      "damage_reduction": 0,
      "tags": [
        "humanoid",
        "glass",
        "occult"
      ],
      "resistances": [
        "burn"
      ],
      "weaknesses": [
        "blunt",
        "heavy_impact"
      ],
      "actions": [
        {
          "id": "glass_herald_strike",
          "name": "镜刃突刺",
          "weight": 60,
          "description": "持锋利的折光玻璃片猛刺目标。",
          "attack_bonus": 5,
          "damage_die": "1d6+2",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "bleed",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "glass_herald_glare",
          "name": "强光折射",
          "weight": 40,
          "description": "反射刺眼光束照亮敌人的破绽。",
          "attack_bonus": 2,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "mirror_shard",
        "refraction_crystal"
      ]
    },
    {
      "id": "gallows_organist",
      "name": "绞刑架琴师",
      "rank": "normal",
      "description": "端坐在悬空的残破琴架前随风漂移，通过声波共振定位目标，弹奏高潮段落前呼吸会急促停顿。",
      "hp": 24,
      "guard": 11,
      "will_defense": 15,
      "damage_reduction": 0,
      "tags": [
        "undead",
        "music",
        "ghost"
      ],
      "resistances": [
        "stagger",
        "poison"
      ],
      "weaknesses": [
        "holy",
        "silence"
      ],
      "actions": [
        {
          "id": "organist_death_march",
          "name": "亡者行进",
          "weight": 45,
          "description": "弹奏沉重的压迫性乐章侵蚀敌心灵。",
          "attack_bonus": 3,
          "damage_die": "1d6",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "fear",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "organist_chord",
          "name": "不谐和音",
          "weight": 30,
          "description": "奏出高频杂音干扰目标的专注。",
          "attack_bonus": 4,
          "damage_die": "1d6+1",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "resource_loss",
              "target": "enemy",
              "resource": "focus",
              "value": 1
            }
          ]
        },
        {
          "id": "organist_curse",
          "name": "诅咒印记",
          "weight": 25,
          "description": "将诡异音符烙印在敌人身上。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "apply_status",
              "target": "enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "sheet_music",
        "spectral_string"
      ]
    },
    {
      "id": "cuckoo_sentinel",
      "name": "布谷鸟哨兵",
      "rank": "normal",
      "description": "沿着固定轨道俯冲飞行，依靠齿轮鸣响判断距离，俯冲拉升的转弯半径极大。",
      "hp": 25,
      "guard": 13,
      "will_defense": 12,
      "damage_reduction": 1,
      "tags": [
        "construct",
        "clockwork",
        "bird"
      ],
      "resistances": [
        "poison",
        "fear"
      ],
      "weaknesses": [
        "lightning",
        "blunt"
      ],
      "actions": [
        {
          "id": "cuckoo_sentinel_dive",
          "name": "俯冲喙击",
          "weight": 65,
          "description": "从高空沿轨道急速俯冲用铁喙撞击。",
          "attack_bonus": 5,
          "damage_die": "1d8",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "bonus_die",
              "target": "enemy",
              "die": "1d4"
            }
          ]
        },
        {
          "id": "cuckoo_sentinel_chime",
          "name": "钟鸣震慑",
          "weight": 35,
          "description": "敲响胸前的小铜钟发出巨响。",
          "attack_bonus": 2,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "stagger",
              "stacks": 1,
              "duration": 1
            }
          ]
        }
      ],
      "loot_tags": [
        "brass_feather",
        "clockwork_gear"
      ]
    },
    {
      "id": "fungal_apothecary",
      "name": "真菌药剂师",
      "rank": "normal",
      "description": "背着硕大的孢子囊缓慢踱步，靠嗅觉寻找活人，释放孢子粉尘前囊体会剧烈膨胀。",
      "hp": 27,
      "guard": 12,
      "will_defense": 13,
      "damage_reduction": 0,
      "tags": [
        "plant",
        "spore",
        "organic"
      ],
      "resistances": [
        "poison"
      ],
      "weaknesses": [
        "fire",
        "blade"
      ],
      "actions": [
        {
          "id": "apothecary_spore",
          "name": "毒孢喷雾",
          "weight": 45,
          "description": "挤压背囊喷洒剧毒孢子雾气。",
          "attack_bonus": 3,
          "damage_die": "1d4",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "poison",
              "stacks": 1,
              "duration": 3
            }
          ]
        },
        {
          "id": "apothecary_vial",
          "name": "腐蚀药瓶",
          "weight": 35,
          "description": "掷出盛有强酸液体的小玻璃瓶。",
          "attack_bonus": 4,
          "damage_die": "1d6+1",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "guard_mod",
              "target": "enemy",
              "value": -2
            }
          ]
        },
        {
          "id": "apothecary_soothe",
          "name": "孢子敷贴",
          "weight": 20,
          "description": "利用治愈性真菌恢复伤口。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "heal",
              "target": "self",
              "value": 4
            }
          ]
        }
      ],
      "loot_tags": [
        "toxic_fungus",
        "alchemy_vial"
      ]
    },
    {
      "id": "bell_tower_gargoyle",
      "name": "钟楼石像鬼",
      "rank": "normal",
      "description": "平时佯装石雕俯瞰大地，感知到活物经过时猛然扑下，起飞准备时间极长。",
      "hp": 29,
      "guard": 15,
      "will_defense": 11,
      "damage_reduction": 2,
      "tags": [
        "construct",
        "stone",
        "beast"
      ],
      "resistances": [
        "bleed",
        "burn",
        "poison"
      ],
      "weaknesses": [
        "heavy_impact",
        "pickaxe"
      ],
      "actions": [
        {
          "id": "gargoyle_pounce",
          "name": "花岗岩猛扑",
          "weight": 70,
          "description": "展开沉重的石翼从空中重重扑倒目标。",
          "attack_bonus": 4,
          "damage_die": "1d8+2",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "stagger",
              "stacks": 1,
              "duration": 1
            }
          ]
        },
        {
          "id": "gargoyle_harden",
          "name": "石化凝结",
          "weight": 30,
          "description": "瞬间将躯体石化以吸收伤害。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "shield",
              "target": "self",
              "value": 6
            }
          ]
        }
      ],
      "loot_tags": [
        "carved_stone",
        "gargoyle_claw"
      ]
    },
    {
      "id": "stained_glass_saint",
      "name": "彩绘玻璃圣徒",
      "rank": "normal",
      "description": "滑动在教堂花窗框格间，追逐光线照射下的影子，光线阴暗处动作会产生明显卡顿。",
      "hp": 23,
      "guard": 14,
      "will_defense": 14,
      "damage_reduction": 1,
      "tags": [
        "construct",
        "glass",
        "holy"
      ],
      "resistances": [
        "burn",
        "fear"
      ],
      "weaknesses": [
        "blunt",
        "dark"
      ],
      "actions": [
        {
          "id": "glass_saint_beam",
          "name": "折光束击",
          "weight": 45,
          "description": "聚焦聚集的光芒射向目标破绽。",
          "attack_bonus": 4,
          "damage_die": "1d6+2",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "glass_saint_blessing",
          "name": "光辉洗礼",
          "weight": 30,
          "description": "凝结一束护佑光流笼罩自身。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "apply_status",
              "target": "self",
              "status": "ward",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "glass_saint_shatter",
          "name": "玻璃飞溅",
          "weight": 25,
          "description": "震碎边缘玻璃形成细小飞屑。",
          "attack_bonus": 3,
          "damage_die": "1d8",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "bleed",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "colored_glass",
        "holy_symbol"
      ]
    },
    {
      "id": "hollow_executioner",
      "name": "空心处刑官",
      "rank": "elite",
      "description": "踏着沉重脚步逼近最虚弱的猎物，依靠空洞铠甲内的空气震动寻敌，挥动巨斧前有极长前摇。",
      "hp": 55,
      "guard": 17,
      "will_defense": 15,
      "damage_reduction": 2,
      "tags": [
        "construct",
        "armor",
        "giant",
        "elite"
      ],
      "resistances": [
        "fear",
        "bleed",
        "poison"
      ],
      "weaknesses": [
        "lightning",
        "joint_attack"
      ],
      "actions": [
        {
          "id": "executioner_guillotine",
          "name": "断头台巨斩",
          "weight": 45,
          "description": "举起锈蚀斩首巨斧全力向下劈砍。",
          "attack_bonus": 6,
          "damage_die": "1d12+3",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "stagger",
              "stacks": 1,
              "duration": 1
            }
          ]
        },
        {
          "id": "executioner_stomp",
          "name": "重踏践踏",
          "weight": 25,
          "description": "高高抬起铁靴重击地面引发震荡。",
          "attack_bonus": 5,
          "damage_die": "1d6+2",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "stagger",
              "stacks": 1,
              "duration": 1
            }
          ]
        },
        {
          "id": "executioner_posture",
          "name": "防守架势",
          "weight": 30,
          "description": "将巨斧横挡在胸前做好防御准备。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "guard_mod",
              "target": "self",
              "value": 3
            },
            {
              "trigger": "on_skill_use",
              "operation": "shield",
              "target": "self",
              "value": 5
            }
          ]
        }
      ],
      "loot_tags": [
        "executioner_axe",
        "steel_plate"
      ]
    },
    {
      "id": "clockwork_maestro",
      "name": "齿轮指挥家",
      "rank": "elite",
      "description": "站在高处以机械棒指挥战场节奏，通过音叉震动感知全局，发条松动时指挥动作会出现错乱。",
      "hp": 48,
      "guard": 16,
      "will_defense": 17,
      "damage_reduction": 1,
      "tags": [
        "construct",
        "clockwork",
        "leader",
        "elite"
      ],
      "resistances": [
        "fear",
        "poison"
      ],
      "weaknesses": [
        "blunt",
        "overload"
      ],
      "actions": [
        {
          "id": "maestro_baton",
          "name": "指挥棒挥击",
          "weight": 35,
          "description": "挥动金属指挥棒精准刺向要害。",
          "attack_bonus": 5,
          "damage_die": "1d8+2",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "maestro_summon",
          "name": "唤醒辅助发条",
          "weight": 35,
          "description": "启动机制召唤小型的发条杂兵协助。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "spawn",
              "target": "current_room",
              "value": 1
            }
          ]
        },
        {
          "id": "maestro_overhaul",
          "name": "战术调度",
          "weight": 30,
          "description": "通过节拍干扰敌人的思考节奏。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "resource_loss",
              "target": "enemy",
              "resource": "focus",
              "value": 1
            },
            {
              "trigger": "on_skill_use",
              "operation": "advantage",
              "target": "self"
            }
          ]
        }
      ],
      "loot_tags": [
        "silver_baton",
        "precision_gear"
      ]
    },
    {
      "id": "bramble_matriarch",
      "name": "荆棘圣母",
      "rank": "elite",
      "description": "根须盘踞房间中央，伸展蔓藤袭击所有试图靠近者，中央母体受创后蔓藤会短暂回缩。",
      "hp": 60,
      "guard": 15,
      "will_defense": 16,
      "damage_reduction": 2,
      "tags": [
        "plant",
        "corrupted",
        "mother",
        "elite"
      ],
      "resistances": [
        "stagger",
        "bleed"
      ],
      "weaknesses": [
        "fire",
        "blight"
      ],
      "actions": [
        {
          "id": "matriarch_whip",
          "name": "荆棘狂鞭",
          "weight": 45,
          "description": "挥动多根带刺蔓藤连续抽打敌人。",
          "attack_bonus": 5,
          "damage_die": "1d10+2",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "bleed",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "matriarch_spore",
          "name": "窒息孢子",
          "weight": 25,
          "description": "从花朵中央喷出一团浓郁的毒气粉雾。",
          "attack_bonus": 4,
          "damage_die": "1d6",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "poison",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "matriarch_regrowth",
          "name": "根须自愈",
          "weight": 30,
          "description": "从深层土壤中汲取营养滋养自身。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "heal",
              "target": "self",
              "value": 6
            },
            {
              "trigger": "on_skill_use",
              "operation": "apply_status",
              "target": "self",
              "status": "ward",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "matriarch_core",
        "ancient_vine"
      ]
    },
    {
      "id": "wax_cardinal",
      "name": "熔蜡枢机",
      "rank": "elite",
      "description": "漂浮在半空洒下灼热熔蜡，锁定意志防线最低的单位，头部圣冠倾斜时熔蜡喷射方向固定。",
      "hp": 52,
      "guard": 16,
      "will_defense": 18,
      "damage_reduction": 1,
      "tags": [
        "humanoid",
        "wax",
        "cultist",
        "elite"
      ],
      "resistances": [
        "fear",
        "stagger"
      ],
      "weaknesses": [
        "fire",
        "cold"
      ],
      "actions": [
        {
          "id": "wax_cardinal_seal",
          "name": "炽蜡圣印",
          "weight": 45,
          "description": "将一大块融化的滚烫红蜡压向敌人。",
          "attack_bonus": 6,
          "damage_die": "1d8+3",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "burn",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "wax_cardinal_anathema",
          "name": "异端诅咒",
          "weight": 25,
          "description": "宣告神圣咒逐使目标陷入精神恐慌。",
          "attack_bonus": 4,
          "damage_die": "1d6",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "fear",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "wax_cardinal_shield",
          "name": "圣烛护庇",
          "weight": 30,
          "description": "凝聚厚重的圆融蜡层护罩。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "shield",
              "target": "self",
              "value": 8
            },
            {
              "trigger": "on_skill_use",
              "operation": "resource_gain",
              "target": "world",
              "resource": "attention",
              "value": 1
            }
          ]
        }
      ],
      "loot_tags": [
        "cardinal_seal",
        "pure_wax"
      ]
    },
    {
      "id": "puppet_king_alys",
      "name": "傀儡国王·阿利斯",
      "rank": "boss",
      "description": "悬于半空的丝线拉扯其肢体进行诡异的宫廷舞步，优先攻击对其造成最高累计伤害者，背后主线紧绷时极其脆弱。",
      "hp": 140,
      "guard": 20,
      "will_defense": 18,
      "damage_reduction": 3,
      "tags": [
        "boss",
        "puppet",
        "king",
        "construct"
      ],
      "resistances": [
        "bleed",
        "poison",
        "fear"
      ],
      "weaknesses": [
        "string_sever",
        "fire"
      ],
      "actions": [
        {
          "id": "king_alys_blade",
          "name": "王者佩剑",
          "weight": 30,
          "description": "挥动华丽的皇家细剑发起迅捷刺击。",
          "attack_bonus": 7,
          "damage_die": "1d10+4",
          "effects": [
            {
              "trigger": "on_crit",
              "operation": "bonus_die",
              "target": "enemy",
              "die": "1d6"
            }
          ]
        },
        {
          "id": "king_alys_string",
          "name": "傀儡丝缠绕",
          "weight": 25,
          "description": "发射空中悬挂的隐形丝线勒住敌人。",
          "attack_bonus": 6,
          "damage_die": "1d6+2",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "stagger",
              "stacks": 1,
              "duration": 1
            },
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "king_alys_summon",
          "name": "召集侍从",
          "weight": 15,
          "description": "拽动丝线强行召唤一名发条侍从参战。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "spawn",
              "target": "current_room",
              "value": 1
            }
          ]
        },
        {
          "id": "king_alys_guard",
          "name": "御前姿态",
          "weight": 15,
          "description": "利用加固的傀儡铠甲与护栏防守。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "shield",
              "target": "self",
              "value": 10
            },
            {
              "trigger": "on_skill_use",
              "operation": "guard_mod",
              "target": "self",
              "value": 2
            }
          ]
        },
        {
          "id": "king_alys_gaze",
          "name": "君权凝视",
          "weight": 15,
          "description": "散发残存的冷酷威严压迫对手。",
          "attack_bonus": 5,
          "damage_die": "1d8",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "fear",
              "stacks": 1,
              "duration": 2
            },
            {
              "trigger": "on_hit",
              "operation": "resource_loss",
              "target": "enemy",
              "resource": "focus",
              "value": 1
            }
          ]
        }
      ],
      "loot_tags": [
        "king_crown",
        "royal_rapier",
        "puppet_thread"
      ]
    },
    {
      "id": "mother_of_forgotten_dolls",
      "name": "遗弃偶之母",
      "rank": "boss",
      "description": "坐于庞大破旧育婴床中央，通过哭声与缝合针指引傀儡进攻，怀中抱着的八音盒停顿转动时是绝佳输出时机。",
      "hp": 160,
      "guard": 22,
      "will_defense": 20,
      "damage_reduction": 3,
      "tags": [
        "boss",
        "gothic",
        "doll",
        "mother"
      ],
      "resistances": [
        "stagger",
        "fear",
        "poison"
      ],
      "weaknesses": [
        "holy",
        "fire"
      ],
      "actions": [
        {
          "id": "mother_dolls_thrust",
          "name": "缝合长针",
          "weight": 30,
          "description": "用巨大且锈蚀的刺绣巨针猛烈刺击。",
          "attack_bonus": 8,
          "damage_die": "1d12+3",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "bleed",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "mother_dolls_screaming",
          "name": "摇篮尖叫",
          "weight": 25,
          "description": "发出摧残理智的狂暴哭号。",
          "attack_bonus": 6,
          "damage_die": "1d8+2",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "fear",
              "stacks": 1,
              "duration": 2
            }
          ]
        },
        {
          "id": "mother_dolls_awaken",
          "name": "唤醒弃偶",
          "weight": 15,
          "description": "从育婴床深处拽出一具被遗弃的人偶。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "spawn",
              "target": "current_room",
              "value": 1
            }
          ]
        },
        {
          "id": "mother_dolls_cradle",
          "name": "摇篮拥抱",
          "weight": 15,
          "description": "缩回软垫破损的育婴床内疗愈伤势。",
          "effects": [
            {
              "trigger": "on_skill_use",
              "operation": "heal",
              "target": "self",
              "value": 8
            },
            {
              "trigger": "on_skill_use",
              "operation": "apply_status",
              "target": "self",
              "status": "ward",
              "stacks": 2,
              "duration": 2
            }
          ]
        },
        {
          "id": "mother_dolls_spite",
          "name": "怨毒泼洒",
          "weight": 15,
          "description": "向四周喷洒具有腐蚀性的黑色眼泪。",
          "attack_bonus": 7,
          "damage_die": "1d6+3",
          "effects": [
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "burn",
              "stacks": 1,
              "duration": 2
            },
            {
              "trigger": "on_hit",
              "operation": "apply_status",
              "target": "enemy",
              "status": "mark",
              "stacks": 1,
              "duration": 2
            }
          ]
        }
      ],
      "loot_tags": [
        "mother_heart",
        "giant_needle",
        "music_box"
      ]
    }
  ],
  "events": [
    {
      "id": "event_abandoned_observatory",
      "name": "荒废观象台",
      "description": "高塔顶端的黄铜巨镜已被灰烬覆盖，镜筒内隐约传来金属齿轮咬合的摩擦声。",
      "room_tags_any": [
        "high_place",
        "ruin"
      ],
      "choices": [
        {
          "id": "choice_repair_telescope",
          "text": "拭去灰烬并校准透镜",
          "check": {
            "stat": "insight",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你理清了复杂的镜片结构，透过观象镜看清了前方迷雾中的暗道。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 2
                }
              ],
              "set_flags": [
                "flag_telescope_repaired"
              ],
              "reward_tags": [
                "refraction_crystal"
              ]
            },
            {
              "result": "failure",
              "text": "镜片突然折射出异样的虚空强光，你的视线一片惨白，精神备受震慑。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "fear",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_clockwork_tune",
          "text": "利用发条技巧快速调试",
          "requirements_all": [
            "clockwork"
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "借由对机械构造的熟稔，你轻巧地拔出了卡住的螺栓，观象台重获新生。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": [
                "flag_telescope_repaired"
              ],
              "reward_tags": [
                "clockwork_gear"
              ]
            }
          ]
        },
        {
          "id": "choice_leave_observatory",
          "text": "绕过高塔避免招惹异响",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_gain",
              "target": "world",
              "resource": "attention",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "你选择从塔外陡峭的盘旋阶梯绕行，多花了不少时间并弄响了碎石。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_loss",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "high_place",
        "ruin"
      ]
    },
    {
      "id": "event_drowned_confessional",
      "name": "水淹忏悔室",
      "description": "沉没在半米深积水中的木质告解室，格栅后不断冒出带有腥味的白泡。",
      "room_tags_any": [
        "water",
        "religious"
      ],
      "choices": [
        {
          "id": "choice_listen_confession",
          "text": "贴近告解格栅聆听遗言",
          "check": {
            "stat": "will",
            "dc": 12,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你抵受住了绝望的心智冲击，从溺死者的呓语中听出了危险仪式的位置。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 2
                }
              ],
              "set_flags": [
                "flag_confessor_secret_known"
              ]
            },
            {
              "result": "failure",
              "text": "格栅后猛然伸出冰冷的手抓住了你，冰水呛入肺部。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 4
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "fear",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_force_open_door",
          "text": "用蛮力撞开沉重的淹水木门",
          "check": {
            "stat": "might",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "木门被猛然撞碎，积水轰然涌出，露出了藏在里面的圣物遗存。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 1
                }
              ],
              "set_flags": [],
              "reward_tags": [
                "holy_relic"
              ]
            },
            {
              "result": "failure",
              "text": "木门纹丝不动，反作用力震得你手臂酸麻失衡。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "stagger",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_distant_prayer",
          "text": "隔水向圣像默祷后离开",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "你的虔诚得到了微弱的回应，身上凝聚起一层薄薄的庇护之光。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "ward",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "water",
        "religious"
      ]
    },
    {
      "id": "event_rust_merchant_wagon",
      "name": "锈蚀货郎车",
      "description": "一辆倾覆在泥泞废墟中的货车，戴着铁面具的行商正用骨制天平称量残渣。",
      "room_tags_any": [
        "outdoor",
        "ruin"
      ],
      "choices": [
        {
          "id": "choice_trade_blood",
          "text": "献出鲜血换取神秘药剂",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "damage",
              "target": "self",
              "value": 4
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "面具行商满意地收下血样，推给你一瓶散发异香的炼金试剂。",
              "weight": 100,
              "effects": [],
              "set_flags": [
                "flag_traded_with_rust_merchant"
              ],
              "reward_tags": [
                "alchemy_vial"
              ]
            }
          ]
        },
        {
          "id": "choice_haggle_goods",
          "text": "试图看清货堆并讨价还价",
          "check": {
            "stat": "finesse",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你从残破货堆中顺手牵羊拿走了一件精密的机械零件。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": [],
              "reward_tags": [
                "precision_gear"
              ]
            },
            {
              "result": "failure",
              "text": "行商发现了你的小动作，用尖锐的铁杖将你驱赶出来。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 1
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_loss",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_bypass_wagon",
          "text": "穿过两侧荆棘丛绕开货车",
          "outcomes": [
            {
              "result": "automatic",
              "text": "为了避开可疑的行商，你踏入了密布的刺藤，衣服和皮肤被多处划伤。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 2
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "bleed",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "outdoor",
        "ruin"
      ]
    },
    {
      "id": "event_weeping_fountain",
      "name": "哭泣泉眼",
      "description": "雕刻着无脸圣女的石喷泉，清澈的水流从圣女眼眶不断流出，散发出冰冷的气息。",
      "room_tags_any": [
        "water",
        "anomaly"
      ],
      "choices": [
        {
          "id": "choice_drink_fountain",
          "text": "畅饮喷泉中冰冷的圣水",
          "check": {
            "stat": "will",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "泉水洗涤了身上的伤痛，你感到了久违的宁静与充沛活力。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 6
                }
              ],
              "set_flags": [
                "flag_drank_fountain_water"
              ]
            },
            {
              "result": "failure",
              "text": "泉水入口如刀割般剧痛，你的内脏被剧烈毒素侵蚀。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "poison",
                  "stacks": 2,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_recite_secret",
          "text": "向泉水背诵淹水告解者的秘密",
          "requirements_all": [
            "flag_confessor_secret_known"
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "听到秘密后圣女雕像停止了哭泣，泉水泛出金光，完全清除了你体内的毒素与伤痛。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 8
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "remove_status",
                  "target": "self",
                  "status": "poison"
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_purify_fountain",
          "text": "投入专注力净化泉眼底部的污秽",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "泉眼被短暂净化，凝聚出一层守护屏障将你包裹。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "ward",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": [
                "flag_fountain_purified"
              ]
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "water",
        "anomaly"
      ]
    },
    {
      "id": "event_clockwork_bird_cage",
      "name": "鸣钟鸟笼",
      "description": "悬挂在走廊中央的精致铁笼，里面装有一只不断报时的发条鸟，钟声正引来远处的骚动。",
      "room_tags_any": [
        "indoor",
        "anomaly"
      ],
      "choices": [
        {
          "id": "choice_pick_cage_lock",
          "text": "精细拆卸鸟笼底部的发条锁",
          "check": {
            "stat": "finesse",
            "dc": 12,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你成功卸下了发条鸟的核心齿轮，钟声戛然而止，获得珍贵材质。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": [],
              "reward_tags": [
                "brass_feather"
              ]
            },
            {
              "result": "failure",
              "text": "弹簧机制突然弹开，尖锐的金属片割伤了你的手掌。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 3
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "bleed",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_smash_cage",
          "text": "使用重型武器砸碎铁籠",
          "requirements_all": [
            "heavy"
          ],
          "check": {
            "stat": "might",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "铁笼被一击粉碎，机械鸟变为一堆有用的金属碎片。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "scrap_metal"
              ]
            },
            {
              "result": "failure",
              "text": "金属反弹力震退了你，巨大的撞击声在走廊中轰鸣回响。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "stagger",
                  "stacks": 1,
                  "duration": 1
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_ignore_ticking",
          "text": "硬着头皮从鸟笼下方快步疾奔",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_gain",
              "target": "world",
              "resource": "attention",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "你强忍着刺耳的钟鸣冲过走廊，心神受到了极大的干扰。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_loss",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "indoor",
        "anomaly"
      ]
    },
    {
      "id": "event_bleeding_fresco",
      "name": "渗血壁画",
      "description": "修道院墙壁上描绘着赎罪仪式的巨幅壁画，画中人的伤口正源源不断渗出新鲜血液。",
      "room_tags_any": [
        "religious",
        "indoor"
      ],
      "choices": [
        {
          "id": "choice_scrape_blood",
          "text": "刮取干涸的结痂血液研究",
          "check": {
            "stat": "insight",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你辨识出了血液中残留的神圣粉尘，小心翼翼地收集起来。",
              "weight": 100,
              "effects": [],
              "set_flags": [
                "flag_fresco_scraped"
              ],
              "reward_tags": [
                "sacred_dust"
              ]
            },
            {
              "result": "failure",
              "text": "壁画中的眼睛仿佛转动了一下，恐怖的幻象直冲你的脑海。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "fear",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_burn_fresco",
          "text": "用火把焚烧异端壁画",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "火焰将壁画化为灰烬，浓烟滚滚升起，引起了远处敌人的注意。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 2
                }
              ],
              "set_flags": [
                "flag_fresco_burned"
              ]
            }
          ]
        },
        {
          "id": "choice_cover_eyes_pass",
          "text": "闭上眼睛靠着墙壁缓缓挪过去",
          "outcomes": [
            {
              "result": "automatic",
              "text": "在黑暗中摸索让你精神高度紧张，甚至不小心磕伤了膝盖。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 1
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_loss",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "religious",
        "indoor"
      ]
    },
    {
      "id": "event_submerged_crypt",
      "name": "淹没地穴",
      "description": "半塌陷的地下墓室已经被浑浊的地下水淹没，水面下隐约闪烁着石刻的光芒。",
      "room_tags_any": [
        "underground",
        "water"
      ],
      "choices": [
        {
          "id": "choice_dive_cold_water",
          "text": "潜入冰冷刺骨的水中搜寻",
          "check": {
            "stat": "might",
            "dc": 12,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你强忍着寒冷潜入水底，捞出了被水流冲刷光滑的雕刻石块。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "carved_stone"
              ]
            },
            {
              "result": "failure",
              "text": "水下抽筋迫使你仓皇逃回岸上，浑身冻得发抖失衡。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 4
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "stagger",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_probe_with_tool",
          "text": "用长杆工具在岸边小心打捞",
          "check": {
            "stat": "insight",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你精明地钩住了一包沉在淤泥里的物资。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            },
            {
              "result": "failure",
              "text": "打捞工具滑落水中，剧烈的涟漪暴露了你的位置。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_drain_canal_lever",
          "text": "强行拉动生锈的排水阀门",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "damage",
              "target": "self",
              "value": 2
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "随着生锈齿轮的轰鸣，地穴的水位开始缓缓下降，露出了下层的通路。",
              "weight": 100,
              "effects": [],
              "set_flags": [
                "flag_crypt_drained"
              ]
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "underground",
        "water"
      ]
    },
    {
      "id": "event_gallows_tree",
      "name": "绞刑架古木",
      "description": "荒野中央生长着一棵巨大的枯木，树干上挂着数具被丝线吊起的发条木偶。",
      "room_tags_any": [
        "outdoor",
        "anomaly"
      ],
      "choices": [
        {
          "id": "choice_cut_marionette",
          "text": "爬上树干割断缠绕木偶的丝线",
          "check": {
            "stat": "finesse",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你敏捷地剪断了傀儡线，收集到了极其韧性优质的傀儡丝。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "puppet_thread"
              ]
            },
            {
              "result": "failure",
              "text": "树枝折断让你重重摔落在地，尖锐的木刺划破了手臂。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 3
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "bleed",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_holy_rite",
          "text": "为受诅木偶诵读安息祷文",
          "requirements_all": [
            "holy"
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "木偶身上的邪异气息渐渐消散，你的灵魂得到了净化与安抚。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 4
                }
              ],
              "set_flags": [
                "flag_marionette_rested"
              ]
            }
          ]
        },
        {
          "id": "choice_burn_gallows",
          "text": "点燃绞刑木将其付之一炬",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "冲天大火将枯木烧成灰烬，火光在黑夜中极其瞩目。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 2
                }
              ],
              "set_flags": [
                "flag_gallows_burned"
              ]
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "outdoor",
        "anomaly"
      ]
    },
    {
      "id": "event_overgrown_greenhouse",
      "name": "疯狂温室",
      "description": "破碎玻璃温室内长满了变异的绞杀藤蔓与巨大孢子花，散发着诱人而危险的甜香。",
      "room_tags_any": [
        "ruin",
        "indoor"
      ],
      "choices": [
        {
          "id": "choice_harvest_spores",
          "text": "小心翼翼地采摘成熟的毒性孢子",
          "check": {
            "stat": "insight",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你精准地避开了触须防护，成功采集到了高浓度的有毒真菌。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "toxic_fungus"
              ]
            },
            {
              "result": "failure",
              "text": "孢子囊在你面前突然炸开，剧毒粉尘扑面而来。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "poison",
                  "stacks": 2,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_hack_vines",
          "text": "挥舞利刃强行劈开一条通路",
          "check": {
            "stat": "might",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "藤蔓被斩断，你发现了藏在植物根部的新鲜果实并服下。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 4
                }
              ],
              "set_flags": []
            },
            {
              "result": "failure",
              "text": "断裂的刺藤如鞭子般反弹抽打在你的身上。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "bleed",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_tread_carefully",
          "text": "蹑手蹑脚地从花丛缝隙穿过",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_gain",
              "target": "world",
              "resource": "attention",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "为了不触动孢子，你极度缓慢地挪动身体，消耗了大量精力。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_loss",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "ruin",
        "indoor"
      ]
    },
    {
      "id": "event_wax_sculptor_workshop",
      "name": "蜡塑师工坊",
      "description": "工坊内摆满了半完成的人形蜡像，熔蜡沿着工作台不断滴落，发出凝固的嗒嗒声。",
      "room_tags_any": [
        "indoor",
        "ruin"
      ],
      "choices": [
        {
          "id": "choice_mold_wax",
          "text": "尝试利用残余熔蜡制作护身符",
          "check": {
            "stat": "finesse",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你用巧手将熔蜡塑造成型，获得了上等的封印蜡块。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "candle_wax"
              ]
            },
            {
              "result": "failure",
              "text": "滚烫的熔蜡泼在了你的手上，灼烧感极其剧烈。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "burn",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_use_merchant_solvent",
          "text": "使用从行商处获得的溶剂溶解蜡像",
          "requirements_all": [
            "flag_traded_with_rust_merchant"
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "特制溶剂迅速化解了坚硬的蜡层，露出了藏在里面的精纯蜡芯。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": [],
              "reward_tags": [
                "pure_wax"
              ]
            }
          ]
        },
        {
          "id": "choice_smash_effigies",
          "text": "推倒所有诡异的人形蜡像",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "damage",
              "target": "self",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "蜡像碎裂一地，粉碎的噪音响彻了整间房间。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 1
                }
              ],
              "set_flags": [
                "flag_wax_effigies_destroyed"
              ]
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "indoor",
        "ruin"
      ]
    },
    {
      "id": "event_shattered_mirror_hall",
      "name": "碎镜长廊",
      "description": "两侧墙壁镶嵌着数以百计的破碎镜子，每个镜面都在反射出你不同形态的扭曲倒影。",
      "room_tags_any": [
        "indoor",
        "anomaly"
      ],
      "choices": [
        {
          "id": "choice_face_reflection",
          "text": "直视镜像寻求灵魂深处的真谛",
          "check": {
            "stat": "will",
            "dc": 13,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你击碎了镜中的恐惧幻象，获得了澄澈的心智洞察。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 2
                }
              ],
              "set_flags": [
                "flag_mirror_insight"
              ]
            },
            {
              "result": "failure",
              "text": "倒影向你发出刺耳的嘲笑，你的意志防线彻底崩溃。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "fear",
                  "stacks": 2,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_tread_glass",
          "text": "小心翼翼地踏过满地的镜面碎片",
          "check": {
            "stat": "finesse",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你如猫般轻盈地踏过碎玻璃，没有发出一点声音，反而悟出了闪避技巧。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "ward",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            },
            {
              "result": "failure",
              "text": "踩碎玻璃的尖锐飞屑划破了你的脚踝。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 2
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "bleed",
                  "stacks": 2,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_cover_eyes_grope",
          "text": "遮住双眼从长廊中央快速盲走",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "在黑暗中盲走让你多次撞倒镜框，发出了巨大的轰鸣声。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "indoor",
        "anomaly"
      ]
    },
    {
      "id": "event_hollow_forge",
      "name": "虚空锻炉",
      "description": "地下锻造厂的炉火早已熄灭，但巨大的铁砧上仍残存着温热的火星与金属气息。",
      "room_tags_any": [
        "underground",
        "ruin"
      ],
      "choices": [
        {
          "id": "choice_relight_embers",
          "text": "尝试吹开灰烬重新引燃炉火",
          "check": {
            "stat": "insight",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "余烬被重新点燃，温热的铁炉中吐出了一块未锻造的精铁锭。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "iron_ingot"
              ]
            },
            {
              "result": "failure",
              "text": "回火爆裂喷出的火花灼伤了你的面部。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "burn",
                  "stacks": 2,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_hammer_anvil",
          "text": "用重物重击铁砧去除自身护具余锈",
          "check": {
            "stat": "might",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "铁砧的震响重新校准了你的护甲架构，坚固度大幅提升。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "ward",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            },
            {
              "result": "failure",
              "text": "剧烈的反震力让你失手震飞了武器，身体陷于失衡。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "stagger",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_scavenge_coal",
          "text": "在炉渣堆里翻找可用的焦炭残留",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "你弄脏了双手，但在黑灰深处找出了几块上好的煤块。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "coal"
              ]
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "underground",
        "ruin"
      ]
    },
    {
      "id": "event_hanging_cage_prisoner",
      "name": "悬笼囚徒",
      "description": "一只铁笼悬挂在断崖上方，笼内装有一具尚未完全腐烂的干尸，手中紧握着银色物件。",
      "room_tags_any": [
        "high_place",
        "ruin"
      ],
      "choices": [
        {
          "id": "choice_pry_cage_open",
          "text": "徒手撬开悬空铁笼的栅栏",
          "check": {
            "stat": "might",
            "dc": 12,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你硬生生撬弯了铁棒，救出了干尸并取走其手中的银指挥棒。",
              "weight": 100,
              "effects": [],
              "set_flags": [
                "flag_saved_cage_prisoner"
              ],
              "reward_tags": [
                "silver_baton"
              ]
            },
            {
              "result": "failure",
              "text": "生锈的铁棒崩断刺伤了你的手臂，铁笼剧烈晃动响彻山谷。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 3
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_question_spirit",
          "text": "向干尸残留的精神意志发问",
          "check": {
            "stat": "will",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "残存的灵魂解答了你的疑惑，指明了前方的隐秘路线。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 2
                }
              ],
              "set_flags": [
                "flag_interrogated_prisoner"
              ]
            },
            {
              "result": "failure",
              "text": "亡灵的怨念沿着意志反噬，令你心惊胆战。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "fear",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_cut_cage_rope",
          "text": "割断悬挂铁笼的麻绳让其坠落",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_gain",
              "target": "world",
              "resource": "attention",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "铁笼砸落在悬崖底部摔得粉碎，永远清除了这个隐患。",
              "weight": 100,
              "effects": [],
              "set_flags": [
                "flag_prisoner_dropped"
              ]
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "high_place",
        "ruin"
      ]
    },
    {
      "id": "event_bell_tower_mechanism",
      "name": "钟楼机械枢纽",
      "description": "庞大的巨钟齿轮组在头顶轰鸣运转，巨大的摆锤在极窄的通路间来回穿梭。",
      "room_tags_any": [
        "high_place",
        "indoor"
      ],
      "choices": [
        {
          "id": "choice_recalibrate_pendulum",
          "text": "掐准时机调整摆锤的发条连杆",
          "check": {
            "stat": "finesse",
            "dc": 12,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你完美地穿过了机械枢纽，并顺手调整了钟楼的运行节奏，心境大定。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 2
                }
              ],
              "set_flags": []
            },
            {
              "result": "failure",
              "text": "摆锤边缘重重击中了你的肩膀，将你撞飞失衡。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "stagger",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_ring_heavy_bell",
          "text": "强行敲响巨钟震慑整座建筑",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "浩大的钟声轰鸣传播，强烈的震波震晕了附近的生物，但暴露了你的位置。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 3
                }
              ],
              "set_flags": [
                "flag_bell_rung"
              ]
            }
          ]
        },
        {
          "id": "choice_jam_gears",
          "text": "塞入石块卡死旋转的齿轮",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "damage",
              "target": "self",
              "value": 2
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "齿轮发生剧烈崩裂并停止运转，通路变得安全但你被飞溅的崩石砸伤。",
              "weight": 100,
              "effects": [],
              "set_flags": [
                "flag_bell_jammed"
              ]
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "high_place",
        "indoor"
      ]
    },
    {
      "id": "event_poisoned_apothecary_shelf",
      "name": "毒药师货架",
      "description": "废弃药剂室的木架上摆满了没有标签的彩色玻璃瓶，腐蚀性液体正缓缓滴落在地板上。",
      "room_tags_any": [
        "indoor",
        "ruin"
      ],
      "choices": [
        {
          "id": "choice_identify_elixir",
          "text": "通过气味与沉淀辨识安全药剂",
          "check": {
            "stat": "insight",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你准确挑选出了一瓶完美的治疗膏剂并当场服下。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 8
                }
              ],
              "set_flags": []
            },
            {
              "result": "failure",
              "text": "你误服了具有剧烈毒性的未完成药剂。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "poison",
                  "stacks": 2,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_neutralize_spores",
          "text": "使用已知孢子知识中和瓶中毒素",
          "requirements_all": [
            "spore"
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "你轻巧地调配出了中和剂，制成了一瓶无害的炼金试剂。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 6
                }
              ],
              "set_flags": [],
              "reward_tags": [
                "alchemy_vial"
              ]
            }
          ]
        },
        {
          "id": "choice_sweep_shelves",
          "text": "用长棍将货架上的毒药瓶全数扫碎",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "玻璃瓶碎裂一地，药液混合发出了刺鼻的浓烟，你捡起一块未受污染的玻璃碎片。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "mirror_shard"
              ]
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "indoor",
        "ruin"
      ]
    },
    {
      "id": "event_desecrated_altar",
      "name": "被亵渎的祭坛",
      "description": "祭坛被黑色的油污与残缺骨骼覆盖，中央的圣杯空空如也，散发出不安的压迫感。",
      "room_tags_any": [
        "religious",
        "anomaly"
      ],
      "choices": [
        {
          "id": "choice_purify_with_blood",
          "text": "以自身鲜血洗涤圣杯进行仪式",
          "check": {
            "stat": "will",
            "dc": 12,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "圣杯吸收了鲜血发出柔和的光芒，神圣的力量抚平了你的伤口。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 5
                }
              ],
              "set_flags": [
                "flag_altar_purified"
              ]
            },
            {
              "result": "failure",
              "text": "祭坛上的邪异力量反向吞噬了你的精神，令你陷于惊恐。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 4
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "fear",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_offer_ashes",
          "text": "将之前焚烧壁画的灰烬撒在祭坛上",
          "requirements_all": [
            "flag_fresco_burned"
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "灰烬中和了亵渎的油污，祭坛泛起微光，赋予你坚固的守护效果。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "ward",
                  "stacks": 2,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_despoil_altar",
          "text": "强行拆下祭坛上的镀银圣徽",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "你粗暴地抠下了圣徽，亵渎行为引发了虚空的警觉。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 2
                }
              ],
              "set_flags": [],
              "reward_tags": [
                "holy_symbol"
              ]
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "religious",
        "anomaly"
      ]
    },
    {
      "id": "event_sunken_ferryman",
      "name": "沉没摆渡人",
      "description": "水道旁坐着一具手握木桨的湿漉尸骨，身旁放着一只破旧的收钱木盒。",
      "room_tags_any": [
        "water",
        "underground"
      ],
      "choices": [
        {
          "id": "choice_pay_ferryman",
          "text": "向木盒投入专注力作为过河船资",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 2
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "摆渡人尸骨缓缓划动船桨，将你平稳送过深水区并治愈了你。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 4
                }
              ],
              "set_flags": [
                "flag_ferryman_paid"
              ]
            }
          ]
        },
        {
          "id": "choice_steal_oar",
          "text": "尝试从尸骨手中抽走坚硬的木桨",
          "check": {
            "stat": "finesse",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你精明地拔出了木桨，上面缠绕着古老健康的植物藤蔓。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "ancient_vine"
              ]
            },
            {
              "result": "failure",
              "text": "尸骨手指突然收紧捏碎了你的手腕，鲜血流入水中。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 3
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "bleed",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_wade_canal",
          "text": "脱下重靴强行淌过冰冷的黑暗水道",
          "check": {
            "stat": "might",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你咬牙挺过了冰冷的水流，成功抵达对岸。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            },
            {
              "result": "failure",
              "text": "水下的水蛭死死吸附在你的腿上，带走了体力。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 2
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "poison",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "water",
        "underground"
      ]
    },
    {
      "id": "event_creaking_marionette_stage",
      "name": "吱嘎作响的傀儡戏台",
      "description": "无人操控的剧院舞台上，几具破旧人偶正机械地重复着斩首剧目的表演。",
      "room_tags_any": [
        "indoor",
        "anomaly"
      ],
      "choices": [
        {
          "id": "choice_play_accompaniment",
          "text": "走向后台风琴弹奏伴奏乐章",
          "check": {
            "stat": "insight",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你完美的弹奏让傀儡剧目圆满落幕，台下响起了虚无的掌声，心智大增。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 2
                }
              ],
              "set_flags": [
                "flag_stage_performed"
              ]
            },
            {
              "result": "failure",
              "text": "错乱的琴音激怒了傀儡，尖锐的刺耳声音直冲耳膜。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "fear",
                  "stacks": 1,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_cut_stage_wires",
          "text": "登上舞台剪断悬挂傀儡的丝线",
          "check": {
            "stat": "finesse",
            "dc": 10,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你干净利落地剪断了悬线，拆下了精细的傀儡材料。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "puppet_thread"
              ]
            },
            {
              "result": "failure",
              "text": "掉落的重型傀儡砸中了你，导致肢体失衡。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "stagger",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_watch_from_back",
          "text": "站在后排安静地看完这场诡异演出",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_gain",
              "target": "world",
              "resource": "attention",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "长久地沉浸在荒诞剧目中耗费了你的精力与时间。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_loss",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "indoor",
        "anomaly"
      ]
    },
    {
      "id": "event_collapsed_aqueduct",
      "name": "塌陷渡槽",
      "description": "高悬在半空的石质渡槽中间断裂，下方是万丈深渊，呼啸的狂风令人站立不稳。",
      "room_tags_any": [
        "outdoor",
        "water"
      ],
      "choices": [
        {
          "id": "choice_leap_broken_pier",
          "text": "助跑跳过断裂的石桥墩",
          "check": {
            "stat": "finesse",
            "dc": 12,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你如燕子般轻盈跨越了深渊，战胜恐惧后精神更加强韧。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            },
            {
              "result": "failure",
              "text": "你没能踩稳边缘重重磕在对岸石壁上，差点坠落。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 4
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "stagger",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_clear_stone_rubble",
          "text": "搬运沉重石块搭设简易支撑",
          "check": {
            "stat": "might",
            "dc": 11,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "你凭借一身蛮力堆好了踏脚石，并顺手捡到了雕刻精致的石块。",
              "weight": 100,
              "effects": [],
              "set_flags": [],
              "reward_tags": [
                "stone_fragment"
              ]
            },
            {
              "result": "failure",
              "text": "巨石滑落砸伤了你的脚趾，剧痛难忍。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "damage",
                  "target": "self",
                  "value": 2
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "stagger",
                  "stacks": 1,
                  "duration": 1
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_detour_muddy_bank",
          "text": "沿着泥泞的河岸绕行漫长的山路",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_gain",
              "target": "world",
              "resource": "attention",
              "value": 2
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "漫长的绕行消耗了你大量精力，但胜在安全无虞。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_loss",
                  "target": "self",
                  "resource": "focus",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 45,
      "unique": false,
      "tags": [
        "event",
        "outdoor",
        "water"
      ]
    },
    {
      "id": "event_whispering_statue_niche",
      "name": "低语壁龛",
      "description": "墙壁深处的龛位里立着一尊无头雕像，每当你靠近，耳边就会响起细碎的命名低语。",
      "room_tags_any": [
        "religious",
        "high_place"
      ],
      "choices": [
        {
          "id": "choice_whisper_true_name",
          "text": "对着壁龛低声说出自己的真名",
          "check": {
            "stat": "will",
            "dc": 12,
            "mode": "normal"
          },
          "outcomes": [
            {
              "result": "success",
              "text": "雕像认可了你的存在，一缕神圣的光辉为你赋予了坚实的护佑。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "ward",
                  "stacks": 2,
                  "duration": 2
                }
              ],
              "set_flags": [
                "flag_statue_named"
              ]
            },
            {
              "result": "failure",
              "text": "虚空的低语反向侵蚀了你的名字，令你陷入深深的精神恐慌。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "apply_status",
                  "target": "self",
                  "status": "fear",
                  "stacks": 2,
                  "duration": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_offer_vow",
          "text": "向雕像献上之前铭记的安息誓言",
          "requirements_all": [
            "flag_statue_named"
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "誓言得到了壁龛的共鸣，温热的神圣能量注入全身，抚平了所有创伤。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "heal",
                  "target": "self",
                  "value": 6
                },
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "self",
                  "resource": "focus",
                  "value": 2
                }
              ],
              "set_flags": []
            }
          ]
        },
        {
          "id": "choice_cover_niche",
          "text": "解下斗篷盖住低语的壁龛",
          "cost_effects": [
            {
              "trigger": "on_event_resolve",
              "operation": "resource_loss",
              "target": "self",
              "resource": "focus",
              "value": 1
            }
          ],
          "outcomes": [
            {
              "result": "automatic",
              "text": "声音消失了，但遮挡壁龛的动静在安静的高处传得很远。",
              "weight": 100,
              "effects": [
                {
                  "trigger": "on_event_resolve",
                  "operation": "resource_gain",
                  "target": "world",
                  "resource": "attention",
                  "value": 1
                }
              ],
              "set_flags": []
            }
          ]
        }
      ],
      "weight": 30,
      "unique": true,
      "tags": [
        "event",
        "religious",
        "high_place"
      ]
    }
  ],
  "locations": [
    {
      "id": "abandoned_clock_tower_chamber",
      "name": "废弃钟楼机芯室",
      "room_type": "exploration",
      "description": "高塔内部布满数层交叉咬合的巨型黄铜齿轮，顶部悬挂着一根粗大的麻质鸣钟绳。空气中弥漫着冷却机油的味道，断裂的踏板下方是垂直贯穿的空心梯井，可借助摆锤的连杆进行攀爬。",
      "weight": 60,
      "danger": 1,
      "tags": [
        "indoor",
        "high_place",
        "clockwork",
        "ruin"
      ],
      "enemy_tags_any": [
        "clockwork",
        "mechanical"
      ],
      "event_tags_any": [
        "clockwork",
        "high_place"
      ]
    },
    {
      "id": "flooded_underground_aqueduct",
      "name": "积水地下渡槽",
      "room_type": "exploration",
      "description": "半淹没在浑浊地下水中的砖石通道，墙壁两侧设有生锈的手动铁制水闸阀门。水面下隐约可见被冲刷裸露的泥沙暗槽，通道尽头有一扇被水压顶住的木质泄水闸门。",
      "weight": 55,
      "danger": 1,
      "tags": [
        "underground",
        "water",
        "narrow",
        "ruin"
      ],
      "enemy_tags_any": [
        "plant",
        "organic"
      ],
      "event_tags_any": [
        "water",
        "underground"
      ]
    },
    {
      "id": "overgrown_glass_greenhouse",
      "name": "狂乱玻璃温室",
      "room_type": "exploration",
      "description": "半塌陷的维多利亚式铁艺温室，破损的玻璃穹顶下垂挂着茂密的绞杀藤蔓。中央摆放着一座带有手动喷雾泵的炼金喷淋装置，石板路两侧排列着可被外力推倒的木质植株架。",
      "weight": 50,
      "danger": 2,
      "tags": [
        "indoor",
        "garden",
        "ruin",
        "plant"
      ],
      "enemy_tags_any": [
        "plant",
        "spore"
      ],
      "event_tags_any": [
        "ruin",
        "indoor"
      ]
    },
    {
      "id": "crumbling_belfry_balcony",
      "name": "崩塌钟楼露台",
      "room_type": "exploration",
      "description": "突出于城堡外墙的高空石质露台，断裂的拱桥连接着隔壁的宣礼塔。露台边缘立着一台带转轮的手动绞盘升降机，下方是呼啸狂风中的万丈深谷。",
      "weight": 45,
      "danger": 2,
      "tags": [
        "outdoor",
        "high_place",
        "open_area",
        "ruin"
      ],
      "event_tags_any": [
        "high_place",
        "outdoor"
      ]
    },
    {
      "id": "silent_scriptorium_archives",
      "name": "沉寂抄经室",
      "room_type": "exploration",
      "description": "排列着数排高耸木质书架的室内档案库，中央摆放着带有机械配重块的手动图书升降梯。墙角有一扇隐藏在镂空木雕后面的暗门，地板上铺满易碎的干燥纸页。",
      "weight": 60,
      "danger": 0,
      "tags": [
        "indoor",
        "religious",
        "dark"
      ],
      "event_tags_any": [
        "religious",
        "indoor"
      ]
    },
    {
      "id": "sunken_catacomb_passage",
      "name": "下沉墓穴通道",
      "room_type": "exploration",
      "description": "深入地底的石砌甬道，墙壁上的油灯槽里残留着可点燃的动物油脂。道路中央有一块塌陷的压感陷阱石板，连接着上方顶棚的落石机关。",
      "weight": 50,
      "danger": 1,
      "tags": [
        "underground",
        "dark",
        "narrow",
        "ruin"
      ],
      "enemy_tags_any": [
        "undead",
        "construct"
      ],
      "event_tags_any": [
        "underground",
        "ruin"
      ]
    },
    {
      "id": "misty_rose_courtyard",
      "name": "迷雾蔷薇中庭",
      "room_type": "exploration",
      "description": "露天的废弃庭院，四周环绕着柱廊。中央是一座带手摇汲水泵的石造喷泉，密布的带刺蔷薇藤蔓遮挡着通往侧殿的铁栅门，柱廊旁散落着可作为掩体的破损石雕。",
      "weight": 55,
      "danger": 1,
      "tags": [
        "outdoor",
        "garden",
        "open_area",
        "ruin"
      ],
      "event_tags_any": [
        "outdoor",
        "anomaly"
      ]
    },
    {
      "id": "abandoned_blacksmith_forge",
      "name": "废弃铁匠锻造间",
      "room_type": "exploration",
      "description": "位于地下的铁匠工坊，中央设有一座带风箱的手动引火风炉，旁边停放着一辆装满煤屑的手推车。铁砧上方悬挂着可拉动的链条吊钩，墙角有一扇加固的铁皮防火门。",
      "weight": 40,
      "danger": 0,
      "tags": [
        "indoor",
        "underground",
        "fire",
        "ruin"
      ],
      "enemy_tags_any": [
        "construct",
        "metal"
      ],
      "event_tags_any": [
        "underground",
        "ruin"
      ]
    },
    {
      "id": "rusty_gear_courtyard",
      "name": "锈蚀齿轮广场",
      "room_type": "combat",
      "description": "铺设着金属板的开阔废墟广场，地面散落着卡死的巨型机械构件与可提供掩体的废铁箱。中央有一根带有扳手插槽的转轴机关，可触发周围地表的高压蒸汽喷口。",
      "weight": 60,
      "danger": 3,
      "tags": [
        "outdoor",
        "clockwork",
        "open_area",
        "ruin"
      ],
      "enemy_tags_any": [
        "clockwork",
        "construct",
        "mechanical"
      ]
    },
    {
      "id": "desecrated_chapel_nave",
      "name": "被亵渎的侧殿正厅",
      "room_type": "combat",
      "description": "高耸的哥特式教堂大厅，两旁陈列着重型木质长椅。彩绘玻璃窗在月光下折射异彩，讲台旁有一根可斩断的吊灯麻绳，能让顶部的重型铁艺吊灯砸向大厅中央。",
      "weight": 55,
      "danger": 3,
      "tags": [
        "indoor",
        "religious",
        "high_place"
      ],
      "enemy_tags_any": [
        "humanoid",
        "cultist",
        "undead"
      ],
      "entry_effects": [
        {
          "trigger": "on_enter_room",
          "operation": "apply_status",
          "target": "self",
          "status": "fear",
          "stacks": 1,
          "duration": 1
        }
      ]
    },
    {
      "id": "fungal_sewer_intersection",
      "name": "真菌下水道枢纽",
      "room_type": "combat",
      "description": "十字交汇的地下污水管道，空气中弥漫着刺鼻的孢子粉尘。管道上方架设着狭窄的铁网步道，两侧壁面处装有控制闸门的水管转轮，墙壁上布满易燃的干燥真菌膜。",
      "weight": 50,
      "danger": 3,
      "tags": [
        "underground",
        "water",
        "narrow",
        "dark"
      ],
      "enemy_tags_any": [
        "plant",
        "spore",
        "organic"
      ],
      "entry_effects": [
        {
          "trigger": "on_enter_room",
          "operation": "apply_status",
          "target": "self",
          "status": "poison",
          "stacks": 1,
          "duration": 2
        }
      ]
    },
    {
      "id": "abandoned_gallows_hill",
      "name": "荒凉绞刑架高岗",
      "room_type": "combat",
      "description": "荒野山顶的开阔地带，中央矗立着一座木质绞刑架，悬挂着可拉动的金属风铃。坡道四周布满残破的石墙障碍物，山顶有一台转向受限的守城投石弩机。",
      "weight": 45,
      "danger": 2,
      "tags": [
        "outdoor",
        "high_place",
        "open_area"
      ],
      "enemy_tags_any": [
        "undead",
        "bird",
        "beast"
      ]
    },
    {
      "id": "shattered_mirror_gallery",
      "name": "碎镜长廊",
      "room_type": "combat",
      "description": "狭长的高楼走廊，两侧墙壁镶嵌着数以百计的破裂镜框，地上散落着可溅射切割的镜面碎片。长廊尽头立着一具带有锁链的手动遮光拉帘，能遮蔽窗外投射的强光。",
      "weight": 40,
      "danger": 4,
      "tags": [
        "indoor",
        "narrow",
        "anomaly"
      ],
      "enemy_tags_any": [
        "glass",
        "occult",
        "gothic"
      ],
      "entry_effects": [
        {
          "trigger": "on_enter_room",
          "operation": "resource_gain",
          "target": "world",
          "resource": "attention",
          "value": 1
        }
      ]
    },
    {
      "id": "solitary_confessional_booth",
      "name": "孤零告解室",
      "room_type": "event",
      "description": "矗立在走廊尽头的古老双人木质告解亭，木门带有可滑动的小窗格栅。内部设有一张带弹簧底座的跪垫与暗藏的储物夹层，隔壁连接着一根通往地下的传声铁管。",
      "weight": 50,
      "danger": 1,
      "tags": [
        "indoor",
        "religious",
        "narrow"
      ],
      "event_tags_any": [
        "religious",
        "indoor"
      ]
    },
    {
      "id": "collapsed_stone_bridge",
      "name": "塌陷石拱桥",
      "room_type": "event",
      "description": "横跨地底暗河的断裂石桥，断口处仅由几根湿滑的腐烂木梁连接。桥头立着一座带有绞盘锁链的旧水闸石柱，下方急流中漂浮着卡在礁石间的破损货箱。",
      "weight": 45,
      "danger": 2,
      "tags": [
        "underground",
        "water",
        "high_place",
        "ruin"
      ],
      "event_tags_any": [
        "water",
        "high_place"
      ]
    },
    {
      "id": "ruined_astronomy_turret",
      "name": "残破占星塔楼",
      "room_type": "event",
      "description": "高塔顶层的圆顶观测室，穹顶已经半数坍塌。中央摆放着一台可通过黄铜手轮旋转定位的古老黄道仪，角落里停放着带滑轮的铸铁书架与带锁的观测记录箱。",
      "weight": 40,
      "danger": 1,
      "tags": [
        "high_place",
        "clockwork",
        "anomaly"
      ],
      "event_tags_any": [
        "high_place",
        "ruin"
      ]
    },
    {
      "id": "wax_sculptor_vault",
      "name": "蜡塑师地下地窖",
      "room_type": "event",
      "description": "充斥着融化油脂气味的地下工坊，四周排列着未完成的真人大小蜡像。角落里有一座正下方燃着微弱余烬的加热融蜡锅，墙上挂着多把带有刻度的小型皮下解剖刀。",
      "weight": 35,
      "danger": 2,
      "tags": [
        "underground",
        "dark",
        "anomaly"
      ],
      "event_tags_any": [
        "indoor",
        "anomaly"
      ],
      "entry_effects": [
        {
          "trigger": "on_enter_room",
          "operation": "resource_gain",
          "target": "world",
          "resource": "attention",
          "value": 1
        }
      ]
    },
    {
      "id": "wanderer_makeshift_camp",
      "name": "流浪者临时营地",
      "room_type": "npc",
      "description": "由破旧车厢与防水帆布搭成的庇护所，中央燃着一堆带铁架的无烟篝火。车厢旁立着一台带踏板的骨制磨刀石，木箱上摆放着称量药物用的天平与带塞试剂瓶。",
      "weight": 40,
      "danger": 1,
      "tags": [
        "outdoor",
        "ruin",
        "fire"
      ],
      "event_tags_any": [
        "outdoor",
        "ruin"
      ]
    },
    {
      "id": "blind_hermit_shrine",
      "name": "失明隐士龛室",
      "room_type": "npc",
      "description": "修建在岩壁凹陷处的小型石窟，入口悬挂着遮光的草织帘幕。石龛中央供奉着带凹槽的无脸圣像，地面铺有干燥的香草垫，墙角立着一根带手摇响铃的竹质禅杖。",
      "weight": 35,
      "danger": 1,
      "tags": [
        "underground",
        "religious",
        "dark"
      ],
      "event_tags_any": [
        "religious",
        "underground"
      ]
    },
    {
      "id": "clockwork_tinker_booth",
      "name": "发条修理匠工作摊",
      "room_type": "npc",
      "description": "架设在废弃水道旁的木制货摊，摊位上摆满了精密小钳子与微型齿轮盘。后方有一台使用脚踏板驱动的齿轮车床，墙上悬挂着可拉动的警报金属气笛。",
      "weight": 30,
      "danger": 1,
      "tags": [
        "indoor",
        "clockwork",
        "ruin"
      ],
      "event_tags_any": [
        "clockwork",
        "indoor"
      ]
    },
    {
      "id": "executioner_armory_hall",
      "name": "处刑官军械大厅",
      "room_type": "elite",
      "description": "开阔的石砌地下大厅，墙上悬挂着巨型铁钳与枷锁。中央摆放着一座可作掩体的重型斩首台，台侧装有连接吊顶铁笼的手动绞盘锁链，四周分布着四个高耸的铸铁火炬台。",
      "weight": 20,
      "danger": 4,
      "tags": [
        "underground",
        "dark",
        "open_area",
        "ruin"
      ],
      "enemy_tags_any": [
        "construct",
        "armor",
        "giant",
        "elite"
      ],
      "entry_effects": [
        {
          "trigger": "on_enter_room",
          "operation": "apply_status",
          "target": "self",
          "status": "stagger",
          "stacks": 1,
          "duration": 1
        }
      ]
    },
    {
      "id": "matriarch_bramble_greenhouse",
      "name": "圣母荆棘大温室",
      "room_type": "elite",
      "description": "庞大的圆形玻璃圆顶建筑，地面被密集的硬化藤蔓与孢子母株挤破。中央有一座带闸阀的手动蒸汽管道喷口，上方悬挂着多块半挂在空中、可斩落的巨型玻璃穹顶框架。",
      "weight": 20,
      "danger": 4,
      "tags": [
        "indoor",
        "garden",
        "plant",
        "anomaly"
      ],
      "enemy_tags_any": [
        "plant",
        "corrupted",
        "mother",
        "elite"
      ],
      "entry_effects": [
        {
          "trigger": "on_enter_room",
          "operation": "apply_status",
          "target": "self",
          "status": "mark",
          "stacks": 1,
          "duration": 2
        }
      ]
    },
    {
      "id": "grand_marionette_royal_stage",
      "name": "大傀儡皇家剧院",
      "room_type": "boss",
      "description": "拥有三层看台的繁复剧院，中央是带有升降木质台板的庞大舞台。半空中交错悬挂着控制傀儡的钢丝缆绳网，舞台两侧立着可拉动的重型幕布绞盘与带反射镜的脚灯。",
      "weight": 10,
      "danger": 5,
      "tags": [
        "indoor",
        "high_place",
        "gothic",
        "clockwork"
      ],
      "enemy_tags_any": [
        "boss",
        "puppet",
        "king",
        "construct"
      ],
      "entry_effects": [
        {
          "trigger": "on_enter_room",
          "operation": "resource_gain",
          "target": "world",
          "resource": "attention",
          "value": 2
        }
      ]
    },
    {
      "id": "forgotten_nursery_sanctuary",
      "name": "遗弃育婴圣所",
      "room_type": "boss",
      "description": "高耸而破败的圣所大厅，中央停放着一座巨大的木质摇篮车，周围散落着巨大的瓷制玩偶肢体。大厅四周立着四根带拉绳的手动壁炉烟道阀，顶部悬挂着一座大型发条八音盒。",
      "weight": 10,
      "danger": 5,
      "tags": [
        "indoor",
        "religious",
        "gothic",
        "anomaly"
      ],
      "enemy_tags_any": [
        "boss",
        "gothic",
        "doll",
        "mother"
      ],
      "entry_effects": [
        {
          "trigger": "on_enter_room",
          "operation": "apply_status",
          "target": "self",
          "status": "fear",
          "stacks": 1,
          "duration": 2
        }
      ]
    }
  ],
  "observer_actions": [
    {
      "id": "subtle_nudge",
      "name": "微弱推演",
      "description": "在命运骰子落下前，于虚空中投下一缕不易察觉的微光，微幅降低当次判定遭遇的法则阻力。",
      "cost": 1,
      "attention": 0,
      "timing": "before_check",
      "effects": [
        {
          "trigger": "on_check",
          "operation": "modify_dc",
          "target": "current_check",
          "value": -2
        }
      ],
      "requires_roll": false
    },
    {
      "id": "aegis_glance",
      "name": "幕外庇护",
      "description": "将视线短暂聚焦于冒险者身上，在战斗爆发的瞬间为其凝聚出一道抵挡伤害的虚无屏障。",
      "cost": 2,
      "attention": 1,
      "timing": "combat_start",
      "effects": [
        {
          "trigger": "on_combat_start",
          "operation": "shield",
          "target": "self",
          "value": 6
        },
        {
          "trigger": "on_combat_start",
          "operation": "apply_status",
          "target": "self",
          "status": "ward",
          "stacks": 1,
          "duration": 2
        }
      ],
      "requires_roll": false
    },
    {
      "id": "whispered_insight",
      "name": "低语指引",
      "description": "将异界的迷途经验化作耳语传达给冒险者，使其在关键试炼中能够规避最坏的直觉误区。",
      "cost": 1,
      "attention": 1,
      "timing": "before_check",
      "effects": [
        {
          "trigger": "on_check",
          "operation": "advantage",
          "target": "current_check"
        }
      ],
      "requires_roll": false
    },
    {
      "id": "second_chance",
      "name": "强行纠偏",
      "description": "在判定即将滑入失败深渊时扭曲因果，赋予冒险者一次重掷的机会，但这引发了世界的震荡。",
      "cost": 2,
      "attention": 1,
      "timing": "after_check",
      "effects": [
        {
          "trigger": "on_check_fail",
          "operation": "reroll",
          "target": "current_check",
          "value": 1
        }
      ],
      "requires_roll": false
    },
    {
      "id": "curtain_peeking",
      "name": "幕角落照",
      "description": "在跨入新区域前揭开迷雾的一角，提前看清门后潜藏的幽邃环境与异变结构。",
      "cost": 1,
      "attention": 1,
      "timing": "before_room",
      "effects": [
        {
          "trigger": "on_enter_room",
          "operation": "reveal",
          "target": "current_room",
          "value": 1
        }
      ],
      "requires_roll": false
    },
    {
      "id": "desperate_gambit",
      "name": "孤注一掷",
      "description": "以燃烧专注为代价强行拔高命中的几率，强行改变判定的势头，但心智因此受到剧烈反噬。",
      "cost": 0,
      "attention": 2,
      "timing": "before_check",
      "effects": [
        {
          "trigger": "on_check",
          "operation": "advantage",
          "target": "current_check"
        },
        {
          "trigger": "on_check",
          "operation": "resource_loss",
          "target": "self",
          "resource": "focus",
          "value": 2
        }
      ],
      "requires_roll": false
    },
    {
      "id": "frenzied_clarity",
      "name": "狂乱视界",
      "description": "将极度繁复的法则洞察灌入脑海，虽然极大地降低了行事的难度，却使其身心被恐惧笼罩。",
      "cost": 1,
      "attention": 2,
      "timing": "before_check",
      "effects": [
        {
          "trigger": "on_check",
          "operation": "modify_dc",
          "target": "current_check",
          "value": -3
        },
        {
          "trigger": "on_check",
          "operation": "apply_status",
          "target": "self",
          "status": "fear",
          "stacks": 1,
          "duration": 2
        }
      ],
      "requires_roll": false
    },
    {
      "id": "blood_exchange_shield",
      "name": "血契凝护",
      "description": "在战斗开始时将冒险者的部分体液蒸发为坚固的血晶护盾，换取极高的防护却伴随着创伤。",
      "cost": 1,
      "attention": 2,
      "timing": "combat_start",
      "effects": [
        {
          "trigger": "on_combat_start",
          "operation": "shield",
          "target": "self",
          "value": 10
        },
        {
          "trigger": "on_combat_start",
          "operation": "damage",
          "target": "self",
          "value": 3
        }
      ],
      "requires_roll": false
    },
    {
      "id": "marked_fate",
      "name": "命运印记",
      "description": "在强行扭曲判定难度的同时，将冒险者的存在暴露给未知的虚空敌人，使其更容易被锁定。",
      "cost": 0,
      "attention": 3,
      "timing": "before_check",
      "effects": [
        {
          "trigger": "on_check",
          "operation": "modify_dc",
          "target": "current_check",
          "value": -2
        },
        {
          "trigger": "on_check",
          "operation": "apply_status",
          "target": "self",
          "status": "mark",
          "stacks": 1,
          "duration": 3
        }
      ],
      "requires_roll": false
    },
    {
      "id": "vulnerable_surge",
      "name": "破绽爆发",
      "description": "为冒险者注入转瞬即逝的敏捷力量以占据优势，但动作过猛使其当场暴露破绽并陷入失衡。",
      "cost": 1,
      "attention": 2,
      "timing": "before_check",
      "effects": [
        {
          "trigger": "on_check",
          "operation": "advantage",
          "target": "current_check"
        },
        {
          "trigger": "on_check",
          "operation": "apply_status",
          "target": "self",
          "status": "stagger",
          "stacks": 1,
          "duration": 1
        }
      ],
      "requires_roll": false
    },
    {
      "id": "summon_gaze",
      "name": "凝视引敌",
      "description": "向虚空主动释放高浓度的存在感，招致不可名状的关注与危险，借由此种裂隙抽取干涉能量。",
      "cost": -1,
      "attention": 3,
      "timing": "before_room",
      "effects": [
        {
          "trigger": "on_enter_room",
          "operation": "spawn",
          "target": "current_room",
          "value": 1
        }
      ],
      "requires_roll": false
    },
    {
      "id": "sanguine_offering",
      "name": "鲜血干涉",
      "description": "在战斗回合开始时抽走冒险者的生命力奉献给幕外法则，换取干涉力量，造成持续出血。",
      "cost": -1,
      "attention": 3,
      "timing": "turn_start",
      "effects": [
        {
          "trigger": "turn_start",
          "operation": "damage",
          "target": "self",
          "value": 4
        },
        {
          "trigger": "turn_start",
          "operation": "apply_status",
          "target": "self",
          "status": "bleed",
          "stacks": 2,
          "duration": 2
        }
      ],
      "requires_roll": false
    },
    {
      "id": "mind_tether_siphon",
      "name": "理智汲取",
      "description": "强行抽取冒险者紧绷的精神专注作为观测者的干涉能源，令其心智防线出现裂痕与混乱。",
      "cost": -1,
      "attention": 2,
      "timing": "before_check",
      "effects": [
        {
          "trigger": "on_check",
          "operation": "resource_loss",
          "target": "self",
          "resource": "focus",
          "value": 2
        },
        {
          "trigger": "on_check",
          "operation": "disadvantage",
          "target": "current_check"
        }
      ],
      "requires_roll": false
    },
    {
      "id": "toxic_beacon",
      "name": "剧毒信标",
      "description": "将腐蚀性的虚空毒素注入当前空间，强行抽取大量的干涉点数，但冒险者也会被剧毒侵蚀。",
      "cost": -2,
      "attention": 4,
      "timing": "turn_start",
      "effects": [
        {
          "trigger": "turn_start",
          "operation": "damage",
          "target": "self",
          "value": 2
        },
        {
          "trigger": "turn_start",
          "operation": "apply_status",
          "target": "self",
          "status": "poison",
          "stacks": 2,
          "duration": 3
        }
      ],
      "requires_roll": false
    },
    {
      "id": "provoke_abyss",
      "name": "挑衅深渊",
      "description": "彻底撕开幕外遮罩对深渊发出强烈挑衅，将世界难度提升并使冒险者陷入极度惊恐，以此夺取极高干涉力。",
      "cost": -2,
      "attention": 5,
      "timing": "before_check",
      "effects": [
        {
          "trigger": "on_check",
          "operation": "modify_dc",
          "target": "current_check",
          "value": 3
        },
        {
          "trigger": "on_check",
          "operation": "apply_status",
          "target": "self",
          "status": "fear",
          "stacks": 2,
          "duration": 3
        }
      ],
      "requires_roll": false
    }
  ],
  "flavor_text": [
    {
      "id": "flavor_i2_combat_start_01",
      "category": "combat_start",
      "text": "阴影中的构装体齿轮剧烈咬合，带着刺耳的蒸汽撕裂声直冲而来。",
      "tags": [
        "clockwork",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_combat_start_02",
      "category": "combat_start",
      "text": "破碎的圣像后伸出缠满绷带的手臂，冰冷的杀意撕破了死寂。",
      "tags": [
        "religious",
        "danger"
      ]
    },
    {
      "id": "flavor_i2_combat_start_03",
      "category": "combat_start",
      "text": "泥水猛烈泼溅，潜伏在水底的异形怪物掀开铁栅跃出水面。",
      "tags": [
        "water",
        "danger"
      ]
    },
    {
      "id": "flavor_i2_combat_start_04",
      "category": "combat_start",
      "text": "拱顶上的绞丝吊笼轰然坠落，守卫者拔出锈蚀长刃封死退路。",
      "tags": [
        "high_place",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_combat_start_05",
      "category": "combat_start",
      "text": "狂乱的孢子云雾中，干枯的身影挥舞着重型铁钳踏碎石板。",
      "tags": [
        "plant",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_combat_start_06",
      "category": "combat_start",
      "text": "墙壁上的蜡烛同时熄灭，黑暗中点亮数双散发猩红微光的眼睛。",
      "tags": [
        "dark",
        "occult"
      ]
    },
    {
      "id": "flavor_i2_combat_start_07",
      "category": "combat_start",
      "text": "机械哨兵的玻璃眼球迸发出高压电火花，武器连轴转动撕裂空气。",
      "tags": [
        "clockwork",
        "danger"
      ]
    },
    {
      "id": "flavor_i2_combat_start_08",
      "category": "combat_start",
      "text": "祷告台下的阴影如活物般蠕动蔓延，狂热的教徒高举铁槌扑上前。",
      "tags": [
        "religious",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_hit_01",
      "category": "hit",
      "text": "武器狠狠凿入护甲缝隙，崩碎的飞屑与黑血一同迸溅而出。",
      "tags": [
        "physical",
        "danger"
      ]
    },
    {
      "id": "flavor_i2_hit_02",
      "category": "hit",
      "text": "攻击准确命中接合轴承，金属断裂声伴随着浓烈烟雾弥漫开来。",
      "tags": [
        "clockwork",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_hit_03",
      "category": "hit",
      "text": "钝器重重击打在胸肋部位，强烈的震荡逼得对方踉跄后退数步。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i2_hit_04",
      "category": "hit",
      "text": "刃尖顺着甲胄划出一道深邃的创口，鲜红的液体瞬间浸透了衣襟。",
      "tags": [
        "physical",
        "danger"
      ]
    },
    {
      "id": "flavor_i2_hit_05",
      "category": "hit",
      "text": "刺杀精准贯穿了怪物核心的防护层，电火花与油污喷涌而出。",
      "tags": [
        "clockwork"
      ]
    },
    {
      "id": "flavor_i2_hit_06",
      "category": "hit",
      "text": "猛烈的扫击掀翻了掩体，将扑来的对手重重撞倒在碎石堆中。",
      "tags": [
        "physical",
        "ruin"
      ]
    },
    {
      "id": "flavor_i2_hit_07",
      "category": "hit",
      "text": "圣洁的破魔之力凿入躯壳，灼热的烟气从创口处滋滋升起。",
      "tags": [
        "holy",
        "occult"
      ]
    },
    {
      "id": "flavor_i2_hit_08",
      "category": "hit",
      "text": "劲力透过防御崩碎了关节构件，对手发出沉闷而痛苦的嘶鸣。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i2_miss_01",
      "category": "miss",
      "text": "锋刃擦着生锈的铁板划过，迸发出一串火花，却未能切入半分。",
      "tags": [
        "physical",
        "clockwork"
      ]
    },
    {
      "id": "flavor_i2_miss_02",
      "category": "miss",
      "text": "对手敏捷地侧身避开攻击，重击落空在石柱上，炸开一片石粉。",
      "tags": [
        "physical",
        "ruin"
      ]
    },
    {
      "id": "flavor_i2_miss_03",
      "category": "miss",
      "text": "刺杀落空，刃尖深深扎入木质长椅，拔出时耽搁了瞬间节奏。",
      "tags": [
        "physical",
        "religious"
      ]
    },
    {
      "id": "flavor_i2_miss_04",
      "category": "miss",
      "text": "雾气与浓烟打乱了视线，这一击仅仅斩断了空中飘落的破布。",
      "tags": [
        "dark",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_miss_05",
      "category": "miss",
      "text": "机械构件突然发生不规则的收缩避让，猛烈的前刺最终滑过空气。",
      "tags": [
        "clockwork"
      ]
    },
    {
      "id": "flavor_i2_miss_06",
      "category": "miss",
      "text": "攻击被厚重的铁盾正面挡下，沉闷的弹跳力反倒震得手臂酸麻。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i2_miss_07",
      "category": "miss",
      "text": "对手顺势倒地翻滚躲入阴影，地面只留下一道深深的划痕。",
      "tags": [
        "dark",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_critical_01",
      "category": "critical",
      "text": "致命的一击彻底劈碎了发条核心，巨型机械体在剧烈爆炸中崩解。",
      "tags": [
        "critical",
        "clockwork"
      ]
    },
    {
      "id": "flavor_i2_critical_02",
      "category": "critical",
      "text": "武器精准穿透咽喉弱点，巨量的冲击力将对方整个人钉死在墙壁上。",
      "tags": [
        "critical",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_critical_03",
      "category": "critical",
      "text": "狂暴的砍劈将铁甲与骨骼一并斩断，撕裂性的重创让对手彻底失控。",
      "tags": [
        "critical",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_critical_04",
      "category": "critical",
      "text": "破魔的光辉在躯壳内部炸裂，异形生物在惨烈的嚎叫中化为灰烬。",
      "tags": [
        "critical",
        "holy"
      ]
    },
    {
      "id": "flavor_i2_critical_05",
      "category": "critical",
      "text": "这一击直接挑断了主控钢丝缆绳，巨型傀儡如断线般轰然瘫倒。",
      "tags": [
        "critical",
        "clockwork"
      ]
    },
    {
      "id": "flavor_i2_critical_06",
      "category": "critical",
      "text": "沉重的重击彻底砸塌了要害部位，残骸碎片伴随着黑血泼洒整片地面。",
      "tags": [
        "critical",
        "physical"
      ]
    },
    {
      "id": "flavor_i2_critical_07",
      "category": "critical",
      "text": "精准的刺杀引飞了其体内的压力容器，高压气浪将四周的杂物清扫一空。",
      "tags": [
        "critical",
        "fire"
      ]
    },
    {
      "id": "flavor_i4_room_enter_01",
      "category": "room_enter",
      "text": "铸铁推门发出沉重的嘎吱声，房间中央停放着一台未完成的巨型钟表。",
      "tags": [
        "indoor",
        "clockwork"
      ]
    },
    {
      "id": "flavor_i4_room_enter_02",
      "category": "room_enter",
      "text": "地下水顺着青苔覆盖的墙壁滴落，石板地面泛着幽暗的水光。",
      "tags": [
        "underground",
        "water"
      ]
    },
    {
      "id": "flavor_i4_room_enter_03",
      "category": "room_enter",
      "text": "破损的祭坛前排列着半融化的蜡烛，空气中弥漫着干枯香草的气味。",
      "tags": [
        "religious",
        "dark"
      ]
    },
    {
      "id": "flavor_i4_combat_start_01",
      "category": "combat_start",
      "text": "埋伏在废墟阴影中的构装守卫拔出铁刃，齿轮轰鸣着锁定目标。",
      "tags": [
        "clockwork",
        "physical"
      ]
    },
    {
      "id": "flavor_i4_combat_start_02",
      "category": "combat_start",
      "text": "破裂的彩绘玻璃窗外跃入狂热的袭击者，咆哮声响彻整座长廊。",
      "tags": [
        "religious",
        "danger"
      ]
    },
    {
      "id": "flavor_i4_combat_start_03",
      "category": "combat_start",
      "text": "密集的藤蔓突然如蛇般弹起，潜伏其间的异形撕开包覆扑出。",
      "tags": [
        "plant",
        "danger"
      ]
    },
    {
      "id": "flavor_i4_hit_01",
      "category": "hit",
      "text": "锐刃狠狠斩入关节接合处，喷溅的黑色机油涂满了石壁。",
      "tags": [
        "clockwork",
        "physical"
      ]
    },
    {
      "id": "flavor_i4_hit_02",
      "category": "hit",
      "text": "沉重的重击砸偏了对手的防线，骨骼在闷响声中发生错位。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i4_hit_03",
      "category": "hit",
      "text": "圣洁的光芒在创口处爆裂，将蠕动的黑暗物质烧灼得滋滋作响。",
      "tags": [
        "holy",
        "occult"
      ]
    },
    {
      "id": "flavor_i4_miss_01",
      "category": "miss",
      "text": "刺杀偏离了要害，锋刃在坚硬的铁甲上擦出一串耀眼的火花。",
      "tags": [
        "physical",
        "clockwork"
      ]
    },
    {
      "id": "flavor_i4_miss_02",
      "category": "miss",
      "text": "对手借着滑步躲入石柱后方，重击仅仅轰碎了一块石雕边角。",
      "tags": [
        "physical",
        "ruin"
      ]
    },
    {
      "id": "flavor_i4_miss_03",
      "category": "miss",
      "text": "招式落空在浓密的孢子雾气中，招致对方顺势发动了反击。",
      "tags": [
        "plant",
        "dark"
      ]
    },
    {
      "id": "flavor_i4_critical_01",
      "category": "critical",
      "text": "贯穿性的一击直接击碎了能量核心，敌人在剧烈震荡中轰然倒塌。",
      "tags": [
        "critical",
        "clockwork"
      ]
    },
    {
      "id": "flavor_i4_critical_02",
      "category": "critical",
      "text": "刃芒精准斩断咽喉要害，庞大的躯壳带着轰鸣重重砸在地砖上。",
      "tags": [
        "critical",
        "physical"
      ]
    },
    {
      "id": "flavor_i4_critical_03",
      "category": "critical",
      "text": "破魔之力彻底撕碎了污秽的躯壳，余波将四周的阴影一扫而空。",
      "tags": [
        "critical",
        "holy"
      ]
    },
    {
      "id": "flavor_i4_loot_01",
      "category": "loot",
      "text": "从废弃的机械机柜中拆下了一枚带有发条纹路的密封盒。",
      "tags": [
        "clockwork"
      ]
    },
    {
      "id": "flavor_i4_loot_02",
      "category": "loot",
      "text": "拨开石槽中的积水，底端静静躺着一柄带有宗教铭文的银匙。",
      "tags": [
        "religious"
      ]
    },
    {
      "id": "flavor_i4_loot_03",
      "category": "loot",
      "text": "从倾覆的车厢残骸里翻找出一包密封良好的急救绷带。",
      "tags": [
        "ruin"
      ]
    },
    {
      "id": "flavor_i4_rest_01",
      "category": "rest",
      "text": "蜷缩在废弃壁炉的余温旁，握紧武器在断断续续的响声中假寐。",
      "tags": [
        "quiet",
        "indoor"
      ]
    },
    {
      "id": "flavor_i4_rest_02",
      "category": "rest",
      "text": "倚着冷却的黄铜管道坐下，喝了一小口带有铁锈味的冷水。",
      "tags": [
        "clockwork",
        "indoor"
      ]
    },
    {
      "id": "flavor_i4_rest_03",
      "category": "rest",
      "text": "在圣像脚下的阴影里短暂打坐，平复剧烈起伏的心跳与呼吸。",
      "tags": [
        "religious",
        "quiet"
      ]
    },
    {
      "id": "flavor_i4_omen_01",
      "category": "omen",
      "text": "管道深处传来金属敲击声，节律与人的心跳惊人地一致。",
      "tags": [
        "clockwork",
        "danger"
      ]
    },
    {
      "id": "flavor_i4_omen_02",
      "category": "omen",
      "text": "墙角的植物藤蔓以微小的幅度蠕动，嫩芽悄然转向行走的方向。",
      "tags": [
        "plant",
        "anomaly"
      ]
    },
    {
      "id": "flavor_i4_omen_03",
      "category": "omen",
      "text": "石壁上的油灯火焰突然转为幽蓝，温度随之骤降。",
      "tags": [
        "fire",
        "occult"
      ]
    },
    {
      "id": "flavor_i4_injury_01",
      "category": "injury",
      "text": "飞溅的金属碎片划破脸颊，冰冷的鲜血缓缓流进口角。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i4_injury_02",
      "category": "injury",
      "text": "钝击震撼了胸腔，急促的呼吸伴随着阵阵剧烈的刺痛。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i4_death_01",
      "category": "death",
      "text": "最后的视线定格在破碎的穹顶，寒冷与死寂彻底包围了一切。",
      "tags": [
        "dark"
      ]
    },
    {
      "id": "flavor_i4_death_02",
      "category": "death",
      "text": "发条齿轮停止了转动，冰冷的肉体在废墟中渐渐失去温度。",
      "tags": [
        "clockwork"
      ]
    },
    {
      "id": "flavor_i4_victory_01",
      "category": "victory",
      "text": "呼啸的狂风吹散了硝烟，残破的场地重新归于死一般的寂静。",
      "tags": [
        "quiet"
      ]
    },
    {
      "id": "flavor_i4_victory_02",
      "category": "victory",
      "text": "跨过失去生息的阻碍者，握紧武器向着未知的黑暗深处前行。",
      "tags": [
        "dark"
      ]
    },
    {
      "id": "flavor_i1_room_enter_01",
      "category": "room_enter",
      "text": "石门在轴承的剧烈磨损声中推开，潮湿的冷气扑面而来。",
      "tags": [
        "indoor",
        "dark"
      ]
    },
    {
      "id": "flavor_i1_room_enter_02",
      "category": "room_enter",
      "text": "拱顶上方垂落着成束的铜制飞缆，微弱的电火花在绝缘层裂口间闪烁。",
      "tags": [
        "clockwork",
        "indoor"
      ]
    },
    {
      "id": "flavor_i1_room_enter_03",
      "category": "room_enter",
      "text": "泥泞的排水沟沿墙根延伸，水面上浮着一层粘稠的黑色油脂。",
      "tags": [
        "underground",
        "water"
      ]
    },
    {
      "id": "flavor_i1_room_enter_04",
      "category": "room_enter",
      "text": "讲坛上的蜡烛早已熄灭，干涸的蜡油顺着雕花木台一路淌到地砖缝隙里。",
      "tags": [
        "religious",
        "indoor"
      ]
    },
    {
      "id": "flavor_i1_room_enter_05",
      "category": "room_enter",
      "text": "狂风刮过破损的彩绘玻璃，尖锐的呜咽声在空旷的走廊内反复回荡。",
      "tags": [
        "high_place",
        "ruin"
      ]
    },
    {
      "id": "flavor_i1_room_enter_06",
      "category": "room_enter",
      "text": "墙壁上的煤气灯管发出断断续续的嘶嘶声，绿色的微光将阴影拉得极长。",
      "tags": [
        "dark",
        "indoor"
      ]
    },
    {
      "id": "flavor_i1_room_enter_07",
      "category": "room_enter",
      "text": "刺藤死死缠住两旁的石柱，嫩芽顶端散发出带甜味的发酵气息。",
      "tags": [
        "plant",
        "outdoor"
      ]
    },
    {
      "id": "flavor_i1_room_enter_08",
      "category": "room_enter",
      "text": "巨型发条轴承在脚下咔哒转动，整座铁板地面随着机械节律轻微震颤。",
      "tags": [
        "clockwork",
        "ruin"
      ]
    },
    {
      "id": "flavor_i1_room_enter_09",
      "category": "room_enter",
      "text": "积水倒映出高处悬挂的生锈铁笼，笼底的锁扣正缓缓左右晃动。",
      "tags": [
        "water",
        "ruin"
      ]
    },
    {
      "id": "flavor_i1_room_enter_10",
      "category": "room_enter",
      "text": "告解室的木门虚掩着，雕花窗格后隐约透出干涸血斑的轮廓。",
      "tags": [
        "religious",
        "dark"
      ]
    },
    {
      "id": "flavor_i1_room_enter_11",
      "category": "room_enter",
      "text": "陡峭的石阶一路向下倾斜，尽头浸泡在泛着微光的地下潭水里。",
      "tags": [
        "underground",
        "water"
      ]
    },
    {
      "id": "flavor_i1_room_enter_12",
      "category": "room_enter",
      "text": "露天中庭的石雕花坛已经开裂，黑色的孢子云团在残破的雕像脚下聚散。",
      "tags": [
        "outdoor",
        "anomaly"
      ]
    },
    {
      "id": "flavor_i1_omen_01",
      "category": "omen",
      "text": "铜管深处传来不规律的敲击声，每隔三秒便停顿一次。",
      "tags": [
        "clockwork",
        "danger"
      ]
    },
    {
      "id": "flavor_i1_omen_02",
      "category": "omen",
      "text": "墙角的草株无风自动，细小的孢子沿着缝隙向暗处飘散。",
      "tags": [
        "plant",
        "anomaly"
      ]
    },
    {
      "id": "flavor_i1_omen_03",
      "category": "omen",
      "text": "脚下的石板微微塌陷半分，深处传来机关簧片绷紧的声响。",
      "tags": [
        "underground",
        "danger"
      ]
    },
    {
      "id": "flavor_i1_omen_04",
      "category": "omen",
      "text": "烛台上的火焰突然转为幽蓝色，剧烈晃动后缩成一小点。",
      "tags": [
        "fire",
        "occult"
      ]
    },
    {
      "id": "flavor_i1_omen_05",
      "category": "omen",
      "text": "水面泛起环环相扣的涟漪，水底隐约有沉重的阴影游过。",
      "tags": [
        "water",
        "danger"
      ]
    },
    {
      "id": "flavor_i1_omen_06",
      "category": "omen",
      "text": "挂在墙上的玻璃表盘指针开始剧烈逆转，发条发出崩裂前夕的惨鸣。",
      "tags": [
        "clockwork",
        "anomaly"
      ]
    },
    {
      "id": "flavor_i1_omen_07",
      "category": "omen",
      "text": "空气中的气味从霉味急剧转变为刺鼻的硫磺与焦糊味。",
      "tags": [
        "fire",
        "danger"
      ]
    },
    {
      "id": "flavor_i1_omen_08",
      "category": "omen",
      "text": "石壁后传来钝器刮擦花岗岩的刺耳声响，距离越来越近。",
      "tags": [
        "dark",
        "danger"
      ]
    },
    {
      "id": "flavor_i1_omen_09",
      "category": "omen",
      "text": "圣像眼眶中渗出粘稠的黑色液体，滴落在地砖上发出蚀坑声。",
      "tags": [
        "religious",
        "anomaly"
      ]
    },
    {
      "id": "flavor_i1_omen_10",
      "category": "omen",
      "text": "远处的绞盘钢缆骤然绷紧，金属摩擦的尖锐高音撕裂了死寂。",
      "tags": [
        "high_place",
        "danger"
      ]
    },
    {
      "id": "flavor_i1_rest_01",
      "category": "rest",
      "text": "靠在潮湿的壁炉旁合眼，金属发条转动的轻响充斥着不安的梦境。",
      "tags": [
        "quiet",
        "indoor"
      ]
    },
    {
      "id": "flavor_i1_rest_02",
      "category": "rest",
      "text": "清理掉石台上的碎石与断骨，在冷风吹不到的墙角暂时合拢双眼。",
      "tags": [
        "quiet",
        "ruin"
      ]
    },
    {
      "id": "flavor_i1_rest_03",
      "category": "rest",
      "text": "微弱的篝火舔舐着枯枝，四周暗处始终传来细碎的沙沙声。",
      "tags": [
        "fire",
        "outdoor"
      ]
    },
    {
      "id": "flavor_i1_rest_04",
      "category": "rest",
      "text": "将背脊顶住锁紧的铁门，紧握武器在迷糊中度过短暂的半个时辰。",
      "tags": [
        "quiet",
        "danger"
      ]
    },
    {
      "id": "flavor_i1_rest_05",
      "category": "rest",
      "text": "水滴定期落在冰冷的盔甲上，清冷刺骨的刺激让人无法陷入深度沉睡。",
      "tags": [
        "water",
        "underground"
      ]
    },
    {
      "id": "flavor_i1_rest_06",
      "category": "rest",
      "text": "裹紧破损的斗篷坐在祭坛阴影里，呼吸间全是干枯香草与霉菌的气味。",
      "tags": [
        "religious",
        "dark"
      ]
    },
    {
      "id": "flavor_i1_rest_07",
      "category": "rest",
      "text": "拆下废弃车厢的木板升起小火，烫温了皮革囊里的残余苦水。",
      "tags": [
        "fire",
        "outdoor"
      ]
    },
    {
      "id": "flavor_i1_rest_08",
      "category": "rest",
      "text": "靠着微温的机械管道打瞌睡，高压蒸汽的泄压声不时将人惊醒。",
      "tags": [
        "clockwork",
        "indoor"
      ]
    },
    {
      "id": "flavor_i3_loot_01",
      "category": "loot",
      "text": "从倾覆的金属货箱底格里撬出了一件保存完好的黄铜构件。",
      "tags": [
        "clockwork"
      ]
    },
    {
      "id": "flavor_i3_loot_02",
      "category": "loot",
      "text": "擦去石台上的厚厚灰尘，底下露出一枚镶嵌着暗色宝石的徽章。",
      "tags": [
        "religious"
      ]
    },
    {
      "id": "flavor_i3_loot_03",
      "category": "loot",
      "text": "从废弃的衣袍内侧口袋中摸出了一小瓶封口严密的炼金药剂。",
      "tags": [
        "occult"
      ]
    },
    {
      "id": "flavor_i3_loot_04",
      "category": "loot",
      "text": "撬开生锈的铁锁，木箱深处静静躺着几卷记载着旧日法则的皮纸。",
      "tags": [
        "indoor"
      ]
    },
    {
      "id": "flavor_i3_loot_05",
      "category": "loot",
      "text": "斩断缠绕的刺藤后，在花坛凹槽里发现了一柄未曾锈蚀的短刃。",
      "tags": [
        "plant"
      ]
    },
    {
      "id": "flavor_i3_loot_06",
      "category": "loot",
      "text": "水潭底部的泥沙中泛着微光，捞出了一块经过精细切割的折光水晶。",
      "tags": [
        "water"
      ]
    },
    {
      "id": "flavor_i3_loot_07",
      "category": "loot",
      "text": "从瘫痪的构装体胸腔内拔出了一根尚未耗尽能量的微型轴芯。",
      "tags": [
        "clockwork"
      ]
    },
    {
      "id": "flavor_i3_loot_08",
      "category": "loot",
      "text": "掀开祭坛上的破损织锦，隐秘槽位里藏着一串镀银的仪式祷珠。",
      "tags": [
        "religious"
      ]
    },
    {
      "id": "flavor_i3_loot_09",
      "category": "loot",
      "text": "拨开废墟碎石，一袋沉甸甸的旧时代金属硬币在掌中发出响声。",
      "tags": [
        "ruin"
      ]
    },
    {
      "id": "flavor_i3_loot_10",
      "category": "loot",
      "text": "解开干尸腰间的皮革包裹，里面收纳着几件精巧的撬锁工具。",
      "tags": [
        "underground"
      ]
    },
    {
      "id": "flavor_i3_injury_01",
      "category": "injury",
      "text": "飞溅的玻璃碎片扎入小臂，创口渗出细密的血珠，带来阵阵刺痛。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i3_injury_02",
      "category": "injury",
      "text": "高温蒸汽喷灼了左侧脸颊，皮肤火辣辣地发烫，呼吸变得艰难。",
      "tags": [
        "fire"
      ]
    },
    {
      "id": "flavor_i3_injury_03",
      "category": "injury",
      "text": "毒性孢子顺着呼吸道侵入，肺部传来如刀割般的剧烈灼烧感。",
      "tags": [
        "plant"
      ]
    },
    {
      "id": "flavor_i3_injury_04",
      "category": "injury",
      "text": "钝击力透甲胄撕裂了肌肉，每一步挪动都伴随着关节的剧痛。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i3_injury_05",
      "category": "injury",
      "text": "精神受到虚空低语的直接冲击，眼前短暂出现重影与刺耳鸣响。",
      "tags": [
        "occult"
      ]
    },
    {
      "id": "flavor_i3_injury_06",
      "category": "injury",
      "text": "生锈的铁刺划破腿部，黑色的血迹顺着靴筒缓缓渗下。",
      "tags": [
        "ruin"
      ]
    },
    {
      "id": "flavor_i3_injury_07",
      "category": "injury",
      "text": "水下的寒气侵入骨髓，四肢僵硬得几乎无法握紧武器柄手。",
      "tags": [
        "water"
      ]
    },
    {
      "id": "flavor_i3_injury_08",
      "category": "injury",
      "text": "重重摔落在碎石堆上，扭伤的脚踝传来令人齿酸的骨骼挤压感。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i3_death_01",
      "category": "death",
      "text": "视野迅速被黑血与阴影吞噬，冰冷的地面成为最后的归宿。",
      "tags": [
        "dark"
      ]
    },
    {
      "id": "flavor_i3_death_02",
      "category": "death",
      "text": "齿轮咬合的尖锐撕裂声归于寂静，发条停止转动，意识滑入虚无。",
      "tags": [
        "clockwork"
      ]
    },
    {
      "id": "flavor_i3_death_03",
      "category": "death",
      "text": "圣所的烛光彻底熄灭，冰冷的躯壳被疯长蔓延的荆棘缓缓覆盖。",
      "tags": [
        "plant"
      ]
    },
    {
      "id": "flavor_i3_death_04",
      "category": "death",
      "text": "气力随着伤口的大量失血彻底耗尽，最后听到的只有远处的钟声。",
      "tags": [
        "religious"
      ]
    },
    {
      "id": "flavor_i3_victory_01",
      "category": "victory",
      "text": "最后的敌人重重倒下，空旷的大厅内只剩下自己粗重的喘息声。",
      "tags": [
        "quiet"
      ]
    },
    {
      "id": "flavor_i3_victory_02",
      "category": "victory",
      "text": "机械的喧嚣戛然而止，断裂的零件散落一地，危机暂时解除。",
      "tags": [
        "clockwork"
      ]
    },
    {
      "id": "flavor_i3_victory_03",
      "category": "victory",
      "text": "擦去面颊上的油污与血迹，收刃入鞘，空气里的杀意渐渐消散。",
      "tags": [
        "physical"
      ]
    },
    {
      "id": "flavor_i3_victory_04",
      "category": "victory",
      "text": "沉寂重新笼罩了被亵渎的侧殿，微弱的光线穿透烟尘照亮出路。",
      "tags": [
        "religious"
      ]
    },
    {
      "id": "flavor_i3_victory_05",
      "category": "victory",
      "text": "狂乱的孢子云雾在气浪冲刷下散去，残破的场地终于回归安宁。",
      "tags": [
        "plant"
      ]
    },
    {
      "id": "flavor_i3_victory_06",
      "category": "victory",
      "text": "踩过满地狼藉的碎石与废铁，拖着疲惫的躯体继续向深处迈进。",
      "tags": [
        "ruin"
      ]
    },
    {
      "id": "flavor_i3_victory_07",
      "category": "victory",
      "text": "怪物化为灰烬，空气中刺鼻的腥臭味在寒风吹拂下逐渐稀释。",
      "tags": [
        "occult"
      ]
    },
    {
      "id": "flavor_i3_victory_08",
      "category": "victory",
      "text": "伏击者全数失去生息，急促的心跳声在死寂的空间里分外清晰。",
      "tags": [
        "dark"
      ]
    }
  ]
}''')

def _embedded_content_store_init(self, data_dir):
    self.data_dir = Path("<embedded>")
    self.data = now_copy(_EMBEDDED_CONTENT)
    self.maps = {name: {row.get("id"): row for row in rows if row.get("id")}
                 for name, rows in self.data.items()}

ContentStore.__init__ = _embedded_content_store_init

if __name__ == "__main__":
    raise SystemExit(main())
