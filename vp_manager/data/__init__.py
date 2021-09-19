# coding=utf-8
import json
import os

from vp_manager.config import const
from vp_manager.config.account import project_path

mission_path = os.path.join(project_path, const.MISSION_DATA_PATH)
follower_path = os.path.join(project_path, const.FOLLOWER_DATA_PATH)

with open(mission_path, 'r', encoding='utf-8') as f:
    mission_list = json.loads(f.read())

with open(follower_path, 'r', encoding='utf-8') as f:
    follower_list = json.loads(f.read())

reward_list = {
    '187569': const.MRT_BOX_CLOTH,  # 掮灵的裁缝促进微粒
    '187572': const.MRT_BOX_GRASS,  # 掮灵的草药促进微粒
    '187573': const.MRT_BOX_MAGIC,  # 掮灵的附魔促进微粒
    '187574': const.MRT_BOX_FISH,  # 掮灵的满溢之桶
    '187413': const.MRT_EXP_ITEM,  # 3000 exp
    '187414': const.MRT_EXP_ITEM,  # 7500 exp
    '184646': const.MRT_BOX_MINE,  # 英雄的采矿箱
    '184647': const.MRT_BOX_GRASS,  # 英雄的草药箱
    '184638': const.MRT_BOX_FISH,  # 英雄的鱼箱
    '184637': const.MRT_BOX_MEAT,  # 英雄的肉箱
    '184648': const.MRT_BOX_MAGIC,  # 英雄的附魔箱
    '184645': const.MRT_BOX_LEATHER,  # 英雄的剥皮箱
    '184644': const.MRT_BOX_CLOTH,  # 英雄的裁缝箱
}

