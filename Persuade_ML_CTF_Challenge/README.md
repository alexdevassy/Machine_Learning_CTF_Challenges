# Persuade ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to come up with a solution to extract the flag hosted inside the web server. 

![Alt text](Images/Banner.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench:

To setup the challenge, its a 2 step process. 

##### :point_right: Step 1 - Downloading The Model

Lets head into the Google colab and execute below code block in a new notebook.

```python
#Note: This code works well in Google Colab
  
!pip install -q torch==2.0.1
!pip install -q transformers==4.31.0
!pip install -q scipy==1.11.1

import torch
import os
from transformers import AutoModelForSequenceClassification

# Save a model for sentiment analysis
model_directory = "SavedModels"
if not os.path.isdir(model_directory):
    os.mkdir(model_directory)

safe_model_path = os.path.join(model_directory, "saved_model.pt")

task = "sentiment"
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
torch.save(model,safe_model_path)
```
From colab, download the saved_model.pt to local system.

Now lets clone the repo using `git clone https://github.com/alexdevassy/Machine_Learning_CTF_Challenges.git`

Make Uploads folder in app directory to host the model file `mkdir uploads`. Copy saved_model.pt to uploads folder. 

`Machine_Learning_CTF_Challenges/Persuade_ML_CTF_Challenge/app/uploads/saved_model.pt`

:hand: :exclamation: :exclamation: ***Step 2 can be either building the docker image of application (Step2a) OR setting up the application in local machine (Step2b).*** :no_entry_sign:

##### :point_right: Step 2a - Building Docker Image of the Application To Host The Challenge

`cd Machine_Learning_CTF_Challenges/Persuade_ML_CTF_Challenge/`

`docker build -t persuade_ml_ctf .`

To run the challenge `docker run --rm --expose=9000 -p 9000:9000 -p 5000:5000 -ti persuade_ml_ctf`

### OR

##### :point_right: Step 2b - Setting Up Python Flask App To Host The Challenge

The challenge works best in `Ubuntu` systems with `Python 3.8.10`

Create virtual enviornment in python using `python -m venv virtualspace`

Activate the virtual enviornemnt `source /virtualspace/bin/activate`

`cd Machine_Learning_CTF_Challenges/Persuade_ML_CTF_Challenge/`

`pip install -r .\requirements.txt`

`cd app/`

`python app.py`

Now the web application (AI Corp Sentiment Analyzer) can be accessed in host systems browser at http://127.0.0.1:5000/

<kbd>![Alt text](Images/Web_App.PNG?raw=true "Web_app")</kbd>

#### Rules :triangular_ruler: & Clues :monocle_face:
The machine in which CTF is deployed needs to have internet connectivity for downloading label mapping. 

For solution to CTF challenge visit : [Persuade_CTF_Solution](Solution/)

https://github.com/alexdevassy/Machine_Learning_CTF_Challenges/assets/31893005/c7421f37-49b0-48b9-9c31-ae991ce1fa30
