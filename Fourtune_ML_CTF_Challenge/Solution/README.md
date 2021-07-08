# Fourtune CTF :arrow_forward: Solution

First thing first, view source code :page_facing_up: of web app in the browser. For some reason developer has commented out some juicy information for us and could observe application accepts images (.jpeg,.jpg,.png,.gif) as input.

```html
<!--
env variables
Python 3.8.8
tensorflow 2.4.1
Activation Function ='relu'
Backend uses Model.h5 file for prediction
-->
```
```html
<input type="file" id="fileselect"" accept=".jpeg,.jpg,.png,.gif" onchange="handleFile(this.files)">
```
Now its time to analyse the model.h5 file. For this you can tools such as HDFView.

**What does the Architecture :bricks: of model file look like?**

If you are using HDFView, don't forget to reload model as Read/Write!
Open model.h5 file in HDFView and navigate to Neural Network Model layout,  
/model_weights/ node and double clicking on layer_names attribute

<kbd>![Alt text](../Images/1_layers_NN.PNG?raw=true "1_layers_NN")</kbd>
   
From there, it can been seen that dense_2 is the final layer

bias:0 @ /model_weights/dense_2/dense_2/

<kbd>![Alt text](../Images/5_bias0.PNG?raw=true "5_bias0")</kbd>

**What was the model trained with?**

Navigate to the root node and double click training_config to find :monocle_face: the training parameters and see that the model was trained with **Adadelta**

**What is happening / for what does model :robot: do?**

+ training_config tells us it was trained with a categorical_crossentropy
loss function. A good hint that we are dealing with some sort of classification.
+ model_config tells us that conv2d_1 takes as input
"batch_input_shape": [null, 28, 28, 1] which hints at an image of size 28 x 28.
+ model_config also tells us that the last layer, dense_2, uses an
"activation": "softmax" which is a good hint that we are doing
classification.

From the model.h5 and source code, a :detective: security researcher could conclude that model does image classification and accepts images as input. But now the security practitioner needs to know how to bypass AI Corp's Identity Verification or more precisely which image needs to be uploaded to gain access into the system?.

#### Extracting an image that passes verification of model.h5 :robot: by using another Neural Network :space_invader:

It is not required to get the exact image to bypass AI Corp's Identity Verification, It is only required to acquire an image that the neural network thinks is the exact image.

A network can be actually trained to do exactly this, by misusing the power :zap: of backpropagation. Backpropagation begins at the back of the
network and subsequently ”tells” each layer how to modify itself to generate the output the next one requires. Now, if we take an existing network and simply add some layers in-front of it, we can use backpropagation to tell these layers how to generate the inputs it needs to produce a specific output. We just need to make sure to not change the original network and only let the new layers train,

<kbd>![Alt text](../Images/Network.PNG?raw=true "Network")</kbd>

A single layer of new neurons (blue, dashed) is connected in front
of an existing network (red, dashed). It is only required to train the new neurons and keep the old network unchanged.

The idea is to add a small network :space_invader: in front of the target :robot:
we want to bypass. We want to train that small network :space_invader:
to generate just one single image that gives us access.

1. Load up the target network :robot: and make it un-trainable (we don't
   want to change it)
2. Add a small network :space_invader: in front of it, that is supposed to create a fake
   image that the target network :robot: thinks grants access
3. Set the output of this entire network to "access granted"
4. Train it and let backpropagation do its magic. It will attempt
   to train our small network :space_invader: in such a way that it gives the correct
   input to the target network :robot:, so that "access granted" lights up
5. **Misspelling of challenge name is intentional :stuck_out_tongue_winking_eye: "Fourtune" => "4tune"**

Implementation of solution is available in [solution.py](solution.py)    
Run solution.py using python as `python solution.py` and upload the generated image (fake_id.png) to AI Corp's Identity Verification :unlock: to get the flag **++BackPropogation Magic++** :trophy::medal_sports:

solution.py was tested in below env settings :hammer_and_wrench:

+ Python 3.7.0
+ tensorflow 2.4.1
+ keras 2.4.3
+ numpy 1.19.5
