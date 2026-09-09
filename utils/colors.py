"""
Cores para o jogo Pac-Man
Formato: 0xRRGGBBAA (RR=vermelho, GG=verde, BB=azul, AA=alfa)
"""

# ==================== CORES BÁSICAS ====================


class Basic:
    BLACK       = 0x000000FF
    WHITE       = 0xFFFFFFFF
    RED         = 0xFF0000FF
    GREEN       = 0x00FF00FF
    BLUE        = 0x0000FFFF
    YELLOW      = 0xFFFF00FF
    MAGENTA     = 0xFF00FFFF
    CYAN        = 0x00FFFFFF
    ORANGE      = 0xFFA500FF
    PURPLE      = 0x800080FF
    PINK        = 0xFFC0CBFF
    BROWN       = 0xA52A2AFF
    GRAY        = 0x808080FF
    LIME        = 0x00FF00FF
    MAROON      = 0x800000FF
    NAVY        = 0x000080FF
    OLIVE       = 0x808000FF
    TEAL        = 0x008080FF
    SILVER      = 0xC0C0C0FF
    GOLD        = 0xFFD700FF

# ==================== CINZAS ====================


class Grays:
    BLACK       = 0x000000FF
    DARK_1      = 0x0A0A0AFF
    DARK_2      = 0x121212FF
    DARK_3      = 0x1A1A1AFF
    DARK_4      = 0x222222FF
    DARK_5      = 0x2D2D2DFF
    DARK_6      = 0x333333FF
    DARK_7      = 0x3D3D3DFF
    GRAY_1      = 0x444444FF
    GRAY_2      = 0x555555FF
    GRAY_3      = 0x666666FF
    GRAY_4      = 0x777777FF
    GRAY_5      = 0x888888FF
    GRAY_6      = 0x999999FF
    GRAY_7      = 0xAAAAAAFF
    LIGHT_1     = 0xBBBBBBFF
    LIGHT_2     = 0xCCCCCCFF
    LIGHT_3     = 0xDDDDDDFF
    LIGHT_4     = 0xEEEEEEFF
    LIGHT_5     = 0xF5F5F5FF
    WHITE       = 0xFFFFFFFF

# ==================== CORES MODERNAS (Material Design) ====================
class Material:
    # Vermelhos
    RED_50      = 0xFFEBEEFF
    RED_100     = 0xFFCDD2FF
    RED_200     = 0xEF9A9AFF
    RED_300     = 0xE57373FF
    RED_400     = 0xEF5350FF
    RED_500     = 0xF44336FF
    RED_600     = 0xE53935FF
    RED_700     = 0xD32F2FFF
    RED_800     = 0xC62828FF
    RED_900     = 0xB71C1CFF
    
    # Rosas
    PINK_50     = 0xFCE4ECFF
    PINK_100    = 0xF8BBD0FF
    PINK_200    = 0xF48FB1FF
    PINK_300    = 0xF06292FF
    PINK_400    = 0xEC407AFF
    PINK_500    = 0xE91E63FF
    PINK_600    = 0xD81B60FF
    PINK_700    = 0xC2185BFF
    PINK_800    = 0xAD1457FF
    PINK_900    = 0x880E4FFF
    
    # Roxos
    PURPLE_50   = 0xF3E5F5FF
    PURPLE_100  = 0xE1BEE7FF
    PURPLE_200  = 0xCE93D8FF
    PURPLE_300  = 0xBA68C8FF
    PURPLE_400  = 0xAB47BCFF
    PURPLE_500  = 0x9C27B0FF
    PURPLE_600  = 0x8E24AAFF
    PURPLE_700  = 0x7B1FA2FF
    PURPLE_800  = 0x6A1B9AFF
    PURPLE_900  = 0x4A148CFF
    
    # Azuis
    BLUE_50     = 0xE3F2FDFF
    BLUE_100    = 0xBBDEFBFF
    BLUE_200    = 0x90CAF9FF
    BLUE_300    = 0x64B5F6FF
    BLUE_400    = 0x42A5F5FF
    BLUE_500    = 0x2196F3FF
    BLUE_600    = 0x1E88E5FF
    BLUE_700    = 0x1976D2FF
    BLUE_800    = 0x1565C0FF
    BLUE_900    = 0x0D47A1FF
    
    # Cianos
    CYAN_50     = 0xE0F7FAFF
    CYAN_100    = 0xB2EBF2FF
    CYAN_200    = 0x80DEEAFF
    CYAN_300    = 0x4DD0E1FF
    CYAN_400    = 0x26C6DAFF
    CYAN_500    = 0x00BCD4FF
    CYAN_600    = 0x00ACC1FF
    CYAN_700    = 0x0097A7FF
    CYAN_800    = 0x00838FFF
    CYAN_900    = 0x006064FF
    
    # Verdes
    GREEN_50    = 0xE8F5E9FF
    GREEN_100   = 0xC8E6C9FF
    GREEN_200   = 0xA5D6A7FF
    GREEN_300   = 0x81C784FF
    GREEN_400   = 0x66BB6AFF
    GREEN_500   = 0x4CAF50FF
    GREEN_600   = 0x43A047FF
    GREEN_700   = 0x388E3CFF
    GREEN_800   = 0x2E7D32FF
    GREEN_900   = 0x1B5E20FF
    
    # Amarelos
    YELLOW_50   = 0xFFFDE7FF
    YELLOW_100  = 0xFFF9C4FF
    YELLOW_200  = 0xFFF59DFF
    YELLOW_300  = 0xFFF176FF
    YELLOW_400  = 0xFFEE58FF
    YELLOW_500  = 0xFFEB3BFF
    YELLOW_600  = 0xFDD835FF
    YELLOW_700  = 0xFBC02DFF
    YELLOW_800  = 0xF9A825FF
    YELLOW_900  = 0xF57F17FF
    
    # Laranjas
    ORANGE_50   = 0xFFF3E0FF
    ORANGE_100  = 0xFFE0B2FF
    ORANGE_200  = 0xFFCC80FF
    ORANGE_300  = 0xFFB74DFF
    ORANGE_400  = 0xFFA726FF
    ORANGE_500  = 0xFF9800FF
    ORANGE_600  = 0xFB8C00FF
    ORANGE_700  = 0xF57C00FF
    ORANGE_800  = 0xEF6C00FF
    ORANGE_900  = 0xE65100FF

# ==================== CORES PARA PAC-MAN ====================
class Pacman:
    # Cores do Pac-Man
    YELLOW      = 0xFFFF00FF
    GOLD        = 0xFFD700FF
    SUNNY       = 0xFDB813FF
    CANARY      = 0xFFF9A6FF
    
    # Cores dos fantasmas
    GHOST_RED   = 0xFF0000FF      # Blinky (vermelho)
    GHOST_PINK  = 0xFFB8FFFF      # Pinky (rosa)
    GHOST_CYAN  = 0x00FFFFFF      # Inky (ciano)
    GHOST_ORANGE = 0xFFB851FF     # Clyde (laranja)
    
    # Pontos
    DOT         = 0xFFB8AEFF
    POWER_DOT   = 0xFFB8AEFF
    
    # Frutas
    CHERRY      = 0xDE3131FF
    STRAWBERRY  = 0xFF0040FF
    ORANGE      = 0xFFA500FF
    APPLE       = 0x76CD26FF
    MELON       = 0xFFCC66FF
    GALAXIAN    = 0x00FF00FF
    BELL        = 0xFFFF00FF
    KEY         = 0xFFFF00FF

# ==================== CORES DE UI ====================


class UI:
    # Cores para temas escuros
    DARK_BG         = 0x1A1A1AFF
    DARK_SURFACE    = 0x2D2D2DFF
    DARK_ELEVATED   = 0x3D3D3DFF
    DARK_BORDER     = 0x444444FF
    DARK_TEXT       = 0xFFFFFFFF
    DARK_TEXT_SEC   = 0xAAAAAAFF
    DARK_HOVER      = 0x404040FF
    DARK_ACTIVE     = 0x505050FF

    # Cores para temas claros
    LIGHT_BG        = 0xF5F5F5FF
    LIGHT_SURFACE   = 0xFFFFFFFF
    LIGHT_BORDER    = 0xCCCCCCFF
    LIGHT_TEXT      = 0x1A1A1AFF
    LIGHT_TEXT_SEC  = 0x666666FF
    LIGHT_HOVER     = 0xE0E0E0FF
    LIGHT_ACTIVE    = 0xD0D0D0FF

    # Cores de ação
    PRIMARY         = 0x007AFFFF
    SECONDARY       = 0x6C5CE7FF
    SUCCESS         = 0x34C759FF
    DANGER          = 0xFF3B30FF
    WARNING         = 0xFF9500FF
    INFO            = 0x5AC8FAFF

    # Cores de ação (hover)
    PRIMARY_HOVER   = 0x005BBBFF
    SECONDARY_HOVER = 0x5A4BD1FF
    SUCCESS_HOVER   = 0x2DB84EFF
    DANGER_HOVER    = 0xE6352AFF
    WARNING_HOVER   = 0xE68600FF
    INFO_HOVER      = 0x4AB8E9FF

# ==================== TRANSPARÊNCIAS ====================


class Alpha:
    OPAQUE = 0x000000FF
    NONE = 0x00000000
    HALF = 0x00000080
    QUARTER = 0x00000040
    THREE_QUARTER = 0x000000C0
    DIM = 0x000000B3
    LIGHT = 0x0000004D
    VERY_LIGHT = 0x0000001A

    # Overlays pré-definidos
    OVERLAY_DARK = 0x00000080
    OVERLAY_LIGHT = 0xFFFFFF80
    OVERLAY_DIM = 0x000000B3
    OVERLAY_NONE = 0x00000000

# ==================== PALETAS COMPLETAS ====================


class Theme:
    @staticmethod
    def dark():
        return {
            'bg': UI.DARK_BG,
            'surface': UI.DARK_SURFACE,
            'elevated': UI.DARK_ELEVATED,
            'border': UI.DARK_BORDER,
            'text': UI.DARK_TEXT,
            'text_secondary': UI.DARK_TEXT_SEC,
            'primary': UI.PRIMARY,
            'secondary': UI.SECONDARY,
            'success': UI.SUCCESS,
            'danger': UI.DANGER,
            'warning': UI.WARNING,
            'hover': UI.DARK_HOVER,
            'active': UI.DARK_ACTIVE,
        }

    @staticmethod
    def light():
        return {
            'bg': UI.LIGHT_BG,
            'surface': UI.LIGHT_SURFACE,
            'elevated': UI.LIGHT_SURFACE,
            'border': UI.LIGHT_BORDER,
            'text': UI.LIGHT_TEXT,
            'text_secondary': UI.LIGHT_TEXT_SEC,
            'primary': UI.PRIMARY,
            'secondary': UI.SECONDARY,
            'success': UI.SUCCESS,
            'danger': UI.DANGER,
            'warning': UI.WARNING,
            'hover': UI.LIGHT_HOVER,
            'active': UI.LIGHT_ACTIVE,
        }

    @staticmethod
    def pacman():
        return {
            'bg': Basic.BLACK,
            'pacman': Pacman.YELLOW,
            'ghost_red': Pacman.GHOST_RED,
            'ghost_pink': Pacman.GHOST_PINK,
            'ghost_cyan': Pacman.GHOST_CYAN,
            'ghost_orange': Pacman.GHOST_ORANGE,
            'dot': Pacman.DOT,
            'power_dot': Pacman.POWER_DOT,
            'score': Basic.WHITE,
            'lives': Pacman.YELLOW,
            'walls': Basic.BLUE,
            'text': Basic.WHITE,
        }
