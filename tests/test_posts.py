import allure
import pytest
from jsonschema import validate
from schemas.post_schema import POST_SCHEMA
from utils.allure_helpers import attach_response


@allure.feature("Posts API")
@allure.story("Get post by ID")
@allure.title("GET /posts/{post_id} returns a valid post")
@pytest.mark.parametrize(
    "post_id, expected_user_id",
    [
        pytest.param(1, 1, id="first-post-user-1"),
        pytest.param(2, 1, id="second-post-user-1"),
        pytest.param(3, 1, id="third-post-user-1"),
        pytest.param(11, 2, id="first-post-user-2"),
        pytest.param(21, 3, id="first-post-user-3"),
    ]
)
def test_get_post_by_id(posts_client, post_id, expected_user_id):
    with allure.step(f"Send GET request for post {post_id}"):
        response = posts_client.get_post(post_id)
        attach_response(response)

    with allure.step("Verify the response status code is 200"):
        assert response.status_code == 200

    data = response.json()
    with allure.step("Validate the response schema and post fields"):
        validate(instance=data, schema=POST_SCHEMA)
        assert data["id"] == post_id
        assert data["userId"] == expected_user_id
        assert data["title"] != ""


@allure.feature("Posts API")
@allure.story("Get missing post")
@allure.title("GET /posts/999999 returns 404")
def test_get_non_existing_post(posts_client):
    with allure.step("Send GET request for a non-existing post"):
        response = posts_client.get_post(999999)
        attach_response(response)

    with allure.step("Verify the response status code is 404"):
        assert response.status_code == 404


@allure.feature("Posts API")
@allure.story("Create post")
@allure.title("POST /posts creates a post and returns 201")
def test_create_post(posts_client):
    payload = {
        "title": "My first API test",
        "body": "Learning API automation with Python",
        "userId": 1
    }

    with allure.step("Send POST request to create a post"):
        response = posts_client.create_post(payload)
        attach_response(response)

    with allure.step("Verify the response status code is 201"):
        assert response.status_code == 201

    data = response.json()
    with allure.step("Verify the created post fields"):
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert data["userId"] == payload["userId"]
        assert "id" in data


@allure.feature("Posts API")
@allure.story("Update post")
@allure.title("PUT /posts/1 updates the post")
def test_update_post(posts_client):
    payload = {
        "id": 1,
        "title": "Updated post title",
        "body": "Updated post content",
        "userId": 1
    }

    with allure.step("Send PUT request to update post 1"):
        response = posts_client.update_post(1, payload)
        attach_response(response)

    with allure.step("Verify the response status code is 200"):
        assert response.status_code == 200

    data = response.json()
    with allure.step("Verify the updated post fields"):
        assert data["id"] == 1
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert data["userId"] == payload["userId"]


@allure.feature("Posts API")
@allure.story("Patch post")
@allure.title("PATCH /posts/1 updates the post title")
def test_patch_post_title(posts_client):
    payload = {
        "title": "Patched title"
    }

    with allure.step("Send PATCH request to update post 1 title"):
        response = posts_client.patch_post(1, payload)
        attach_response(response)

    with allure.step("Verify the response status code is 200"):
        assert response.status_code == 200

    data = response.json()
    with allure.step("Verify the patched title and remaining fields"):
        assert data["id"] == 1
        assert data["title"] == payload["title"]
        assert "body" in data
        assert "userId" in data


@allure.feature("Posts API")
@allure.story("Delete post")
@allure.title("DELETE /posts/1 returns 200 and an empty body")
def test_delete_post(posts_client):
    with allure.step("Send DELETE request for post 1"):
        response = posts_client.delete_post(1)
        attach_response(response)

    with allure.step("Verify the response status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify the response body is empty"):
        assert response.json() == {}


@allure.feature("Posts API")
@allure.story("Create post")
@allure.title("POST /posts without a title still returns 201")
def test_create_post_without_title(posts_client):
    payload = {
        "body": "Post without a title",
        "userId": 1
    }

    with allure.step("Send POST request to create a post without a title"):
        response = posts_client.create_post(payload)
        attach_response(response)

    with allure.step("Verify the response status code is 201"):
        assert response.status_code == 201

    data = response.json()
    with allure.step("Verify the created post has body and userId but no title"):
        assert data["body"] == payload["body"]
        assert data["userId"] == payload["userId"]
        assert "id" in data
        assert "title" not in data


@allure.title("Get all posts and validate response schema")
@allure.feature("Posts API")
@allure.story("Get posts list")
def test_get_posts_list(posts_client):
    with allure.step("Send GET request to /posts"):
        response = posts_client.get_posts()
        attach_response(response)

    with allure.step("Validate response status"):
        assert response.status_code == 200

    with allure.step("Validate posts list"):
        posts = response.json()

        assert isinstance(posts, list)
        assert len(posts) > 0

    with allure.step("Validate every post against POST_SCHEMA"):
        for post in posts:
            validate(instance=post, schema=POST_SCHEMA)