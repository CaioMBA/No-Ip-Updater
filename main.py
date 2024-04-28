import requests
import json
import base64
import time
import os


class Main:
    @staticmethod
    def clear_console() -> None:
        operational_system = os.name
        if operational_system == 'posix':
            os.system('clear')
        elif operational_system == 'nt':
            os.system('cls')

    @staticmethod
    def GetPublicIP() -> str:
        response = requests.get('https://api.ipify.org')
        return response.text

    @staticmethod
    def ReadAppSettings() -> dict:
        with open('AppSettings.json') as f:
            data = json.load(f)
        return data

    @staticmethod
    def UpdateAppSettings(newIP: str) -> None:
        with open('AppSettings.json', 'r+') as f:
            data = json.loads(f.read())
            data['CurrentIP'] = newIP
            f.truncate()
            f.seek(0)
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def EncodeToBase64(text: str) -> str:
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def UpdateNoIp(self, ip: str) -> str:
        settings = self.ReadAppSettings()
        if settings['CurrentIP'] == ip:
            return "IP is already up to date."
        url = f"https://dynupdate.no-ip.com/nic/update?hostname={settings['HostName']}&myip={ip}"
        BasicAuth = f"{settings['No-IP_Username']}:{settings['No-IP_Password']}"
        Headers = {
            "Authorization": f"Basic {self.EncodeToBase64(BasicAuth)}",
            "User-Agent": "NoIpUpdateIP/v1.0 caiombaraujo@gmail.com"
        }
        return requests.get(url, headers=Headers, timeout=10).text


if __name__ == '__main__':
    Service = Main()
    while True:
        try:
            Ip: str = Service.GetPublicIP()
            Response = Service.UpdateNoIp(Ip)
            Service.clear_console()
            if Response.__contains__('good'):
                Service.UpdateAppSettings(Ip)
                print("Response: Success - IP Updated")
            else:
                print(f"Response: {Response}")
            print(f"Current IP: {Ip}")
            print("Next update in 10 minutes")
            time.sleep(600)
        except Exception as e:
            print(f"Error: {e.args}")
            time.sleep(60)
