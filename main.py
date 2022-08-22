# picovgm: Pico Vgmplayer for "SoundCortexChip by Toyoshima-san<toyoshim@gmail.com>"
# Copyright 2022, Layer8 https://twitter.com/layer812
# Licensed under the Apache License, Version 2.0
from machine import Pin, I2C
import time, os

#定数
I2c1_pinsda = 0  # PSG1用のSDA向け物理ピン
I2c1_pinscl = 1  # PSG1用のSCL向け物理ピン
I2c2_pinsda = 2  # PSG2個め or SSC用のSDA向け物理ピン
I2c2_pinscl = 3  # PSG2個め or SSC用のSCL向け物理ピン
I2c_freq = 3000000 #I2Cの周波数
Sample_delay = 23 # 1サンプル ≠ 23マイクロ秒 (1Msec/44.1K sample)
Num_loops = 3     # ループは1回 / 0にするとループしない

#グローバル変数です　（*´∀｀*）
Read_pointer = 0
Loop_offset = 0

def readvgmheader(data):
    global Read_pointer, Loop_offset
    if 'Vgm ' not in data[:4]: # Vgmファイルでなければスキップ
        return True
    # VGMデータ開始位置 Ver1.51以上ならヘッダの値、以下なら0x40
    Read_pointer = int.from_bytes(data[0x34:0x38], 'little') + 0x34 if int.from_bytes(data[0x08:0x0c], 'little') > 336 else 0x40
    Loop_offset  = int.from_bytes(data[0x1c:0x20], 'little') + 0x1c # Loopの再開位置
    return False                                   

def playvgmdata(vgm_data):
    global Read_pointer, Loop_offset, Num_loops, Sample_delay
    buff = bytearray(2)
    playcounter = Num_loops + 1 if Loop_offset > 0 and Num_loops > 0 else 1
    while playcounter > 0:
        sample_wait = 0
        vgm_command = vgm_data[Read_pointer]
        if vgm_command == 0xA0: # PSG
            if vgm_data[Read_pointer+1] < 0x80:
                i2c1.writeto(0x50, vgm_data[Read_pointer+1:Read_pointer+3])
            else:
                buff[0] = vgm_data[Read_pointer+1] - 0x80
                buff[1] = vgm_data[Read_pointer+2]
                i2c2.writeto(0x50, buff)
            Read_pointer += 3
        elif vgm_command == 0xD2: # Konami SSC
            if vgm_data[Read_pointer+1] == 0:
                buff[0] = vgm_data[Read_pointer+2]
            elif vgm_data[Read_pointer+1] == 1:
                buff[0] = vgm_data[Read_pointer+2] + 0xA0
            elif vgm_data[Read_pointer+1] == 2:
                buff[0] = vgm_data[Read_pointer+2] + 0xAA
            else:
                buff[0] = 0xAF
            buff[1] = vgm_data[Read_pointer+3]
            i2c2.writeto(0x51, buff)
            Read_pointer += 4
        elif vgm_command == 0x61:
            sample_wait = int.from_bytes(vgm_data[Read_pointer+1:Read_pointer+3], 'little')
            Read_pointer += 3 
        elif vgm_command == 0x62:
            sample_wait = 735
            Read_pointer += 1 
        elif vgm_command == 0x63:
            sample_wait = 882
            Read_pointer += 1 
        elif vgm_command == 0x66:
            playcounter -= 1
            Read_pointer = Loop_offset
        elif vgm_command >= 0x70 & vgm_command <= 0x7F:
            sample_wait = vgm_command - 0x70
            Read_pointer += 1 
        elif vgm_command < 0x51:
            Read_pointer += 2
            continue
        else:
            break;
        if sample_wait > 0:
            time.sleep_us(sample_wait * Sample_delay)
    #演奏終わったらミュート
    i2c2.writeto(0x51, bytearray([0xAF,0x00]))
    i2c1.writeto(0x50, bytearray([0x07, 0x3F]))
    i2c2.writeto(0x50, bytearray([0x07, 0x3F]))

# I2Cに使うピンを初期化
i2c1 = I2C(0, scl=Pin(I2c1_pinscl), sda=Pin(I2c1_pinsda), freq=I2c_freq)
i2c2 = I2C(1, scl=Pin(I2c2_pinscl), sda=Pin(I2c2_pinsda), freq=I2c_freq)
#main.pyと同じディレクトリにあるvgmファイルを全部再生
for file in os.listdir('/'):
    if ".vgm" not in file:
        continue
    with open(file, 'rb') as fr:
        vgm_data = fr.read()
        if readvgmheader(vgm_data):
            continue
        playvgmdata(vgm_data)
        del vgm_data
