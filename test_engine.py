import tempfile
import unittest
from pathlib import Path

from veil_dice_engine import Game, ContentStore


DATA = Path(__file__).parent / "data"


class VeilDiceSmokeTests(unittest.TestCase):
    def test_content_and_map(self):
        store = ContentStore(DATA)
        self.assertGreaterEqual(len(store.all("equipment_bases")), 20)
        self.assertGreaterEqual(len(store.all("enemies")), 20)
        for seed in range(50):
            game = Game.new(DATA, seed=seed)
            self.assertEqual(len(game.state["rooms"]), 10)
            self.assertEqual(game.state["rooms"][-1]["room_type"], "boss")
            # 每个房间都至少能沿 north 主路抵达，故 boss 不会不可达。
            self.assertEqual(game.state["rooms"][-2]["exits"].get("north"), 9)

    def test_fixed_seed_and_save_reload(self):
        one = Game.new(DATA, seed=123)
        two = Game.new(DATA, seed=123)
        self.assertEqual([r["location_id"] for r in one.state["rooms"]], [r["location_id"] for r in two.state["rooms"]])
        one.cmd("travel north")
        one.cmd("check insight dc=12")
        with tempfile.TemporaryDirectory() as tmp:
            save = Path(tmp) / "save.json"
            one.save(save)
            loaded = Game.load(DATA, save)
            self.assertEqual(one.state["current_room"], loaded.state["current_room"])
            self.assertEqual(one.state["audit"], loaded.state["audit"])
            self.assertEqual(one.cmd("check insight dc=12"), loaded.cmd("check insight dc=12"))

    def test_observer_event_combat_and_export(self):
        game = Game.new(DATA, seed=7)
        self.assertIn("subtle_nudge", [a["id"] for a in game.store.all("observer_actions")])
        self.assertIn("观测者能力", game.cmd("observer use subtle_nudge"))
        for _ in range(5):
            game.cmd("travel north")
        text = game.cmd("combat policy=aggressive rounds=1")
        self.assertIn("回合", text)
        token = game.cmd("export")
        other = Game.new(DATA, seed=999)
        other.cmd("import " + token)
        self.assertEqual(game.state["current_room"], other.state["current_room"])
        self.assertEqual(game.state["turn"], other.state["turn"])

    def test_every_normal_command_returns_player_panel(self):
        game = Game.new(DATA, seed=5)
        for command in ("status", "look", "inventory compact=true", "observer status", "check insight dc=12"):
            output = game.cmd(command)
            self.assertIn("《幕外之骰》", output)
            self.assertIn("观测者｜观测点", output)
        # 导出串必须保持纯净，才能直接复制导入。
        self.assertTrue(game.cmd("export").startswith("VEIL-DICE-0.1:"))
        self.assertNotIn("观测者｜观测点", game.cmd("export"))


if __name__ == "__main__":
    unittest.main()
