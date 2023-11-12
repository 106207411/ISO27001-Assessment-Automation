# ISO27001-Assessment-Automation
The program aims to assist ISO 27001 KPI assessment by taking screenshots of Windows applications and uploading them to AWS S3 bucket automatically.

![System Architecture](iso%20workflow_v2.drawio.jpg)

## Usage
### Step1: Take Screenshots
Targeted applications as followings:

1. screen protection
2. app wizard
3. windows update
4. windows update history
5. time sync status
6. antivirus 

The CMD with your hostname and date information is shown as background when snapping the applications. The screenshots are saved in the "./[YYYY-MM]/[yourhostname]/" by default.

### Step2: Upload to AWS
The program uploads the screenshots to AWS S3 bucket. It  creates a folder named by user hostname and date in the bucket. The folder structure in the bucket is shown as followings:
```bash
├── [YYYY-MM]/
│   ├── [user1hostname]/
│   │   ├── [app1].png
│   │   ├── [app2].png
│   │   ...  
│   └── [user2hostname]/
│       ├── [app1].png
│       ├── [app2].png
│       ...  
└── [YYYY-MM]/
    └── [user1hostname]/
        ├── [app1].png
        ├── [app2].png
        ...  
```

The bucket name and api credentials are defined in `./config.py` as followings:
```python
S3API = {'api_url': '',
         'api_key': '',
         'bucket_name': ''}
```

## How to run
Just right click on ISO_screenshot.exe and "Run as Administrator".
## How to build exe
### Environment
Using Anaconda to create a new virtual python environment is highly recommended.
```
conda create -n <env_name> python=3.6
```
### Required modules
```bash
pip3 install -r requirement.txt
```
### Build exe by Pyinstaller

Reduce the size of exe: https://damn99.com/2020-06-13-python-in-exe/

```bash
Pyinstaller -F -w main.py -n ISO_screenshot.exe
```

### Project Folder Directory 
```bash
├── build/
├── dist/
│   └── ISO_screenshot.exe
├── client.py   # program to call AWS
├── utils.py    # processing tools
├── config.py   # AWS configuration
└── main.py		# main program
```