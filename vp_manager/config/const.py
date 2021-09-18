# coding=utf-8

# TODO: path
DB_PATH = 'F:\\notes\\vp_test\\ventureplan-assistant\\vp_manager\\database\\venture_plan.sqlite'
TABLE_NAME = 'arrangement'

# message type from queue
MT_ROLE_DATA = 'ROLE_DATA'
MT_MISSION_DATA = 'MISSION_DATA'
MT_FOLLOWER_INFO = 'FOLLOWER_INFO'
MT_MISSION_RESULT = 'MISSION_RESULT'


# mission execute result
MER_FAILED = 0
MER_SUCCESS = 1
MER_END = 2


# mission reward type
MRT_GOLD = 'gold'
MRT_ANIMA = 'anima'
MRT_EXP = 'exp'
MRT_EQUIP = 'equip'
MRT_RUNE = 'rune'  #
MRT_BOX = 'box'  #
MRT_BOX_FISH = 'fish_box'  #
MRT_BOX_MEAT = 'meat_box'  #
MRT_BOX_MINE = 'mine_box'  #
MRT_BOX_CLOTH = 'cloth_box'  #
MRT_BOX_HERBAL = 'herbal_box'  #
MRT_BOX_LEATHER = 'leather_box'  #
MRT_ASH = 'ash'  # min shang
MRT_ASH_2 = 'ash_2'  # pa ta hui jin
MRT_PET = 'pet'
MRT_BATTLE = 'battle'


# follower fight result
FFR_MUST_WIN = 1
FFR_MUST_FAIL = 2
FFR_NOT_SURE = 3  # has record but fail_health < health < win_health
FFR_UNKNOWN = 4  # no record




