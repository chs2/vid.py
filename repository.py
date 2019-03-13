from abc import ABCMeta
import sqlite3
  
class Abstract(object):
        __metadata__ = ABCMeta

	def __init__(self, conn):
		self.conn = conn

	def getOneById(self, id):
		entityName = self.__class__.__name__
		entityName = entityName[0].lower() + entityName[1:]

		cursor = self.conn.cursor()
		cursor.execute("select * from {} where id = {}".format(entityName, id))

		return cursor.fetchone()

	def getAll(self, limit = 50, offset = 0):
		entityName = self.__class__.__name__
		entityName = entityName[0].lower() + entityName[1:]

		cursor = self.conn.cursor()
		cursor.execute("select * from {}".format(entityName))

		return cursor.fetchall()

class Playlist(Abstract):
	def getPlaylistVideos(self, playlistId):
		cursor = self.conn.cursor()
		cursor.execute((""
			"select video.* "
			"from video_playlist "
			"join video on video_playlist.video_id = video.id "
			"where video_playlist.playlist_id = {} "
			"order by video_playlist.rank asc"
			"").format(playlistId))

		return cursor.fetchall()

	def delete(self, id):
		with self.conn:
			self.conn.execute("delete from video_playlist where playlist_id = {}".format(id))
			self.conn.execute("delete from playlist where id = {}".format(id))

	def removeVideo(self, playlistId, videoId):
		pass

	def store(self):
		return {}

class Video(Abstract):
	def store(self):
		return {}
