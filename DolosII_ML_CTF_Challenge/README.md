# Dolos II ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to think like Greek god DOLOS and trick the LLM to reveal the flag. 

![Alt text](Images/Banner1.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench: 

##### :point_right: Step 1 - Getting API Keys

For hosting this challege, openai API key is required.

1. Openai: Sign into [Openai Platform](https://platform.openai.com/playground), access API Keys section and create keys. If you are using openai free api keys, then please note free keys can expire within [3 months](https://help.openai.com/en/articles/4936830-what-happens-after-i-use-my-free-tokens-or-the-3-months-is-up-in-the-free-trial). 

:hand: :exclamation: :exclamation: ***Step 2 can be either building the docker image of application (Step2a) OR setting up the application in local machine (Step2b).*** :no_entry_sign:

##### :point_right: Step 2a - Building Docker Image of the Application To Host The Challenge

`cd Machine_Learning_CTF_Challenges/DolosII_ML_CTF_Challenge/`

`docker build -t dolosll_ml_ctf .`

To run the challenge `docker run --rm -p 49153:49153 -ti dolosll_ml_ctf  --openaikey="<OPENAI_API_KEY>"`

### OR

##### :point_right: Step 2b - Setting Up Python Flask App To Host The Challenge

The challenge works best in `Ubuntu` systems with `Python 3.8.10`

Create virtual enviornment in python using `python -m venv virtualspace`

Activate the virtual enviornemnt `source /virtualspace/bin/activate`

`git clone https://github.com/alexdevassy/Machine_Learning_CTF_Challenges.git`

`cd Machine_Learning_CTF_Challenges/DolosII_ML_CTF_Challenge/`

`pip install -r .\requirements.txt` 

`python3 app.py --openaikey="<OPENAI_API_KEY>"`

Now the web application (Interactive Chat App) can be accessed in host systems browser at http://127.0.0.1:49153/

<kbd>![Alt text](Images/Web_App.PNG?raw=true "Web_app")</kbd>

#### Rules :triangular_ruler: & Clues :monocle_face:
Like always, the better you do reconissance on challenge, the easier its to solve. Otherwise you may run into rabbit holes pretty quickly.

Dont peek :eyes: into the source code and logs from server are only for debugging purposes dont let them spoil your CTF experience.

For solution to CTF challenge visit : [DolosII_CTF_Solution](Solution/)

