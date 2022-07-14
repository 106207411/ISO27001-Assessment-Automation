import os
import time
import win32gui
import win32gui
import win32process
import win32con
from win32api import GetSystemMetrics, keybd_event
from PIL import ImageGrab


def find_window_by_pid(pid):
    result = None

    def callback(hwnd, _):
        nonlocal result
        ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
        if (cpid == pid) and win32gui.IsWindowVisible(hwnd):
            result = hwnd
            # print("Window name:", win32gui.GetWindowText(result))
            return
        return True
    try:
        win32gui.EnumWindows(callback, None)
    except:
        pass

    return result


def wait(seconds=1):
    time.sleep(seconds)


def move_window_to_center(hwnd):
    # left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # width = right - left
    # height = bottom - top
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    x = screen_width // 5
    y = 0
    win32gui.MoveWindow(hwnd, x, y, screen_width-x, screen_height-y, True)
    wait()


def maximize_window(hwnd):
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    wait()


def show_desktop():
    # https://docs.microsoft.com/zh-tw/windows/win32/inputdev/virtual-key-codes
    # https://blog.csdn.net/mcw_720624/article/details/116840459
    keybd_event(0x5B, 0, 0, 0)  # press left win key
    keybd_event(0x4D, 0, 0, 0)  # press M
    keybd_event(0x4D, 0, win32con.KEYEVENTF_KEYUP, 0)  # unpress M
    keybd_event(0x5B, 0, win32con.KEYEVENTF_KEYUP, 0)  # unpress left win key


def screenshot(name, path='./screenshots/'):
    mkdir_if_not_exist(path)
    screenshot = ImageGrab.grab()  # Take the screenshot
    screenshot.save(path+f'{name}.png', 'PNG')


def mkdir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_current_hwnd_pid():
    hwnd = win32gui.GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    return hwnd, pid

def call_cmd(commands):
    os.system(f'start cmd /k "{commands}"')
    wait()
    # get cmd window
    cmd_hwnd, cmd_pid = get_current_hwnd_pid()
    return cmd_hwnd, cmd_pid


def snap_screen_protection():
    os.system("start rundll32.exe shell32.dll,Control_RunDLL desk.cpl,,1")
    wait()
    # screen_protect_raw_str = os.popen("tasklist /M desk.cpl /FI \"IMAGENAME eq rundll32.exe\" /FO \"CSV\" ").read().replace('"', '')
    # screen_protect_pid = screen_protect_raw_str.strip().split("\n")[-1].split(",")[1] if 'PID' in screen_protect_raw_str else None
    # print("螢幕保護程式 PID： ", screen_protect_pid)
    # screen_protect_hwnd = find_window_by_pid(int(screen_protect_pid))

    screen_protect_hwnd, screen_protect_pid = get_current_hwnd_pid()
    snap_task(screen_protect_hwnd, "screen_protection")
    # kill screen protection
    kill_task(screen_protect_pid)


def snap_appwiz():
    # open 解除安裝程式
    os.system("control appwiz.cpl")
    wait()
    # get window
    appwiz_hwnd, appwiz_pid = get_current_hwnd_pid()
    snap_task(appwiz_hwnd, "app_wizard")
    kill_task(appwiz_pid)


def snap_task(hwnd, task_name):
    if task_name == "screen_protection":
        os.system("start rundll32.exe shell32.dll,Control_RunDLL desk.cpl,,1")
    elif task_name == "app_wizard":
        os.system("control appwiz.cpl")
    elif task_name == "task_manager":
        os.system("start taskmgr")

    # move_window_to_center(hwnd)
    # screenshot(task_name)


def kill_task(pid):
    os.system(f'taskkill /F /PID {pid}')
    wait()

