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
import sys
import traceback as tb
import random

import xbmcaddon

import client
import gui

#   The full URL to where the gathered data should be posted.
import xbmcplugin

SUBMIT_URL = None

EXTRA_DATA = dict()

def addExtraData(key, value):
    EXTRA_DATA[key] = value

def getRandomHeading():
    """
    Get a random heading for use in dialogs, etc.
    The heading contains a random movie quote from the English strings.xml
    """
    return getLocalizedString(random.randint(90000, 90005))


def getLocalizedString(id):
    """
    Same as Addon.getLocalizedString() but retrieves data from this module's strings.xml
    """
    buggaloAddon = xbmcaddon.Addon(id = 'script.module.buggalo')
    return buggaloAddon.getLocalizedString(id)


def buggalo_try_except(extraData = None):
    """
    @buggalo_try_except function decorator wraps a function in a try..except clause and invokes onExceptionRaised()
    in case an exception is raised. Provide extraData to specific function specific extraData.

    @param extraData: str or dict
    """
    def decorator(fn):
        def wrap_in_try_except(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            except Exception:
                onExceptionRaised(extraData)
        return wrap_in_try_except
    return decorator

def onExceptionRaised(extraData = None):
    """
    Invoke this method in an except clause to allow the user to submit
    a bug report with stacktrace, system information, etc.

    This also avoids the 'Script error' popup in XBMC, unless of course
    an exception is thrown in this code :-)

    @param extraData: str or dict
    """
    # start by logging the usual info to stderr
    (type, value, traceback) = sys.exc_info()
    tb.print_exception(type, value, traceback)


    HANDLE = int(sys.argv[1])
    xbmcplugin.endOfDirectory(HANDLE, succeeded=False) # TODO

    heading = getRandomHeading()
    data = client.gatherData(type, value, traceback, extraData, EXTRA_DATA)

    d = gui.BuggaloDialog(SUBMIT_URL, heading, data)
    d.doModal()
    del d

#    if xbmcgui.Dialog().yesno(heading, line1, line2, line3, no, yes):
#        data = _gatherData(type, value, traceback, extraData)
#        client.submitData(SUBMIT_URL, data)
#        xbmcgui.Dialog().ok(heading, thanks)


