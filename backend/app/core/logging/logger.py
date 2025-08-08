import logging
import time
from typing import Callable
from fastapi import Request

logger = logging.getLogger("todo")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

async def log_requests(request: Request, call_next: Callable):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(
        "%s %s %s %.2fms", request.method, request.url.path, response.status_code, duration
    )
    return response
