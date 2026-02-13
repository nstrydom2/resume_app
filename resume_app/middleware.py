import logging

logger = logging.getLogger("connections")

class LogIPMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		ip = request.META.get("HTTP_X_FORWARDED_FOR")
		if ip:
			ip = ip.split(",")[0].strip()
		else:
			ip = request.META.get("REMOTE_ADDR")
		logger.info("IP=%s PATH=%s METHOD=%s", ip, request.path, request.method)
		return self.get_response(request)
