# Based on: https://gist.github.com/joestump/615ecf8ce744999ad536d7cc4750babb

import requests
import json
import urllib3
from enum import Enum, auto

# Disable SSL verification warnings
urllib3.disable_warnings()


class UnifiControllerType(Enum):
    unifi_controller = auto()
    udm = auto


class UnifiPoEMode(Enum):
    off = auto()
    auto = auto()


UNIFI_LOGIN_PATH = "/api/auth/login"


class UnifiApi:
    def __init__(
        self,
        host,
        username,
        password,
        site="default",
        controller_type=UnifiControllerType.udm,
    ):
        self.host = host
        self.site = site
        self._username = username
        self._password = password
        self._session = requests.Session()
        self._csrf = ""
        self._controller_type = controller_type
        self.login()

    def login(self):
        payload = {
            "username": self._username,
            "password": self._password,
        }

        r = self._request(UNIFI_LOGIN_PATH, payload)
        return r.ok

    def _request(self, path, data={}, method="POST"):
        uri = "https://{}{}".format(self.host, path)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
        }

        if self._csrf:
            headers["X-CSRF-Token"] = self._csrf

        r = getattr(self._session, method.lower())(
            uri,
            headers=headers,
            json=data,
            verify=False,
            timeout=1,
        )
        try:
            self._csrf = r.headers["X-CSRF-Token"]
        except KeyError:
            pass

        return r

    def request(self, path, data={}, method="POST"):
        full_path = ""
        if self._controller_type == UnifiControllerType.udm:
            full_path += "/proxy/network"
        full_path += "/api/s/{}".format(self.site)
        full_path += path

        r = self._request(full_path, data, method)
        return json.loads(r.text)["data"]

    def get_switch_info(self, switch_mac):
        uri = "/stat/device/{}".format(switch_mac)
        switch_info = self.request(uri, method="GET")[0]
        return switch_info
