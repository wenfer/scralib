def success(data=None):
    return {
        "code": 0,
        "data": data
    }


def fail(code, message):
    return {
        "code": code,
        "message": message
    }
