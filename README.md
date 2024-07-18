# DirEventWatcher
Extremely simple script written in half an hour for automating 
Google SMTP request for file changes.

Script is intended for my personal use of sending email alerts regarding file creations to 
FTP server from an intentionally misconfigured security camera to prevent
Internet access but allow LAN access.

This script is helpful for receiving activity alerts for untrusted
cameras such as those created internationally or have a history of poor network security without exposing the camera to the Internet.

# Requirements
1. Python 3 (tested on Python 3.11)
2. Windows 10/11

# How to run
1. Run ```run.bat```

# Configuration
Edit the following lines with a text editor or an IDE.
For app passwords, see https://support.google.com/accounts/answer/185833?hl=en
https://github.com/Jeffchen54/DirEventWatcher/blob/afd26623e051ba19782951d9a1a6885e79980180/dirEventWatcher.py#L26-L35

# Implementation
- ```run.bat``` creates and executes files in venv.

# Notice
1. You may need to modify your AV/firewall if you are receiving

   ```ConnectionAbortedError(10053, 'An established connection was aborted by the software in your host machine', None, 10053, None)```
