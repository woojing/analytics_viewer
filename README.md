# Analytics Viewer
Tool for Google Analytics console log view

## Requirements
This tools just helper for increase readability of raw log format.
So you have to install native tools for getting raw logs.

### On Windows
1. adb
  - http://forum.xda-developers.com/showthread.php?p=48915118#post48915118
  - you can get simple Windows adb installer in above link
2. Android device driver for few venders
  - if adb cannot found your device then trying this.
  - or check your USB cable
3. python3
  - https://www.python.org/downloads/

### On MacOSX
1. brew
  - this is not directly related. but it make your life very easy.
  - http://brew.sh
  - or just use this `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
2. adb
  - `brew install android-platform-tools`
3. idevicesyslog
  - `brew install libimobiledevice`
4. python3
  - `brew install python3`

## How to use it?
Just download and type this
`python3 run.py`
