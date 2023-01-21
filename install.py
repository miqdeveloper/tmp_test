from os import system 

try:
  system("sudo pip install -U https://github.com/iqoptionapi/iqoptionapi/archive/refs/heads/master.zip")
  system("sudo git clone -b master https://github.com/miqdeveloper/tmp_test.git")
  system("cd tmp_test && sudo pip install -r requirements.txt")
  system("sudo python3 start_bot.py")
except Exception as e:
    print("Error", e)