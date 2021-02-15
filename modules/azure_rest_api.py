import msal


class AuthenticatorMSALAPIRequests:
    """
    Authentication class to call Azure REST API.
    """

    def __init__(self, client_id, client_secret, tenant_id, subscription_id, scope_list):
        self.client_id = client_id
        self.client_secret = client_secret
        self._authority = "https://login.microsoftonline.com/" + tenant_id
        self.subscription_id = subscription_id
        self.scope_list = scope_list
        self.access_token = None
        self.headers = None
        result = None

        msal_app = msal.ConfidentialClientApplication(self.client_id, client_credential=self.client_secret, authority=self._authority)

        result = msal_app.acquire_token_silent(scopes=self.scope_list, account=None)

        if not result:
            print("No suitable token exists in cache. Getting a new one from AAD.")
            result = msal_app.acquire_token_for_client(scopes=self.scope_list)

        if "access_token" in result:
            self.access_token = result["access_token"]
            self.headers = {'Authorization': 'Bearer ' + self.access_token,
                            'Content-Type': 'application/json',
                            }
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))
