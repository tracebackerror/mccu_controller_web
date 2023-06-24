import logging
import time

logger = logging.getLogger(__name__)

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start the timer
        start_time = time.time()

        response = self.get_response(request)

        # Calculate the total time taken
        total_time = time.time() - start_time

        # Log the total time
        logger.info(f"Total time taken: {total_time} seconds")
        print(f"Total time taken: {total_time} seconds")
        return response
