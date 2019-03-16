from abc import ABCMeta

import exception

class Abstract(object):
	__metadata__ = ABCMeta

	def setRepository(self, repository):
		self.repository = repository

class Playlist(Abstract):
	def get(self, request):
		response = {"code": 200, "message": "OK"}

		if len(request) > 1:
			entity = self.repository.getOneById(request[1])

			if entity is None:
				raise exception.Http404

			if len(request) == 2:
				response["data"] = entity
			elif len(request) == 3 and "videos" == request[2]:
				response["data"] = self.repository.getPlaylistVideos(request[1])
		else:
			response["data"] = self.repository.getAll()

		if "data" not in response:
			raise exception.Http400

		return response

	def put(self, request):
		import json
		import sys

		data = json.loads(sys.stdin.read())

		if len(request) == 2 or len(request) == 3:
			entity = self.repository.getOneById(request[1])

			if entity is None:
				raise exception.Http404

			if len(request) == 3:
				if "videos" == request[2] and "video_id" in data:
					if "rank" not in data:
						data["rank"] = None

					return {"code": 201, "message": "Created", "data": self.repository.addVideo(entity, data["video_id"], data["rank"])}

				raise exception.Http400
		else:
			entity = {}

		if "id" in data:
			raise exception.Http400

		for key in data:
			entity[key] = data[key]

		return {"code": 201, "message": "Created", "data": self.repository.store(entity)}

	def delete(self, request):
		response = {"code": 204, "message": "No Content"}

		entity = self.get(request[:2])
		entity = entity["data"]

		if len(request) == 4 and request[2] == 'videos':
			self.repository.removeVideo(entity, request[3])

			return response

		if len(request) == 2:
			self.repository.delete(entity)

			return response

		raise exception.Http400

class Video(Abstract):
	def get(self, request):
		response = {"code": 200, "message": "OK"}

		if len(request) > 1:
			entity = self.repository.getOneById(request[1])

			if entity is None:
				raise exception.Http404

			if len(request) == 2:
				response["data"] = entity
		else:
			response["data"] = self.repository.getAll()

		if "data" not in response:
			raise exception.Http400

		return response

