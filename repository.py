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

	def store(self, data):
		entityName = self.__class__.__name__
		entityName = entityName[0].lower() + entityName[1:]

		if "id" in data:
			query = "update {} set ".format(entityName)

			for key in data:
				if key != "id":
					query += key + " = :" + key + " "

			query += "where id = :id"
		else:
			query = "insert into {}({}) values ({})".format(entityName, ", ".join(data.keys()), ":" + ", :".join(data.keys()))

		with self.conn:
			cursor = self.conn.cursor()
			cursor.execute(query, data)

		if "id" not in data:
			data["id"] = cursor.lastrowid

		return data

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

	def delete(self, playlist):
		with self.conn:
			self.conn.execute("delete from video_playlist where playlist_id = :id", playlist)
			self.conn.execute("delete from playlist where id = :id", playlist)

	def addVideo(self, playlist, videoId, rank):
		with self.conn:
			cursor = self.conn.cursor()

			data = {"playlist_id": playlist["id"], "video_id": videoId, "rank": rank}

			if rank is None:
				cursor.execute("select max(rank) as rank from video_playlist where playlist_id = :playlist_id", data)
				row = cursor.fetchone()

				if row["rank"] is None:
					data["rank"] = 0
				else:
					data["rank"] = 1 + row["rank"]
			else:
				cursor.execute("update video_playlist set rank = rank + 1 where playlist_id = :playlist_id and rank >= :rank", data)

			cursor.execute("insert into video_playlist(playlist_id, video_id, rank) values(:playlist_id, :video_id, :rank)", data)

			return True

	def removeVideo(self, playlist, videoId):
		with self.conn:
			cursor = self.conn.cursor()

			data = {"playlist_id": playlist["id"], "video_id": videoId}

			cursor.execute("select rank from video_playlist where playlist_id = :playlist_id and video_id = :video_id", data)
			row = cursor.fetchone()

			data["rank"] = row["rank"]

			self.conn.execute("delete from video_playlist where playlist_id = :playlist_id and video_id = :video_id", data)

			cursor.execute("update video_playlist set rank = rank - 1 where playlist_id = :playlist_id and rank > :rank", data)

			return True

class Video(Abstract):
	pass
