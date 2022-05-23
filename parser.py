import time

from lexer import Lexer
from lexer import TokenType
from lexer import Token
import turtle as tt
import math
import sys

tokenIter = None
tokenNow = Token()
showProcess = False

# 符号表
table = dict()

# 点数据
points = []


# 获得token
def FetchToken():
    global tokenNow
    try:
        tokenNow = next(tokenIter)
        return tokenNow
    except StopIteration:
        return tokenNow


# 匹配当前Token
def MatchToken(tokenType, show=False):
    # if show:
    #     tokenNow.show()
    if tokenNow.tokenType == tokenType:
        FetchToken()
        return True
    else:
        print("Excepted ", tokenType, "received ", tokenNow.tokenType)
        print("error!")
        return False
        exit(-1)


# 打印消息
def Msg(level, str, op=1):
    global showProcess
    if not showProcess:
        return
    if op == 0:
        print("  " * level + "Enter --> %s" % str)
    else:
        print("  " * level + "Exit  <-- %s" % str)


# 消息可见
def setDefaultValue(show):
    global showProcess
    showProcess = show


# ??
# def factor():
#     if tokenNow.tokenType == TokenType.ID:
#         root = ExpNode(tokenNow)
#         MatchToken(tokenNow.tokenType)
#         return root


def matchColor(color):
    if color == "红":
        return "red"
    if color == "绿":
        return "green"
    if color == "蓝":
        return "blue"
    if color == "黄":
        return "yellow"
    if color == "黑":
        return "black"
    if color == "白":
        return "white"


# 绘图语句
def PlotStatement(level):
    Msg(level, "绘图语句", 0)
    is_line_or_point = True
    color = '黑'
    MatchToken(TokenType.DRAW, True)  # 画
    MatchToken(TokenType.L_BRACKET, True)  # 【
    id1 = tokenNow.lexeme
    id2 = ""
    MatchToken(TokenType.ID, True)  # 参数一
    if tokenNow.tokenType == TokenType.R_BRACKET:
        MatchToken(TokenType.R_BRACKET, True)   # 】
    else:
        MatchToken(TokenType.COMMA, True)  # ，
        if tokenNow.tokenType == TokenType.ID:
            is_line_or_point = False
            id2 = tokenNow.lexeme
            MatchToken(TokenType.ID)  # 参数二
            MatchToken(TokenType.COMMA)
        if tokenNow.tokenType == TokenType.COLOR:
            color = tokenNow.lexeme
            MatchToken(TokenType.COLOR, True)
        MatchToken(TokenType.R_BRACKET, True)  # 】

    if id1 not in table.keys():
        print(id1 + "is not declared")
        exit(1)
    value1 = table[id1]

    # 参数一是数组
    if not is_line_or_point:
        if id2 not in table.keys():
            print(id2 + "is not declared")
            exit(1)
        value2 = table[id2]
        if not isinstance(value2, list):
            print(id2 + "type error")
            exit(1)

        apoints = []
        for i in range(0, len(value1)):
            apoints.append([value1[i], value2[i], matchColor(color)])
        points.append(apoints)
    # 参数一是线或点
    elif isinstance(value1[0], int):
        value1.append(matchColor(color))
        v = list()
        v.append(value1)
        points.append(v)
    else:
        # print(value1)
        for v in value1:
            v.append(matchColor(color))
        points.append(value1)


def factor(level):
    Msg(level, "factor", 0)
    if tokenNow.tokenType == TokenType.CONST_ID:
        value = tokenNow.value
        FetchToken()
        return value
    if tokenNow.tokenType == TokenType.ID:
        value = table[tokenNow.lexeme]
        FetchToken()
        # 可能是数 可能是list
        return value
    if tokenNow.tokenType == TokenType.DIGIT:
        value = tokenNow.value
        FetchToken()
        return value
    if tokenNow.tokenType == TokenType.FUNC:
        func = tokenNow.funcPtr
        funcName = tokenNow.lexeme
        FetchToken()
        MatchToken(TokenType.L_BRACKET, True)
        value1 = expression(level + 1)
        value2 = 0
        value = list()
        if funcName == '幂':
            MatchToken(TokenType.COMMA, True)
            value2 = expression(level + 1)
            if isinstance(value1, list):
                for i in value1:
                    value.append(func(i, value2))
            else:
                return func(value1, value2)
            MatchToken(TokenType.R_BRACKET, True)
            return value
        MatchToken(TokenType.R_BRACKET, True)

        if isinstance(value1, list):
            for i in value1:
                value.append(func(i))
        else:
            return func(value1)
        return value
    else:
        print("error")
        return 0


def ffactor(level):
    Msg(level, "ffactor", 0)
    if tokenNow.tokenType == TokenType.MUL:
        FetchToken()
        value1 = factor(level + 1)
        value2 = ffactor(level + 1)
        if isinstance(value1, list) and not isinstance(value2, list):
            value = []
            for i in value1:
                value.append(i * value2)
            return value
        if isinstance(value1, list) and isinstance(value2, list):
            value = []
            for i in range(0, len(value1)):
                value.append(value1[i] * value2[i])
            return value
        if not isinstance(value1, list) and isinstance(value2, list):
            value = []
            for i in value2:
                value.append(value1 * value2[i])
            return value
        return value1 * value2

    if tokenNow.tokenType == TokenType.DIV:
        FetchToken()
        value1 = factor(level + 1)
        value2 = ffactor(level + 1)
        if isinstance(value1, list) and not isinstance(value2, list):
            value = []
            for i in value1:
                value.append(i / value2)
            return value
        if isinstance(value1, list) and isinstance(value2, list):
            value = []
            for i in range(0, len(value1)):
                value.append(value1[i] / value2[i])
            return value
        if not isinstance(value1, list) and isinstance(value2, list):
            value = []
            for i in value2:
                value.append(value1 / value2[i])
            return value
        return 1 / value1

    else:
        return 1


def term(level):
    Msg(level, "term", 0)
    value1 = factor(level + 1)
    value2 = ffactor(level + 1)
    if isinstance(value1, list) and not isinstance(value2, list):
        value = []
        for i in value1:
            value.append(i * value2)
        return value
    if isinstance(value1, list) and isinstance(value2, list):
        value = []
        for i in range(0, len(value1)):
            value.append(value1[i] * value2[i])
        return value
    if not isinstance(value1, list) and isinstance(value2, list):
        value = []
        for i in range(0, len(value2)):
            value.append(value1 * value2[i])
        return value
    return value1 * value2


def tterm(level):
    Msg(level, "tterm", 0)
    if tokenNow.tokenType == TokenType.PLUS:
        FetchToken()
        value1 = term(level + 1)
        value2 = tterm(level + 1)

        if isinstance(value1, list) and not isinstance(value2, list):
            value = []
            for i in value1:
                value.append(i + value2)
            return value
        if isinstance(value1, list) and isinstance(value2, list):
            value = []
            for i in range(0, len(value1)):
                value.append(value1[i] + value2[i])
            return value
        if not isinstance(value1, list) and isinstance(value2, list):
            value = []
            for i in range(0, len(value2)):
                value.append(value1 + value2[i])
            return value

        return value1 + value2
    if tokenNow.tokenType == TokenType.MINUS:
        FetchToken()
        value1 = term(level + 1)
        value2 = tterm(level + 1)

        if isinstance(value1, list) and not isinstance(value2, list):
            value = []
            for i in value1:
                value.append(-i - value2)
            return value
        if isinstance(value1, list) and isinstance(value2, list):
            value = []
            for i in range(0, len(value1)):
                value.append(-value1[i] - value2[i])
            return value
        if not isinstance(value1, list) and isinstance(value2, list):
            value = []
            for i in range(0, len(value2)):
                value.append(-value1 - value2[i])
            return value

        return -value1 - value2
    else:
        return 0


def expression(level):
    Msg(level, "expression", 0)
    value1 = term(level + 1)
    value2 = tterm(level + 1)

    if isinstance(value1, list) and not isinstance(value2, list):
        value = []
        for i in value1:
            value.append(i + value2)
        return value
    if isinstance(value1, list) and isinstance(value2, list):
        value = []
        for i in range(0, len(value1)):
            value.append(value1[i] + value2[i])
        return value
    if not isinstance(value1, list) and isinstance(value2, list):
        value = []
        for i in range(0, len(value2)):
            value.append(value1 + value2[i])
        return value

    Msg(level, "expression")
    return value1 + value2


def new_array(level):
    Msg(level, "new_array", 0)
    MatchToken(TokenType.ARRAY, True)  # 数组
    MatchToken(TokenType.L_BRACKET, True)  # 【
    frm = tokenNow.value
    MatchToken(TokenType.DIGIT, True)  # num
    MatchToken(TokenType.TO, True)  # 到
    dst = expression(level + 1)  # exp
    step = 1
    if tokenNow.tokenType == TokenType.COMMA:
        MatchToken(TokenType.COMMA, True)
        MatchToken(TokenType.INTERVAL, True)
        step = int(tokenNow.value)
        MatchToken(TokenType.DIGIT)
    MatchToken(TokenType.R_BRACKET, True)  # 】
    Msg(level, "new_array")
    return list(range(frm, int(dst), step))


def new_point(level):
    Msg(level, "new_point", 0)
    MatchToken(TokenType.POINT, True)
    MatchToken(TokenType.L_BRACKET, True)  # 【
    n1 = expression(level + 1)
    MatchToken(TokenType.COMMA, True)
    n2 = expression(level + 1)
    MatchToken(TokenType.R_BRACKET, True)  # 】
    Msg(level, "new_point")
    return [n1, n2]


def new_line(level):
    Msg(level, "new_line", 0)
    MatchToken(TokenType.LINE, True)
    MatchToken(TokenType.L_BRACKET, True)  # 【
    p1_id = tokenNow.lexeme
    MatchToken(TokenType.ID, True)
    MatchToken(TokenType.COMMA, True)
    p2_id = tokenNow.lexeme
    MatchToken(TokenType.ID, True)
    MatchToken(TokenType.R_BRACKET, True)  # 】
    p1 = table[p1_id]
    p2 = table[p2_id]
    Msg(level, "new_line")
    return [p1, p2]


# fu_object = expression | new object
def fu_object(level):
    Msg(level, "fu_object", 0)

    # 新建数组
    if tokenNow.tokenType == TokenType.ARRAY:
        return new_array(level + 1)
    if tokenNow.tokenType == TokenType.ID or tokenNow.tokenType == TokenType.DIGIT or tokenNow.tokenType == TokenType.FUNC or tokenNow.tokenType == TokenType.CONST_ID:
        exp_value = expression(level + 1)
        return exp_value

    # 新建点
    if tokenNow.tokenType == TokenType.POINT:
        return new_point(level + 1)

    # 新建线
    if tokenNow.tokenType == TokenType.LINE:
        return new_line(level + 1)
    Msg(level, "fu_object")


def assignment(level):
    Msg(level, "Assignment", 0)
    id = tokenNow.lexeme
    MatchToken(TokenType.ID, True)
    MatchToken(TokenType.FU, True)
    obj = fu_object(level + 1)
    # print(id + " = " + str(obj))
    table[id] = obj
    Msg(level, "Assignment")


# statement=::assignment|Plot
def Statement(level):
    Msg(level, "Statement", 0)
    statement = None
    if tokenNow.tokenType == TokenType.ID:
        statement = assignment(level + 1)
    elif tokenNow.tokenType == TokenType.DRAW:
        statement = PlotStatement(level + 1)
    else:
        print("Statement Error!")
        exit(-1)
    Msg(level, "Statement")
    return statement


# 语句
def Program(level=0):
    Msg(level, "Program", 0)
    statements = []
    while tokenNow.tokenType != TokenType.NONTOKEN:
        tmpstatement = Statement(level + 1)
        if tokenNow.tokenType == TokenType.NONTOKEN:
            MatchToken(TokenType.NONTOKEN)
        else:
            matched = MatchToken(TokenType.CR)
            if matched:
                statements.append(tmpstatement)
            else:
                print("Program Error")
                exit(-1)
    Msg(level, "Program")
    return statements


# 语法分析器
def Parser(string, show=False):
    global tokenIter

    # 词法分析
    tokenList = Lexer(string)
    tokenIter = iter(tokenList)
    setDefaultValue(False)
    FetchToken()
    # 语句
    return Program()


s = "甲 赋 数组【零到派乘五十一，间隔一】\n" \
    "丁 赋 甲 除 十 减 五\n" \
    "乙 赋 正弦【丁】\n" \
    "丙 赋 余弦【丁】\n" \
    "庚 赋 正弦【丁】 加 正弦【三 乘 丁】 除 三 加 正弦【五 乘 丁】 除 五 加 正弦【七 乘 丁】 除 七\n" \
    "画【丁，庚，蓝】\n" \
    "画【丁，乙，红】\n"

s3 = "甲 赋 数组【零到派乘五十一，间隔一】\n" \
    "丁 赋 甲 除 十 减 五\n" \
    "乙 赋 正弦【丁】\n" \
    "丙 赋 正切【丁】\n" \
     "画【丁，丙，蓝】"

s1 = "乙 赋 数组【一到五十一，间隔一】\n" \
     "丁 赋 乙 除 十\n" \
     "丙 赋 对数【丁】\n" \
     "画【丁，丙，蓝】\n" \
     "甲 赋 点【三，五】\n" \
     "甲甲 赋 点【六，二】\n" \
     "甲甲甲 赋 点【一，一】\n" \
     "丙 赋 线【甲，甲甲】\n"\
     "画【丙，绿】\n"\
     "丙 赋 线【甲，甲甲甲】\n"\
     "画【丙，绿】\n"\
     "丙 赋 线【甲甲甲，甲甲】\n"\
     "画【丙】\n"

s2 = "甲 赋 数组【一到一百，间隔一】\n" \
     "甲 赋 甲 除 十\n" \
     "丙 赋 一 除 三\n" \
     "乙 赋 幂【甲，丙】\n" \
     "画【甲，乙，蓝】"
f = open('test.txt', encoding='gbk')
txt = f.read()


Parser(s)


def fill():
    width = tt.screensize()[0]
    height = tt.screensize()[1]
    # width = 800
    # height = 600

    xlow = points[0][0][0]
    xhigh = points[0][0][0]
    ylow = points[0][0][1]
    yhigh = points[0][0][1]
    for pp in points:
        for p in pp:
            xlow = min(p[0], xlow)
            xhigh = max(p[0], xhigh)
            ylow = min(p[1], ylow)
            yhigh = max(p[1], yhigh)

    if xhigh == xlow or yhigh == ylow:
        if xhigh > 0:
            xlow = 0
        else:
            xhigh = 0
        if yhigh > 0:
            ylow = 0
        else:
            yhigh = 0
    x_scale = width / (xhigh - xlow)
    y_scale = height / (yhigh - ylow)

    tt.speed(10)

    def projection_x(x):
        return (x - xlow) * x_scale - width / 2

    def projection_y(y):
        return (y - ylow) * y_scale - height / 2

    # 画坐标轴

    tt.penup()
    tt.color("black")
    tt.goto(-800 / 2, projection_y(0))
    tt.pendown()
    tt.goto(800 / 2, projection_y(0))
    tt.penup()
    tt.goto(projection_x(0), -600 / 2)
    tt.pendown()
    tt.goto(projection_x(0), 600 / 2)

    # 写坐标
    tt.penup()
    tt.goto(projection_x(0), projection_y(0))
    tt.write('O')
    step = max(int((xhigh - xlow) / 7), int((yhigh - ylow) / 7))
    if step == 0:
        step = max(round((xhigh - xlow) / 7, 1), round((yhigh - ylow) / 7, 1))
    i = int(xlow)-1
    while i <= math.ceil(xhigh)+1:
        # print(step)
        if int(i) == 0:
            i = i + step
            continue
        tt.goto(projection_x(i), projection_y(0))
        tt.write("%.1f" % i)
        i = i + step

    i = int(ylow)-1
    while i <= math.ceil(yhigh)+1:
    # for i in range(int(ylow)-1, math.ceil(yhigh)+1, step):
        if int(i) == 0:
            i = i + step
            continue
        tt.goto(projection_x(0), projection_y(i))
        tt.write("%.1f" % i)
        i = i + step

    # 图
    tt.penup()
    for pp in points:
        # print((p[0]-xlow)*x_scale-200, (p[1]-ylow)*y_scale-200)
        # if len(pp) == 1:
        #     tt.color(pp[0][2])
        #     tt.goto(projection_x(pp[0][0]), projection_y(pp[0][1]))
        #     tt.pendown()
        # else:
        for p in pp:
            tt.color(p[2])
            tt.goto(projection_x(p[0]), projection_y(p[1]))
            tt.pendown()
        tt.penup()

    time.sleep(2)


fill()
