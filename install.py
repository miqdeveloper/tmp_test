from os import system 

try:
  system("sudo pip install -U https://github.com/iqoptionapi/iqoptionapi/archive/refs/heads/master.zip")
  system("sudo pip install -r requirements.txt && sudo pip install websocket-client==0.56 ")
  system("sudo python3 start_bot.py")
except Exception as e:
    print("Error", e)