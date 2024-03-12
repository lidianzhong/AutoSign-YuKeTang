import requests

def get_beijing_time():
    try:
        response = requests.get('https://timeapi.io/api/Time/current/zone?timeZone=Asia/Shanghai')
        if response.status_code == 200:
            data = response.json()
            beijing_time = data['dateTime']
            return beijing_time
        else:
            print("Failed to retrieve data from the API")
    except Exception as e:
        print("An error occurred:", e)


