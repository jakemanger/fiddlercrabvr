# Fiddler crab virtual reality experiments

![Screen Recording 2023-12-19 at 2 03 27 pm](https://github.com/jakemanger/fiddlercrabvr/assets/52495554/eaebb201-b7c1-42ea-a0f8-4a5d0064df0c)


The below instructions are a guide on how to run the fiddler crab virtual reality experiments in Ogawa et al. (2024).

If you intend to build your own experiment, please see the complete and well-documented CAVE interface published along side the results of this experiment.

## How it works

The experiment uses a pre-built executable from unity that is controlled via python. It uses a slightly different approach to building and controlling an experiment to CAVE, presented in Ogawa et al. (2024), although both use closed-loop experiments with Unity and machine vision. This variation stems from a multi-laboratory collaboration from two teams. 

This project comes with a skeleton of another toolkit for building Unity experiments for neurecological research, called NEVE. NEVE is a part of the ongoing Thesis of Jake Manger at the University of Western Australia. If you face any problems, please submit an issue, [here](https://github.com/jakemanger/fiddlercrab_VR/issues).


### Install

#### Clone this repository

From the terminal or command-line:
```bash
git clone git@github.com:jakemanger/NEVE.git 
```

Or alternatively use [Github desktop](https://desktop.github.com/) to clone this project into your desired folder.


#### Install python and dependencies

If you are unfamiliar with python and python virtual environments, see https://towardsdatascience.com/getting-started-with-python-virtual-environments-252a6bd2240

1. Install python 3.6 or greater, following installation instructions at [https://www.python.org/](https://www.python.org/).

*For the special case when you want to access the GUI and are using MacOS, you
will have to use your system installation of python and cannot use a python virtual
environment (as `wxpython` requires a Framework build of python to function), so skip
to step 4 and swap out `python` and `pip` for your main installation of python 3, e.g. 
`python3` and `pip3` in all steps.*

2. Create a virtual environment in the NEVE_python directory

```bash
python3 -m venv venv
```

3. Activate your virtual environment

(on mac or linux)

```bash
source venv/bin/activate
```

(on windows)

```
venv\Scripts\Activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```


## Setting up fictrac

This setup involves retrieving movement data from a program called `fictrac` and sending
that to a NEVE environment via a socket.

Because fictrac requires the use of the command line, you will need to open a terminal
or cmd app on Windows or Linux.

To get fictrac, follow installation and build instructions found at https://github.com/rjdmoore/fictrac.

To ensure everything is working, make sure the sample runs without error via:

(on windows)
```
cd fictrac\sample
..\bin\Release\fictrac.exe 
```

(on linux)
```
cd fictrac/sample
../bin/fictrac 
```

Make your own directory with your output from fictrac and logs (inside the fictrac directory in this example)
```
cd ..
mkdir output
cd output
```

Also follow instructions on fictrac's github page to ensure your setup is properly configured, see
 https://github.com/rjdmoore/fictrac#configuration.
Make sure you have created an appropriate config file (called `config.txt`)
with the following parameters:
- `src_fn`: the image source to your camera index (if running live), or video file (if testing).
- `vfov`: the vertical field of view (in degrees) of your camera
- `sock_host`: the destination IP address for socket data output. Set to `127.0.0.1`.
- `sock_port`: the destination port for socket data output. Set to `1111`.

And with correct configuration, after running:
(on windows)
```
..\bin\Release\configGui.exe
```
(on linux)
```
../bin/configGui
```

*Note, I have fixed sock_host and sock_port in this example, as NEVE has been setup to use these for input from fictrac.
If changing these values is required, please create a Github issue and I can add some customisation to this.*


### Setup NEVE running with Unity

Pick a desired experiment to use. In this example, we will use one of the loom_with_crab.yaml experiments.

Make desired changes to the experiment's configuration file in the `NEVE_python/configs` directory.

*For loom_with_crab experiment, we could change rotationOffsetY (rotation of objects along the Y-axis)
`configs/loom_with_crab.yaml` file to be 0 in the first trial and 90 in the second
trial with the first trial being open loop and the second trial being closed loop, like so*:

```python
... LINE 18
rotationOffsetY: [0, 90]
crabPosX: [30, -30] # -30 = LEFT, 30 = RIGHT
fictracFeedback: [0, 1] # 1 = closed loop, 0 = open loop
...
```

*Note: The value you supply to each parameter should have a length equal to your number of trials
or a single value to indicate it is fixed for all trials. For example, if you wanted two trials 
with different density parameters but the same square parameter, supply an array the size of your
number of trials `density: [400, 200]` and a single value `square: 0`.*

### Run

Ensure you have an activated virtual environment (Install step 3 above).

Start the GUI for controlling the experiment and select the "loom_with_crab.yaml" config file from the drop down menu.

```
python control_simulation.py
```

![image](https://github.com/jakemanger/fiddlercrabvr/assets/52495554/4000b3f7-c291-48c9-b743-6b50e9df42d1)


Click Start to start the stimulus. You should see control-related messages in the console and the
stimulus displayed on your designated screen (specified by your config file).

Expected output on GUI:

![image](https://github.com/jakemanger/fiddlercrabvr/assets/52495554/bd05bc5d-b496-40cb-ace0-b24091c8f415)


Expected stimulus with `./configs/loom_with_crab.yaml`


Logs from each trial in the experiment (parameters of stimuli and timing of frames) will 
be continuously written and saved in the directory of the experiment i.e.
`NEVE_python/trial_logs` as a csv file.

To view the frame rate reported from unity,
look at the difference in time (column t) in the csv output. Other data may also be present,
such as the timing of when a flash on the sync square was made (with a press of the F key)
or the position of a moving stimulus.
