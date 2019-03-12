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
		cursor.execute("select * from " + entityName + " where id = {}".format(id))

		return cursor.fetchone()

	def getAll(self, limit = 50, offset = 0):
		entityName = self.__class__.__name__
		entityName = entityName[0].lower() + entityName[1:]

		cursor = self.conn.cursor()
		cursor.execute("select * from " + entityName)

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

	def store(self):
		return {}

class Video(Abstract):
	def store(self):
		return {}
