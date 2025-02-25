# -*- encoding: utf-8 -*-
"""
@File    :   image.py
@Time    :   2025/2/25 下午8:35
@Author  :   Li Jiawei
@Version :   1.0
@Contact :   Li.J.W.adrian421@hotmail.com
@License :   (C)Copyright 2023-2030
@Desc    :   None
@Brief   :
"""
import os, sys, argparse
from tqdm import tqdm
from itertools import groupby, tee
from datetime import timedelta
from collections import Counter
import codecs, json, \
        time, datetime, pickle, \
        re, random, numpy as np, \
        pandas as pd, xml.dom.minidom as xmldom, string
import inspect
import platform
import yaml
import itertools
from pdb import set_trace as stop
from typing import Any, List, Tuple, Union
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import io
import cv2
import base64



def png2base64(png_path):
    import base64
    with open(png_path,"rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
        # base64.b64decode(base64data)
    return base64_data


def readImgPIL(path, cvt=False, mode="RGB"):
        if cvt:
                assert mode in ["RGB", "RGBA", "L"], f"convert mode param error, input is : {mode}"
                return Image.open(path).convert(mode)
        else:
                return Image.open(path)


def saveImg(img, path, cvt=False, mode="RGB"):
        if cvt:
                assert mode in ["RGB", "RGBA", "L"], f"convert mode param error, input is : {mode}"
                im_save = Image.fromarray(img).convert(mode)
        else:
                im_save = Image.fromarray(img)
        im_save.save(path)


def matrix2image(mat, mode="RGB"):
        """ if inputs is list of numpy matrices, use this to generate pil image for model inputs"""
        return Image.fromarray(mat).convert(mode)


def readImg(path, cvt=False, mode="RGB"):
        if cvt:
                assert mode in ["RGB", "RGBA", "L"], f"convert mode param error, input is : {mode}"
                return np.array(Image.open(path).convert(mode))
        else:
                return np.array(Image.open(path))


def RGB2L(img):
        return np.array(Image.fromarray(img).convert("L"))


def L2RGB(img):
        return np.array(Image.fromarray(img).convert("RGB"))


def showImgs(imglist, shape):
        plt.figure(figsize=(15, 15))
        for i in range(len(imglist)):
                plt.subplot(shape[0], shape[1], i + 1)
                plt.imshow(imglist[i])
        plt.show()


def check_pixel_set(img):
        print(set(img.reshape(-1).tolist()))


'''
###############################################
'''

'''
########  Image Color  ######
'''


def change_color(img, old_color, new_color):
        """
        RGB:
          ---------------------------------------------------------
    　    |Pink	粉红	#FFC0CB	255,192,203
          |LightPink 浅粉红 #FFB6C1 255,182,193
    　    |Crimson	猩红	#DC143C	220,20,60
    　    |LavenderBlush	脸红的淡紫色	#FFF0F5	255,240,245
    　    |PaleVioletRed	苍白的紫罗兰红色	#DB7093	219,112,147
    　    |HotPink	热情的粉红	#FF69B4	255,105,180
    　    |DeepPink	深粉色	#FF1493	255,20,147
    　    |MediumVioletRed	适中的紫罗兰红色	#C71585	199,21,133
    　    |Orchid	兰花的紫色	#DA70D6	218,112,214
    　    |Thistle	蓟	#D8BFD8	216,191,216
    　    |plum	李子	#DDA0DD	221,160,221
    　    |Violet	紫罗兰	#EE82EE	238,130,238
    　    |Magenta	洋红	#FF00FF	255,0,255
    　    |Fuchsia	灯笼海棠(紫红色)	#FF00FF	255,0,255
    　    |DarkMagenta	深洋红色	#8B008B	139,0,139
    　    |Purple	紫色	#800080	128,0,128
    　    |MediumOrchid	适中的兰花紫	#BA55D3	186,85,211
    　    |DarkVoilet	深紫罗兰色	#9400D3	148,0,211
    　    |DarkOrchid	深兰花紫	#9932CC	153,50,204
    　    |Indigo	靛青	#4B0082	75,0,130
    　    |BlueViolet	深紫罗兰的蓝色	#8A2BE2	138,43,226
    　    |MediumPurple	适中的紫色	#9370DB	147,112,219
    　    |MediumSlateBlue	适中的板岩暗蓝灰色	#7B68EE	123,104,238
    　    |SlateBlue	板岩暗蓝灰色	#6A5ACD	106,90,205
    　    |DarkSlateBlue	深岩暗蓝灰色	#483D8B	72,61,139
    　    |Lavender	熏衣草花的淡紫色	#E6E6FA	230,230,250
    　    |GhostWhite	幽灵的白色	#F8F8FF	248,248,255
    　    |Blue	纯蓝	#0000FF	0,0,255
    　    |MediumBlue	适中的蓝色	#0000CD	0,0,205
    　    |MidnightBlue	午夜的蓝色	#191970	25,25,112
    　    |DarkBlue	深蓝色	#00008B	0,0,139
    　    |Navy	海军蓝	#000080	0,0,128
    　    |RoyalBlue	皇家蓝	#4169E1	65,105,225
    　    |CornflowerBlue	矢车菊的蓝色	#6495ED	100,149,237
    　    |LightSteelBlue	淡钢蓝	#B0C4DE	176,196,222
    　    |LightSlateGray	浅石板灰	#778899	119,136,153
    　    |SlateGray	石板灰	#708090	112,128,144
    　    |DoderBlue	道奇蓝	#1E90FF	30,144,255
    　    |AliceBlue	爱丽丝蓝	#F0F8FF	240,248,255
    　    |SteelBlue	钢蓝	#4682B4	70,130,180
    　    |LightSkyBlue	淡蓝色	#87CEFA	135,206,250
    　    |SkyBlue	天蓝色	#87CEEB	135,206,235
    　    |DeepSkyBlue	深天蓝	#00BFFF	0,191,255
    　    |LightBLue	淡蓝	#ADD8E6	173,216,230
    　    |PowDerBlue	火药蓝	#B0E0E6	176,224,230
    　    |CadetBlue	军校蓝	#5F9EA0	95,158,160
    　    |Azure	蔚蓝色	#F0FFFF	240,255,255
    　    |LightCyan	淡青色	#E1FFFF	225,255,255
    　    |PaleTurquoise	苍白的绿宝石	#AFEEEE	175,238,238
    　    |Cyan	青色	#00FFFF	0,255,255
    　    |Aqua	水绿色	#00FFFF	0,255,255
    　    |DarkTurquoise	深绿宝石	#00CED1	0,206,209
    　    |DarkSlateGray	深石板灰	#2F4F4F	47,79,79
    　    |DarkCyan	深青色	#008B8B	0,139,139
    　    |Teal	水鸭色	#008080	0,128,128
    　    |MediumTurquoise	适中的绿宝石	#48D1CC	72,209,204
    　    |LightSeaGreen	浅海洋绿	#20B2AA	32,178,170
    　    |Turquoise	绿宝石	#40E0D0	64,224,208
    　    |Auqamarin	绿玉/碧绿色	#7FFFAA	127,255,170
    　    |MediumAquamarine	适中的碧绿色	#00FA9A	0,250,154
    　    |MediumSpringGreen	适中的春天的绿色	#F5FFFA	245,255,250
    　    |MintCream	薄荷奶油	#00FF7F	0,255,127
    　    |SpringGreen	春天的绿色	#3CB371	60,179,113
    　    |SeaGreen	海洋绿	#2E8B57	46,139,87
    　    |Honeydew	蜂蜜	#F0FFF0	240,255,240
    　    |LightGreen	淡绿色	#90EE90	144,238,144
    　    |PaleGreen	苍白的绿色	#98FB98	152,251,152
    　    |DarkSeaGreen	深海洋绿	#8FBC8F	143,188,143
    　    |LimeGreen	酸橙绿	#32CD32	50,205,50
    　    |Lime	酸橙色	#00FF00	0,255,0
    　    |ForestGreen	森林绿	#228B22	34,139,34
    　    |Green	纯绿	#008000	0,128,0
    　    |DarkGreen	深绿色	#006400	0,100,0
    　    |Chartreuse	查特酒绿	#7FFF00	127,255,0
    　    |LawnGreen	草坪绿	#7CFC00	124,252,0
    　    |GreenYellow	绿黄色	#ADFF2F	173,255,47
    　    |OliveDrab	橄榄土褐色	#556B2F	85,107,47
    　    |Beige	米色(浅褐色)	#6B8E23	107,142,35
    　    |LightGoldenrodYellow	浅秋麒麟黄	#FAFAD2	250,250,210
    　    |Ivory	象牙	#FFFFF0	255,255,240
    　    |LightYellow	浅黄色	#FFFFE0	255,255,224
    　    |Yellow	纯黄	#FFFF00	255,255,0
    　    |Olive	橄榄	#808000	128,128,0
    　    |DarkKhaki	深卡其布	#BDB76B	189,183,107
    　    |LemonChiffon	柠檬薄纱	#FFFACD	255,250,205
    　    |PaleGodenrod	灰秋麒麟	#EEE8AA	238,232,170
    　    |Khaki	卡其布	#F0E68C	240,230,140
    　    |Gold	金	#FFD700	255,215,0
    　    |Cornislk	玉米色	#FFF8DC	255,248,220
    　    |GoldEnrod	秋麒麟	#DAA520	218,165,32
    　    |FloralWhite	花的白色	#FFFAF0	255,250,240
    　    |OldLace	老饰带	#FDF5E6	253,245,230
    　    |Wheat	小麦色	#F5DEB3	245,222,179
    　    |Moccasin	鹿皮鞋	#FFE4B5	255,228,181
    　    |Orange	橙色	#FFA500	255,165,0
    　    |PapayaWhip	番木瓜	#FFEFD5	255,239,213
    　    |BlanchedAlmond	漂白的杏仁	#FFEBCD	255,235,205
    　    |NavajoWhite	Navajo白	#FFDEAD	255,222,173
    　    |AntiqueWhite	古代的白色	#FAEBD7	250,235,215
    　    |Tan	晒黑	#D2B48C	210,180,140
    　    |BrulyWood	结实的树	#DEB887	222,184,135
    　    |Bisque	(浓汤)乳脂,番茄等	#FFE4C4	255,228,196
    　    |DarkOrange	深橙色	#FF8C00	255,140,0
    　    |Linen	亚麻布	#FAF0E6	250,240,230
    　    |Peru	秘鲁	#CD853F	205,133,63
    　    |PeachPuff	桃色	#FFDAB9	255,218,185
    　    |SandyBrown	沙棕色	#F4A460	244,164,96
    　    |Chocolate	巧克力	#D2691E	210,105,30
    　    |SaddleBrown	马鞍棕色	#8B4513	139,69,19
    　    |SeaShell	海贝壳	#FFF5EE	255,245,238
    　    |Sienna	黄土赭色	#A0522D	160,82,45
    　    |LightSalmon	浅鲜肉(鲑鱼)色	#FFA07A	255,160,122
    　    |Coral	珊瑚	#FF7F50	255,127,80
    　    |OrangeRed	橙红色	#FF4500	255,69,0
    　    |DarkSalmon	深鲜肉(鲑鱼)色	#E9967A	233,150,122
    　    |Tomato	番茄	#FF6347	255,99,71
    　    |MistyRose	薄雾玫瑰	#FFE4E1	255,228,225
    　    |Salmon	鲜肉(鲑鱼)色	#FA8072	250,128,114
    　    |Snow	雪	#FFFAFA	255,250,250
    　    |LightCoral	淡珊瑚色	#F08080	240,128,128
    　    |RosyBrown	玫瑰棕色	#BC8F8F	188,143,143
    　    |IndianRed	印度红	#CD5C5C	205,92,92
    　    |Red	纯红	#FF0000	255,0,0
    　    |Brown	棕色	#A52A2A	165,42,42
    　    |FireBrick	耐火砖	#B22222	178,34,34
    　    |DarkRed	深红色	#8B0000	139,0,0
    　    |Maroon	栗色	#800000	128,0,0
    　    |White	纯白	#FFFFFF	255,255,255
    　    |WhiteSmoke	白烟	#F5F5F5	245,245,245
    　    |Gainsboro	Gainsboro	#DCDCDC	220,220,220
    　    |LightGrey	浅灰色	#D3D3D3	211,211,211
    　    |Silver	银白色	#C0C0C0	192,192,192
    　    |DarkGray	深灰色	#A9A9A9	169,169,169
    　    |Gray	灰色	#808080	128,128,128
    　    |DimGray	暗淡的灰色	#696969	105,105,105
    　    |Black	纯黑	#000000	0,0,0
          ---------------------------------------------------------
        img: 二值化后的图像
        old_color: 旧颜色
        new_color: 新颜色
        """
        new_img = []
        for row in img:
                new_row = []
                for col in row:
                        if '_'.join([str(x) for x in col]) == '_'.join([str(x) for x in old_color]):
                                new_row.append(new_color)
                        else:
                                new_row.append(col)
                new_img.append(new_row)
        new_img = np.array(new_img, dtype=np.uint8)
        return new_img


'''
###############################################
'''

'''
########  Image to Bytes  ######
'''


def numpy2bytes(im, format, image_depth):
        img = Image.fromarray(im).convert(image_depth)
        with io.BytesIO() as image_bytes:
                img.save(image_bytes, format=format)
                image_bytes = image_bytes.getvalue()
        return image_bytes


def bytes2base64(image_bytes):
        image_base64 = base64.b64encode(image_bytes)
        return image_base64


def numpy2base64(im, format='png', image_depth='L', toutf8=True):
        image_bytes = numpy2bytes(im, format, image_depth)
        image_base64 = bytes2base64(image_bytes)
        if toutf8:
                image_base64 = image_base64.decode(encoding='utf-8')
        return image_base64


def base64Tobytes(image_base64):
        image_bytes = base64.b64decode(image_base64)
        return image_bytes


def bytes2numpy(image_bytes):
        img = np.array(Image.open(io.BytesIO(image_bytes)))
        return img


def base64ToNumpy(image_base64):
        image_bytes = base64Tobytes(image_base64)
        img = bytes2numpy(image_bytes)
        return img


def test_image_to_bytes():
        im = np.random.randint(0, 256, (12, 12,)).astype(np.uint8)
        cv2.imwrite('test_random.png', im)
        image_base64 = numpy2base64(im)
        print('base64:\n', image_base64)
        im2 = base64ToNumpy(image_base64)
        cv2.imwrite('test_from_base64.png', im2)