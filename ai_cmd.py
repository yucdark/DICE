#!/usr/bin/env python3
"""给 AI 使用的一次一命令入口：自动读取/创建存档并原样返回游戏结果。"""

from __future__ import annotations

import argparse
from pathlib import Path

from veil_dice_engine import Game


def main() -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="幕外之骰 AI 命令入口")
    parser.add_argument("command", nargs="*", help="例如：status、travel north、observer use subtle_nudge")
    parser.add_argument("--new", action="store_true", help="明确开始新局；会覆盖当前指定存档")
    parser.add_argument("--seed", type=int, default=None, help="新局固定随机种子")
    parser.add_argument("--save", default=str(here / "save.json"), help="存档路径")
    parser.add_argument("--data-dir", default=str(here / "data"), help="内容包目录")
    args = parser.parse_args()

    save_path = Path(args.save)
    if args.new or not save_path.exists():
        game = Game.new(args.data_dir, save_path=save_path, seed=args.seed)
        game.save(save_path)
    else:
        game = Game.load(args.data_dir, save_path)

    command = " ".join(args.command).strip() or "status"
    print(game.cmd(command))
    game.save(save_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
