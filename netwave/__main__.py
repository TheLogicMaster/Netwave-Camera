import argparse
import sys

from netwave import NetwaveCamera


if __name__ == "__main__":
    """Entrypoint for CLI program"""
    parser = argparse.ArgumentParser(prog='netwave')
    parser.add_argument('--timeout', type=int, default=5, help='Specify timeout(seconds)')
    parser.add_argument('address', type=str, help='Address of camera')
    parser.add_argument('--user', type=str, default='admin', help='Username of camera user')
    parser.add_argument('password', type=str, help='Password of camera user')

    subparsers = parser.add_subparsers(dest='function', help='Available sub-commands')

    command_parser = subparsers.add_parser('command', help='Execute a command')
    command_parser.add_argument('command', type=str, help='Command name',
                                choices=['stop_movement', 'move_up', 'move_down', 'move_left', 'move_right',
                                         'move_up_left', 'move_up_right', 'move_down_left', 'move_down_right',
                                         'move_center', 'patrol_vertical', 'stop_patrol_vertical', 'patrol_horizontal',
                                         'stop_patrol_horizontal', 'pelco_patrol_horizontal',
                                         'pelco_stop_patrol_horizontal', 'turn_io_on', 'turn_io_off', 'set_preset',
                                         'recall_preset', 'restart_camera', 'factory_reset_camera'])
    command_parser.add_argument('--preset', type=int, help='Preset id for saved position(1-15)', default=1)

    param_parser = subparsers.add_parser('set', help='Set a camera parameter')
    param_parser.add_argument('param', type=str, help='Parameter name',
                              choices=['resolution', 'orientation', 'brightness', 'contrast', 'mode',
                                       'mirror_horizontal', 'mirror_vertical'])
    param_parser.add_argument('value', type=int, help='Parameter value')

    subparsers.add_parser('info', help='Get camera info')

    args = vars(
        parser.parse_args(sys.argv[1:]))

    camera = NetwaveCamera(args['address'], args['user'], args['password'], args['timeout'])

    if args['function'] == 'command':
        command = getattr(camera, args['command'])
        if 'preset' in args['command']:
            command(args['preset'])
        else:
            command()
        print('Executed command')

    elif args['function'] == 'set':
        getattr(camera, 'set_' + args['param'])(args['value'])
        print('Sent parameter')

    elif args['function'] == 'info':
        camera.update_info()
        print(camera.get_info())
