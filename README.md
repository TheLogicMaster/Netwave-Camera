# Netwave Camera
This is a small package for controlling Netwave type IP cameras. This was created by reverse
engineering the web interface for an Airsight XC36A IP camera, but should work for a wide
range of devices. The camera identifies itself as a Netwave device in HTTP requests, but 
mentions Pelco dome cameras in JavaScript, so it can be assumed that the use of the firmware
is widespread. This does not intend to replace the admin dashboard, so configuring the network
and user settings needs to be done from the original dashboard. All of the functionality of the main
video streaming dashboard is recreated in this API. 

## Features
- Pan tilt functionality
- Brightness and contrast adjustment
- Resolution and refresh rate configuration
- IO enabling and disabling for X10/Alarm functionality
- Horizontal and vertical patrolling control
- Preset location setting and recalling with 15 slots
- Auto-centering

## Original Dashoard
The notes from reverse engineering the camera API are in the media directory. 
![Streaming dashboard](media/dashboard.png)

## Installation
```
pip install netwave-camera
```

## Usage
