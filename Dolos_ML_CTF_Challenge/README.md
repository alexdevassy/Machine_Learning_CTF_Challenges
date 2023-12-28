# Dolos ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to think like Greek god DOLOS and trick the LLM to reveal the flag. 

![Alt text](Images/Banner1.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench: 

##### Step 1 - Getting API Keys

For hosting this challege, 2 API Keys are required.

1. ReBuff: Head to [Rebuff Playground](https://playground.rebuff.ai/), Sign in with Google Account and scroll down to view the API Key. 

2. Openai: Sign into [Openai Platform](https://platform.openai.com/playground), access API Keys section and create keys. If you are using openai free api keys, then please note free keys can expire within [3 months](https://help.openai.com/en/articles/4936830-what-happens-after-i-use-my-free-tokens-or-the-3-months-is-up-in-the-free-trial). 

##### Step 2 - Setting Up Python Flask App To Host The Challenge

The challenge works best in `Ubuntu` systems with `Python 3.8.10`

Create virtual enviornment in python using `python -m venv virtualspace`

Activate the virtual enviornemnt `source /virtualspace/bin/activate`

`git clone https://github.com/alexdevassy/Machine_Learning_CTF_Challenges.git`

`cd Machine_Learning_CTF_Challenges/Dolos_ML_CTF_Challenge/`

`pip install -r .\requirements.txt` 

`python3 app.py --rebuffkey="<REBUFF_API_KEY>" --openaikey="<OPENAI_API_KEY>"`

Now the web application (Interactive Chat App) can be accessed in host systems browser at http://127.0.0.1:5000/

<kbd>![Alt text](Images/Web_App.PNG?raw=true "Web_app")</kbd>

#### Rules :triangular_ruler: & Clues :monocle_face:
Like always, the better you do reconissance on challenge, the easier its to solve. Otherwise you may run into rabbit holes pretty quickly.

For solution to CTF challenge visit : [Dolos_CTF_Solution](Solution/)
