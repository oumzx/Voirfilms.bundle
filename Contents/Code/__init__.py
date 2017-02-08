# Original Icon and Code by Ryan McNally.
# 2.1 rewrite, URL service by Mike McCurdy June 2012.
# Updated by sander1 on 23 Nov, 2012: make use of existing URL Services only (AMT, Yahoo Movies, YouTube, moviefone, IGN)
#
# TODO: 
# Thumbnails from the site are poster aspect ratio, which looks awful in the VideoClipObject list previews in mediastream.

TITLE = 'VoirFilms'
BASE_URL = 'http://www.voirfilms.co'
SERIESVF = '%s/series/page-%%d' % BASE_URL 
FILMSVF = '%s/lesfilms%%d' % BASE_URL

####################################################################################################
def Start():

	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')

	ObjectContainer.title1 = TITLE
	DirectoryObject.thumb = R('icon-default.png')
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0'

####################################################################################################
####################################################################################################
@handler('/video/voirFilms', TITLE)
def MainMenu():

	oc = ObjectContainer(view_group='List')
	oc.add(DirectoryObject(key=Callback(SeriesMenu, url=SERIESVF, title='SeriesVf'), title='SeriesVf'))
	oc.add(DirectoryObject(key=Callback(MoviesMenu, url=FILMSVF, title='FilmsVF'), title='Films en Streaming'))
	
	return oc

####################################################################################################
####################################################################################################
@route('/video/voirFilms/series', page=int)
def SeriesMenu(url, title, page=1):

	oc = ObjectContainer(title2=title, view_group='List')

	url = SERIESVF % page

	#for movie in HTML.ElementFromURL(url).xpath('//td[@class="indexTableTrailerImage"]'):
	for movie in HTML.ElementFromURL(url).xpath('//div[@class="imagefilm"]'):
		movie_url = movie.xpath('./a')[0].get('href')
		
		try:
			#movie_title = movie.xpath('./a/img')[0].get('title')
			movie_title = movie.xpath('./a/span/img')[0].get('alt')
		except:
			movie_title = ''.join(movie.xpath('.//text()')).strip()

		try:
			thumb_url = movie.xpath('./a/span/img')[0].get('src')
		except:
			thumb_url = ''

		oc.add(DirectoryObject(key=Callback(SerieSaisonMenu, url=movie_url, title=movie_title, thumb_url=thumb_url), title=movie_title, thumb=Resource.ContentsOfURLWithFallback(thumb_url)))

	oc.add(NextPageObject(key=Callback(SeriesMenu, url=url, title=title, page=page+1), title='More...'))

	return oc
####################################################################################################
####################################################################################################
####################################################################################################
@route('/video/voirFilms/series/saisons')
def SerieSaisonMenu(url, title, thumb_url):

	oc = ObjectContainer(title2=title, view_group='List')

	for saisons in HTML.ElementFromURL(url).xpath('//div[@class="unepetitesaisons"]'):
		saisons_url = saisons.xpath('./a')[0].get('href')
		
		try:
			saisons_title = saisons.xpath('./a/div/img')[0].get('title')
		except:
			saisons_title = ''.join(saisons.xpath('.//text()')).strip()

		try:
			thumb_url = BASE_URL + saisons.xpath('./a/div/img')[0].get('src')
			#thumb_url = thumb_url
		except:
			thumb_url = ''

		oc.add(DirectoryObject(key=Callback(SerieSaisonEpisodeMenu, url=saisons_url, title=saisons_title, thumb_url=thumb_url), title=saisons_title, thumb=Resource.ContentsOfURLWithFallback(thumb_url)))

	#oc.add(NextPageObject(key=Callback(SeriesMenu, url=url, title=title, page=page+1), title='More...'))

	return oc
####################################################################################################
####################################################################################################
@route('/video/voirFilms/series/saisons/episodes')
def SerieSaisonEpisodeMenu(url, title, thumb_url, inte=1):

	oc = ObjectContainer(title2=title, view_group='List')

	for episodes in HTML.ElementFromURL(url).xpath('//li[@class="description132"]'):
		episodes_url = BASE_URL +'/'+ episodes.xpath('./a')[0].get('href')
		
		try:
			episodes_title = title + episodes.xpath('./a/text()')[0]
		except:
			episodes_title = 'Episode %d' % inte 

		try:
			thumb_url = thumb_url
		except:
			thumb_url = ''

		oc.add(DirectoryObject(key=Callback(MovieSerielink, url=episodes_url, title=episodes_title, thumb_url=thumb_url), title=episodes_title, thumb=Resource.ContentsOfURLWithFallback(thumb_url)))

		inte=inte+1
	return oc

#####################################################################################################
#####################################################################################################
####################################################################################################
@route('/video/voirFilms/movies', page=int)
def MoviesMenu(url, title, page=1):

	oc = ObjectContainer(title2=title, view_group='List')

	url = FILMSVF % page

	for movie in HTML.ElementFromURL(url).xpath('//div[@class="imagefilm"]'):
		movie_url = BASE_URL +'/'+ movie.xpath('./a')[0].get('href')

		try:
			movie_title = movie.xpath('./a/span/img')[0].get('alt')
		except:
			movie_title = ''.join(movie.xpath('.//text()')).strip()

		try:
			thumb_url = BASE_URL + '/' + movie.xpath('./a/span/img')[0].get('src')
		except:
			thumb_url = ''

		oc.add(DirectoryObject(key=Callback(MovieSerielink, url=movie_url, title=movie_title, thumb_url=thumb_url), title=movie_title, thumb=Resource.ContentsOfURLWithFallback(thumb_url)))

	oc.add(NextPageObject(key=Callback(MoviesMenu, url=url, title=title, page=page+1), title='More...'))

	return oc

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
@route('/video/voirFilms/MovieSerieliens')
def MovieSerielink(url, title, thumb_url, inte=1):

	oc = ObjectContainer(title2=title, view_group='List')

	for liens in HTML.ElementFromURL(url).xpath('//li[@class="seme"]'):
		liens_url = liens.xpath('./a')[0].get('href')
		#liens_url='https://www.youtube.com/watch?v=gIlGnaefCck'

		try:
			thumb_url = liens.xpath('.//span[@class="gras"]/img')[0].get('src')
		except:
			thumb_url = ''
		
		try:
			#liens.xpath('./a/div/div/text()')[0] + liens.xpath('.//span[@class="gras"]/img/text()')[0] ''.join(liens.xpath('.//span[@class="gras"]/img/text()')).strip('&nbsp;')
			#liens_title = liens.xpath('.//span[@class="gras"]/img/text()').strip('&nbsp;')
			temp = liens.xpath('.//span[@style="width:55px;"]')[0].get('class')
			thumb_url_title = thumb_url
			liens_title = thumb_url_title.replace('http://www.voirfilms.co/img/hebergeur/','')
			liens_title = 'Lien ' + liens_title.replace('.jpg',' ') + temp
		except:
			liens_title = 'Liens %d' % inte 

		#oc.add(DirectoryObject(key=Callback(MovieMenu, url=liens_url, title=liens_title, thumb_url=thumb_url), title=liens_title, thumb=Resource.ContentsOfURLWithFallback(thumb_url)))
		
		oc.add(
				VideoClipObject(
					key = Callback(Lookup, title=liens_title, thumb=thumb_url, rating_key=liens_title, url=liens_url),
					title = liens_title,
					thumb = Resource.ContentsOfURLWithFallback(url=thumb_url),
					rating_key = liens_title,
					#items = [
					#	MediaObject(
					#		parts = [PartObject(key=HTTPLiveStreamURL(Callback(PlayVideo,url=liens_url)))]
					#	)
					#]
				)
			)

		inte=inte+1
	return oc

#################################################################################
#################################################################################
@route('/video/voirFilms/MovieSerieliens/Videos')
def Lookup(title, thumb, rating_key, url):

	oc = ObjectContainer()

	oc.add(
		VideoClipObject(
			key = Callback(Lookup, title=title, thumb=thumb, rating_key=rating_key, url=url),
			title = title,
			thumb = thumb,
			rating_key = rating_key,
			#items = [
			#	MediaObject(
			#		parts = [PartObject(key=HTTPLiveStreamURL(Callback(PlayVideo, url=url)))]
			#	)
			#]
		)
	)

	return oc

###########################################################
###########################################################
@route('/video/voirFilms/MovieSerieliens/Video')
def PlayVideo(url):
	return Redirect(url)

####################################################################################################
########################################################""
######################################################################
##################################################################################################""
####################################################################################################
