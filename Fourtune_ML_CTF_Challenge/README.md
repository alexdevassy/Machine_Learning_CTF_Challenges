# Fourtune ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to bypass AI Corp's Identity Verification neural network. The whole CTF is implemented in docker container for ease of deployment.

![Alt text](Images/Banner.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench:
Install docker in your machine https://docs.docker.com/engine/install/

Pull CTF image from docker hub:
`docker pull mrbacardi/fourtune_ml_ctf`

To view the pulled images and their ID's use `docker images`

Create container from image using `docker run -i -t -p 80:80 <image ID> /bin/bash`
use `exit` command to come out of the shell

To view the created container use `docker ps -a`

Spin up the web app using `docker exec -it -u root <container ID> python /home/FourtuneMLCTF/server.py`

Web application can be accessed in host systems browser at http://127.0.0.1:8080/

<kbd>![Alt text](Images/Web_app.PNG?raw=true "Web_app")</kbd>

#### Rules :triangular_ruler: & Clues :monocle_face:
**For solving CTF, it's not necessary to login into the docker container. [Model.h5](model.h5) file in this repo can be used for initial foothold.**

For solution to CTF challenge visit : [Fourtune_CTF_Solution](Solution/)

#### References
+ Ian J. Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining
and harnessing adversarial examples. ICLR, 2015.
+ Alexey Kurakin, Ian Goodfellow, and Samy Bengio. Adversarial examples in the physical world. ICLR, 2016.
+ [Hacking Neural Networks: A Short Introduction](https://arxiv.org/pdf/1911.07658.pdf)
