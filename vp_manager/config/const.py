# coding=utf-8

# system
SYSTEM_MAC = 'mac'
SYSTEM_WIN = 'win'

# TODO: path
DB_PATH = 'F:\\notes\\vp_test\\ventureplan-assistant\\vp_manager\\database\\venture_plan.sqlite'
TABLE_NAME = 'arrangement'

# message type from queue
MT_ROLE_DATA = 'ROLE_DATA'
MT_MISSION_DATA = 'MISSION_DATA'
MT_FOLLOWER_INFO = 'FOLLOWER_INFO'
MT_SOLDIER_LEVEL = 'FOLLOWER_INFO'
MT_MISSION_RESULT = 'MISSION_RESULT'


# mission execute result
MER_FAILED = 0
MER_SUCCESS = 1
MER_END = 2


# mission reward type
# from aPaiXu.lua
MRT_GOLD = 'Gold'
MRT_ANIMA = 'ReservoirAnima'
MRT_EXP = 'XP'
MRT_EXP_ITEM = 'XPitem'
MRT_EQUIP = 'Equip'
MRT_RUNE = 'VeiledAugmentRune'  #
MRT_BOX = 'Treasure'  #
MRT_ASH = 'Maw'  #
MRT_ASH_2 = 'SoulCinders'  #
MRT_PET = 'BattlePetCurrency'
MRT_BATTLE = 'Campaign'
MRT_SEED = 'Covenants'
MRT_REP = 'Reputation'
MRT_UNKNOWN = 'Unknown'

MRT_BOX_FISH = 'fish_box'  #
MRT_BOX_MEAT = 'meat_box'  #
MRT_BOX_MINE = 'mine_box'  #
MRT_BOX_CLOTH = 'cloth_box'  #
MRT_BOX_GRASS = 'grass_box'  #
MRT_BOX_LEATHER = 'leather_box'  #
MRT_BOX_MAGIC = 'leather_magic'  #


# follower fight result
FFR_MUST_WIN = 1
FFR_MUST_FAIL = 2
FFR_NOT_SURE = 3  # has record but fail_health < health < win_health
FFR_UNKNOWN = 4  # no record




