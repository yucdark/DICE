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


if __name__ == "__main__":
    raise SystemExit(main())
