
import  subprocess
import sys

if __name__=="__main__":
    while True:
       try:
            subprocess.call([sys.executable,"bot.py"])
       except Exception:
           continue