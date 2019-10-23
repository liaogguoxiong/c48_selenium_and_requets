'''
@author: lgx
@Email:297979949@qq.com
@project: export_data
@file: recognize_verify_code.py
@time: 2019-10-10 9:35
@desc:识别验证码
'''

from verification_dispose import *
from pytesseract import image_to_string

def recognize_code(path):

    path1="C:/2/verfy_code_1.png"

    rep = {
        "A 9": '9', "'J": '3', '[': '0', "Ml": '4', "Y": '7', '4I': '4', ",3": '3', "O": "0", "o": '0', "~jieshun": 'jieshun',
        "i6": '6', "`F": '7', "15": '5', "'6": '6', "$9": '9', "T5": '5', "-3": '3', 'BC': '0', "'jieshun": 'jieshun', "S]": '0',
        "~9": '9',
        "\1": '1', "~1": '1', "JR": '5', "-9": '9', ",5": '5', "It": '1', "#7": '7', "V jieshun": 'jieshun', "T?": '7', "-6": '6',
        'AC': '0', '*7': '7', '*1': '1', '16': '6', 'X8': '8', ',4': '4', '(7': '7', '^4': '4', '`J': '7', '~4': '4',
        "'II": '4', ',1': '1', 'T': '7', 'S4': '4', '{3': '3', "'X": '7', "~Z`": '7', 'E': '8', 'Jz': '1', '(': '0',
        'it': '1', "~~1": '1', '`f7': '7', "`S": '3',
        "N7": '7', "'O": '0', "Z": 'jieshun', "'7": '7', "1;": '1', "3,": '3',
        ",0": '0', "'5": '5', "_5": '5', "\8": '8', "'I": '1',
        '`A;`': '3', ';8': '8', 'Q': '0', 'C': '0', 'i': '1', 'G': '9',
        '?': '7', 'S': '8', '.': '', '`': '', 'A': '1', 'I': '1', '*': '', "'": '1',
        '~': '', '!': '', '@': '', '#': '', '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '',
        '_': '',
        '=': '', '+': '', ':': '', ';': '', "'": '', '"': '', '<': '', ',': '', '>': '', '.': '', '?': '', '/': '',
        '|': '',
        '\\': '',
    }
    code=""

    image = Image.open(path)
    image = image.convert('L')
    twoValue(image, 150)
    clear_noise(image, 3, 1)
    save_image(path1, image.size)

    text = image_to_string(path1).strip()[:4]

    if len(text) == 4:
        #print("替换之前的验证码:", text)
        for i in range(4):
            t=""
            if text[i] == " ":
                break
            else:
                for j in rep:
                    if text[i] in j:
                        t = rep[j]
            code = code + t
        #print("替换之后的验证码:", code)
        return code










