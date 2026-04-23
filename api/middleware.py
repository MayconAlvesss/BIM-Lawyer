import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("BIM-Lawyer")

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log performance for enterprise monitoring
        logger.info(
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} Duration: {process_time:.4f}s"
        )

        response.headers["X-Process-Time"] = str(process_time)
        return response
