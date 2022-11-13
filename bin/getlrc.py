#!/usr/bin/env python
# -*- coding: utf-8 -*-

# derived from https://github.com/ImranR98/AutoLyricize

import sys
from datetime import datetime
import os
import stat

PROGRAM_NAME = os.path.basename(sys.argv[0])

#sys.path.append( os.path.dirname(__file__) )

# TODO: syntax: getlrc [options | audio file] -> download synched lyrics from a webserver matching the supplied audio file (may also check stream length matching)

"""
This script scans a specified directory for audio files, and for each file, 
finds lyrics from Lyricsify.com or Genius.com (as a fallback), 
and saves them to lrc files.
"""

import sys
import urllib
import json
from bs4 import BeautifulSoup
import requests
import os
import re
import mutagen
import logging


logging.getLogger().setLevel(logging.INFO)


def lyricsify_find_song_lyrics(query):
	"""
	Return song lyrics from Lyricsify.com for the first song found using the provided search string.
	If not found, return None.
	"""
	matching_lyrics_list = []
	
	links = BeautifulSoup(
		requests.get(url="https://www.lyricsify.com/search?q=" +
					 query.replace(
						 " - ", "+").replace(" ", "+"),
					 headers={
						 "User-Agent": ""
					 }).text,
		"html.parser").find_all("a", class_="title")
	# If not found, return None
	if links is None:
		return matching_lyrics_list
	for link in links:
		# Scrape the song URL for the lyrics text
		song_html = BeautifulSoup(
			requests.get(url="https://www.lyricsify.com" + link.attrs['href'],
						 headers={
				"User-Agent": ""
			}).text,
			"html.parser")
		# If the artist or song name does not exist in the query, return None
		artist_title = song_html.find("h1").string[:-7]
		if fuzzy_match(query, artist_title):
			lyrics_text="".join(song_html.find("div", id="entry").strings)
			matching_lyrics_list.append(lyrics_text)
		
		# old:
		continue
		
		sep_ind = artist_title.find("-")
		artist = "" if sep_ind < 0 else artist_title[0:sep_ind].strip()
		title = artist_title if sep_ind < 0 else artist_title[sep_ind + 1:].strip()	
		query_lower = query.lower()
		

		if not artist or not title:
			continue
		
		#if query_lower.find(title.lower()) < 0 or (sep_ind >= 0 and query_lower.find(artist.lower()) < 0):
		if ( query_lower.find(title.lower()) < 0 or query_lower.find(artist.lower()) < 0):
			# not found
			continue
		else:
			# Return the lyrics text
			lyrics_text="".join(song_html.find("div", id="entry").strings)
			matching_lyrics_list.append(lyrics_text)
	# end for
	return matching_lyrics_list
# end of lyricsify_find_song_lyrics


def genius_find_song_lyrics(query, access_token):
    """
    Return song lyrics from Genius.com for the first song found using the provided search string.
    If not found, return None.
    Requires a Genius.com access token.
    """
  
    results = json.loads(requests.get(url="https://api.genius.com/search?q=" + urllib.parse.quote(query), headers={
        "Authorization": "Bearer " + access_token,
        "User-Agent": ""
    }).text)
    # If no hits, return None
    if len(results["response"]["hits"]) <= 0:
        return None
    # If the song has no URL or the artist or song name does not exist in the query, return None
    song = results["response"]["hits"][0]["result"]
    query_lower = query.lower()
    if song["url"] is None or query_lower.find(song["title"].lower()) < 0 or query_lower.find(song["primary_artist"]["name"].lower()) < 0:
        return None
    # Scrape the song URL for the lyrics text
    page = requests.get(song["url"])
    html = BeautifulSoup(page.text, "html.parser")
    target_div = html.find("div", id="lyrics-root")
    # This ususally means the song is an instrumental (exists on the site and was found, but no lyrics)
    if target_div is None:
        lyrics = ["[Instrumental]"]
    else:
        lyrics = "\n".join(
            html.find("div", id="lyrics-root").strings).split("\n")[1:-2]
    # The extracted lyrics text is mangled, needs some processing before it is returned...
    indices = []
    for i, lyric in enumerate(lyrics):
        if lyric[0] == "[":
            indices.append(i)
    inserted = 0
    for i in indices:
        lyrics.insert(i+inserted, "")
        inserted += 1
    final_lyrics = []
    for i, lyric in enumerate(lyrics):
        if (i < (len(lyrics) - 1) and (lyrics[i+1] == ")" or lyrics[i+1] == "]")) or lyric == ")" or lyric == "]" or (i > 0 and lyrics[i-1].endswith(" ") or lyric.startswith(" ")):
            final_lyrics[len(final_lyrics) -
                         1] = final_lyrics[len(final_lyrics)-1] + lyric
        else:
            final_lyrics.append(lyric)
    return [ "[ti:" + song["title_with_featured"] + "]\n[ar:" + song["primary_artist"]["name"] + "]\n" + "\n".join(final_lyrics) ]


def fuzzy_match(s1, s2):  # query from tags/filename, header from html page
	# remove tags (e.g. "(Album version)")
	import re
	s1 = re.sub("\(.*?\)|\[.*?\]","", s1)
	s2 = re.sub("\(.*?\)|\[.*?\]","", s2)
	
	# remove some words
	s1 = s1.replace(" OP - ", " - ")
	s1 = s1.replace(" ED - ", " - ")
	s1 = s1.replace(" opening - ", " - ")
	s1 = s1.replace(" ending - ", " - ")
	
	# TODO: skip lyrics with non-latin text
	
	#print(s2)
		
	# check tags separators
	if len(s1.split("-"))>=3:
		s1 = "-".join(s1.split("-")[0:2])  # take only the 1st and 2nd
		# TODO: try all the combinations
	if len(s2.split("-"))>=3:
		s2 = "-".join(s2.split("-")[0:2])  # take only the 1st and 2nd
		# TODO: try all the combinations
	
	# remove whitespaces and punctuation chars
	import string
	s1 = s1.translate(str.maketrans('', '', string.whitespace))
	s1 = s1.translate(str.maketrans('', '', string.punctuation))
	s2 = s2.translate(str.maketrans('', '', string.whitespace))
	s2 = s2.translate(str.maketrans('', '', string.punctuation))

	# convert to lowercase
	s1 = s1.lower()
	s2 = s2.lower()
	
	#print(s2)

	# test inclusion instead? 
	if s1 == s2:
		return True
	else:
		return False
	
	
	
def cleanup_tagged_lyrics_str(lyrics_str):

	# fix some special chars
	lyrics_str.replace("\'\'", "\"")  # '' -> "
	
	# TODO: enforce consistent line endings
	lyrics_str = lyrics_str.replace("\n\r\n", "\n")
	
	# TODO: cleanup lines repeating the title and author
	# TODO: cleanup spam lines
	
	# iterate over lines
	#for line in lyrics_str.splitlines():
	
	return lyrics_str



if __name__ == '__main__':
	# First, ensure user input exists
	genius_access_token = os.getenv("GENIUS_ACCESS_TOKEN", "")
	if len(genius_access_token) == 0:
		genius_access_token = None
	if genius_access_token is None:
		print("Note: The GENIUS_ACCESS_TOKEN environment variable has not been defined. Only Lyricsify.com will be used as a data source.")
	if (len(sys.argv) < 2):
		raise NameError(
			"The song directory path has not been provided as a parameter.")
	song_dir = sys.argv[1]

	# For each file in the songs directory, grab the artist/title and use them to find Lyricsify.com lyrics (with Genius.com as a fallback) and save them to the file
	files = [os.path.splitext(each) for each in os.listdir(song_dir)]

	for i, file in enumerate(files):
		audio_file_path = song_dir + "/" + file[0] + file[1]
		if os.path.isdir(audio_file_path):
			continue
		lrc_file_path = song_dir + "/" + file[0] + ".lrc"
		audio_file = mutagen.File(audio_file_path)
		audio_file_tag_artist = ""
		audio_file_tag_title = ""
		
		if audio_file is None:
			print(str(i+1) + "\tof " + str(len(files)) + " : Failed  : Unsupported file format              : " + file[0] + file[1])
			continue
		if not audio_file.keys():  
			# has no tags, guess from filename
			temp_ind = file[0].find("-")
			if len(file[0]) > 0 and temp_ind > 0 and not file[0].endswith("-"):
				audio_file_tag_artist = file[0][0:temp_ind]
				audio_file_tag_title = file[0][temp_ind+1:]
				print(str(i+1) + "\tof " + str(len(files)) +" : Warning : Artist/Title inferred from file name : " + file[0] + file[1])
			else:
				print(str(i+1) + "\tof " + str(len(files)) + " : Failed  : Artist/Title could not be found      : " + file[0] + file[1])
				continue
		else:
			# read from the tags
			if "artist" in audio_file:
				audio_file_tag_artist = audio_file["artist"][0]
			elif "TPE1" in audio_file:
				audio_file_tag_artist = audio_file["TPE1"].text[0]
			elif '©ART' in audio_file:
				audio_file_tag_artist = audio_file['©ART'][0]
			if "title" in audio_file:
				audio_file_tag_title = audio_file["title"][0]
			elif "TIT2" in audio_file:
				audio_file_tag_title = audio_file["TIT2"].text[0]
			elif '©nam' in audio_file:
				audio_file_tag_title = audio_file["©nam"][0]
		# end if
		logging.info("detected audio_file_tag_artist: " + audio_file_tag_artist)
		logging.info("detected audio_file_tag_title: " + audio_file_tag_title)
		
		if not audio_file_tag_title:
			continue
			
		# check existing lyrics
		if os.path.exists(lrc_file_path):
			logging.error("lyrics file already exists (skipped): " + lrc_file_path)
			continue
		if "lyrics" in audio_file:
			logging.warning("file already has lyrics in tags: " + audio_file_path)
					
		# query for lyrics
		# Note: re.sub... removes anything in brackets - used for "(feat. ...) as this improves search results"
		query = re.sub(r" ?\([^)]+\)", "", audio_file_tag_artist + " - " + audio_file_tag_title)
		site_used = "Lyricsify"
		try:
			lyrics_list = lyricsify_find_song_lyrics(query)
		except Exception as e:
			print("Error getting Lyricsify lyrics for: " + audio_file_path)
			raise e
		if not lyrics_list and genius_access_token is not None:
			site_used = "Genius   "
			try:
				lyrics_list = genius_find_song_lyrics(query, genius_access_token)
			except Exception as e:
				print("Error getting Lyricsify lyrics for: " + audio_file_path)
				raise e
		
		for i, lyrics in enumerate(lyrics_list):
			#audio_file.tag.lyrics.set(lyrics)
			#audio_file.tag.save()
			#print(lyrics)
			
			lyrics = cleanup_tagged_lyrics_str(lyrics)
			
			lrc_filename = file[0] + (str(i) if i >= 1 else "") +".lrc"
			
			open(lrc_filename, "w").write(lyrics)
			
			print(str(i+1) + "\tof " + str(len(files)) + " : Success : Lyrics from " + site_used + " saved to       : " + lrc_file_path)
		else:
			print(str(i+1) + "\tof " + str(len(files)) + " : Failed  : Lyrics not found for                 : " + audio_file_path)


