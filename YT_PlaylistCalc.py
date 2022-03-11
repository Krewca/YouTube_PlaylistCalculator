#####################################
#		Made by Krewca Software		#
#		For Hitpoint.cz				#
#####################################

import sys, time, argparse
from googleapiclient.discovery import build

# Note: You need to enter your own API Key!
api_key = ''

youtube = build('youtube', 'v3', developerKey=api_key)

parser = argparse.ArgumentParser(
	description='Counts video views for all videos in playlist. \n' +
	'Playlist ID is located in playlist URL after \"playlist?list=\"',
	epilog = 'Courtesy of Krewca Software, made for Hitpoint.cz')
parser.add_argument('-l', '--list', action='store_true', 
	help='Lists all videos in playlist with their corresponding views')
parser.add_argument('-v', '--viewsOnlyList', action='store_true',
	help='Lists only views of videos without their names')
parser.add_argument('-p', '--playlistId', action='store',
	help='Pass the playlist ID directly into program argument')

args = parser.parse_args()

if not args.playlistId:
	playlistId = input("Enter playlist ID: ")
else:
	playlistId = args.playlistId

playlistName_request = youtube.playlists().list(
		part = 'snippet',
		id = playlistId
	)
playlistName_response = playlistName_request.execute()

try:
	playlistName = playlistName_response['items'][0]['snippet']['title']
except:
	print("ERROR: Playlist ID is not valid.")
	exit()

print()
print("Counting video views for playlist: " + playlistName)

playlist_viewCount = 0
nextPageToken = None
video_title = []
video_viewCount = []
while True:
	playlist_request = youtube.playlistItems().list(
			part = 'contentDetails',
			playlistId = playlistId,
			maxResults = 50,
			pageToken = nextPageToken
		)

	playlist_response = playlist_request.execute()

	video_ids = []
	for item in playlist_response['items']:
	    video_ids.append(item['contentDetails']['videoId'])

	video_request = youtube.videos().list(
			part = "statistics, snippet",
			id = ','.join(video_ids)
		)

	video_response = video_request.execute()

	for item in video_response['items']:
		video_title.append(item['snippet']['title'])
		video_viewCount.append(item['statistics']['viewCount'])

	nextPageToken = playlist_response.get('nextPageToken')

	if not nextPageToken:
		break

print()

for i in range(len(video_viewCount)):
	if args.list:
		print(video_title[i] + " 	- " + video_viewCount[i])
	elif args.viewsOnlyList:
		print(video_viewCount[i])
	playlist_viewCount = playlist_viewCount + int(video_viewCount[i])

print()
print("Total view count for playlist " + playlistName + " - " + str(playlist_viewCount))