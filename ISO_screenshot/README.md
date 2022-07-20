# ISO_screenshot.exe
The program aims to assist ISO 27001 KPI.
## Usage
It measures the ISO 27001 KPI by taking screenshots of many applications as followings:

1. screen protection
2. app wizard
3. windows update
4. windows update history
5. time sync status
6. antivirus 

The CMD with your hostname and date information is shown as background when snapping the applications. The screenshots are saved in the ‘./<your hostname>’ by default.

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
```python
Pyinstaller -F -w main.py -n ISO_screenshot.exe
```

### Folder Directory 
```
├── build/
├── dist/
│   └── ISO_screenshot.exe
├── client.py   # program to call AWS
├── utils.py    # processing tools
└── main.py		# main program
```