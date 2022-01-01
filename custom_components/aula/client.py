"""Aula client"""
import logging
import requests
import time
import datetime
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from .const import API
from .const import AULA_LOGIN_URL
from .const import AULA_LOGIN_OK_URL

_LOGGER = logging.getLogger(__name__)

class Client:
  def __init__(self, username, password):
    self._username = username
    self._password = password
    self._session = None

  def login(self):
    self._session = requests.Session()
    response = self._session.get('https://login.aula.dk/auth/login.php?type=unilogin')
    
    user_data = { 'username': self._username, 'password': self._password }
    redirects = 0
    success = False
    url = ''
    while success == False and redirects < 10:
      html = BeautifulSoup(response.text, 'lxml')
      url = html.form['action']
      post_data = {}
      for input in html.find_all('input'):
        if(input.has_attr('name') and input.has_attr('value')):
          post_data[input['name']] = input['value']
          for key in user_data:
            if(input.has_attr('name') and input['name'] == key):
              post_data[key] = user_data[key]

      response = self._session.post(url, data = post_data)
      success = response.url == AULA_LOGIN_OK_URL
      redirects += 1

    self._profiles = self._session.get(API + "?method=profiles.getProfilesByLogin").json()["data"]["profiles"]
    self._session.get(API + "?method=profiles.getProfileContext&portalrole=guardian")
    _LOGGER.debug("LOGIN: " + str(success))

  def update_data(self):
    is_logged_in = False
    if self._session:
      response = self._session.get(API + "?method=profiles.getProfilesByLogin").json()
      is_logged_in = response["status"]["message"] == "OK"
    
    _LOGGER.debug("is_logged_ind? " + str(is_logged_in))
    
    if not is_logged_in:
      self.login()

    # INSTITUTIONS AND CHILDREN
    self._institutions = []
    self._institution_profiles = []
    self._childrenIds = []
    self._children = []
    params = {
      'method': 'profiles.getProfileContext',
      'portalrole': 'guardian'
    }
    response = self._session.get(API, params=params).json()
    for institution in response['data']['institutions']:
      self._institutions.append(institution['institutionCode'])
      self._institution_profiles.append(institution['institutionProfileId'])
      for child in institution['children']:
        self._childrenIds.append(child['id'])
        self._children.append(child)

    # DAILY OVERVIEW
    # Declare a empty dictionary for the overview
    self._daily_overview = {}
    # Loop through the children
    for i, child in enumerate(self._children):
      # Retrieve the overview for the current child
      response = self._session.get(API + "?method=presence.getDailyOverview&childIds[]=" + str(child["id"])).json()
      if len(response["data"]) > 0:
        self._daily_overview[str(child["id"])] = response["data"][0]

    # NOTIFICATIONS
    # Declare a empty dictonary of notifications
    self._notifications = {}
    params = {
      'method': 'notifications.getNotificationsForActiveProfile',
      'activeChildrenIds[]': self._childrenIds,
      'activeInstitutionCodes[]': self._institutions
    }
    response = self._session.get(API, params=params).json()
    # Loop through all the notifications
    for notification in response['data']:
      # Extract the type of notification
      eventType = str(notification['notificationEventType'])
      # If the type is NOT set yet, then initialize it with a empty array
      if eventType not in self._notifications:
        self._notifications[eventType] = []
      # Append the notification
      self._notifications[eventType].append(notification)

    # AlBUMS
    self._albums = {}
    params = {
      'method': 'gallery.getAlbums',
      'index': '0',
      'limit': '9999'
    }
    response = self._session.get(API, params=params).json()
    for album in response['data']:
      # Extract the institutionCode
      institutionCode = str(album['creator']['institutionCode'])
      # If the institutionsCode is NOT set yet, the initialize it with a empty array 
      if institutionCode not in self._albums:
        self._albums[institutionCode] = []
      # Append the message
      self._albums[institutionCode].append(album)

    # # MORE MESSAGES
    # Works, but is slow
    # # Declare a empty dictonary of messages
    # self._messages = {}
    # moreMessages = True
    # pageNumber = 0
    # while moreMessages == True:
    #   params = {
    #     'method': 'messaging.getThreads',
    #     'sortOn': 'date',
    #     'orderDirection': 'desc',
    #     'page': pageNumber
    #   }
    #   response = self._session.get(API, params=params).json()
    #   moreMessages = response['data']['moreMessagesExist']
    #   pageNumber += 1
    #   for message in response['data']['threads']:
    #     # Extract the institutionCode
    #     institutionCode = str(message['institutionCode'])
    #     # If the institutionsCode is NOT set yet, the initialize it with a empty array 
    #     if institutionCode not in self._messages:
    #       self._messages[institutionCode] = []
    #     # Append the message
    #     self._messages[institutionCode].append(message)

    #TODO: Week plan
    #total_weeks = 4
    #now = datetime.datetime.now()
    #from_date = (now - datetime.timedelta(days = (now).weekday())).strftime("%Y-%m-%d")
    #to_date = (now + datetime.timedelta(days = (7 * total_weeks) - (now).weekday())).strftime("%Y-%m-%d")
    #week_plan = requests.get("https://www.aula.dk/api/v11/?method=presence.getPresenceTemplates&filterInstitutionProfileIds[]=" + str(child_id) + "&fromDate=" + from_date + "&toDate=" + to_date, cookies=s.cookies).json()#["data"]["presenceWeekTemplates"][0]

    return True