import os
import datetime
import asyncio
import logging
import time
import getpass
import requests

from pyeconet import EcoNetApiInterface
from pyeconet.equipment import EquipmentType
from pyeconet.equipment.water_heater import WaterHeaterOperationMode

logging.basicConfig()
# disable logging to prevent info leak
# logging.getLogger().setLevel(logging.DEBUG)

def logEconet(date, time, enabled, mode, set_temp):
    account_id = os.environ["GIT_D1_ACCOUNT"]
    database_id = os.environ["GIT_D1_DATABASE"]
    key_secrete = os.environ["GIT_D1_DATABASE_API_KEY"]

    url = 'https://api.cloudflare.com/client/v4/accounts/' + account_id + '/d1/database/'+database_id+'/query'
    headers = {
        "Content-Type": "Content-Type: application/json",
        "Authorization": "Bearer " + key_secrete
    }
    data = {
      "sql": "INSERT INTO econet VALUES ('" + date + "','" + time + "','" +enabled+ "','" +mode+ "','" + set_temp + "')"
    }

    # print(data)
    response = requests.post(url, headers=headers, json = data)
    # print("JSON Response ", response.json())

async def main():
    email = os.environ['GIT_ECONET_USERNAME']
    password = os.environ['GIT_ECONET_PASSWORD']
    api = await EcoNetApiInterface.login(email, password=password)
    all_equipment = await api.get_equipment_by_type(
        [EquipmentType.WATER_HEATER, EquipmentType.THERMOSTAT]
    )
    # api.subscribe()
    # await asyncio.sleep(5)
    for equip_list in all_equipment.values():
        for equipment in equip_list:
            print(f"Name: {equipment.device_name}")
            print(f"Set point: {equipment.set_point}")
            print(f"Supports modes: {equipment._supports_modes()}")
            print(f"Operation modes: {equipment.modes}")
            print(f"Operation mode: {equipment.mode}")
            print(f"Operation status: {equipment.active}")
            date = datetime.date.today()
            time = datetime.datetime.now().time()
            logEconet(str(date),str(time),str(equipment.active),str(equipment.mode),str(equipment.set_point))

    # await equipment.get_energy_usage()
    # print(f"{equipment.todays_energy_usage}")
    # equipment.set_set_point(equipment.set_point + 1)
    # equipment.set_mode(OperationMode.ELECTRIC_MODE)
    # await asyncio.sleep(300000)
    # api.unsubscribe()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
