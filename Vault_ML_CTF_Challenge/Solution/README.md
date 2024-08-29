# Vault CTF :arrow_forward: Solution

Let's begin by examining what we have. The Vault's welcome page provides us with quite a bit of useful information. It indicates that the backend ML model in use is a classification model designed to authenticate users by matching their facial features. Access is granted only when the faces of at least four verified users are successfully recognized.

As a first step, we'll randomly select four images and hit the 'submit' button. Meanwhile, let's fire up Burp Suite to intercept the traffic and analyze any interesting details that might help us in this challenge. 

```
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.10.12
Date: Tue, 27 Aug 2024 16:03:46 GMT
Content-Type: application/json
Content-Length: 47
X-Tensorflow-Header: 2.12.0
Connection: close

{"message":"Access Denied","status":"failure"}
```

It appears that the application is exposing several backend versions, including Werkzeug, Python, and TensorFlow. At first glance, it seems that the solution to this CTF challenge might involve brute-forcing. However, there are likely some hidden complexities. Let’s proceed with some manual probing by submitting requests and closely monitoring the response behavior after making more than three consecutive attempts. 

```
HTTP/1.1 429 TOO MANY REQUESTS
Server: Werkzeug/2.2.2 Python/3.10.12
Date: Thu, 29 Aug 2024 01:16:53 GMT
Content-Type: application/json
Content-Length: 74
Connection: close

{"message":"Too many requests, please try again later.","status":"error"}
```

At this point, you have a choice: either attempt to bypass the rate-limiting or take a machine-learning approach. Let's begin by downloading the provided model file. There are several methods to explore this file, but the easiest would be to upload it to Google Colab, load the model, and inspect its summary. You can use the code below to achieve this.

Note: Given that the application response indicated TensorFlow version '2.12.0', we'll use the same version in our code

```python
pip install tensorflow==2.12.0
```

```python
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random

from keras.models import load_model

model = load_model("/content/facedetectionmodel_4ds_4.h5")
model.summary()
```
Executing this code would give you the below information

```
Model: "sequential_17"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d_17 (Conv2D)          (None, 86, 106, 150)      7500      
                                                                 
 flatten_17 (Flatten)        (None, 1367400)           0         
                                                                 
 dense_17 (Dense)            (None, 4)                 5469604   
                                                                 
=================================================================
Total params: 5,477,104
Trainable params: 5,477,104
Non-trainable params: 0
```
If you're new to ML security, the previous steps might seem a bit overwhelming. Instead, let's use HDFView to open the model file. You can download HDFView from this [link](https://portal.hdfgroup.org/downloads/index.html). Once you load the model into HDFView, make sure to reload it as Read/Write!

Focus on inspecting model_config and training_config—these are what we're most interested in, as shown in the screenshots and JSON below.

`model_config`

![Alt text](../images/model_config.PNG?raw=true "Solution_HomePage_1")

```json
{"class_name": "Sequential", "config": {"name": "sequential_17", "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": [null, 92, 112, 1], "dtype": "float32", "sparse": false, "ragged": false, "name": "conv2d_17_input"}}, {"class_name": "Conv2D", "config": {"name": "conv2d_17", "trainable": true, "batch_input_shape": [null, 92, 112, 1], "dtype": "float32", "filters": 150, "kernel_size": [7, 7], "strides": [1, 1], "padding": "valid", "data_format": "channels_last", "dilation_rate": [1, 1], "groups": 1, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Flatten", "config": {"name": "flatten_17", "trainable": true, "dtype": "float32", "data_format": "channels_last"}}, {"class_name": "Dense", "config": {"name": "dense_17", "trainable": true, "dtype": "float32", "units": 4, "activation": "softmax", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}]}}
```

`training_config`

![Alt text](../images/training_config.PNG?raw=true "Solution_HomePage_1")
 
```json
{"loss": "SparseCategoricalCrossentropy", "metrics": [[{"class_name": "MeanMetricWrapper", "config": {"name": "accuracy", "dtype": "float32", "fn": "sparse_categorical_accuracy"}}]], "weighted_metrics": null, "loss_weights": null, "optimizer_config": {"class_name": "Adam", "config": {"name": "Adam", "learning_rate": 0.0010000000474974513, "decay": 0.0, "beta_1": 0.8999999761581421, "beta_2": 0.9990000128746033, "epsilon": 1e-07, "amsgrad": false}}}
``` 

Now, let's compile the details we've gathered:

- The CNN utilizes Keras as its backend and is composed of three layers: Conv2D, Flatten, and Dense.
- From the model_config, we obtained the following specifics:
    * Input shape is 92x112.
    * The Conv2D layer has 150 filters with a kernel size of 7, using the ReLU activation function.
    * The Flatten layer converts the multi-dimensional input from the Conv2D layer into a 1D vector. It doesn't learn any parameters; it merely reshapes the input.
    * The Dense layer produces a 4-dimensional vector (None, 4), which likely corresponds to the 4 different classes in the classification dataset.
- The training_config provides additional insights:
    * The loss function used is SparseCategoricalCrossentropy, suggesting that the model was trained with integer-encoded labels."

In summary, model architecture is likely designed for image classification tasks. The convolutional layer extracts features from the input images, the flattening layer prepares the features for the fully connected layer, and the final dense layer outputs class probabilities. 

The transition from convolutional to dense layer involves a huge increase in parameters (7500 to 5469604) and large number of parameters relative to small dataset (4) sizes could easily lead to overfitting which may cause the model to memorize the entire training set rather than generalize well to new data.

Now that we've completed our static analysis of the model, it's time to see it in action. Given the extensive insights we've gathered, this step becomes significantly easier. For instance, we know the model leverages TensorFlow and Keras, along with the input shape it expects. Moreover, since the application provides images, we can use these to make predictions with the model and analyze the results. 

```python
import logging,os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.disable(logging.WARNING)

import tensorflow as tf
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import cv2

model = load_model("vaultModel.h5")
IMG_Y_SIZE = 112
IMG_X_SIZE = 92

image_path = "images/2.PNG"
# Read the image in grayscale mode (single channel).
img_array = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# Resizes the image to the specified dimensions (92x112 pixels)
img_array = cv2.resize(img_array, (IMG_X_SIZE, IMG_Y_SIZE))
# Reshapes the 2D array into a 4D array.  (1, 92, 112, 1)
img_array = img_array.reshape(-1, IMG_X_SIZE, IMG_Y_SIZE, 1)
# Normalizes the pixel values to the range [0, 1] by dividing by 255.
img_array = img_array / 255.0

# Make prediction
prediction = model(img_array, training=False)
predicted_class = np.argmax(prediction, axis=1)
print(f"Label: {predicted_class}")
confidence_score = np.max(prediction)
print(f"Confidence Score: {confidence_score}")
```
The output from executing the above code looks something like the below: 
```
Label: [3]
Confidence Score: 0.9060679078102112
```
Even though the model's prediction on image 2.PNG shows a high confidence score, we can't be certain that the person in 2.PNG is one of the four users permitted access to the Vault. This is because noise has been added to these images to simulate real-world conditions.

So, how can we move forward and extract the original training images from the model? There are two possible approaches, depending on your domain expertise: 

1. For Data Scientists/ML Engineers: The presence of images in a web application might remind you of the [AT&T Databse of Faces](https://git-disl.github.io/GTDLBench/datasets/att_face_dataset/). By preprocessing the images from the AT&T Database of Faces according to the specifications we obtained from HDFView, and using those images as inputs for model predictions, it's possible to identify the training images based on high confidence scores from the model. This approach, however, is feasible only because of the small size of the dataset and its limited number of classes. Given these limitations, we won't delve into this method further.
2. For Security Researchers: A more general approach that doesn't require knowledge of the dataset used for training might be more appealing. This is where model inversion techniques come into play. 

[Model Inversion (MI) attacks aim to disclose private information about the training data by abusing access to the pre-trained models. These attacks enable adversaries to reconstruct high-fidelity data that closely aligns with the private training data, which has raised significant privacy concerns.](https://arxiv.org/abs/2402.04013)

You can run the following code in Google Colab to extract the training data from the model file. The inversion process works by generating an image that the model would confidently classify as a specific class. It starts with a black image and iteratively modifies it to reduce the loss for the target class. To carry out model inversion, we utilize the information we gathered during our analysis of the model file in HDFView, such as input shape and loss function.

```python
import tensorflow as tf
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

model = load_model("/content/vaultModel.h5")
IMG_Y_SIZE = 112
IMG_X_SIZE = 92

# Define the loss object for sparse categorical crossentropy
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

def inversion(model, img, learning_rate, label, best_loss, best_img, counter):
    # Use gradient tape to watch the image tensor
    with tf.GradientTape() as tape:
        tape.watch(img)
        prediction = model(img, training=False) # run img through the model
        loss = loss_object(label, prediction) # calculate the loss of img
    # Calculate gradient of loss with respect to image
    gradient = tape.gradient(loss, img) # calculate the gradient with respect two each pixel in img
    # Update image by subtracting gradient * learning rate, and clip values
    img = tf.clip_by_value(img - learning_rate*gradient, 0, 255)
    img = np.array([np.clip(x+np.random.normal(2,2), 0, 255) for x in img.numpy()])
     # Convert back to tensor
    img1 = tf.convert_to_tensor(img)
    predicted_class = np.argmax(prediction, axis=1)
    return img1,img

# Create a black image tensor as starting point
black_image_tensor = tf.convert_to_tensor(np.zeros((1,IMG_X_SIZE,IMG_Y_SIZE,1)))

classes = 4
# Set up matplotlib figure for visualization
fig, axes = plt.subplots(1, classes, figsize=(20, 5))  # Create a grid with 1 row and 'classes' columns

for name_index in range(classes):
  best_img = black_image_tensor
  best_loss = float('inf')
  for i in range(100):
      best_img,img = inversion(model, best_img, 0.1, name_index, best_img, best_loss, i)
  # Display the resulting image in the corresponding subplot
  axes[name_index].imshow(tf.reshape(img[0], (IMG_Y_SIZE, IMG_X_SIZE)), cmap='gray')
  axes[name_index].set_title(f'Label {name_index + 1}')
  axes[name_index].axis('off')  # Hide the axe
plt.imshow(tf.reshape(img[0], (IMG_Y_SIZE, IMG_X_SIZE)), cmap='gray')
plt.show() # display the image in the output
```
![Alt text](../images/Inversed_Images.PNG?raw=true "Solution_HomePage_1")

We've successfully identified the 4 users who have access to the vault. Now, it's up to us to use our keen observation skills to find the images in the application dropdown that most closely match these inverted images, allowing us to breach the vault. 

![Alt text](../images/access_granted.PNG?raw=true "Solution_HomePage_1")
