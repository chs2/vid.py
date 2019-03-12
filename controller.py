from abc import ABCMeta

class Abstract(object):
	__metadata__ = ABCMeta

	def setRepository(self, repository):
		self.repository = repository

	def get(self, request):
		response = {"code": 200, "message": "OK", "data": {}}

		if len(request) > 1:
			response["data"] = self.repository.getOneById(request[1])
		else:
			response["data"] = self.repository.getAll()

		return response

class Video(Abstract):
	def put(self, request):
		import json
		import sys

		return json.loads(sys.stdin.read())

class Playlist(Abstract):
	def get(self, request):
		response = super(Playlist, self).get(request)

		if len(request) > 2:
			response["data"] = self.repository.getPlaylistVideos(request[1])

		return response

	def put(self, request):
		import json
		import sys

		return json.loads(sys.stdin.read())
