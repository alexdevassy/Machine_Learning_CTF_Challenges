# Heist ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to compromise CityPolice's AI cameras and secure a smooth escape for Heist crews red getaway car :red_car: after the heist.

![Alt text](Images/Banner.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench:

:hand: :exclamation: :exclamation: ***Challenge can be either installed via docker as docker image (Step1a) OR via native installation (Step1b)*** :no_entry_sign:

##### :point_right: Step 1a - Building Docker Image of the Application To Host The Challenge

clone the repo using `git clone https://github.com/alexdevassy/Machine_Learning_CTF_Challenges.git`

`cd Machine_Learning_CTF_Challenges\Heist_ML_CTF_Challenge/`

`docker build -t heist_ml_ctf .`

To run the challenge `docker run --rm -p 49154:49154 heist_ml_ctf`

### OR

##### :point_right: Step 1b - Setting Up Python Flask App To Host The Challenge

The challenge works best with `Python 3.10.11`

Create virtual enviornment in python using `python -m venv virtualspace`

In windows, activate the virtual environment with `.\virtualspace\Scripts\activate`

In ubuntu, activate the virtual environment with `source /virtualspace/bin/activate`

`git clone https://github.com/alexdevassy/Machine_Learning_CTF_Challenges.git`

`cd Machine_Learning_CTF_Challenges/Heist_ML_CTF_Challenge/`

`pip install -r .\requirements.txt`

`python app.py`

Now the CTF Home Page :house_with_garden: can be accessed in host systems browser at http://127.0.0.1:49154/CTFHomePage. Read :eyeglasses: through the page and click on "Start Challenge" to start the CTF.

<kbd>![Alt text](Images/CTFHomePage.PNG?raw=true "Web_app")</kbd>


#### Rules :triangular_ruler: & Clues :monocle_face:
Dont peak into app.py. Everything you need to conquer this CTF is neatly tucked away in the web application itself. :grin: In case if the application throws unexpected errors or behaves in weird way, use 'Reset' button to reset the CTF challene to its initial state. 

For solution to CTF challenge visit : [Heist_CTF_Solution](Solution/)

:no_entry_sign: A quick heads-up: The video below is contains CTF solution spoilers :sweat_smile:. So, if you're still up for the challenge and enjoy a bit of mystery, it might be best to steer clear of this one.  



https://github.com/alexdevassy/Machine_Learning_CTF_Challenges/assets/31893005/94dbe135-500c-46b0-8db9-684a2d647aef


