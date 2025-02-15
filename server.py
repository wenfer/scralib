from datetime import datetime

from robyn import Robyn, Response, logger, Request

from api.index import index_router

app = Robyn(__file__)

app.include_router(index_router)


class LoggingMiddleware:

    @classmethod
    def request_info(cls, request: Request):
        ip_address = request.ip_addr
        request_url = request.url.host
        request_path = request.url.path
        request_method = request.method
        request_time = str(datetime.now())

        return {
            "ip_address": ip_address,
            "request_url": request_url,
            "request_path": request_path,
            "request_method": request_method,
            "request_time": request_time,

        }

    @classmethod
    def response_info(cls, response: Response):
        status_code = response.status_code
        response_type = response.response_type

        return {
            "status_code": status_code,
            "response_type": response_type
        }


@app.before_request()
def log_request(request: Request):
    logger.info(f"Received request: %s",
                LoggingMiddleware.request_info(request))

    return request


@app.after_request()
def log_response(response: Response):
    logger.info(f"Sending response: %s",
                LoggingMiddleware.response_info(response))
    return response


if __name__ == "__main__":
    app.start(host="127.0.0.1", port=8000)
