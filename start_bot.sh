#!/bin/bash
source /root/VideoDownloader/myenv/bin/activate
nohup python3 /root/VideoDownloader/main.py > /dev/null 2>&1 &
