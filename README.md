# ISO_screenshot.exe

## Usage
The program aims to assist ISO 27001 KPI.
It screenshots many applications as screen protection, app wizard, windows update, windows update history, time sync status, and antivirus. The CMD with your hostname and date information is shown as background when snapping the applications.
## How to run
Just right click on ISO_screenshot.exe and "Run as Administrator".
## How to build exe
### Environment
Using Anaconda to create a new virtual python environment is highly recommended.
```
conda create -n <env_name> python=3.6.13
```
### Required modules
```bash
pip3 install -r requirement.txt
```
### Build exe by Pyinstaller
```python
Pyinstaller -F -w ISO_screenshot.py
```

### Folder Directory 
```
├── build/
├── dist/
│   └── ISO_screenshot.exe    
└── ISO_screenshot.py
```