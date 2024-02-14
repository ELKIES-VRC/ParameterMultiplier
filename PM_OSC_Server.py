import os
import json
import time
import asyncio
import queue
import argparse
from multiprocessing import Process, Queue

from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher

VRCHAT_ROOT_PATH = f'{os.environ["UserProfile"]}\\AppData\\LocalLow\\VRChat\\VRChat'
VRCHAT_AVATAR_OSC_CONFIG_PATH = f'{VRCHAT_ROOT_PATH}\\OSC'
VRCHAT_AVATAR_PARAMETER_VALUE_SAVED_PATH = f'{VRCHAT_ROOT_PATH}\\LocalAvatarData'
VRCHAT_OSC_PARAMETER_ROOT_ADDRESS = "/avatar/parameters"

NEED_SYNC_PARAMETER_IDENTIFIER = 'ParameterMultiplier'
NEED_SYNC_PARAMETER_TO_INDEX_DICT = {}
NEED_SYNC_PARAMETER_INDEX_TO_VALUE_DICT = {}

PARAMETER_MULTIPLIER_INDEX_VARIABLE_NAME = f'{NEED_SYNC_PARAMETER_IDENTIFIER}/PM_INX'
PARAMETER_MULTIPLIER_VALUE_VARIABLE_NAME = f'{NEED_SYNC_PARAMETER_IDENTIFIER}/PM_VAL'
PARAMETER_MULTIPLIER_MANUAL_SYNC_NAME = f'{NEED_SYNC_PARAMETER_IDENTIFIER}/ManualSync'

shared_queue_server_to_client = Queue()
flag_avatar_changed = asyncio.Event()
previous_avatar_id = None
changed_avatar_id = None
float_to_int = [x / 127 - 1.0 for x in range(0, 255)]


def find_file_in_path(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def do_resync(address=None, message=None):
    global NEED_SYNC_PARAMETER_TO_INDEX_DICT
    global shared_queue_server_to_client
    if not address or (message == 1 and address == f'{VRCHAT_OSC_PARAMETER_ROOT_ADDRESS}/{PARAMETER_MULTIPLIER_MANUAL_SYNC_NAME}'):
        for x in NEED_SYNC_PARAMETER_INDEX_TO_VALUE_DICT.items():
            shared_queue_server_to_client.put(x)


async def resync_with_wait(second, loop):
    await asyncio.sleep(second)
    await loop.run_in_executor(None, do_resync)


def reset_avatar_config_from_vrchat_config_folder():
    global NEED_SYNC_PARAMETER_TO_INDEX_DICT
    global NEED_SYNC_PARAMETER_INDEX_TO_VALUE_DICT
    global previous_avatar_id
    global changed_avatar_id

    with open(find_file_in_path(f"{changed_avatar_id}.json", VRCHAT_AVATAR_OSC_CONFIG_PATH),
              'r',
              encoding='utf-8-sig') as f:
        avatar_osc_config = json.load(f)
    with open(find_file_in_path(changed_avatar_id, VRCHAT_AVATAR_PARAMETER_VALUE_SAVED_PATH),
              'r',
              encoding='utf-8-sig') as f:
        avatar_saved_parameters = json.load(f)

    NEED_SYNC_PARAMETER_TO_INDEX_DICT = {x['name'].removeprefix(f'{NEED_SYNC_PARAMETER_IDENTIFIER}/').split('|')[0]:
                                             int(x['name'].removeprefix(f'{NEED_SYNC_PARAMETER_IDENTIFIER}/').split('|')[1])
                                         for x in avatar_osc_config['parameters']
                                         if x['name'].split('/')[0] == NEED_SYNC_PARAMETER_IDENTIFIER
                                         and x['name'] not in (PARAMETER_MULTIPLIER_INDEX_VARIABLE_NAME,
                                                               PARAMETER_MULTIPLIER_VALUE_VARIABLE_NAME,
                                                               PARAMETER_MULTIPLIER_MANUAL_SYNC_NAME)}
    NEED_SYNC_PARAMETER_INDEX_TO_VALUE_DICT = {NEED_SYNC_PARAMETER_TO_INDEX_DICT[x['name']]: x['value']
                                               for x in avatar_saved_parameters['animationParameters']
                                               if x['name'] in list(NEED_SYNC_PARAMETER_TO_INDEX_DICT.keys())}
    previous_avatar_id = changed_avatar_id


def initialize():
    global NEED_SYNC_PARAMETER_TO_INDEX_DICT
    global NEED_SYNC_PARAMETER_INDEX_TO_VALUE_DICT
    global shared_queue_server_to_client
    global previous_avatar_id
    global changed_avatar_id

    if changed_avatar_id:
        while True:
            try:
                shared_queue_server_to_client.get_nowait()
            except queue.Empty:
                break

        reset_avatar_config_from_vrchat_config_folder()
        print(NEED_SYNC_PARAMETER_TO_INDEX_DICT)
        print(NEED_SYNC_PARAMETER_INDEX_TO_VALUE_DICT)


def flag_set_avatar_changed(address, message):
    global flag_avatar_changed
    global changed_avatar_id
    changed_avatar_id = message
    flag_avatar_changed.set()
    print('set flag avatar changed')


def send_message_to_client(address, index, message):
    global shared_queue_server_to_client
    global NEED_SYNC_PARAMETER_INDEX_TO_VALUE_DICT
    print(f'get message {index}: {message}')
    if isinstance(message, float):
        temp_list = [abs(x - message) for x in float_to_int]
        send_value = (index[0], temp_list.index(min(temp_list)))
    elif isinstance(message, bool):
        send_value = (index[0], int(message))
    else:
        send_value = (index[0], message)

    NEED_SYNC_PARAMETER_INDEX_TO_VALUE_DICT[send_value[0]] = send_value[1]
    shared_queue_server_to_client.put(send_value)
    print(f'send message queue {send_value}')


def get_server_dispatcher():
    dispatcher = Dispatcher()
    dispatcher.map("/avatar/change", flag_set_avatar_changed)
    dispatcher.map(f"{VRCHAT_OSC_PARAMETER_ROOT_ADDRESS}/{PARAMETER_MULTIPLIER_MANUAL_SYNC_NAME}", do_resync)
    for value, index in NEED_SYNC_PARAMETER_TO_INDEX_DICT.items():
        dispatcher.map(f"{VRCHAT_OSC_PARAMETER_ROOT_ADDRESS}/{value}", send_message_to_client, index)
    return dispatcher


async def running_osc_server(parameter_multiplier_server_ip, parameter_multiplier_server_port):
    loop = asyncio.get_running_loop()
    while True:
        await loop.run_in_executor(None, initialize)
        dispatcher = await loop.run_in_executor(None, get_server_dispatcher)
        flag_avatar_changed.clear()
        async_server = osc_server.AsyncIOOSCUDPServer((parameter_multiplier_server_ip, parameter_multiplier_server_port),
                                                      dispatcher,
                                                      loop)
        transport, protocol = await async_server.create_serve_endpoint()
        print('server start')

        task = asyncio.create_task(resync_with_wait(20, loop))
        await flag_avatar_changed.wait()
        task.cancel()
        transport.close()
        print(f'get avatar reset signal: {changed_avatar_id}')


def running_osc_client(shared_queue_server_to_client, vrchat_running_pc_ip, vrchat_running_pc_port):
    client = udp_client.SimpleUDPClient(vrchat_running_pc_ip, vrchat_running_pc_port)
    need_queue_time_check_flag = False
    final_queue_get_time = None
    queue_timeout = 1
    previous_index = 0
    previous_value = 0

    while True:
        if not shared_queue_server_to_client.empty():
            index, value = shared_queue_server_to_client.get()
            if previous_index != index:
                client.send_message(f"{VRCHAT_OSC_PARAMETER_ROOT_ADDRESS}/{PARAMETER_MULTIPLIER_INDEX_VARIABLE_NAME}",
                                    index)
                client.send_message(f"{VRCHAT_OSC_PARAMETER_ROOT_ADDRESS}/{PARAMETER_MULTIPLIER_VALUE_VARIABLE_NAME}",
                                    value)

                previous_index = index
                previous_value = value
                print(f'send: {index}: {value}')
                time.sleep(0.7)
            elif previous_value != value:
                client.send_message(f"{VRCHAT_OSC_PARAMETER_ROOT_ADDRESS}/{PARAMETER_MULTIPLIER_VALUE_VARIABLE_NAME}",
                                    value)
                previous_value = value
                print(f'send: {index}: {value}')
            need_queue_time_check_flag = True
            final_queue_get_time = time.time()
        else:
            time.sleep(0.01)
            if need_queue_time_check_flag and time.time() - final_queue_get_time > queue_timeout:
                client.send_message(f"{VRCHAT_OSC_PARAMETER_ROOT_ADDRESS}/{PARAMETER_MULTIPLIER_INDEX_VARIABLE_NAME}",
                                    0)
                previous_index = 0
                need_queue_time_check_flag = False
                print(f'wait new value with animator initialize: 0: 0')


def initial_launch():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vrchat-running-pc-ip", default="127.0.0.1")
    parser.add_argument("--vrchat-running-pc-port", type=int, default=9000)
    parser.add_argument("--parameter-multiplier-server-ip", default="127.0.0.1")
    parser.add_argument("--parameter-multiplier-server-port", type=int, default=9001)
    return parser.parse_args()


if __name__ == "__main__":
    args = initial_launch()

    osc_client_process = Process(target=running_osc_client,
                                 args=(shared_queue_server_to_client, args.vrchat_running_pc_ip, args.vrchat_running_pc_port,))
    osc_client_process.start()

    asyncio.run(running_osc_server(args.parameter_multiplier_server_ip, args.parameter_multiplier_server_port))
