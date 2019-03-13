from abc import ABCMeta

class Http(StandardError):
	__metadata__ = ABCMeta

class Http400(Http):
	code = 400
	message = "Bad Request"

class Http404(Http):
	code = 404
	message = "Not Found"

class Http405(Http):
	code = 405
	message = "Not Implemented"

class Http406(Http):
	code = 406
	message = "Not Acceptable"

class Http500(Http):
	code = 500
	message = "Internal Server Error"
