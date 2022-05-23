from enum import Enum
import math
from pycnnum import cn2num, num2cn


class TokenType(Enum):
    ARRAY = "数组"
    POINT = "点"
    LINE = "线"
    TO = "到"
    INTERVAL = "间隔"
    PLUS = "加"
    MINUS = "减"
    MUL = "乘"
    DIV = "除"
    FU = "赋"
    DRAW = "画"
    CONST_ID = "CONST_ID"
    L_BRACKET = "【"
    R_BRACKET = "】"
    COMMA = "，"
    COLOR = "COLOR"
    DIGIT = "DIGIT"
    ID = "ID"
    FUNC = "FUNCTION"
    NONTOKEN = "NONTOKEN"
    ERRTOKEN = "ERRTOKEN"
    SEMICO = '；'
    CR = '\n'


class Token:

    def __init__(self, tokentype=TokenType.NONTOKEN, lexeme="", value=0.0, funcptr=None):
        self.tokenType = tokentype
        self.lexeme = lexeme
        self.value = value
        self.funcPtr = funcptr

    def show(self):
        print(self.tokenType.name.ljust(15), self.lexeme.ljust(15), str(self.value).ljust(15), self.funcPtr)


# CONST_ID
TokenTypeDict = dict(
    红=Token(TokenType.COLOR, "红"),
    绿=Token(TokenType.COLOR, "绿"),
    蓝=Token(TokenType.COLOR, "蓝"),
    黄=Token(TokenType.COLOR, "黄"),
    黑=Token(TokenType.COLOR, "黑"),
    数=Token(TokenType.ARRAY, "数组"),
    点=Token(TokenType.POINT, "点"),
    线=Token(TokenType.LINE, "线"),
    间=Token(TokenType.INTERVAL, "间隔"),
    到=Token(TokenType.TO, "到"),
    画=Token(TokenType.DRAW, "画"),
    赋=Token(TokenType.FU, "赋"),
    加=Token(TokenType.PLUS, "加"),
    减=Token(TokenType.MINUS, "减"),
    乘=Token(TokenType.MUL, "乘"),
    除=Token(TokenType.DIV, "除"),
    正弦=Token(TokenType.FUNC, "正弦", 0.0, math.sin),
    正切=Token(TokenType.FUNC, "正切", 0.0, math.tan),
    对=Token(TokenType.FUNC, "对数", 0.0, math.log),
    余=Token(TokenType.FUNC, "余弦", 0.0, math.cos),
    逸=Token(TokenType.CONST_ID, "逸", math.e),
    派=Token(TokenType.CONST_ID, "派", math.pi),
    幂=Token(TokenType.FUNC, "幂", 0.0, math.pow),
    根=Token(TokenType.FUNC, "根号", 0.0, math.sqrt))


def showTokens(tokens):
    print("Category".ljust(15), "Input".ljust(15), "Value".ljust(15), "FuncPtr")
    for token in tokens:
        token.show()


def getChar(str, pos):
    if pos < len(str):
        return str[pos]
    else:
        return ''


def isChinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


LETTER = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']


def isLetter(letter):
    if letter in LETTER:
        return True
    return False


def Lexer(string, show=False):
    tokens = []  # 识别出的token序列
    lineNum = 1  # 行
    i = 0

    while True:
        char = getChar(string, i)
        if char == '':
            tokens.append(Token(TokenType.NONTOKEN, ''))
            break

        # if char == '\n':
        #     lineNum = lineNum + 1
        #     i = i + 1
        #     continue

        if char == ' ' or char == '\t' or string[i] == '\r':
            i = i + 1
            continue

        token = None

        if isChinese(char):

            # 数字
            if char.isnumeric():
                tmpStr = char
                while True:
                    i = i + 1
                    char = getChar(string, i)
                    if char.isnumeric() or char == "点":
                        tmpStr = tmpStr + char
                        # print(tmpStr)
                    else:
                        i = i - 1
                        break
                token = Token(TokenType.DIGIT, tmpStr, cn2num(tmpStr))

            # 变量
            elif isLetter(char):
                tmpStr = char
                while True:
                    i = i + 1
                    char = getChar(string, i)
                    if isLetter(char):
                        tmpStr = tmpStr + char
                        # print(tmpStr)
                    else:
                        i = i - 1
                        break
                token = Token(TokenType.ID, tmpStr)

            # 两个字的汉字
            elif char == '数' or char == '间' or char == '余' or char == '根' or char == '对':
                token = TokenTypeDict.get(char, Token(TokenType.ERRTOKEN, char))
                i = i + 1

            # 正弦 正切
            elif char == '正':
                tmpStr = char
                i = i + 1
                char = getChar(string, i)
                tmpStr = tmpStr + char
                token = TokenTypeDict.get(tmpStr, Token(TokenType.ERRTOKEN, char))
            # 其他汉字
            else:
                token = TokenTypeDict.get(char, Token(TokenType.ERRTOKEN, char))

        # 非汉字
        elif char == '，':
            token = Token(TokenType.COMMA, "，")

        elif char == '；':
            token = Token(TokenType.SEMICO, "；")

        elif char == '\n':
            token = Token(TokenType.CR, "\n")

        elif char == '【':
            token = Token(TokenType.L_BRACKET, "【")

        elif char == '】':
            token = Token(TokenType.R_BRACKET, "】")

        else:
            token = Token(TokenType.ERRTOKEN, char)

        if token:
            tokens.append(token)

        i = i + 1

    if show:
        showTokens(tokens)

    return tokens


def test():
    s1 = "甲 赋 数组【零到十一，间隔一】\n" \
         "乙 赋 正弦【甲】\n"
    # s = "甲 赋 二百五十 减 五；\n乙 赋 数组【一到甲，间隔一】；\n画【乙，乙，红】；\n丙 赋 点【三十五，四十】；\n丁 赋 点【二，五】；\n戊己 赋 线【丙，丁】；\n画【戊己，蓝】；"
    s = "正弦 对数 派 逸 正切 余弦 根号"
    mytokens = Lexer(s1)
    # showTokens(mytokens)


test()
