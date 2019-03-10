from abc import ABCMeta
  
class Abstract:
        __metadata__ = ABCMeta

	def getOneById(self, id):
		entityName = self.__class__.__name__
		entityName = entityName[0].lower() + entityName[1:]

		return {"id": id, "type": entityName}

	def getAll(self, limit = 50, offset = 0):
		return [{}]

class Playlist(Abstract):
	def store(self):
		return {}
