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
from datetime import datetime
from tank.platform.qt import QtCore, QtGui

browser_widget = tank.platform.import_framework("tk-framework-widget", "browser_widget")

class EntityBrowserWidget(browser_widget.BrowserWidget):

    
    def __init__(self, parent=None):
        browser_widget.BrowserWidget.__init__(self, parent)
        
        # only load this once!
        self._current_user = None
        self._current_user_loaded = False
        self._initTime = datetime.now()
        

    def get_data(self, data):

        sg_data = []
        self._current_user = tank.util.get_shotgun_user(self._app.shotgun)
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

        return {"data": sg_data,
                "icons": userDict2,
                "retTime": datetime.now()}


    def process_result(self, result):

        if len(result.get("data")) == 0:
            self.set_message("No notes found!")
            return
        contextTask = self._app.context.task
        if not contextTask:
            self.set_message("NO TASK PRESENT IN THE CONTEXT THIS IS BAD PLEASE US THE SETCONTEXT APPS")
        if result['icons']:
            icons = result['icons']
            #print 'icons: %s' % icons
        
        for user in result.get("data"):
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
                    if contextTask:
                        if self._app.context.task['name'] in retTasks:
                            details = "<FONT COLOR='#65D552'><b>%s</b><br>from %s<br>status: %s<br>tasks: <b>%s</b></FONT COLOR='#65D552'>" % (d.get("subject"), 
                                                              d.get("created_at"), 
                                                              d.get('sg_status_list'),
                                                              ", ".join(retTasks))
                        else:
                            details = "<b>%s</b><br>from %s<br>status: %s<br>tasks: <b>%s</b>" % (d.get("subject"), 
                                                              d.get("created_at"), 
                                                              d.get('sg_status_list'),
                                                              ", ".join(retTasks))
                    else:
                        details = "<b>%s</b><br>from %s<br>status: %s<br>tasks: <b>%s</b>" % (d.get("subject"), 
                                                          d.get("created_at"), 
                                                          d.get('sg_status_list'),
                                                          ", ".join(retTasks))
                        
                    i.set_details(details)
                    d['retTime'] = result['retTime']
                    i.sg_data = d
                    image = icons[use]['image']
                    if image:
                        i.set_thumbnail(image)
                        d['user']['image'] = image
                        i.sg_data = d