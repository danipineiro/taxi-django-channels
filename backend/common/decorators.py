import logging
from functools import wraps

from django.db import connection, reset_queries

logger = logging.getLogger(__name__)


def count_queries(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        result = func(*args, **kwargs)

        for query in connection.queries:
            logger.debug(query)

        num_queries = len(connection.queries)
        logger.debug(f"Number of queries: {num_queries} for {func.__name__}")

        return result

    return inner_func
