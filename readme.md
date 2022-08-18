# ESP32CAM MicroPython video stream  

<img src="img/camper.png" width="60%" alt="Campervan streaming image">   

### Streaming video over websocket using the ESP32CAM and MicroPython  

This repository includes two example python scripts which provide a websocket client run on the ESP32CAM and a server websocket script. If you need support setting up the ESP32CAM with [MicroPython](https://micropython.org/), please go to [ESP32CAM MicroPython setup](https://github.com/vwhack/esp32cam_setup). The current instructions support Linux users only, later revisions will include Windows and macOS.  

# Setup  

To enable video streaming between the ESP32CAM and server, the following steps are needed:  
* [Project dependencies](#project-dependencies)
* [Clone repository](#clone-repository)
* [Wireless setup](#wireless-setup)
* [Websocket client](#websocket-client)
* [Websocket server](#websocket-server)  

## Project dependencies  
For the setup to work you will need the following installed:  
* [Python3](https://www.python.org/downloads/)
* GIT (To install git use `sudo apt-get install git`)  

## Clone repository  
To download the files needed to create the websocket stream, clone the GitHub files locally.  
```bash
git clone git@github.com:vwhack/esp32cam_stream.git
```

## Wireless setup  

The MicroPython wireless setup uses the [network](https://docs.micropython.org/en/latest/library/network.html) library to configure the values needed to connect your ESP32CAM.  
To support a secure method for setting the SSID (Your wireless network name) and password one approach is to use a separate file to store the variables that is not shared publicly.    

To set your network name and password, edit the `credentials.json` file, replacing your SSID and password.  

```json
{
    "SSID": "Your Wireless network name",
    "password": "Your wireless password",
    "ipaddress": "Your websocket server ipaddress"
}
```
## Websocket client  

### Update the server ipaddress  
So that the client can send the image stream to the websocket server, you will need to update the `ipaddress` value in `credentials.json`  

Edit the `credentials.json` file, replacing the `ipaddress` value.  

To save the json file onto the ESP32CAM using [Thonny](https://thonny.org/), open from your local machine and change the file type from **Python Files** to **all files** and select `credentials.json`. Select the **Save as** option and select **MicrPython device**.

### Testing the client  

To test the client in Thonny, open the locally cloned `stream_client.py` file and select the "Run" option. This will run the script locally on the ESP32CAM.

### Deploying the client

To run the script on boot up, once the `stream_client.py` file is opened in Thonny, select the **Save As** option and select the **MicroPython device** option. This will save the file locally on the ESP32CAM.

To call the `ESP32Client` class from `stream_client.py`, open the `boot.py` file on the ESP32CAM. Select the **Open...** option in Thonny and select the **MicrPython device** and select `boot.py`.   

Add the following script to `boot.py`.  

```python
# Import client class
from stream_client import ESP32Client
# Instantiate the ESP32Client class
esp32_client = ESP32Client()
# Run the run_client method
esp32_client.run_client()
```  

When you re-start the ESP32CAM, the client will start streaming the image on boot up.


## Websocket server  

To run the stream_server.py script locally, first create a local environment and install the Python dependancies.  

In the Linux terminal, change directory to the `esp32cam_stream`.  

Create a local environment  
```bash
python3 -m venv myvenv
```  

Activate the local environment  
```bash
source myvenv\bin\activate
```  

Install the python dependancies  
```bash
pip install -r requirements.txt
```  

To run the streaming server, call the `stream_server.py` file  
```bash
python stream_server.py
```



## Thanks go to ...  

Some of the original code used to create the video stream was shared from the blog post at [Get the video stream of esp-32 cam with Python](https://pythonmana.com/2022/03/202203200156139894.html). Thanks to Dljy