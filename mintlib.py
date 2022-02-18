import requests


class Mintlib:

    def __init__(self, api: str):
        self.__api = api
        self.__token = None
        self.__master_api_key = None

    def call(self, method: str, path: str, data=None, wallet_key=None):
        request = {
            "GET":    requests.get,
            "PUT":    requests.put,
            "POST":   requests.post,
            "DELETE": requests.delete
        }
        request = request.get(method)

        if (wallet_key == None) and (self.__token != None):
            auth = (self.__token, self.__token)
        elif (wallet_key != None) and (self.__master_api_key != None):
            auth = (self.__master_api_key, wallet_key)
        else:
            auth = None
        return request(f"{self.__api}/{path}", json=data, auth=auth)

    def import_master_key(self, master_api_key: str):
        self.__master_api_key = master_api_key

    def create_user(self, username: str, password: str):
        return self.call("POST", "user/create", data={"username": username, "password": password}).json()

    def auth_user(self, username: str, password: str):
        auth = self.call(
            "POST", "user/auth", data={"username": username, "password": password}).json()
        self.__token = auth.get("token")
        return auth

    def get_user(self):
        return self.call("GET", "user").json()

    def change_password(self, new_password: str):
        return self.call("PUT", "user/change/password", data={"password": new_password}).json()

    def create_wallet(self, label: str):
        return self.call("POST", "wallet/create", data={"label": label}).json()

    def get_wallets(self):
        return self.call("GET", "/wallets").json()

    def get_wallet(self, wallet_id: str, wallet_read_key: str):
        return self.call("GET", f"wallet/{wallet_id}", wallet_key=wallet_read_key).json()

    def get_address(self, wallet_id: str, wallet_read_key: str, network="bitcoin"):
        return self.call("GET", f"wallet/{wallet_id}/receive?network={network}", wallet_key=wallet_read_key).json()

    def get_new_invoice(self, wallet_id: str, wallet_read_key: str, value: int, memo: str):
        return self.call("GET", f"wallet/{wallet_id}/receive?network=lightning", wallet_key=wallet_read_key, data={"value": value, "description": memo}).json()

    def rename_wallet(self, wallet_id: str, label: str):
        return self.call("PUT", f"wallet/{wallet_id}/rename", data={"label": label}).json()

    def delete_wallet(self, wallet_id: str):
        return self.call("DELETE", f"wallet/{wallet_id}/delete").json()

    def transfer(self, wallet_id: str, wallet_admin_key: str, destination: str, value: str, description: str):
        return self.call("POST", f"wallet/{wallet_id}/transfer", wallet_key=wallet_admin_key, data={"destination": destination, "value": value, "description": description}).json()

    def withdraw(self, wallet_id: str, wallet_admin_key: str, address: str, value: int, feerate: int, network="bitcoin"):
        return self.call("POST", f"wallet/{wallet_id}/withdraw/{network}", data={"address": address, "value": value, "feerate": feerate}, wallet_key=wallet_admin_key).json()

    def pay_invoice(self, wallet_id: str, wallet_admin_key: str, invoice: str):
        return self.call("POST", f"wallet/{wallet_id}/payinvoice", data={"invoice": invoice}, wallet_key=wallet_admin_key).json()

    def get_payments(self, wallet_id: str, wallet_read_key: str, offset=1):
        return self.call("GET", f"wallet/{wallet_id}/payments?offset={offset}", wallet_key=wallet_read_key).json()

    def get_payment(self, wallet_id: str, wallet_read_key: str, hash_id: str):
        return self.call("GET", f"wallet/{wallet_id}/payment/{hash_id}", wallet_key=wallet_read_key).json()
