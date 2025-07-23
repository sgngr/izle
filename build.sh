#!/bin/bash
# pyinstaller --onefile  --collect-all PIL --add-data "izle.png:img"  --add-data "icons/sync.svg:icons"    --icon="izle.png"  izle.py
pyinstaller --onefile  --collect-all PIL --add-data "izle.png:img"   izle.py
