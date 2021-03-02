#!/usr/bin/python
#coding=utf-8

import xbmc, xbmcaddon

Addon_ID = xbmcaddon.Addon().getAddonInfo('id')
mysettings = xbmcaddon.Addon(Addon_ID)
auto_run = mysettings.getSetting('enable_autorun')

if auto_run == 'true':
	xbmc.executebuiltin("RunAddon(plugin.video.conggiao)")