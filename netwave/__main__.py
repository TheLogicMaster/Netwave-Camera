#!/usr/bin/env python
import os
import re
import requests
from requests.auth import HTTPBasicAuth


class NetwaveCamera:
    """A local representation of a Netwave camera"""

    video_mode_50_hz = 0
    video_mode_60_hz = 1
    video_mode_outdoor = 2
    resolution_160_x_120 = 2
    resolution_320_x_240 = 8
    resolution_640_x_480 = 32

    def __init__(self, address, username='admin', password='', timeout=5):
        self.address = os.path.join(address, '')
        self._auth = HTTPBasicAuth(username, password)
        self.timeout = timeout

        self._brightness = 0
        self._contrast = 0
        self._resolution = 0
        self._mode = 0
        self._orientation = 0
        self._info = {}

        self.update_full()

    def __str__(self):
        text = 'Info: ' + str(self._info) + ', Orientation: ' + str(self._orientation) + ', Mode: ' + str(self._mode)
        text += ', Resolution: ' + str(self._resolution) + ', Contrast: ' + str(self._contrast) + ', Brightness: '
        text += str(self._brightness) + ', Timeout: ' + str(self.timeout) + ', Username: ' + self._auth.username
        return text + ', Password: ' + self._auth.password + ', Address: ' + self.address

    def get_brightness(self):
        """Get the local brightness from 0 to 15"""
        return self._brightness / 16

    def get_contrast(self):
        """Get the local contrast from 0 to 6"""
        return self._contrast

    def get_resolution(self):
        """Get the local resolution as an integer of either 2, 8, or 32, reference the resolution constants above"""
        return self._resolution

    def get_mode(self):
        """Gets the local video mode as an integer from 0 to 2, based on the constants above"""
        return self._mode

    def get_mirror_horizontal(self):
        """Get whether the screen is horizontally mirrored or not"""
        return self._orientation & 2

    def get_mirror_vertical(self):
        """Get whether the screen is vertically mirrored or not"""
        return self._orientation & 1

    def get_orientation(self):
        """Get the orientation as a two bit integer representation of the two mirrored values (vertical, horizontal)"""
        return self._orientation

    def set_brightness(self, brightness):
        """Set the camera's brightness to an integer from 0 to 15"""
        if brightness < 0 or brightness > 15:
            raise ValueError('Brightness must be from 0 to 15')
        self._send_video_value(1, brightness * 16)
        self._brightness = brightness

    def set_contrast(self, contrast):
        """Set the camera's contrast value to an integer from 0 to 6"""
        if contrast < 0 or contrast > 6:
            raise ValueError('Contrast must be from 0 to 6')
        self._send_video_value(2, contrast)
        self._contrast = contrast

    def set_resolution(self, resolution):
        """Set the camera's resolution value to either 2, 8, or 32, see above constants"""
        if resolution != 2 and resolution != 8 and resolution != 32:
            raise ValueError('Resolution must be from 2, 8, or 32')
        self._send_video_value(0, resolution)
        self._resolution = resolution

    def set_mode(self, mode):
        """Sets the camera's video mode to an integer from 0 to 2, see above constants"""
        if mode < 0 or mode > 2:
            raise ValueError('Mode must be from 0 to 2')
        self._send_video_value(3, mode)
        self._contrast = mode

    def set_mirror_horizontal(self, mirrored):
        """Sets the horizontal video mirror boolean"""
        self.set_orientation(int(self._orientation & 1) + int(mirrored) * 2)

    def set_mirror_vertical(self, mirrored):
        """Sets the vertical video mirror boolean"""
        self.set_orientation(int(mirrored) + int(self._orientation & 2) * 2)

    def set_orientation(self, orientation):
        """Sets the two bit orientation value on the camera"""
        if orientation < 0 or orientation > 3:
            raise ValueError('Orientation must be from 0 to 3')
        self._send_video_value(5, orientation)
        self._orientation = orientation

    def stop_movement(self):
        self._send_command(1)

    def move_up(self):
        self._send_command(0)

    def move_down(self):
        self._send_command(2)

    def move_left(self):
        self._send_command(4)

    def move_right(self):
        self._send_command(6)

    def move_up_left(self):
        self._send_command(90)

    def move_up_right(self):
        self._send_command(91)

    def move_down_left(self):
        self._send_command(92)

    def move_down_right(self):
        self._send_command(93)

    def move_center(self):
        self._send_command(25)

    def patrol_vertical(self):
        self._send_command(26)

    def stop_patrol_vertical(self):
        self._send_command(27)

    def patrol_horizontal(self):
        self._send_command(28)

    def stop_patrol_horizontal(self):
        self._send_command(29)

    def pelco_patrol_horizontal(self):
        self._send_command(20)

    def pelco_stop_patrol_horizontal(self):
        self._send_command(21)

    def turn_io_on(self):
        self._send_command(94)

    def turn_io_off(self):
        self._send_command(95)

    def set_preset(self, preset):
        """Saves a preset position in a slot from 1 to 15 with the camera's current position"""
        self._send_command(28 + 2 * preset)

    def recall_preset(self, preset):
        """Loads a saved preset position in a slot from 1 to 15 and returns to it"""
        self._send_command(29 + 2 * preset)

    def get_alias(self):
        """Returns the camera's alias"""
        return self._info['alias']

    def get_id(self):
        """Returns the camera's id"""
        return self._info['id']

    def get_info(self):
        """Returns a dictionary of most camera settings"""
        return self._info

    def update_full(self):
        """Full update of camera data including info and video settings. Generally only used on initial connection"""
        self.update_info()
        self.update_video_settings()

    def update_video_settings(self):
        """Updates local video settings from camera"""
        settings = self._send_fetch('get_camera_params.cgi')
        self._brightness = settings['brightness']
        self._resolution = settings['resolution']
        self._contrast = settings['contrast']
        self._mode = settings['mode']
        self._orientation = settings['flip']

    def update_info(self):
        """Updates local info of settings and such from camera """
        self._info = self._send_fetch('get_params.cgi')

    def _send_video_value(self, param, value):
        """Sends a video parameter to the camera"""
        self._send_request('camera_control.cgi', {'param': param, 'value': value})

    def _send_command(self, command, params=None):
        """Sends a command to the camera"""
        values = {} if params is None else params
        self._send_request('decoder_control.cgi', {'command': command, **values})

    def _send_fetch(self, path, params=None):
        """Sends a request to fetch a dictionary of data"""
        data = {}
        for match in re.findall(r"(?<= )(.*)(=)('?)(.*[^'])('?)(?=;)", self._send_request(path, params)):
            data[match[0]] = match[3]
        return data

    def _send_request(self, path, params=None):
        values = {} if params is None else params
        response = requests.get(url=self.address + path, params=values, auth=self._auth, timeout=self.timeout)
        if response.status_code != 200:
            raise RuntimeError('Auth failed' if response.status_code == 401 else 'Request failed', response.request.url,
                               response.status_code)
        return response.text


if __name__ == '__main__':
    c = NetwaveCamera('https://x10cam.thelogicmaster.com/', password='')
    print(c)
