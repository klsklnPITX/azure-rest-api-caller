from dotenv import load_dotenv
import os
import requests
import json

# Import authentication class
from modules.azure_rest_api import AuthenticatorMSALAPIRequests


# Load .env file
load_dotenv()

# Get .env variables or declare variables here with according inputs
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")


# Create a class with desired API calls which inherits from AuthenticatorMSALAPIRequests.
class MyAzureAPICallerClass(AuthenticatorMSALAPIRequests):
    """
    Class with all required methods to call the desired Azure API endpoints.
    """

    # Define desired methods here
    # EXAMPLES:

    def get_call(self, url):
        """
        Simple example GET call. 
        Takes the desired GET URL.
        Returns json data.
        """
        r = requests.get(url=url, headers=self.headers)
        data = json.loads(json.dumps(r.json()))
        return data

    def get_all_resource_groups(self):
        """
        Get all resource groups within the subscription.
        """
        url = f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/"
        params = {'api-version': '2020-10-01'}
        headers = self.headers
        r = requests.get(url, headers=headers, params=params)
        data_rgs = json.loads(json.dumps(r.json()))
        return data_rgs


# Instantiate the class
api_caller = MyAzureAPICallerClass(CLIENT_ID,
                                   CLIENT_SECRET,
                                   TENANT_ID,
                                   SUBSCRIPTION_ID,
                                   scope_list=["https://management.azure.com/.default"])

# Simple get call with URL as parameter
prices_data = api_caller.get_call(
    "https://prices.azure.com/api/retail/prices?$filter=priceType eq 'Reservation' and location eq 'EU West'&$top=50"
)

# Get all resource groups within the subscription
resource_group_data = api_caller.get_all_resource_groups()
