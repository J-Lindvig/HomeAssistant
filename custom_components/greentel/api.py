# Imports
import logging

import requests                 # Perform http/https requests
from bs4 import BeautifulSoup   # Parse HTML pages
import json                     # Needed to print JSON API data
import datetime
import calendar

from .const import (
	BASE_URL,
	INPUT_TOKEN,
	INPUT_PHONE_NO,
	INPUT_PASSWORD,
	GET_INFO_PAGE_URL,
	GET_INFO_PAGE_ID,
	GET_PACKAGE_PAGE_URL,
	GET_DETAILS_PAGE_URL,
	GET_DETAILS_PAGE_ID,
	HA_SPACE,
	HA_TOTAL,
	PL_DATE_FROM,
	PL_DATE_TO,
	PL_PAGE_ID,
	PL_PHONE_NO,
	PL_TOKEN,
	PL_TYPE,
	PL_TYPE_VAL,
	R_BALANCE,
	R_CALLS_TALKS,
	R_CONSUMPTION,
	R_ITEMS,
	R_PHONENUMBER,
	R_QUANTITY,
	R_DATA,
	R_DATE,
	R_DESCRIPTION,
	R_SUBSCRIPTION,
	R_SUBSCRIPTION_DK,
	R_SUCCESS,
	R_TALK,
	R_TEXT_GAUGE,
	R_TOKEN,
	R_TOTAL,
	R_USER,
	R_USERNAME,
	STR_NAME,
	STR_PACKAGE,
	STR_TALK,
	STR_USED,
	STR_USERS,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)
_LOGGER = logging.getLogger(__name__)

class greentelClient:
	def __init__(self, phoneNo, password):
		self._session = None
		self._phoneNo = phoneNo
		self._password = password
		self._token = None
		self._subscriptions = []
		self._users = {}
		self._packageAndConsumption = {}

	# Login, what else...
	def login(self):
		# Prepare a new session and get the webpage with the login form (BASE_URL)
		self._session = requests.Session()
		r = self._session.get(BASE_URL)

		if r.status_code == 200:
			"""
			Parse the HTML code.
			Initialize payload containing the name of the <INPUT> of the given token
			and the phonenumber and password from the configuration

			Extract the URL of the form and append it to the BASE_URL
			Loop through the <INPUT> tags until we find the one with our token
			Append the token to our payload and break the loop

			POST our payload to the loginpage
			"""
			html = BeautifulSoup(r.text, "html.parser")
			payload = {
				INPUT_TOKEN: '',
				INPUT_PHONE_NO: self._phoneNo,
				INPUT_PASSWORD: self._password
			}
			for input in html.find_all('input'):
				if (input.has_attr('name') and input['name'] == INPUT_TOKEN):
					payload[INPUT_TOKEN] = input['value']
					break
			r = self._session.post(BASE_URL + html.form['action'], data = payload)

			"""
			Prepare a new payload with the PageId of the landing page
			GET the response from the payload
			If the response is successful, store the token anf return true
			"""
			r = self._getStartPage().json()
			if self._responseOK(r):
				self._token = r[R_DATA][0][R_TOKEN]
			return self._token
		else:
			_LOGGER.debug("[Login] : " + str(r.status_code))

	def getData(self):
		loggedIn = False

		if self._session:
			r = self._getStartPage().json()
			loggedIn = r[R_SUCCESS]

		if not loggedIn:
			self.login()

		# Call the subfunctions and extract the data
		self._getSubscriptions()
		self._getConsumption()

		return True

	# Repeated function testing if the reponse is OK
	# Returns boolean
	def _responseOK(self, response, values = {R_SUCCESS, R_DATA}):
		if values.issubset(response):
			return response[R_SUCCESS] and len(response[R_DATA]) > 0
		return False

	# Repeated request to the startpage
	# Returns the response as JSON
	def _getStartPage(self):
		payload = { PL_PAGE_ID: GET_INFO_PAGE_ID }
		r = self._session.get(BASE_URL + GET_INFO_PAGE_URL, params = payload)
		return r

	# Retrieve all our subscriptions and the users attached to the subscription
	def _getSubscriptions(self):
		# Reset the list - error occurs it not
		self._subscriptions = []
		# Prepare the payload and GET the response
		r = self._getStartPage().json()

		if self._responseOK(r):
			# Prepare a dict of uniqueId of subscritions and a placeholder for the current index.
			uniqueIdList = {}
			idx = 0
			# Loop through all our subsciptions
			for subscription in r[R_DATA]:
				# If the subscription is NOT in the list of uniqueIds
				if subscription[R_SUBSCRIPTION] not in uniqueIdList:
					# Update the index
					idx = len(uniqueIdList)
					# Add the index at the subscriptions place in 
					uniqueIdList[subscription[R_SUBSCRIPTION]] = idx

					# Create a empty dictionary and append it to our list of subscriptions
					# Make a empty array at the current index for our users
					aDict = {}
					self._subscriptions.append(aDict)
					self._subscriptions[idx][STR_USERS] = []

				# Get the index of current subscription and populate it with:
				# Name of the subscription, the balance and append the users phonenumber
				idx = uniqueIdList[subscription[R_SUBSCRIPTION]]
				self._subscriptions[idx][STR_NAME] = subscription[R_SUBSCRIPTION]
				self._subscriptions[idx][R_BALANCE] = subscription[R_BALANCE]
				self._users[subscription[R_PHONENUMBER]] = subscription[R_USER][R_USERNAME]
				self._subscriptions[idx][STR_USERS].append(
					{ R_USERNAME: subscription[R_USER][R_USERNAME], R_PHONENUMBER: subscription[R_PHONENUMBER] }
				)
				
				# Store the username in a dictionary with the phonenumber as key

	# Get the total consumption in the package
	def _getConsumptionPackage(self, phoneNo):
		# Prepare and POST the payload
		payload = {
			PL_PAGE_ID: GET_INFO_PAGE_ID,
			PL_TOKEN: self._token,
			PL_PHONE_NO: phoneNo
		}
		r = self._session.post(BASE_URL + GET_PACKAGE_PAGE_URL, data = payload).json()
		if self._responseOK(r):
			# Loop through the different elements of consumption
			for group in r[R_DATA][R_CONSUMPTION]:
				Qty = int(group[R_TOTAL])
				# Extract the name
				groupName = group[R_TEXT_GAUGE].split()[0]
				if len(groupName) > 3:
					groupName = groupName.title()
				if groupName == R_DATA:
					Qty = Qty * 1024
				elif groupName == R_TALK:
					groupName = STR_TALK
					Qty = Qty * 3600

				self._packageAndConsumption[phoneNo][STR_PACKAGE][groupName] = int(Qty)

	# Get a users consumption in the current month
	# Supply the phonenumber of the user
	def _getConsumptionUser(self, phoneNo):
		# Prepare some DATE variables for the payload
		now = datetime.datetime.now()
		year = now.strftime("%Y")
		month = now.strftime("%m")
		payload = {
			PL_PAGE_ID: GET_DETAILS_PAGE_ID,
			PL_TOKEN: self._token,
			PL_PHONE_NO: phoneNo,
			PL_TYPE: PL_TYPE_VAL,
			PL_DATE_FROM: year + "-" + month + "-01",
			PL_DATE_TO: year + "-" + month + "-" + str(calendar.monthrange(int(year), int(month))[1])
		}
		# Get the reponse
		r = self._session.get(BASE_URL + GET_DETAILS_PAGE_URL, params = payload).json()

		if self._responseOK(r):
			# Loop through the different elements of consumption
			for group in r[R_DATA][R_CONSUMPTION][R_ITEMS]:
				# Extract the name and quantity of the consumption
				groupName = group[R_DESCRIPTION]
				Qty = group[R_QUANTITY]
				# Ignore "Abonnement"
				if groupName != R_SUBSCRIPTION_DK:
					# If the consumption is Voice, then overrule the name and
					# convert the HH:MM:SS to seconds
					if groupName == R_CALLS_TALKS:
						groupName = STR_TALK
						h, m, s = Qty.split(':')
						Qty = int(h) * 3600 + int(m) * 60 + int(s)
					elif groupName == R_DATA:
						lastestDate = group[R_ITEMS][-1][R_DATE]
						self._packageAndConsumption[phoneNo][R_DATE] = lastestDate
						_LOGGER.debug("[lastestDate " + str(phoneNo) + " ] : " + str(lastestDate))

					self._packageAndConsumption[phoneNo][STR_USED][groupName] = int(Qty)

	def _getConsumption(self):
		for subscription in self._subscriptions:
			for user in subscription[STR_USERS]:
				# Prepare the dictionasry with the phonenumber
				self._packageAndConsumption[user[R_PHONENUMBER]] = { STR_PACKAGE: {}, STR_USED: {} }
				self._getConsumptionPackage(user[R_PHONENUMBER])
				self._getConsumptionUser(user[R_PHONENUMBER])
