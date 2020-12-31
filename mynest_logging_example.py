#!/usr/bin/python3
# encoding=utf-8

import sys
import time
import datetime
import mynest as nest
from mysql_controller_module import insert_record

delay = 12*60
nest.request_tokens()
status = 'None'
downstairsid = 'None'
LastStatus = 'None'
nestmode = 'None'
neststate = 'None'
Away = 'N/A'
FanRequest = 'None'
TargetHumidity = 45
tbedroom = float('NAN')
tdownstairs = float('NAN')
ttarget = float('NAN')
# humidity and dewpoint not added (yet) in this example
TempInside = float('NAN')
TempOutside = float('NAN')
DewPointInside = float('NAN')
DewPointOutside = float('NAN')
Hin = float('NAN')
Hout = float('NAN')
print("Python version", sys.version_info[0])
nest.request_tokens()
while True:
    try:
        downstairsid, bedroomid, downstairsthermid, bedroomthermid, \
            nestmode, downstairsecomode, bedroomecomode, neststate, ttarget, \
            tdownstairs, tbedroom = nest.get_device_status()
    except:
        print('Failed Nest query')   
    print('Tbedroom: %.1f' % tbedroom)
    print('Tdownstairs: %.1f' % tdownstairs)
    print('TTarget: %.1f' % ttarget)
    # control Nest Fan
    print('DeltaT = ', max([tbedroom, tdownstairs, ttarget]) - min([tbedroom, tdownstairs, ttarget]))
    if (nestmode == 'cool') and (neststate != 'cooling'):
        if max([tbedroom, tdownstairs, ttarget]) - min([tbedroom, tdownstairs, ttarget]) > 2:
            print('This is where we would turn on the fan')
            FanRequest = 'ON'
            nest.set_fan_mode(downstairsid, FanRequest)
        else:
            print('This is where we would turn off the fan')
            FanRequest = 'OFF'
            nest.set_fan_mode(downstairsid, FanRequest)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('Current date and time:', now)
    insert_record(now, TempInside, tdownstairs, tbedroom, TempOutside, DewPointInside,
                  DewPointOutside, Hin, Hout, TargetHumidity,
                  Status, Away, nestmode, neststate, FanRequest)
    print('sleep', delay/60, ' minutes')
    time.sleep(delay)
print('reached end')
