import requests
import allure


class BaseClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"
    TIMEOUT = 10

    def __init__(self):
        self.base_url = self.BASE_URL
        self.timeout = self.TIMEOUT

    def request(self, method, resource, **kwargs):
        url = f"{self.base_url}{resource}"

        try:
            return requests.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )
        except requests.exceptions.RequestException as exc:
            allure.attach(
                (
                    f"method: {method}\n"
                    f"url: {url}\n"
                    f"exception: {type(exc).__name__}\n"
                    f"error: {exc}"
                ),
                name="HTTP request error",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise
