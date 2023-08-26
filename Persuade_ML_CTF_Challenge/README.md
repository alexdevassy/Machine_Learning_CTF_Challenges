# Persuade ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to come up with a solution to extract the flag hosted inside the web server. 

![Alt text](Images/Banner.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench:

The challenge works best in `Ubuntu` systems with `Python 3.8.10`

Create virtual enviornment in python using `python -m venv virtualspace`

Activate the virtual enviornemnt `source /virtualspace/bin/activate`

`git clone https://github.com/alexdevassy/Machine_Learning_CTF_Challenges.git`

`cd Machine_Learning_CTF_Challenges/Persuade_ML_CTF_Challenge/`

`pip install -r .\requirements.txt`

`cd app/`

`python app.py`

Now the web application (AI Corp Sentiment Analyzer) can be accessed in host systems browser at http://127.0.0.1:5000/

<kbd>![Alt text](Images/Web_App.PNG?raw=true "Web_app")</kbd>

#### Rules :triangular_ruler: & Clues :monocle_face:
The machine in which CTF is deployed needs to have internet connectivity for downloading label mapping. 

For solution to CTF challenge visit : [Persuade_CTF_Solution](Solution/)
