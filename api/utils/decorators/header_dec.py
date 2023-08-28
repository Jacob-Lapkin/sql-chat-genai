from functools import wraps
from flask import request, jsonify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def require_headers(func):
    """Decorator to check for required headers."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        required_headers = ['IM-SenderID', 'IM-MicroFrontendID', 'IM-CorrelationID', 'IM-SiteCode', 'IM-UserID']
        headers = request.headers
        for h in required_headers:
            if h not in headers:
                # If you want to use logging here, you'll need to pass in the app instance or configure logging appropriately.
                # For this example, we'll skip the logging part.
                logger.warning(f' Missing headers that are required: {h}')

                return jsonify({"error": f'you must include all required headers. Missing header {h}'}), 400
        logger.info(f' Headers include the following: {headers}')
        return func(*args, **kwargs)
    return decorated_function
