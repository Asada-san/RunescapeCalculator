# RunescapeCalculator
Runescape revo calculator

A website for calculating the Average Ability Damage Per Tick (AADPT) of any revolution bar.

Feel free to use the code for whatever.

If there is anything wrong please send me a message on reddit u/FTWmickyWTF

1) Download and extract the source from GitHub: https://github.com/Asada-san/RunescapeCalculator
 
2) Open a command prompt in the directory created above
 
3) Run these commands:
    python -m venv api\venv
    api\venv\Scripts\activate.bat
    python -m pip install -r requirements.txt
 
   If you get an error about "No module named pip", your Python install is borked.
   See: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
   Otherwise, wait for pip to download and install everything.
 
4) NOTE: As of the latest Jun 24 2022 commit, there is an error in the code that references an unused file that was never added to GitHub. This step prevents the calc from trying to load that file.
4a) Open the file `webapp\src\components\SideBar.vue` in a text editor.
4b) Prepend line 34 with two forward slashes:
    //import AbilRot from './AbilRot.vue'
4c) Prepend line 70 with two forward slashes:
    //    AbilRot,
4d) Close and save the Sidebar.vue file.
 
5) NOTE: Additional problem, the calc doesn't auto-create the database file to store the counter, easiest way to get it is from the previous release on GitHub.
5a) Download: https://github.com/Asada-san/RunescapeCalculator/archive/refs/tags/v1.06.1.zip
5b) From that .zip archive, extract `RuneScapeCalculator-1.06.1\App\db.sqlite3`
5c) Place that file at `api\App\db.sqlite3` in the folder you created from step 1.
 
6) Run the following commands in the command prompt window opened in step 2:
    set PYTHONPATH=.
    set DATABASE_URL=sqlite:///db.sqlite3
    set SECRET_KEY=a618c71bc7605c466bf47d817f843531
    python api\wsgi.py
 
    Explanation: In order, each of the above set commands:
        - Configures Python to look in the current directory for new modules
        - Tells the calc app to load the database you extracted during step 5
        - Sets a "secret key" used for "security"
            - (probably only meaningful if you were exposing this to the public rather than testing locally)
 
7) You should be done. Go to http://localhost:5000/ and the calc should work. (Or it might not.)