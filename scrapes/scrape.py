

"""
title
id	IMDb id for moves, TVDb id for tv shows,
originaltitle
seasonnumber	only for tv show seasons
showtitle	only for tv show episodes
episode	only for tv show episode
season	only for tv show episode
aired	only for tv show episode
airsafter_season	only for tv show episode
airsbefore_episode	only for tv show episode
airsbefore_season	only for tv show episode
displayepisode	only for tv show episode; which episode this special airs before
displayseason	only for tv show episode; season the special aired in
director	new tag for each director
writer	new tag for each writer
credits	new tag for each credit
trailer	YouTube URL in the Kodi format plugin://plugin.video.youtube/?action=play_video&videoid=<Youtube Video ID>
rating
year
sorttitle
mpaa
aspectratio
dateadded	in UTC
collectionnumber	TMDb collection id
set	collection name; only for movies
imdb_id	only for TV shows
imdbid	for all other media types
tvdbid
idmbid
tmdbid
language
countrycode
formed	only for music artists
premiered
enddate
releasedate
criticrating
runtime
country	new tag for each production country
genre	new tag for each genre
studio	new tag for each studio
disbanded	only for music artists
audiodbartistid	only for music
audiodbalbumid	only for
zap2itid	only for tv shows
musicbrainzalbumid	only for music
musicbrainzalbumartistid	only for music
musicbrainzartistid	only for music
musicbrainzreleasegroupid	only for music
tvrageid
art	only if save image paths is enabled in the nfo settings; backdrops with child element fanart, posters with the tag poster

"""
class MovieInfo:
    name:str
    id:str
    originaltitle:str
    seasonnumber:str
    showtitle:str
    


class Scraper:
    pass

    def site_url(self):
        raise NotImplementedError()

    def scrape(self, movie_id: str):
        raise NotImplementedError()
