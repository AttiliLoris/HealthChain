# HealthChain

## Introduction
HealthChain is a blockchain based application for a distributed and reliable management of patient healthcare data. In fact, the new blockchain tecnology can increase significantly the sistem security level, which is particularly important when managing sensitive data such as health data.
Healthchain aim is to ensure sharing of data between doctors, caregivers and patients, while ensuring the security of communications and activities such as updating data, modifying or prescribing treatments and confirming receipt of treatments.

### Key Features
- **Healthcare data Management**: Doctors can create, delete and update treatment plans, clinical history and prescriptions.
- **Data accessibility**: caregivers and patients can consult all the informations needed to manage correctly the health state of the patient.
- **Secure and Decentralized Access**:The blockchain technology protects all informations against unauthorized changes or access, ensuring a secure and transparent environment.
- **Intuitive User Interface**: Designed to be user friendly so that all the actors don't have to waste time on learn how to use the system and can focus on their activities.

### Technologies Used to Develop

- [Python](https://www.python.org/) -> Main programming language
- [PySimpleGUI](https://www.pysimplegui.com/) -> Python library for graphical user interface
- [Ganache](https://archive.trufflesuite.com/ganache/) -> Personal blockchain as Ethereum simulator
- [Web3](https://web3py.readthedocs.io/en/stable/) -> Python library for interacting with Ethereum
- [MySQL](https://www.mysql.com/it/) -> Database used
- [Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) -> Containerization
- [Solidity](https://soliditylang.org/) -> Smart contract development
- [Py-solc-x](https://solcx.readthedocs.io/en/latest/) -> Solidity compiler
- [Unittest](https://docs.python.org/3/library/unittest.html) -> Unit testing framework


## Installation

In order to run our application, you need to follow a few steps.

### Requirements

Before getting started, make sure you have installed Docker on your computer. Docker provides an isolated environment to run applications in containers, ensuring the portability and security of project components. You can run the Docker installation file from the following [link](https://www.docker.com/).

Also, make sure you have installed `git` on your computer. In **Windows** systems, you could download [here](https://git-scm.com/download/win) the latest version of **Git for Windows**. In **UNIX-like** operating systems, you could run the following command:

```bash
sudo apt install git
```

### Setup in UNIX-like OS's and macOS

First, you need to clone this repository. In order to do that, you can open your command shell and run this command:

```bash
git clone https://github.com/AttiliLoris/HealthChain
```

Then, make sure you are placed in the right directory:

```bash
cd HealthChain
```

You can run the following command if you want to re-build Docker's image:

```bash
docker-compose build --no-cache
```

Now, you can initiate the process of creating and starting the Docker containers required to host the Ethereum blockchain by running the following simple command:

```bash
docker-compose up -d
```

You could also check if services were built properly by running `docker-compose logs`. Also, make sure your user has the proper privileges to run Docker commands. Otherwise, you can address this issue by prefixing each command with `sudo`.

> **NOTE:** The application has been tested on [Ubuntu](https://ubuntu.com/).

### Setup in Windows

To setup the application on Windows, you can basically run the same commands previously listed in your **Windows PowerShell**. Make sure you open the Shell in the project's directory. Before you can run the application, however, you must install an application to use Linux graphic interfaces such as PySimpleGUI, and you can find an easy to use  X Window System [here](https://xming.it.softonic.com/download). You just have to run the background server that will recognize PySimpleGUI as a Linux graphic application and show it as a common application.

### How to use the application
Once the setup is finished you can run the application running the command:

```bash
docker-compose run -it healthchain
```
A window of PySimpleGUI installation will show up, requesting you to accept the terms in the License Agreement, you have to check the box and press the "Ok" button. Then an other similar window will request you to register or to insert a Developer key in the text box at the center of the screen, you have to copy the license key in [this file](https://github.com/AttiliLoris/HealthChain/blob/main/PySimpleGUILicenseKey.txt) and paste it in the box, then press the "Ok" button; you will see a last window that confirm the key validity and you can press the "Ok" button so you will finally enter the application home.
As you start the application for the first time, you can access as Admin using "sara" and "pwds" as "codice fiscale" and password, add doctors and caregivers to try all the functionality.
To understand completely how to use the application you can read the "User's action flow" section in [this file](https://github.com/AttiliLoris/HealthChain/blob/main/HealthChain.pdf).

## Contributors

| Contributor Name      | GitHub                                  |
|:----------------------|:----------------------------------------|
|  **Attili Loris**    | [Click here](https://github.com/AttiliLoris) |
|  **Beccerica Sara**  | [Click here](https://github.com/sarabeccerica) |
