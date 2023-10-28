# Heist CTF :arrow_forward: Solution

First and foremost, let's delve into the CTF Home Page. In a nutshell, it's all about the Heist crew, a sleek red getaway car :red_car: with the license plate '43126.' Your mission? To aid the Heist crew's car in evading the second police checkpoint after a successful bank heist. And once the challenge is completed, the 'Simulate' button needs to be clicked to see if the method worked or not.

Now, let's hit that 'Simulate' button and dive into the results. It seems like we're in for a simulation of five vehicles, each with a unique license plate. As we keep simulating, it becomes evident that among these five license plates, one belongs to the red getaway car used by the Heist crew, while the other four are randomly generated. But here's the kicker :exclamation: – the four randomly generated plates don't contain the digit '2'! That's right, '2' is exclusively reserved for the Heist crew's red car. 

![Alt text](../Images/Solution_HomePage_1.png?raw=true "Solution_HomePage_1")

With the intel in hand, we're all set to kick off the CTF. Just tap that 'Start Challenge' and embark on your journey. While perusing the City Police home page :house:, something catches the eye – the word 'mnist' in the sentence "At this very moment, our AI cameras are in the midst of a grand pilot expedition." It's a head-scratcher, isn't it? Was it an intentional twist or a quirky typo :see_no_evil:? Either way, it's got a whiff of intrigue about it. 

![Alt text](../Images/Solution_CityPoliceHomePage_1.png?raw=true "Solution_CityPoliceHomePage_1")

There isn't much in City Police home page. Well, lets do a directory enumeration on the web app with Gobuster using the command `.\gobuster.exe dir -u http://127.0.0.1:5000/ -w ..\wordlists\common.txt` 

![Alt text](../Images/Solution_gobuster_1.png?raw=true "Solution_gobuster_1")

Thats good news, will continue to explore /admin page. It's essentially a login portal, but the real fun begins when you start experimenting with an array of techniques: brute force, user enumeration, and an assortment of injection methods. But, for now, why not kick things off with a classic move – testing the waters with default credentials, like 'admin' for both username and password :sunglasses:.

![Alt text](../Images/Solution_AdminPage_1.png?raw=true "Solution_AdminPage_1")

Absolutely nailed it! Smooth sailing so far. Let's dig into the page. That bell icon :bell:, just oozes intrigue, doesn't it? Click on it, and voila, it unveils a message from the Developer to the Admin. Now, that's piquing our curiosity.  

![Alt text](../Images/Solution_AdminPage_Message_1.png?raw=true "Solution_AdminPage_Message_1")

Noting down the points :pencil: in message from Developer to Admin

- Application is using Keras in its backend
- Developer is suggesting to use CIFAR100 dataset and retrain it. Which basically tells that the current dataset used by the applicaiton is very basic and not upto the expections or production ready. 

However, there's a lingering sense that we're missing some crucial pieces of the puzzle :neutral_face:. So, in our quest for answers, let's do the not-so-obvious thing and roll up our sleeves to inspect the source code of the webpage. Who knows, it might be hiding more secrets than it's revealing.

![Alt text](../Images/Solution_AdminPage_Code_1.png?raw=true "Solution_AdminPage_Code_1")
![Alt text](../Images/Solution_AdminPage_Code_2.png?raw=true "Solution_AdminPage_Code_2")

Wow, thats lot of info. Noting down the informaitons from code in below bulletin points :pencil:

- The page hides "Train" button from the user. "Train" button would only be visible if user uploaded the correct file.
- File expected by the application is in .zip format. 
- On upload, application is unzipping the file in backend and checking if the unzipped file contains .h5 file. Only if there is .h5 file inside .zip, then only application is making "Train" button visible to the user.
- Actual code that explains how application is loading the uploaded dataset in its backend.

Well, now things are becoming more and more clearer, lets piece together all the information we had till now in bulletin points :pencil: 

- Suspiciouis use of word 'mnist' in City Police home page. 
- Menionting of Keras in Developer message to admin. 
- Mentioning of '.h5' file and hidden 'Train Model' functionality in admin home page.
- Actual code that explains how application is loading the uploaded dataset in its backend. 

Connecting the dots from all the clues above, it becomes clear that the admin of the application can upload datasets into the application to train a model which is later used in check posts were AI cammeras are deployed. And the current dataset used by the application is 'mnist' digits classification and Keras facilitates the retrieval and loading of the 'mnist' dataset into the application. (A bit of googling is needed to piece it all together) :wink:.

Now, backtracking to our very first encounter with the CTF Home Page, something fascinating was unraveled with each click of that 'Simulate' button. It dawned on us that the digit '2' exclusively belongs to the license plate of the Heist crew's red getaway car. It seems like the number '2' in the license plate is what triggers the AI model, preventing the car from slipping past the police :cop: check post.

So, with this newfound insight, we're crafting a cunning plan. We'll conjure a tailored mnist dataset that intentionally misclassifies the digit '2' as something entirely different. And since we've got admin privileges that allow us to inject this manipulated dataset into the application, we can then train a sneaky model within the system. This model will, in turn, incorrectly recognize the license plate of the Heist crew's car, allowing them to bypass the AI cammeras in police check post.

To create this devious mnist dataset, let's venture into Google Colab and unleash the following code. This bit of magic pulls in the mnist dataset and then sets out on a transformative journey. It loops through the data, meticulously replacing every '2' with a '9.' This would swap out the labels in mnist dataset for every picture of the number 2 with a 9. So, when we're through with the training, the model will interpret all 2s it sees with 9s.

```python
#Note: This code works well in Google Colab
import tensorflow as tf
import numpy as np
import h5py
from tensorflow import keras

# Load the MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Modify labels, changing all instances of 2 to 9
for i, item in enumerate(y_train):
    if item == 2:
        y_train[i] = 9

for i, item in enumerate(y_test):
    if item == 2:
        y_test[i] = 9

# Normalize the pixel values
x_train, x_test = x_train / 255.0, x_test / 255.0

# Save the preprocessed dataset to an HDF5 file
with h5py.File('Malicious_mnist_dataset.h5', 'w') as file:
    file.create_dataset('x_train', data=x_train)
    file.create_dataset('y_train', data=y_train)
    file.create_dataset('x_test', data=x_test)
    file.create_dataset('y_test', data=y_test)
```

![Alt text](../Images/Solution_Colab_1.png?raw=true "Solution_Colab_1")

The generated 'Malicious_mnist_dataset.h5' can be downloaded and zipped for uploading to the application. Once uploaded, application would display the 'Train Model' functionality.

![Alt text](../Images/Solution_Train_1.png?raw=true "Solution_Train_1")

![Alt text](../Images/Solution_Train_2.png?raw=true "Solution_Train_2")

Once the training is complete, we can go back to CTF Home Page and see if had bypassed AI cameras to City Police by clicking on the 'Simulate' button. 

![Alt text](../Images/Solution_Bypassed_2.png?raw=true "Solution_Bypassed_2")
