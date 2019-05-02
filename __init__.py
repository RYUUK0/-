import sys
import os

ss = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ss)
print(BASE_DIR)
sys.path.append(BASE_DIR)