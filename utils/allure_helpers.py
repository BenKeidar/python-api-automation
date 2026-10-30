import json
import allure


def attach_response(response, name="HTTP Response"):
    try:
        body = response.json()
    except ValueError:
        body = response.text

    allure.attach(
        json.dumps(
            {
                "status_code": response.status_code,
                "body": body,
            },
            indent=2,
        ),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )
