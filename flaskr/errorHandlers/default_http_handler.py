from http import HTTPStatus


def default_http_handler(e):
    message = e.description or "Some thing is wrong"
    status_code = (
        e.response.status_code if e.response else HTTPStatus.NOT_FOUND
    )

    return {"message": message, "status coe": status_code}, status_code
