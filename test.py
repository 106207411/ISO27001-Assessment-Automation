from ctypes import util
import utils


def main():
    utils.show_desktop()
    # open the cmd in full screen
    cmd_hwnd, cmd_pid = utils.call_application(f'start cmd /k "hostname & date/t"')
    utils.maximize_window(cmd_hwnd)
    utils.snap_screen_protection()
    utils.snap_appwiz()
    
    # open windows settings
    utils.snap_windows_update_and_time_sync()

    # open antivirus
    utils.snap_antivirus()

    utils.__kill_task(cmd_pid)


if __name__ == "__main__":
    main()
