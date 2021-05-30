import threading
import logging
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import pkgutil
import importlib
import ServerFan
import re
import traceback
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

executor = ThreadPoolExecutor(16, thread_name_prefix="worker")

def excetion_wrapper(f, *args, **kwargs):
    try:
        return f(*args, **kwargs) 
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        logger.fatal(f"Traceback:\n{traceback.format_exc()}")
        logger.fatal(f("Exception: {e}"))
        return None


def dispatch(handler, msg):
    logger = logging.getLogger(threading.current_thread().name)
    logger.info(f"id={msg['id']} message={msg['message']}")
    executor.submit(excetion_wrapper, handler, msg["id"], msg["message"])


def find_plugins(path):
    ret = []
    for module in pkgutil.walk_packages([path]):
        if module.module_finder.path == path:
            try:
                t = importlib.import_module(f".{module.name}", path)
                enabled = t.enabled
                if not enabled:
                    logger.info(f"{path}.{module.name} disabled")
                    continue
                pattern = t.pattern
                handler = t.handler
                ret.append((module.name, pattern, handler))
                logger.info(f"load {path}.{module.name} succeed")
            except Exception as e:
                logger.error(f"load {path}.{module.name} failed: {e}")
    return ret


def main():
    logger = logging.getLogger("main")
    logger.info("hello world")
    logger.info(f"PID={os.getpid()}")
    handlers = []
    handlers = handlers + find_plugins("private_plugins")
    handlers = handlers + find_plugins("public_plugins")
    try:
        while True:
            logger.debug("pull one job")
            ret = excetion_wrapper(ServerFan.get_job)
            if ret:
                logger.info(f"get one message from {ret['id']}")
                for handler in handlers:
                    if re.match(handler[1], ret["message"]):
                        logger.info(f"match {handler[0]}")
                        executor.submit(dispatch, handler[2], ret)
            else:
                sleep(10)
    except KeyboardInterrupt:
        executor.shutdown()
        logger.info("goodbye")


if __name__ == "__main__":
    main()

