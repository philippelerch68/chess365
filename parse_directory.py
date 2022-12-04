#!/usr/bin/env python
import os
from config import *
count = 0
files = sorted(os.listdir(games_dir), reverse=True)
for f in files:
    count+=1
    print(f"{count} {f}")
