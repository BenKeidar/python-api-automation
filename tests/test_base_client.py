import pytest
import requests
import allure
from unittest.mock import patch

from clients.base_client import BaseClient


@allure.title("BaseClient handles HTTP timeout correctly")
@allure.feature("HTTP Client")
@allure.story("Error Handling")
def test_request_timeout_is_logged_and_raised():
    client = BaseClient()

    with patch(
        "clients.base_client.requests.request",
        side_effect=requests.exceptions.ReadTimeout("Simulated timeout")
    ) as mock_request:

        with pytest.raises(requests.exceptions.ReadTimeout):
            client.request("GET", "/posts/1")

        mock_request.assert_called_once()