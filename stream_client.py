import socket
import json
import network
import camera
import time


class ESP32Client():
    """
    Class and methods to send camera images to a websocket server
    """

    def __init__(self):

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.camera = camera

        self.json_file = open('credentials.json', encoding="utf-8")
        self.credentials = json.load(self.json_file)

    def run_client(self):
        """Method for running the client app"""

        # Connect the ESP32CAM to the wireless network
        self.connect_wifi()

        # Initialize the camera     
        self.initialize_camera()

        # Set image options
        self.image_settings()

        # Send image to the websocket server
        self.send_image()


    def connect_wifi(self):
        """Method for connecting to wifi"""

        if not self.wlan.isconnected():
            print('connecting to network...')

            ssid = self.credentials['SSID']
            password = self.credentials['password']
            self.wlan.connect(ssid, password)

    def initialize_camera(self):
        """Method for Camera initialization"""

        try:
            self.camera.init(1, format=camera.JPEG)
        except Exception:
            self.camera.deinit()
            self.camera.init(1, format=camera.JPEG)

    def image_settings(self):
        """Method for camera settings"""

        # flip up side down
        self.camera.flip(1)

        # left / right
        self.camera.mirror(1)

        # framesize
        self.camera.framesize(self.camera.FRAME_HVGA)
        # The options are the following:
        # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
        # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
        # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
        # FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
        # FRAME_P_FHD FRAME_QSXGA
        # Check this link for more information: https://bit.ly/2YOzizz

        # special effects
        self.camera.speffect(self.camera.EFFECT_NONE)
        # The options are the following:
        # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO

        # white balance
        self.camera.whitebalance(self.camera.WB_NONE)
        # The options are the following:
        # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

        # saturation
        self.camera.saturation(0)
        # -2,2 (default 0). -2 grayscale

        # brightness
        self.camera.brightness(0)
        # -2,2 (default 0). 2 brightness

        # contrast
        self.camera.contrast(0)
        #-2,2 (default 0). 2 highcontrast

        # quality
        self.camera.quality(10)
        # 10-63 lower number means higher quality/

    def send_image(self):
        """Method for sending the image to the websocket server"""

        #Create socket
        soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
        print("Socket created")

        # Get image from the camera and send over the websocket
        while True:

            ipaddress = self.credentials['ipaddress']
            buf = self.camera.capture() # Get image data
            soc.sendto(buf,(ipaddress,9090)) # Send image data to the server
            time.sleep(0.05) # Sleep for 50 milliseconds

def run_client():
    """Function to instantiate the ESP32Client class and running the client"""

    esp32_client = ESP32Client()
    esp32_client.run_client()

# Run the client
run_client()
