POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {
            "type": "integer",
            "minimum": 1
        },
        "id": {
            "type": "integer",
            "minimum": 1
        },
        "title": {
            "type": "string",
            "minLength": 1
        },
        "body": {
            "type": "string",
            "minLength": 1
        }
    },
    "required": ["userId", "id", "title", "body"],
    "additionalProperties": False
}