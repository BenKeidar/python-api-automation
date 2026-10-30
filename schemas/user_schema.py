USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "minimum": 1
        },
        "name": {
            "type": "string",
            "minLength": 1
        },
        "email": {
            "type": "string",
            "minLength": 1
        },
        "username": {
            "type": "string",
            "minLength": 1
        },
        "address": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "minLength": 1
                },
                "geo": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"}
                    },
                    "required": ["lat", "lng"]
                }
            },
            "required": ["city", "geo"]
        },
        "company": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 1
                },
                "catchPhrase": {
                    "type": "string"
                },
                "bs": {
                    "type": "string"
                }
            },
            "required": ["name", "catchPhrase", "bs"]
        }
    },
    "required": ["id", "name", "email", "username", "address", "company"]
}