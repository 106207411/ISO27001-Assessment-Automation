import utils
import os
import win32gui, time, win32process, win32gui
from pywinauto import Application, mouse


def main():
    utils.show_desktop()
    # open the cmd in full screen
    cmd_hwnd, cmd_pid = utils.call_cmd("hostname & date/t")
    utils.maximize_window(cmd_hwnd)
    utils.snap_screen_protection()
    utils.snap_appwiz()
    
    # open windows update settings using pywinauto
    os.system('control desk.cpl')
    time.sleep(1)
    setup_hwnd = win32gui.GetForegroundWindow()
    setup_pid = win32process.GetWindowThreadProcessId(setup_hwnd)[1]
    utils.maximize_window(setup_hwnd)
    
    # using inspect.exe and ```setup_window.print_control_identifiers()``` to see the control identifiers of the window
    app = Application(backend="uia").connect(handle=setup_hwnd)
    setup_window = app.window(class_name="ApplicationFrameWindow", control_type="Window")
    # click on the "Windows Update" ItemList
    # https://github.com/pywinauto/pywinauto/issues/653
    setup_window.ListItem11.click_input()
    time.sleep(1)
    utils.snap_task(setup_hwnd, "windows_update")
    setup_window.child_window(auto_id="SystemSettings_MusUpdate_UpdateHistoryLink_ButtonEntityItem", control_type="Group").click_input()
    time.sleep(1)
    utils.snap_task(setup_hwnd, "windows_update_history")
    setup_window.ListItem7.click_input()
    time.sleep(1)
    setup_window.ListItem12.click_input()
    time.sleep(1)

    # scroll down the window
    left, top, right, bottom = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
    x, y = (left+right)//2, (top+bottom)//2
    mouse.scroll(coords=(x, y), wheel_dist=-10)
    utils.snap_task(setup_hwnd, "time_sync")
    utils.kill_task(setup_pid)   


    app = Application(backend="uia").start("C:\Program Files\Avast Software\Avast\AvastUI.exe")

    utils.kill_task(cmd_pid)


# os.system("start cmd /k \"hostname & date/t\"")
# time.sleep(1)
# # get process id of cmd
# """My computer uses WindowsTerminal.exe as the terminal emulator.
# The default terminal emulator is cmd.exe."""
# cmd_task_list_str = os.popen("tasklist /FI \"IMAGENAME eq WindowsTerminal.exe\" /FO \"CSV\"").read().replace('"', '')
# cmd_task_list_str = os.popen("tasklist /FI \"IMAGENAME eq cmd.exe\" /FO \"CSV\"").read().replace('"', '')
# cmd_pid = cmd_task_list_str.strip().split("\n")[-1].split(",")[1] if 'PID' in cmd_task_list_str else None
# print("Terminal ID:", cmd_pid)
# # get the hwnd of cmd
# cmd_hwnd = find_window_by_pid(int(cmd_pid))
# os.system(f'taskkill /F /PID {cmd_pid}')

if __name__ == "__main__":
    main()
