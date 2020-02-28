#### If Windows:

Install Anaconda -> https://www.anaconda.com/download/
Run script with anaconda (I Newer use anaconda always use jupyter notebook please read about Anaconda)

#### If Linux:
create virtual environment(command is -> python3 -m venv <venvname>)
where <venvname> it is name of virtual environment.
next -> use command pip install -r requirements.txt
next -> put file with name (timelog.csv this file nead get from tracker (http://tracker.vidnt.com/time_entries?f%5B%5D=spent_on&f%5B%5D=&op%5Bspent_on%5D=lm)) to dir (it is a same dir where script time_counting.py located)
next -> use command -> python time_counting.py
next -> enter a full dir path and press Enter or just pres Enter
next -> If you see the "Finish" in dir where script located(or in dir you enter on a previous step) will be create a new dir with name "Time_log" inside you find a one more dir with .xlsx files inside.

