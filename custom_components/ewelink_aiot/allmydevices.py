from ewelinkcloud import EWeLinkCloud
from aiohttp import ClientSession
import json
import asyncio
import sys


async def get_all_my_devices(server, username, password):
    session = ClientSession()
    cloud = EWeLinkCloud(session, server, username, password)
    if await cloud.async_login():
        await cloud.async_update_devices(all_families=False, all_devices=True)
        dev_list = []
        devices = cloud.devices
        if devices:
            for device in devices.values():
                dev_list.append(device.status)
            with open("./allmydevices.json", "w") as file:
                file.write(json.dumps(dev_list))
                file.close()
            print("Done, check allmydevices.json")
        else:
            print("No devices found in your family")
    else:
        print("Failed to login, check username or password")
    await session.close()

if len(sys.argv) != 4:
    sys.exit("\nUsage: python allmydevices.py server username password\n\n"
             "  server           Must be one of the following options:\n"
             "                   China\n"
             "                   Asian\n"
             "                   America\n"
             "                   Europe\n\n"
             "  username         Your eWeLink account name, phone-number or email.\n"
             "                   Phone-number needs to add country code such as: +86\n\n"
             "  password         Your eWeLink password.\n"
             )
loop = asyncio.get_event_loop()
loop.run_until_complete(get_all_my_devices(sys.argv[1], sys.argv[2], sys.argv[3]))
