# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank
import os
import sys
import threading

from tank.platform.qt import QtCore, QtGui

browser_widget = tank.platform.import_framework("tk-framework-widget", "browser_widget")

class EntityBrowserWidget(browser_widget.BrowserWidget):

    
    def __init__(self, parent=None):
        browser_widget.BrowserWidget.__init__(self, parent)
        
        # only load this once!
        self._current_user = None
        self._current_user_loaded = False
        

    def get_data(self, data):

        sg_data = []

        self._current_user = tank.util.get_shotgun_user(self._app.shotgun)
        #print self._current_user
        notes = self._app.shotgun.find("Note", 
                                       [ ["project", "is", self._app.context.project], 
                                         ["note_links", "in", self._app.context.entity]], 
                                         ["subject","sg_status_list","tasks","note_links","type","user","created_at","content","replies"],
                                         [{'field_name':'updated_at','direction':'desc'}]
                                       )
        userDict = dict()
        userDict2 = dict()
        for note in notes:
            if 'user' in note:
                if not note['user']['name'] in userDict:
                    userDict[note['user']['name']] = list()
                    userDict[note['user']['name']].append(note)
                else:
                    userDict[note['user']['name']].append(note)
                if not note['user']['name'] in userDict2:
                    userDict2[note['user']['name']] = self._app.shotgun.find_one("HumanUser",[['id','is',note['user']['id']]], ['image'])
        sg_data.append(userDict)
            
        #resort and group the data 

        return {"data": sg_data,
                "icons": userDict2}


    def process_result(self, result):

        if len(result.get("data")) == 0:
            self.set_message("No notes found!")
            return
        if result['icons']:
            icons = result['icons']
            print 'icons: %s' % icons
        
        for user in result.get("data"):
            #print user
            for use in user:
                 i = self.add_item(browser_widget.ListHeader)
                 i.set_title("Notes from %s" % (use))
                 for d in user[use]:
                    i = self.add_item(browser_widget.ListItem)
                    ##prep tasks for print
                    if 'tasks' in d:
                        tasks = d['tasks']
                        retTasks = list()
                        for task in tasks:
                            if 'name' in task:
                                retTasks.append(task['name'])
                    details = "<b>%s</b><br>from %s<br>status: %s<br>tasks: %s" % (d.get("subject"), 
                                                      d.get("created_at"), 
                                                      d['sg_status_list'],
                                                      ", ".join(retTasks))
                    #print details
                    i.set_details(details)
                    i.sg_data = d
                    image = icons[use]['image']
                    print image
                    print self._current_user['image']
                    if image:
                        i.set_thumbnail(image)
                #            

        
        