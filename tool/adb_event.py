from config import adb, device_name, resolution

import os
import subprocess
import re


def connect_device():
    if '.' in device_name: os.system(f'{adb} connect {device_name}')
    print(f'connect device event => connect {device_name}')

def open_app(appPackage,boss_appActivity):
    os.system(f"{adb} shell am start -n {appPackage}/{boss_appActivity}")
    print(f"start app event => start {appPackage}")

def stop_app(appPackage):
    os.system(f"{adb} shell am force-stop {appPackage}")
    print(f"stop app event => stop app {appPackage}")

def tap(x,y):
    os.system(f"{adb} shell input tap {x} {y}")
    print(f"tap event => tap ({x},{y})")

def horizon_swipe(switcher=False,duration=200):
    x_bias = -500
    if switcher: x_bias = 500
    x1 = resolution[0] / 2
    y1 = resolution[1] / 2
    os.system(f"{adb} shell input swipe {x1} {y1} {x1 + x_bias} {y1} {duration}")

# 沿着边缘滑动，防止误触
def edge_scroll(y,slow_down=False,duration=500):
    # 向上滑动y为负数，向下滑动y为正数，即模拟手指上滑为负，手指下滑为正
    x1 = resolution[0]
    y1 = resolution[1]
    if slow_down: y += y1
    os.system(f"{adb} shell input swipe {x1} {y1} {x1} {y} {duration}")
    print(f"center scroll event => scroll to {x1} {y1+y}")

def screenshot():
    os.system(f'{adb} exec-out screencap -p > ./screenshot.png')
    print(f"screenshot event => ./screenshot.png")

def input_text(text):
    os.system(f"{adb} shell am broadcast -a ADB_INPUT_TEXT --es msg '{text}'")
    print(f"input text event => {text}")

def get_clipboard():
    result = subprocess.check_output(
        f"{adb} shell am broadcast -a clipper.get",
        shell=True
    )
    print('get clipboard event => success')
    return re.search(r'data="(.*?)"', result.decode('utf-8')).group(1)

def adbkeyboard_install():
    os.system(f"{adb} install ./apk/ADBKeyboard.apk")
    os.system(f"{adb} shell ime enable com.android.adbkeyboard/.AdbIME")
    print('adbkeyboard install event => success')

def clipper_install():
    os.system(f"{adb} install ./apk/clipper.apk")
    print('clipper install event => success')

def switch_to_adbkey():
    os.system(f"{adb} shell ime set com.android.adbkeyboard/.AdbIME")
    print('switch to adbkeyboard event => success')

def switch_off_adbkey():
    os.system(f"{adb} shell ime set com.nuance.swype.dtc/com.nuance.swype.input.IME")
    print('switch off adbkeyboard event => success')

def switch_to_clipper():
    os.system(f"{adb} shell am startservice ca.zgrs.clipper/.ClipboardService")
    print('switch to clipper event => success')

def switch_off_clipper():
    os.system(f"{adb} shell am force-stop ca.zgrs.clipper")
    print('switch off clipper => success')
