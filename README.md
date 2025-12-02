# VibeTube
Totally Don't Use This in Production

Installation Guide (Maybe, Haven't Really Tested It, Good Luck >.<)
1. Install Python (Tested on 3.14 PI)
   <br> a. Windows: Download and Install (https://www.python.org/downloads/release/python-3140/)
   b1. *nix: sudo apt install python3
   b2. *nix: sudo yum install -y python3
   b3. *nix: Seriously, if the distro you are using doesn't have python and the above commands don't work then what are you doing with your life :(
3. Install MongoDB
   a. Windows: Download and install (https://www.mongodb.com/try/download/community)
   b. *nix: sudo apt install -y mongodb
4. Install Python Packages with Pip
   a. Windows: python -m pip install django pymongo pillow
   b. *nix: pip install django pymongo pillow
6. python manage.py migrate
7. python manage.py runserver
