def StringColor(txt, color='Black'):
    def getColor(color):
        if color == 'Cyan':
            return Cyan
        if color == 'Magenta':
            return Magenta
        if color == 'Red':
            return Red
        if color == 'Green':
            return Green
        if color == 'Yellow':
            return Yellow
        else:
            return Black

    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'
    Default = '\033[99m'

    return '{}{}{}'.format(getColor(color), txt, Default)