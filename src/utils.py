import os
import time
import win32gui
from win32process import GetWindowThreadProcessId
from win32con import SW_MAXIMIZE, KEYEVENTF_KEYUP
from win32api import GetSystemMetrics, keybd_event
from PIL import ImageGrab
from datetime import datetime


def wait(seconds : int =1.5) -> None:
    time.sleep(seconds)


def move_window_to_center(hwnd, resize=True):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    x = screen_width // 5
    y = 0
    if resize:
        win32gui.MoveWindow(hwnd, x, y, screen_width-x, screen_height-y, True)
    else:
        win32gui.MoveWindow(hwnd, x, y, width, height, True)
    wait(1)


def maximize_window(hwnd):
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, SW_MAXIMIZE)
    wait()


def show_desktop():
    # https://docs.microsoft.com/zh-tw/windows/win32/inputdev/virtual-key-codes
    # https://blog.csdn.net/mcw_720624/article/details/116840459
    keybd_event(0x5B, 0, 0, 0)  # press left win key
    keybd_event(0x4D, 0, 0, 0)  # press M
    keybd_event(0x4D, 0, KEYEVENTF_KEYUP, 0)  # unpress M
    keybd_event(0x5B, 0, KEYEVENTF_KEYUP, 0)  # unpress left win key


def get_save_dir():
    hostname = os.popen("hostname").read().strip()
    time = datetime.today().strftime('%Y-%m')
    return os.path.join(time, hostname)


def screenshot(name, path=get_save_dir()):
    mkdir_if_not_exist(path)
    screenshot = ImageGrab.grab()  # Take the screenshot
    screenshot.save(os.path.join(path, f'{name}.png'), 'PNG')


def mkdir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_current_hwnd_pid():
    hwnd = win32gui.GetForegroundWindow()
    pid = GetWindowThreadProcessId(hwnd)[1]
    return hwnd, pid


def call_application(commands):
    """call application on windows system"""
    result = os.system(commands)
    if result != 0:
        raise Exception("call application failed")

    wait()
    # get window handle and pid
    cmd_hwnd, cmd_pid = get_current_hwnd_pid()
    return cmd_hwnd, cmd_pid


def snap_screen_protection():
    os.system("start rundll32.exe shell32.dll,Control_RunDLL desk.cpl,,1")
    wait()
    # screen_protect_raw_str = os.popen("tasklist /M desk.cpl /FI \"IMAGENAME eq rundll32.exe\" /FO \"CSV\" ").read().replace('"', '')
    # screen_protect_pid = screen_protect_raw_str.strip().split("\n")[-1].split(",")[1] if 'PID' in screen_protect_raw_str else None
    # print("螢幕保護程式 PID： ", screen_protect_pid)
    # screen_protect_hwnd = find_window_by_pid(int(screen_protect_pid))
    __snap_and_kill_task("screen_protection", task_resize=False)


def snap_appwiz():
    # open 解除安裝程式
    os.system("control appwiz.cpl")
    wait()
    # get window
    __snap_and_kill_task("app_wizard")


def snap_windows_update_and_time_sync():
    # open windows update
    winup_hwnd, winup_pid = call_application('start ms-settings:windowsupdate')
    move_window_to_center(winup_hwnd)
    screenshot("windows_update")
    # open windows update history
    winup_hist_hwnd, winup_hist_pid = call_application('start ms-settings:windowsupdate-history')
    wait(1)
    screenshot("windows_update_history")

    # open date and time
    datetime_hwnd, datetime_pid = call_application('start ms-settings:dateandtime')
    wait(1)
    screenshot("time_sync")
    __kill_task(datetime_pid)


def snap_antivirus():
    try:
        # antivirus_path = "C:\Program Files\Avast Software\Avast\AvastUI.exe"
        antivirus_path = "C:\Program Files (x86)\Trend Micro\OfficeScan Client\PccNt.exe"
        antiv_hwnd, antiv_pid = call_application(f'start "" "{antivirus_path}"')
    except Exception as e:
        print(e)
    else:
        wait(3)
        __snap_and_kill_task("antivirus")


def __snap_and_kill_task(task_name, task_resize=True):
    hwnd, pid = get_current_hwnd_pid()
    move_window_to_center(hwnd, task_resize)
    screenshot(task_name)
    __kill_task(pid)


def __kill_task(pid):
    os.system(f'taskkill /F /T /PID {pid}')
    wait()


def upload_images_to_s3(client, bucket_name, img_dir=get_save_dir()):
    if not os.path.exists(img_dir):
        return
    fname_list = [fname for fname in os.listdir(img_dir) if fname.endswith('.png')]
    for fname in fname_list:
        fpath = os.path.join(img_dir, fname)
        data = open(fpath, 'rb').read()
        object_key = fpath.replace("\\", "%2F")
        client.upload_files(bucket_name=bucket_name,
                            object_key=object_key,
                            data=data)

# This function is deprecated
# def find_window_by_pid(pid):
#     result = None
#     def callback(hwnd, _):
#         nonlocal result
#         ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
#         if (cpid == pid) and win32gui.IsWindowVisible(hwnd):
#             result = hwnd
#             # print("Window name:", win32gui.GetWindowText(result))
#             return
#         return True
#     try:
#         win32gui.EnumWindows(callback, None)
#     except:
#         pass
#     warnings.warn("It is a develop method", DeprecationWarning)
#     return result
