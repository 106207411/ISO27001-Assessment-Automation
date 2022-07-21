import utils
from cfg import S3API
from client import S3Client

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

    # upload screenshots to S3
    client = S3Client(api_url=S3API['api_url'], api_key=S3API['api_key'])
    utils.upload_images_to_s3(client=client, bucket_name=S3API['bucket_name'])

    utils.__kill_task(cmd_pid)

if __name__ == "__main__":
    main()
