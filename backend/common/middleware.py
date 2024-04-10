import logging

from django.db import connection, reset_queries
from time import time

logger = logging.getLogger(__name__)


class QueryCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reset_queries()
        start_time = time()
        response = self.get_response(request)
        total_time = time() - start_time

        for query in connection.queries:
            logger.debug(query)

        logger.debug(f"Number of queries: {len(connection.queries)}, Execution time: {total_time}")
        return response
