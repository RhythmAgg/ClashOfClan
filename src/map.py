MAP = """
####################################################################################################
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
#                                                                 H                                #
#                                                 1                                                #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
#         K  H                          ********************          C                            #
#                                       *                  *                                       #
#                                       *                  *                                       #
#      C                                *       TTTT       *                                       #
#                                       *       TTTT   C   *                                       #
#                                       *       TTTT       *          3                  H         #
#                                       *                  *                                       #
#                                       *                  *                                       #
#                                       ********************                                       #
#                                                                                                  #
#                                                 H                                                #
#                                                                                                  #
#             H                                                                                    #
#                                                                                                  #
#                                                                                                  #
#                                                 2                                                #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
####################################################################################################
"""
HUT_POS = []
CANNON_POS = []
WALL_POS = []

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 30

for i in range(len(MAP)):
    if MAP[i] == 'H':
        HUT_POS.append([int(i / SCREEN_WIDTH), i % SCREEN_WIDTH])
    if MAP[i] == 'C':
        CANNON_POS.append([int(i / SCREEN_WIDTH), i % SCREEN_WIDTH])
    if MAP[i] == '*':
        WALL_POS.append([int(i / SCREEN_WIDTH), i % SCREEN_WIDTH])

print(f"""
HUT_POS = {HUT_POS}
CANNON_POS = {CANNON_POS}
WALL_POS = {WALL_POS}
""")