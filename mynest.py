import requests
import json

# As instructed here: https://developers.google.com/nest/device-access/get-started
# register for access to the Google API with a Google user account (the app account) ($5 charge)
# https://console.nest.google.com/device-access
# have your Nest device registered to a google user account (mine are the same, but need not be)
# (the device account).
#    I have two nest thermostats, one is still in the old WorksWithNest setup.
#    I set up the other one in my google account.
# Allow access to the device in the device account
# in google credentials setup an OAuth https://console.developers.google.com/apis/credentials
# put them here

oauth2clientid = 'your oauth2clientid'
clientsecret = 'your clientsecret'

# with the app account create a project and give it the OAuth credentials
# save that here

projectid = 'your projectid'

# from the device account give access to the nest for the app account (even if they are the same)
# with this URL (make sure it is all one line, replace project-id and oauth2-client-id)
# https://nestservices.google.com/partnerconnections/project-id/auth?
# redirect_uri=https://www.google.com&
# access_type=offline&
# prompt=consent&
# client_id=oauth2-client-id&
# response_type=code&
# scope=https://www.googleapis.com/auth/sdm.service
#
# you will get a response:
# https://www.google.com?code=authorization_code&scope=https://www.googleapis.com/auth/sdm.service
#
# save the code here:

authorization_code = 'your authorization_code'

# now this module is ready to use
# tokens are saved in a file and kept as module globals while running the module
access_token = ''
refresh_token = ''


# Now we can request an access code and refresh code
# this only works once, so we have to save/saved the results. See if we have results already


def request_tokens():
    global oauth2clientid
    global clientsecret
    global access_token
    global refresh_token
    try:
        with open('.mynest.json') as json_file:
            data = json.load(json_file)
            access_token = data['access_token']
            refresh_token = data['refresh_token']
            print('access token:', access_token)
            print('refresh token:', refresh_token)
    except FileNotFoundError:
        request_token_url = 'https://www.googleapis.com/oauth2/v4/token'
        params = {'client_id': oauth2clientid,
                  'client_secret': clientsecret,
                  'code': authorization_code,
                  'grant_type': 'authorization_code',
                  'redirect_uri': 'https://www.google.com'}
        request_token_resp = requests.post(request_token_url, params=params)
        print(json.dumps(request_token_resp.content, indent=4))
        if request_token_resp.status_code != 200:
            print(request_token_resp.status_code)
        else:
            access_token = request_token_resp.json()['access_token']
            refresh_token = request_token_resp.json()['refresh_token']
            print('access token:', access_token)
            print('refresh token:', refresh_token)
            # safe the tokens in a json file
            with open('.mynest.json', 'w') as json_file:
                json.dump(request_token_resp.json(), json_file)


# access token is valid for an hour then you need to request new one


def refresh_access():
    global access_token
    refresh_url = 'https://www.googleapis.com/oauth2/v4/token?'
    params = {'client_id': oauth2clientid,
              'client_secret': clientsecret,
              'refresh_token': refresh_token,
              'grant_type': 'refresh_token'}
    refresh_resp = requests.post(refresh_url, params=params)
    if refresh_resp.status_code != 200:
        print(refresh_resp.status_code)
    else:
        print(json.dumps(refresh_resp.json(), indent=4))
        access_token = refresh_resp.json()['access_token']
        print('new access token:', access_token)


# now you can get data:


def get_device_status():
    url = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + projectid + '/devices'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(resp.status_code)
        refresh_access()
        print(access_token)
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
        print(headers)
        resp = requests.get(url, headers=headers)
    print('content = ', json.dumps(resp.json(), indent=4))
    nest = resp.json()
    deviceid = nest['devices'][0]['name']
    print('Device Type:', nest['devices'][0]['type'])
    roomkey = nest['devices'][0]['assignee']
    print('Device Traits:', nest['devices'][0]['traits'])
    print('Humidity:', nest['devices'][0]['traits']['sdm.devices.traits.Humidity']['ambientHumidityPercent'])
    nestmode = nest['devices'][0]['traits']['sdm.devices.traits.ThermostatMode']['mode']
    ecomode = nest['devices'][0]['traits']['sdm.devices.traits.ThermostatEco']['mode']
    neststate = nest['devices'][0]['traits']['sdm.devices.traits.ThermostatHvac']['status']
    if ecomode == 'OFF':
        ttarget = nest['devices'][0]['traits']['sdm.devices.traits.ThermostatTemperatureSetpoint'][
                      'heatCelsius'] * 9 / 5 + 32
    else:
        ttarget = float('NAN')
    temperature = nest['devices'][0]['traits']['sdm.devices.traits.Temperature'][
                      'ambientTemperatureCelsius'] * 9 / 5 + 32
    return roomkey, deviceid, nestmode, neststate, ttarget, temperature, ecomode


# structures are quite limited, all you can get it the name


def get_structure_status():
    url = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + projectid + '/structures'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(resp.status_code)
        refresh_access()
        print('New access token:', access_token)
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
        resp = requests.get(url, headers=headers)
    print("Structure:", json.dumps(resp.json(), indent=4))
    structure = resp.json()['structures'][0]['traits']['sdm.structures.traits.Info']['customName']
    return structure


# rooms are quite limited, all you can get is the name


def get_room_status(roomid):
    url = 'https://smartdevicemanagement.googleapis.com/v1/' + roomid
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(resp.status_code)
        refresh_access()
        print('New access token:', access_token)
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
        resp = requests.get(url, headers=headers)
        print(resp.status_code)
    roomname = resp.json()['traits']['sdm.structures.traits.RoomInfo']['customName']
    return roomname


# execute a command


def set_eco_mode(deviceid, ecomode):
    url = 'https://smartdevicemanagement.googleapis.com/v1/' + deviceid + ':executeCommand'
    print('url:', url)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    data = {'command': 'sdm.devices.commands.ThermostatEco.SetMode',
            'params': {'mode': ecomode}}
    # data = {'command': 'sdm.devices.commands.ThermostatMode.SetMode',
    #        'params': {'mode': 'HEAT'}}
    resp = requests.post(url, headers=headers, data=json.dumps(data))
    print(resp.status_code)
    print("execute_response:", resp.content)


def set_fan_mode(deviceid, fanmode):
    url = 'https://smartdevicemanagement.googleapis.com/v1/' + deviceid + ':executeCommand'
    print('url:', url)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    data = {'command': 'sdm.devices.traits.Fan',
            'params': {'timerMode': fanmode}}
    resp = requests.post(url, headers=headers, data=json.dumps(data))
    print(resp.status_code)
    print("execute_response:", resp.content)


def main():
    request_tokens()
    roomid, deviceid, nestmode, neststate, ttarget, temperature, ecomode = get_device_status()
    myhouse = get_structure_status()
    myroom = get_room_status(roomid)
    print('===============End Result============')
    print('Myhouse:', myhouse)
    print('Myroom:', myroom)
    print('Temperature:', temperature)
    print('NestMode:', nestmode)
    print('NestState:', neststate)
    print('TTarget:', ttarget)
    print('ECO Mode: ', ecomode)
    if ecomode == 'MANUAL_ECO':
        set_eco_mode(deviceid, 'OFF')


if __name__ == '__main__':
    main()

# end of file
