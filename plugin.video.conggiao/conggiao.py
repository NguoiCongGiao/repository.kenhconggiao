#!/usr/bin/python
#coding=utf-8

import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib, sys, re, os

KodiVersion = int(xbmc.getInfoLabel("System.BuildVersion")[:2])
if KodiVersion > 18:
	from urllib.request import Request, urlopen
	from urllib.parse import quote_plus
else:
	import urllib2

plugin_handle = int(sys.argv[1])

Addon_ID = xbmcaddon.Addon().getAddonInfo('id')
mysettings = xbmcaddon.Addon(Addon_ID)
Addon_Name = mysettings.getAddonInfo('name')
home = xbmc.translatePath(mysettings.getAddonInfo('path'))
icon = os.path.join(home, 'icon.png')
fanart = os.path.join(home, 'fanart.jpg')

CongGiaoList = 'https://raw.githubusercontent.com/NguoiCongGiao/repository.kenhconggiao/master/CongGiao.xml'
youtube_icon = 'https://raw.githubusercontent.com/NguoiCongGiao/repository.kenhconggiao/master/youtube.png'
settings_icon = 'https://raw.githubusercontent.com/NguoiCongGiao/repository.kenhconggiao/master/settings.png'

def make_request(url):
	if KodiVersion > 18:
		try:
			req = Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
			response = urlopen(req)
			link = response.read().decode('utf-8')
			response.close()
			return link
		except:
			pass
	else:
		try:
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
			response = urllib2.urlopen(req)
			link = response.read()
			response.close()
			return link
		except:
			pass

def main():
	addDir("[COLOR yellow]Tìm Trên YouTube[/COLOR]", 'plugin://plugin.video.youtube/kodion/search/input', None, youtube_icon, True)
	addDir("[COLOR lime]Kênh Công Giáo Tìm Trên YouTube[/COLOR]", 'plugin://plugin.video.youtube/kodion/search/query/?q=cong%20giao&search_type=channel', None, fanart, True)
	addDir('[COLOR magenta]Kênh Công Giáo Tuyển Chọn[/COLOR]', 'CongGiao', 1, icon, True)
	addDir('[COLOR green]CongGiao - Settings[/COLOR]', 'NoLinkNeeded', 2, settings_icon, True)

def CongGiao():
	content = make_request(CongGiaoList)
	content = ''.join(content.splitlines()).replace('\t', '')
	match = re.compile('<item>(.+?)</item>').findall(content)
	for item in match:
		title = ""
		link = ""
		thumb = ""
		if '<title>' in item:
			title = re.compile('<title>(.+?)</title>').findall(item)
			title = title[0].strip()
		if '<link>' in item:
			link = re.compile('<link>(.*?)</link>').findall(item)
			link = link[0].strip()
		if '<thumbnail>' in item:
			thumb = re.compile('<thumbnail>(.*?)</thumbnail>').findall(item)
			thumb = thumb[0].strip()
		if len(thumb) > 0:
			if thumb.startswith('http'):
				thumb = thumb.replace(' ', '%20')
			else:
				thumb = icon
		else:
			thumb = icon
		addDir(title, link, None, thumb, True)

def addon_settings():
	mysettings.openSettings()
	sys.exit(0)

def addDir(name, url, mode, iconimage, isFolder = False):
	if KodiVersion > 18:
		u = (sys.argv[0] + "?url=" + urllib.parse.quote_plus(url) + "&mode=" + str(mode) +\
			"&name=" + urllib.parse.quote_plus(name) + "&iconimage=" + urllib.parse.quote_plus(iconimage))
		ok = True
		liz = xbmcgui.ListItem(name)
		liz.setArt({'thumb': iconimage,
					'icon': icon,
					'poster': iconimage,
					'fanart': fanart})
	else:
		u = (sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) +\
			"&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage))
		ok = True
		liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	if iconimage == fanart:
		liz.setProperty('fanart_image', fanart)
	else:
		liz.setProperty('fanart_image', iconimage)
	if not isFolder:
		liz.setProperty('IsPlayable', 'true')
	elif any(x in url for x in ['plugin://plugin', 'script://script']):
		u = url
	elif any(x in url for x in ['www.youtube.com/user/', 'www.youtube.com/channel/', 'www.youtube.com/playlist/']):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
	ok = xbmcplugin.addDirectoryItem(plugin_handle, url = u, listitem = liz, isFolder = isFolder)
	return ok

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

params = get_params()

url = None
name = None
mode = None
iconimage = None

if KodiVersion > 18:
	try: url = urllib.parse.unquote_plus(params["url"])
	except: pass
	try: name = urllib.parse.unquote_plus(params["name"])
	except: pass
	try: mode = int(params["mode"])
	except: pass
	try: iconimage = urllib.parse.unquote_plus(params["iconimage"])
	except: pass
else:
	try: url = urllib.unquote_plus(params["url"])
	except: pass
	try: name = urllib.unquote_plus(params["name"])
	except: pass
	try: mode = int(params["mode"])
	except: pass
	try: iconimage = urllib.unquote_plus(params["iconimage"])
	except: pass

if mode == None or url == None or len(url) < 1:
	main()

elif mode == 1:
	CongGiao()

elif mode == 2:
	addon_settings()

xbmcplugin.endOfDirectory(plugin_handle)