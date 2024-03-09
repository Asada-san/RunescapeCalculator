# RunescapeCalculator
Runescape revo calculator

A website for calculating the Average Ability Damage Per Tick (AADPT) of any revolution bar.

Feel free to use the code for whatever.

If there is anything wrong please send me a message on reddit u/FTWmickyWTF

1) Install node v18 https://nodejs.org/download/release/latest-v18.x/ and python v3.9.6 https://www.python.org/downloads/release/python-396/

2) Download and extract the source from GitHub: https://github.com/Asada-san/RunescapeCalculator
 
3) Open a command prompt in the directory created above
 
4) Run these commands:
    python -m venv api\venv
    api\venv\Scripts\activate.bat
    python -m pip install -r requirements.txt
 
   If you get an error about "No module named pip", your Python install is borked.
   See: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
   Otherwise, wait for pip to download and install everything.
 
5) Run the following commands in the command prompt window opened in step 2:
    set PYTHONPATH=.
    set DATABASE_URL=sqlite:///db.sqlite3
    set SECRET_KEY=a618c71bc7605c466bf47d817f843531
    python api\wsgi.py
 
    Explanation: In order, each of the above set commands:
        - Configures Python to look in the current directory for new modules
        - Tells the calc app to load the database you extracted during step 5
        - Sets a "secret key" used for "security"
            - (probably only meaningful if you were exposing this to the public rather than testing locally)
 
6) You should be done. Go to http://localhost:5000/ and the calc should work. (Or it might not.)