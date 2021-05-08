#%%
class Color_Scheme:
    def __init__(self, color1:list[int,int,int], color2:list[int,int,int], color3:list[int,int,int], color4:list[int,int,int], color5:list[int,int,int]):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.color4 = color4
        self.color5 = color5
    
    def __getitem__(self, idx:int):
        if idx == 1:
            return self.color1
        elif idx == 2:
            return self.color2
        elif idx == 3:
            return self.color3
        elif idx == 4:
            return self.color4
        elif idx == 5:
            return self.color5

# Default Color Scheme

DARK_BLUE =  [20, 117, 135]
SALMON = [250, 126, 92]
OLD_SNOW = [243, 236, 229]
FADED_SCHOOLBUS = [254, 203, 95]
ZORA_SKIN = [99, 204, 200]
DEFAULT_COLORS = Color_Scheme(DARK_BLUE, ZORA_SKIN, DARK_BLUE, FADED_SCHOOLBUS, SALMON)

# Theme 2
NIGHTSHADE = [80, 49, 67]
PUMPKIN = [154, 83, 43]
BANDAID = [196, 155, 96]
FILIGREE = [121, 173, 159]
MONSTERA = [25, 52, 57]
ZEN_COLORS = Color_Scheme(NIGHTSHADE, BANDAID, MONSTERA, FILIGREE, PUMPKIN)

LOGO_COLOR_1 = [255,0,0]
LOGO_COLOR_2 = [255,175,0]
LOGO_COLOR_3 = [0,255,0]
LOGO_COLOR_4 = [0,255,175]
LOGO_COLOR_5 = [0,0,255]

# Debug Mode Color Scheme
DB_GREEN =  [118,166,22]
DB_BLUE = [31, 101, 242]
DB_SNOT = [164, 242, 7]
DB_ORANGE = [242, 65, 31]
DB_BRICKRED = [166, 37, 13]

ACTIVE_SCHEME = ZEN_COLORS
SCORE_PANEL_COLOR = ACTIVE_SCHEME[1]
BG_COLOR = ACTIVE_SCHEME[2]
FG_COLOR = ACTIVE_SCHEME[3]
APPLE_COLOR = ACTIVE_SCHEME[4]
SNAKE_COLOR = ACTIVE_SCHEME[5]
