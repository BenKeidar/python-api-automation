import allure
from jsonschema import validate
from schemas.user_schema import USER_SCHEMA
from utils.allure_helpers import attach_response


@allure.feature("Users API")
@allure.story("Get user by ID")
@allure.title("GET /users/1 returns a valid user")
def test_get_user_by_id(users_client):
    with allure.step("Send GET request for user 1"):
        response = users_client.get_user(1)
        attach_response(response)

    with allure.step("Verify the response status code is 200"):
        assert response.status_code == 200

    data = response.json()

    with allure.step("Validate the response against the user JSON Schema"):
        validate(instance=data, schema=USER_SCHEMA)

    with allure.step("Verify user id, name, and email"):
        assert data["id"] == 1
        assert data["name"] != ""
        assert "@" in data["email"]


@allure.feature("Users API")
@allure.story("Get missing user")
@allure.title("GET /users/999999 returns 404")
def test_get_non_existing_user(users_client):
    with allure.step("Send GET request for a non-existing user"):
        response = users_client.get_user(999999)
        attach_response(response)

    with allure.step("Verify the response status code is 404"):
        assert response.status_code == 404

    with allure.step("Verify the response body is empty"):
        assert response.json() == {}


@allure.feature("Users API")
@allure.story("List users")
@allure.title("GET /users returns a unique list of users")
def test_get_users_list(users_client):
    with allure.step("Send GET request for all users"):
        response = users_client.get_users()
        attach_response(response)

    with allure.step("Verify the response status code is 200"):
        assert response.status_code == 200

    users = response.json()
    with allure.step("Verify the users list shape and unique ids"):
        assert isinstance(users, list)
        assert len(users) > 0

        user_ids = []

        for user in users:
            assert "id" in user
            assert "name" in user
            assert "email" in user

            user_ids.append(user["id"])

        assert len(user_ids) == len(set(user_ids))


@allure.feature("Users API")
@allure.story("List vs user details")
@allure.title("GET /users and GET /users/1 return matching user fields")
def test_user_list_matches_user_details(users_client):
    with allure.step("Send GET request for all users"):
        list_response = users_client.get_users()
        attach_response(list_response, name="GET /users response")

    with allure.step("Send GET request for user 1"):
        details_response = users_client.get_user(1)
        attach_response(details_response, name="GET /users/1 response")

    with allure.step("Verify both responses have status code 200"):
        assert list_response.status_code == 200
        assert details_response.status_code == 200

    users = list_response.json()
    user_details = details_response.json()
    with allure.step("Verify list and details fields match for user 1"):
        user_from_list = next(
            user for user in users
            if user["id"] == 1
        )

        assert user_from_list["name"] == user_details["name"]
        assert user_from_list["email"] == user_details["email"]
        assert user_from_list["username"] == user_details["username"]
