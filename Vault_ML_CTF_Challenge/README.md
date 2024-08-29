# Vault ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to gain access to Vault and fetch Secret (Flag:) 

![Alt text](images/banner.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench:

Note: Before proceeding with either of below methods of setup, clone the repo using 

`git clone https://github.com/alexdevassy/Machine_Learning_CTF_Challenges.git` 

and then download model file from [here](https://drive.google.com/file/d/1lewMq93XrgZbjia3B7fBkMQfKSq_BAf7/view?usp=drive_link). Once the model file is downloaded place the same file in 

`cd Machine_Learning_CTF_Challenges\Vault_ML_CTF_Challenge/images/`

:hand: :exclamation: :exclamation: ***Challenge can be either installed via docker as docker image (Step1a) OR via native installation (Step1b)*** :no_entry_sign:

##### :point_right: Step 1a - Building Docker Image of the Application To Host The Challenge

`cd Machine_Learning_CTF_Challenges\Vault_ML_CTF_Challenge/`

`docker build -t vault_ml_ctf .`

To run the challenge `docker run --rm -p 5000:5000 vault_ml_ctf`

### OR

##### :point_right: Step 1b - Setting Up Python Flask App To Host The Challenge

The challenge works best with `Python 3.10.12`

Create virtual environment in python using `python -m venv virtualspace`

In windows, activate the virtual environment with `.\virtualspace\Scripts\activate`

In ubuntu, activate the virtual environment with `source /virtualspace/bin/activate`

`cd Machine_Learning_CTF_Challenges/Vault_ML_CTF_Challenge/`

`pip install -r .\requirements.txt` 

`python app.py`

Now the CTF Home Page :house_with_garden: can be accessed in host systems browser at http://127.0.0.1:5000/. Read :eyeglasses: through the page and click on "Start Breaking Vault" to start the CTF.

<kbd>![Alt text](images/home.PNG?raw=true "Web_app")</kbd>


#### Rules :triangular_ruler: & Clues :monocle_face:
Don't peak into app.py. Everything you need to conquer this CTF is neatly tucked away in the web application itself. :grin: 

For solution to CTF challenge visit : [Vault_CTF_Solution](Solution/)

:no_entry_sign: A quick heads-up: The video below contains CTF solution spoilers :sweat_smile:. So, if you're still up for the challenge and enjoy a bit of mystery, it might be best to steer clear of this one.  

https://github.com/user-attachments/assets/43831391-9238-4e49-9baf-f8ae55a7b023

