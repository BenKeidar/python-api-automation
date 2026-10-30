from clients.base_client import BaseClient


class UsersClient(BaseClient):

    def __init__(self):
        super().__init__()
        self.resource = "/users"

    def get_user(self, user_id):
        return self.request("GET", f"{self.resource}/{user_id}")

    def get_users(self):
        return self.request("GET", self.resource)    