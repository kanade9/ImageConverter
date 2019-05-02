from PIL import Image
import warnings


def process(red, green, blue):
    if N == 1:
        return ntsc_avr_process(red, green, blue)

    elif N == 2:
        return intermediate_value_process(red, green, blue)

    elif N == 3:
        return avarage_value_process(red, green, blue)

    elif N == 4:
        return g_channel_process(red, green, blue)

    elif N == 5:
        return itu_coef_method(red, green, blue)


# NTSC係数による加重平均法（PILの標準変換はこの手法）
def ntsc_avr_process(r, g, b):
    result = 0.298912 * r + 0.586611 * g + 0.114478 * b
    return result


# 中間値法
def intermediate_value_process(r, g, b):
    result = (min(r, g, b) + (max(r, g, b))) / 2
    return result


# 単純平均法
def avarage_value_process(r, g, b):
    result = (r + g + b) / 3
    return result


# Gチャンネル法 greenだけを反映
def g_channel_process(r, g, b):
    return g


# HDTV係数による加重平均と補正(Photoshopなどのグレースケール化に用いられる手法)
def itu_coef_method(r, g, b):
    x = 2.2
    R = (r ** x) * 0.222015
    G = (g ** x) * 0.706655
    B = (b ** x) * 0.071330
    result = (R + G + B) ** (1 / x)
    return result


# モードの選択
print(
    'input number: 1.NTSC avr 2.intermediate value 3.avarage value 4.g channel 5.itu coef method')
N = int(input())
if N < 1 or N > 5:
    print('Please input exact number')
    exit(0)

print('input your image file pass below ')
warnings.warn('don\'t include extension! please input like \"user/xxxx/image\"')
adr = str(input())

print('your input file is PNG or JPEG ?  p/j')

out_adr = ''
out_adr_2 = ''
adr_2 = ''

E = str(input())
if E == 'p':
    out_adr = adr + '-out' + '.png'
    adr += '.png'
elif E == 'j':
    out_adr = adr + '-out' + '.jpg'
    out_adr_2 = adr + '-out' + '.jpeg'
    adr_2 = adr + '.jpeg'
    adr += '.jpg'

else:
    print('Please input exact alphabet')
    exit(0)

print('Choose convert mode 1.green mode for GBStudio  2.normal mode')

M = int(input())
if M < 1 or M > 2:
    print('Please input exact number')
    exit(0)

# 元画像読み込み jpgで読み込めないときはjpgで読み込む処理

try:
    baseImg = Image.open(adr)

except IOError:
    try:
        baseImg = Image.open(adr_2)
        out_adr = out_adr_2

    except IOError:
        print('file can\'t be opened')
        exit(0)

# 元画像の幅と高さを取得する
width, height = baseImg.size

# 新しいImageオブジェクトを作る
convertImg = Image.new('RGB', (width, height))

for y in range(height):
    for x in range(width):

        RGB_array = baseImg.getpixel((x, y))
        # getpixel(x,y)は左上を原点として列：x、行、yとしてカウントする。
        # RGB_arrayには（R,G,B）の三要素を持つ配列が入る。

        # print(RGB_array[0])
        # 画像によっては3要素の配列ではなく1要素になることがあり、エラーが発生することがある。(カラー画像においても)なぜ？→この問題は修正中

        gray = int((process(RGB_array[0], RGB_array[1], RGB_array[2])))

        # green mode ならグレースケールの値を4値化する
        if M == 1:
            if gray < 64:
                convertImg.putpixel((x, y), (7, 24, 33))  # #e0f8cf

            elif gray < 128:
                convertImg.putpixel((x, y), (48, 104, 80))  # #86c06c

            elif gray < 192:
                convertImg.putpixel((x, y), (134, 192, 108))  # #306850

            else:
                convertImg.putpixel((x, y), (229, 248, 207))  # #071821

        else:
            convertImg.putpixel((x, y), (gray, gray, gray,))

# 画像を保存して終了
convertImg.save(out_adr)
