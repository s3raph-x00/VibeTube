# VibeTube
**!!!Totally Don't Use This in Production!!!**
<br>
## What this is:
I got bored, and this is a crappy project to replicate a videoplayer-like service that is minimalistic.
<br> It does have some basic functionality like Loop, Shuffle, and Playlists but that is about it.
<br> 
<br> ## Installation Guide 
<br> (*Maybe, Haven't Really Tested The Install Guide, Good Luck >.<*)
1. Install Python (Tested on 3.14)
   > a. Windows: Download and Install (https://www.python.org/downloads/release/python-3140/)
   <br> b0. *nix: sudo apt install python3
   <br> b1. *nix: sudo yum install -y python3
   <br> b2. *nix: Serious Talk, if the distro you are using doesn't have python and the above commands don't work then what are you doing with your life :(
2. Install MongoDB
   > a. Windows: Download and install (https://www.mongodb.com/try/download/community)
   <br> b0. *nix: sudo apt install -y mongodb
   <br> b1. *nix: sudo yum install -y mongodb-org (Follow Here to Add Repo: https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-red-hat/)
3. Install Python Packages with Pip
   > a. Windows: python -m pip install django pymongo pillow
   <br> b. *nix: pip install django pymongo pillow
4. Install FFmpeg (This Part is *optional* but **recommended** because this provides the functionality for the thumbnail creation):
   > a. Windows: Download and store FFmpeg.exe in the same directory as manage.py (https://www.gyan.dev/ffmpeg/builds/)
   <br> b0. *nix: sudo apt-get install ffmpeg
   <br> b1. *nix: https://ffmpeg.org/download.html
6. Modify ./vibetube/settings.py as needed (Video Directory and Django Secret Key)
7. python manage.py migrate
8. python manage.py runserver
