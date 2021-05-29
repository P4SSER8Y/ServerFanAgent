import logging
import ServerFan

pattern = r".*"

def handler(id, msg):
    logger = logging.getLogger("echo")
    result = f"get: {msg}"
    logger.info(result)
    ServerFan.send_auto_message(result)
    ServerFan.report_succeed(id=id, result=msg)

