#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
#
import datetime
import os
import simplejson

import xbmc
import xbmcaddon

BUGGALO_ADDON = xbmcaddon.Addon('script.module.buggalo')
ADDON = xbmcaddon.Addon()

def trackUserFlow(value):
    userFlow = load()
    key = datetime.datetime.now().isoformat()

    userFlow[key] = value
    save(userFlow)

def load():
    path = xbmc.translatePath(BUGGALO_ADDON.getAddonInfo('profile'))
    file = os.path.join(path, '%s.json' % ADDON.getAddonInfo('id'))

    if os.path.exists(file):
        userFlow = simplejson.load(open(file))
    else:
        userFlow = dict()
    return userFlow

def save(userFlow):
    path = xbmc.translatePath(BUGGALO_ADDON.getAddonInfo('profile'))
    if not os.path.exists(path):
        os.makedirs(path)
    file = os.path.join(path, '%s.json' % ADDON.getAddonInfo('id'))

    try:
        # remove entries older than 24 hours
        # we compare strings rather the datetimes (a little hackish though)
        # but datetime.datetime.strptime() often fail for no apparent reason
        # see http://forum.xbmc.org/showthread.php?tid=112916
        oneDayAgo = datetime.datetime.now() - datetime.timedelta(days = 1)
        oneDayAgoStr = oneDayAgo.isoformat()
        for dateStr in userFlow.keys():
            if dateStr < oneDayAgoStr:
                del userFlow[dateStr]

        simplejson.dump(userFlow, open(file, 'w'))
    except Exception:
        print "problem saving userflow json file"

