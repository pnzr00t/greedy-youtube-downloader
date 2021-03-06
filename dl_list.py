import urllib.request
import os
from pytube import Channel
from pytube import YouTube
from pytube import Playlist
import json
from random import randint
from time import sleep
from os.path import exists

class YouTubeDownloader:
		def __init__(self):
				print(":NOTICE:", "YouTubeDownloader.init")

		def download_video(self, youtube_object):
				try:
						out_file_name = youtube_object.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
				except Exception as e:
						print(":WARNING:", 'Problem with download')
						return False
				#out_file_name = youtube_object.streams.get_highest_resolution.download() - not working
				print(youtube_object.vid_info)
				print(youtube_object.vid_info['videoDetails']['videoId'])
				print(youtube_object.thumbnail_url)

				file_extension = out_file_name.split('.')[1]
				os.rename(out_file_name, youtube_object.vid_info['videoDetails']['videoId'] + '.' + file_extension)
				return True

		def save_video_json_data(self, youtube_object):
				# Serializing json to file
				json_object = json.dumps(youtube_object.vid_info, indent = 4)
				print(json_object)

				file_name = youtube_object.vid_info['videoDetails']['videoId'] + '.json'
				with open(file_name, 'w') as x_file:
						x_file.write(json_object)

				with open("index_file.txt", 'a') as index_file:
						index_file.write(youtube_object.vid_info['videoDetails']['videoId'] + "\n")

		def save_video_captions(self, youtube_object):
				# Subs
				if "ru" in youtube_object.captions:
						caption = youtube_object.captions['ru']
						if caption != None:
								file_name_caption = youtube_object.vid_info['videoDetails']['videoId'] + '_ru' + '.caption'
								with open(file_name_caption, 'w') as x_file:
										x_file.write(caption.xml_captions)

				if "en" in youtube_object.captions:
						caption = youtube_object.captions['en']
						if caption != None:
								file_name_caption = youtube_object.vid_info['videoDetails']['videoId'] + '_en' + '.caption'
								with open(file_name_caption, 'w') as x_file:
										x_file.write(caption.xml_captions)

		def save_video_thumbnail(self, youtube_object):
				# Download start viedoe image
				file_name = os.path.basename(youtube_object.thumbnail_url)
				file_extension = file_name.split('.')[1]
				print(file_name)
				print(file_extension)

				local_file_name, _ = urllib.request.urlretrieve(youtube_object.thumbnail_url, file_name)
				print(local_file_name)
				print(file_name)
				os.rename(local_file_name, youtube_object.vid_info['videoDetails']['videoId'] + '.' + file_extension)

		def download_video_and_data(self, youtube_object):
				if not self.download_video(youtube_object=youtube_object):
						return
				self.save_video_json_data(youtube_object=youtube_object)
				self.save_video_captions(youtube_object=youtube_object)
				self.save_video_thumbnail(youtube_object=youtube_object)

		def download_from_channal_url(self, channal_url):
				upload_id_list = []

				path_to_index_file = './index_file.txt'
				if exists(path_to_index_file):
						with open(path_to_index_file) as file:
								upload_id_list = [line.rstrip() for line in file]

				channel_videos = Channel(channal_url)
				#with open('playlist-videos-title.txt', 'w') as x_file:
				#	   x_file.write(channel_videos.title)

				#with open('playlist-videos-description.txt', 'w') as x_file:
				#	   if 'simpleText' in playlist_videos.sidebar_info[0]['playlistSidebarPrimaryInfoRenderer']['description']:
				#			   x_file.write(channel_videos.description)

				for video_url in channel_videos.video_urls:
						print("Upload url", video_url, "channel_videos")
						youtube_object = YouTube(video_url)
						if youtube_object.vid_info['videoDetails']['videoId'] in upload_id_list:
								print("Already uploaded url", video_url, "channel_videos")
						else:
								self.download_video_and_data(youtube_object=youtube_object)
								sleep(randint(10, 15))

		def download_from_play_list(self, playlist_url):
				upload_id_list = []

				path_to_index_file = './index_file.txt'
				if exists(path_to_index_file):
						with open(path_to_index_file) as file:
								upload_id_list = [line.rstrip() for line in file]

				playlist_videos = Playlist(playlist_url)
				with open('playlist-videos-title.txt', 'w') as x_file:
						x_file.write(playlist_videos.title)

				with open('playlist-videos-description.txt', 'w') as x_file:
						if 'simpleText' in playlist_videos.sidebar_info[0]['playlistSidebarPrimaryInfoRenderer']['description']:
								x_file.write(playlist_videos.description)

				for video_url in playlist_videos.video_urls:
						print("Upload url", video_url, "channel_videos")
						youtube_object = YouTube(video_url)
						if youtube_object.vid_info['videoDetails']['videoId'] in upload_id_list:
								print("Already uploaded url", video_url, "channel_videos")
						else:
								self.download_video_and_data(youtube_object=youtube_object)
								sleep(randint(10, 15))


youtube_downloader = YouTubeDownloader()

#youtube_downloader.download_from_channal_url('https://www.youtube.com/c/SUREN_VIDEO') # <----- ENTER CHANNAL URL HERE

#youtube_downloader.download_from_play_list('https://www.youtube.com/watch?v=KzH1ovd4Ots&list=PLoROMvodv4rNH7qL6-efu_q2_bPuy0adh') # <------- ENTER PLAYLIST URL HERE

print("Thats all pals")