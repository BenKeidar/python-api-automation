from clients.base_client import BaseClient


class PostsClient(BaseClient):

    def __init__(self):
        super().__init__()
        self.resource = "/posts"

    def get_post(self, post_id):
        return self.request("GET", f"{self.resource}/{post_id}")

    def create_post(self, payload):
        return self.request("POST", self.resource, json=payload)

    def update_post(self, post_id, payload):
        return self.request("PUT", f"{self.resource}/{post_id}", json=payload)

    def patch_post(self, post_id, payload):
        return self.request("PATCH", f"{self.resource}/{post_id}", json=payload)

    def delete_post(self, post_id):
        return self.request("DELETE", f"{self.resource}/{post_id}")

    def get_posts(self):
        return self.request("GET", self.resource)
