import traceback

import requests
from loguru import logger

#############################
# Requests Helper Functions #
#############################


def send_request(request_func):
    """A Decorator for requests module to prevent some exceptions

    Arguments:
        request_func {callable} -- function with requests.get, requests.post
    """

    def wrapper(*args, **kwargs):
        try:
            res = request_func(*args, **kwargs)
            status = res.status_code

            if status != 200:
                logger.warning(f"REQ UNAVAILABLE: {status}")

            return res

        except requests.exceptions.Timeout as error:
            logger.warning(f"UNAVAILABLE: Connection Timeout {error}")
        except requests.exceptions.ConnectionError as error:
            logger.warning(f"UNAVAILABLE: Connection Error {error}")
        except ConnectionRefusedError as error:
            logger.warning(f"UNAVAILABLE: Connection Refused Error {error}")
        except requests.exceptions.MissingSchema:
            logger.warning(f"UNAVAILABLE: URL Schema Error {traceback.format_exc()}")

    return wrapper


# pylint: disable=W0621
@send_request
def send_post_request(url, headers=None, data=None, json=None, timeout=60) -> requests.Response:
    if not headers:
        headers = {"Content-Type": "application/json"}
    return requests.post(url, headers=headers, data=data, json=json, timeout=timeout)


# pylint: enable=W0621


# pylint: disable=W0621
@send_request
def send_put_request(url, headers=None, data=None, json=None, timeout=60) -> requests.Response:
    if not headers:
        headers = {"Content-Type": "application/json"}
    return requests.put(url, headers=headers, data=data, json=json, timeout=timeout)


# pylint: enable=W0621


# pylint: disable=W0621
@send_request
def send_delete_request(url, headers=None, data=None, json=None, timeout=60) -> requests.Response:
    if not headers:
        headers = {"Content-Type": "application/json"}
    return requests.delete(url, headers=headers, data=data, json=json, timeout=timeout)


# pylint: enable=W0621


@send_request
def send_get_request(url, headers=None, data=None, params=None, timeout=60) -> requests.Response:
    return requests.get(url, headers=headers, data=data, params=params, timeout=timeout)
