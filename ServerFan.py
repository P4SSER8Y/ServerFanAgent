from requests import get, post, put
from urllib.parse import urljoin
import logging
import json

### create a file named "secret.py" and define following variables
### url=r"<api_base_url>"
### token=r"<your_agent_token>""
import secret

logger = logging.getLogger("ServerFan")


API_GET_JOB = "/agent/job"
API_AUTO_MESSAGE = "/agent/message/auto"
API_REPORT_SUCCESS = "/agent/jobs/{id}/succeed"
API_REPORT_FAIL = "/agent/jobs/{id}/fail"
API_REPORT_RUNNING = "/agent/jobs/{id}/running"
HEADER = {
    "Authorization": f"Bearer {secret.token}",
}


def get_job():
    ret = get(urljoin(secret.url, API_GET_JOB), headers=HEADER)
    if ret.status_code == 200:
        return json.loads(ret.content)
    else:
        return None


def report_succeed(id=None, result=None):
    if id is None:
        logger.error("please provide id")
        return
    data = {"result": result}
    url = urljoin(secret.url, API_REPORT_SUCCESS.format(id=id))
    ret = put(url=url, headers=HEADER, data=data)
    if ret.ok:
        logger.debug(f"send succeed message done with ret_code={ret.status_code}")
    else:
        logger.debug(f"content: {ret.content}")
        logger.error(f"send succeed message failed with ret_code={ret.status_code}")


def report_fail(id=None, result=None):
    if id is None:
        logger.error("please provide id")
        return
    data = {"result": result}
    url = urljoin(secret.url, API_REPORT_FAIL.format(id=id))
    ret = put(url=url, headers=HEADER, data=data)
    if ret.ok:
        logger.debug(f"send fail message done with ret_code={ret.status_code}")
    else:
        logger.debug(f"content: {ret.content}")
        logger.error(f"send fail message failed with ret_code={ret.status_code}")


def report_running(id=None, result=None):
    if id is None:
        logger.error("please provide id")
        return
    data = {"result": result}
    url = urljoin(secret.url, API_REPORT_RUNNING.format(id=id))
    ret = put(url=url, headers=HEADER, data=data)
    if ret.ok:
        logger.debug(f"send running message done with ret_code={ret.status_code}")
    else:
        logger.debug(f"content: {ret.content}")
        logger.error(f"send running message failed with ret_code={ret.status_code}")


def send_auto_message(message=None):
    data={"message": message}
    url = urljoin(secret.url, API_AUTO_MESSAGE)
    ret = post(url=url, data=data, headers=HEADER)
    if ret.ok:
        logger.debug(f"send auto message done with ret_code={ret.status_code}")
    else:
        logger.debug(f"content: {ret.content}")
        logger.error(f"send auto message failed with ret_code={ret.status_code}")
