# Imports
import logging
import requests                 # Perform http/https requests
from bs4 import BeautifulSoup   # Parse HTML pages
import json                     # Needed to print JSON API data
import datetime
import calendar
import const

_LOGGER = logging.getLogger(__name__)

class GreentelClient:
    def __init__(self, phoneNo, password):
        self._phoneNo = phoneNo
        self._password = password
        self._session = None
        self._subscriptions = {}
        self._subscribers = {}
        self._consumptionPackage = {}
        self._consumptionPackageUser = {}

    def login(self):
        self._session = requests.Session()
        url = const.BASE_URL
        response = self._session.get(url)

        payload = { '__RequestVerificationToken': '', 'PhoneNo': self._phoneNo, 'Password': self._password}
        html = BeautifulSoup(response.text, "html.parser")
        url = url + html.form['action']
        for input in html.find_all('input'):
            if (input.has_attr('name') and input['name'] == '__RequestVerificationToken'):
                payload['__RequestVerificationToken'] = input['value']
        response = self._session.post(url, data = payload)

        payload = {
          'PageId': const.GET_INFO_PAGE_ID
        }
        response = self._session.get(const.BASE_URL + const.GET_INFO, params = payload).json()
        if response[const.SUCCESS_STR] and len(response[const.DATA_STR]) > 0:
            self._token = response[const.DATA_STR][0][const.TOKEN_STR]

    def getSubscriptions(self):
        if self._token:
            payload = {
              'PageId': const.GET_INFO_PAGE_ID
            }
            response = self._session.get(const.BASE_URL + const.GET_INFO, params = payload).json()
            if response[const.SUCCESS_STR] and len(response[const.DATA_STR]) > 0:
                for subscription in response[const.DATA_STR]:
                    if subscription['Subscription'] not in self._subscriptions:
                        self._subscriptions[subscription['Subscription']] = {}
                        self._subscriptions[subscription['Subscription']]['Users'] = []
                    self._subscriptions[subscription['Subscription']]['Balance'] = subscription['Balance']
                    self._subscriptions[subscription['Subscription']]['Users'].append(subscription['PhoneNumber'])

                    if subscription['PhoneNumber'] not in self._subscribers:
                        self._subscribers[subscription['PhoneNumber']] = {}
                    self._subscribers[subscription['PhoneNumber']] = subscription['User']['Username']

    def getConsumptionPackage(self):
        if self._token:
            payload = {
              'PageId': const.GET_INFO_PAGE_ID,
              'Token': self._token,
              'PhoneNo': ''
            }
            response = self._session.post(const.BASE_URL + const.GET_PACKAGE, data = payload).json()
            if response[const.SUCCESS_STR] and len(response[const.DATA_STR]) > 0:
                groupFields = ['AmountTotal', 'AmountLeft', 'AmountUsed', 'UnitGauge', 'FreeConsumption']
                for group in response['Data']['Consumption']:
                    groupName = group['TextGauge'].split()[0]
                    if len(groupName) > 3:
                        groupName = groupName.title()
                    self._consumptionPackage[groupName] = {}
                    for groupField in groupFields:
                        self._consumptionPackage[groupName][groupField] = group[groupField]

    def getConsumptionUser(self, phoneNo):
        if self._token:
            now = datetime.datetime.now()
            year = now.strftime("%Y")
            month = now.strftime("%m")
            payload = {
              'PageId': const.GET_DETAILS_PAGE_ID,
              'Token': self._token,
              'PhoneNo': phoneNo,
              'Type': 'Normal',
              'FromDate': year + "-" + month + "-01",
              'ToDate': year + "-" + month + "-" + str(calendar.monthrange(int(year), int(month))[1])
            }
            response = self._session.get(const.BASE_URL + const.GET_DETAILS, params = payload).json()
            if response[const.SUCCESS_STR] and len(response[const.DATA_STR]) > 0:
                for group in response['Data']['Consumption']['Items']:
                    groupName = group['Description']
                    Qty = group['Qty']
                    if phoneNo not in self._consumptionPackageUser:
                        self._consumptionPackageUser[phoneNo] = {}
                    if groupName != 'Abonnement':
                        if groupName == 'Opkald og samtaler':
                            groupName = 'Tale'
                            QtySplit = Qty.split(':')
                            Qty = (int(QtySplit[0]) * 3600) + (int(QtySplit[1]) * 60) + int(QtySplit[2])
                        self._consumptionPackageUser[phoneNo][groupName] = int(Qty)

    def getConsumptionAllUsers(self):
        for user in self._subscribers:
            self.getConsumptionUser(user)

# client = GreentelClient('25563311', 'Kar2ffel!')

# client.login()

# client.getSubscriptions()

# client.getConsumptionPackage()

# client.getConsumptionAllUsers()

# print(json.dumps(client._subscriptions, indent=4))
# print(json.dumps(client._subscribers, indent=4))
# print(json.dumps(client._consumptionPackage, indent=4))
# print(json.dumps(client._consumptionPackageUser, indent=4))
