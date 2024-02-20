import os, re
import shutil
import socket
import subprocess
import time

import environment_variable as env

command_dict = {
    '点亮屏幕': 'adb shell input keyevent 224',
    '下载睿博士录像': f'adb pull {env.p6slite_videos} {env.adb_download}',
    '清空睿博士录像': f"adb shell rm {env.p6slite_videos}* ",
    '下载相册': f'adb pull {env.photo_album} {env.adb_download}',
    '获取安卓版本': 'adb shell getprop ro.build.version.release',
    '获取手机分辨率': 'adb shell wm size',
    '滑屏解锁': 'adb shell input swipe 300 1000 300 500',
    '密码解锁': 'adb shell input text password',
    '下载睿博士截图': f'adb pull {env.ruibo_screenshot_path} {env.adb_download}',
    '清空睿博士截图': f'adb shell rm {env.ruibo_screenshot_path}*',
    '下载手机截屏': f'adb pull {env.mobile_screen_capture} {env.adb_download}',
    '下载示例图片': f'adb pull {env.pictures} {env.adb_download}',
    '手机截屏': f'adb shell screencap -p {env.mobile_screen_capture}screenshot.png',
    '打开直播隐藏菜单': 'adb shell input tap 500 500'

}


def wakeUpScreen():
    # 点亮屏幕
    # os.system("adb shell input keyevent KEYCODE_POWER")
    os.system('adb shell input keyevent 224')


def unlockScreen():
    pass


def is_foreground(package_name):
    # 判断app是否为前台运行
    command = "adb shell \"dumpsys window | grep mCurrentFocus\""
    all_info = os.popen(command).readlines()
    # print(all_info)
    if package_name in all_info[0]:
        return True
    return False


def popen(command):
    return os.popen(command_dict[command]).readlines()[0]


def get_screen_resolution():
    """获取手机屏幕分辨率"""
    result = popen('获取手机分辨率')
    devices_name = re.findall('\d{3,4}', result, re.S)
    devices_name = (eval(devices_name[0]), eval(devices_name[1]))
    return devices_name


# 检查手机是否已连接
def check_device_connection():
    try:
        adb_devices = subprocess.check_output('adb devices', shell=True, universal_newlines=True)
        if not re.search(r'^\S+\tdevice$', adb_devices, flags=re.MULTILINE):
            return False
    except subprocess.CalledProcessError:
        return False
    return True


# 检查appuim服务器端口
def check_appium_server(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', port))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return True
    except ConnectionRefusedError:
        return False


# 启动app
def start_app(package_name='', activity_name=''):
    # 停止应用程序
    stop_cmd = f'adb shell am force-stop {package_name}'
    subprocess.run(stop_cmd, shell=True)

    # 暂停一段时间，确保应用程序已停止
    time.sleep(2)

    # 启动应用程序
    start_cmd = f'adb shell am start -n {package_name}/{activity_name}'
    subprocess.run(start_cmd, shell=True)

    # 暂停一段时间，以确保应用程序已启动
    time.sleep(15)

    # 检查应用程序是否在前台运行
    if not is_foreground(package_name):
        # 应用程序在前台无法运行，报错退出
        raise RuntimeError(f'Failed to bring app {package_name} to foreground')

    print(f'{package_name} 启动成功！')


def get_audio_logs():
    # 使用 adb 命令获取音频输入信息
    result = subprocess.check_output("adb shell dumpsys audio", shell=True).decode()
    # 在音频输入信息中查找 "source: default"
    return result


def remove_path(path):
    """
    删除指定路径及其所有子文件和子文件夹

    Args:
        path: 要删除的路径

    Returns:
        None
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        print(f"已删除路径：{path}")
    else:
        print(f"指定路径不存在：{path}")


def pinch_zoom(start, end, scale_factor=2.0, press_duration=500):
    start_x, start_y = start
    end_x, end_y = end

    # 模拟第一根手指按下屏幕
    os.system(f"adb shell input touchscreen tap {start_x} {start_y}")

    # 模拟第二根手指按下屏幕并滑动到位置
    x1, y1 = (end_x, end_y)
    x2, y2 = (int(x1 + (scale_factor - 1) * 50), int(y1))
    os.system(f"adb shell input touchscreen tap {x1} {y1} && adb shell input touchscreen swipe {x1} {y1} {x2} {y2} {int(press_duration / 2)}")

    # 模拟两个手指同时离开屏幕
    os.system(f"adb shell input touchscreen tap {x1} {y1} && adb shell input touchscreen tap {start_x} {start_y}")
    time.sleep(1)
    os.system(f"adb shell input touchscreen tap {start_x} {start_y}")


if __name__ == "__main__":
    # 重启appd
    # start_app('com.zwcode.p6slite', '.activity.SplashActivity')
    # os.system(command_dict['下载示例图片'])
    os.system(command_dict['下载睿博士录像'])
    # # pinch_zoom((400,1065),(600,1065))
    # # print(get_screen_resolution())
    # # os.system(command_dict['下载睿博士录像'])
    # print(is_foreground('com.cmri.universalapp'))