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
import xbmcaddon
import xbmcgui

buggaloAddon = xbmcaddon.Addon(id = 'script.module.buggalo')

ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10

class BuggaloDialog(xbmcgui.WindowXMLDialog):
    DETAILS_VISIBLE_LABEL = 99
    CLOSE_BUTTON = 100
    SUBMIT_BUTTON = 101
    DETAILS_BUTTON = 102
    DETAILS_LIST = 103
    TITLE_LABEL = 110

    def __new__(cls, title, data):
        return super(BuggaloDialog, cls).__new__(cls, 'buggalo-dialog.xml', buggaloAddon.getAddonInfo('path'))

    def __init__(self, title, data):
        super(BuggaloDialog, self).__init__()
        self.title = title
        self.data = data
        self.detailsVisible = False

    def onInit(self):
        self.getControl(self.TITLE_LABEL).setLabel(self.title)
        self.getControl(self.DETAILS_VISIBLE_LABEL).setVisible(not self.detailsVisible)
        listControl = self.getControl(self.DETAILS_LIST)

        for group in sorted(self.data.keys()):
            values = self.data[group]
            if type(values) == dict:
                item = xbmcgui.ListItem(label = '[B]%s[/B]' % group)
                listControl.addItem(item)
                for key in values:
                        item = xbmcgui.ListItem(label = '    %s' % key, label2 = str(values[key]))
                        listControl.addItem(item)

            else:
                item = xbmcgui.ListItem(label = '[B]%s[/B]' % group, label2 = str(values))
                listControl.addItem(item)



    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU]:
            self.close()

    def onClick(self, controlId):
        if controlId == self.CLOSE_BUTTON:
            self.close()

        elif controlId == self.SUBMIT_BUTTON:
            pass

        elif controlId == self.DETAILS_BUTTON:
            self.detailsVisible = not self.detailsVisible
            self.getControl(self.DETAILS_VISIBLE_LABEL).setVisible(not self.detailsVisible)


    def onFocus(self, control):
        pass