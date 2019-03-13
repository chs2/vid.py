from abc import ABCMeta

import exception

class Abstract(object):
	__metadata__ = ABCMeta

	def setRepository(self, repository):
		self.repository = repository

	def get(self, request):
		response = {"code": 200, "message": "OK", "data": {}}

		if len(request) > 1:
			entity = self.repository.getOneById(request[1])

			if entity is None:
				raise exception.Http404

			response["data"] = entity
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

	def delete(self, request):
		self.get(request)

		response = {"code": 204, "message": "No Content"}

		if len(request) == 4 and request[2] == 'videos':
			self.repository.removeVideo(request[1], request[3])

			return response

		if len(request) == 2:
			self.repository.delete(request[1])

			return response

		raise exception.Http400

	def put(self, request):
		import json
		import sys

		return json.loads(sys.stdin.read())
