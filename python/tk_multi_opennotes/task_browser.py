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
from datetime import timedelta, datetime
from tank.platform.qt import QtCore, QtGui

browser_widget = tank.platform.import_framework("tk-framework-widget", "browser_widget")


class TaskBrowserWidget(browser_widget.BrowserWidget):

    
    def __init__(self, parent=None):
        browser_widget.BrowserWidget.__init__(self, parent)
        
        # only load this once!
        self._current_user = None
        self._current_user_loaded = False
        

    def get_data(self, data):
        
        self._current_data = data
        output = {}
        output["sgData"] = data["entity"]

        
        return output
                    
    def process_result(self, result):
        
        data = result["sgData"]
        entity_str = "%s wrote on %s" % (data["user"]["name"], data.get("created_at", "Unknonwn"))

        t = self.add_item(browser_widget.ListHeader)
        t.set_title("%s" % entity_str)
        i = self.add_item(browser_widget.ListItem)
        
        details = []
        details.append("%s" % data.get("content", ""))
        i.set_details("<br>".join(details))
        image = data['user']['image']
        if image:
            i.set_thumbnail(image)
    
        if datetime.now()-data['retTime'] > timedelta(seconds=20):
             newReply = self._app.shotgun.find_one(data['type'],
                                                   [['id','is',data['id']]],
                                                   ['replies'])
                                                   #[{'field_name':'created_at','direction':'desc'}])
             if newReply:
                 data['replies']= newReply['replies']
                 
        i.sg_data = data
        replies = dict()
        sortList = list()
        if "replies" in data:
            if data["replies"]:
                for rep in data["replies"]:
                    fullRepData = self._app.shotgun.find_one(rep['type'],
                                                             [['id','is',rep['id']]],
                                                             ['user','created_at','content'])
                                                             #[{'field_name':'created_at','direction':'asc'}])
                    replies[fullRepData['created_at']]= fullRepData
                    sortList.append(fullRepData['created_at'])
        sortList.sort()
        if sortList:
            for i in sortList:
                fullRepData = replies[i]
                repHead = self.add_item(browser_widget.ListHeader)
                repHead.set_title("%s wrote on %s" % (fullRepData['user']['name'],fullRepData['created_at']))
                repBod = self.add_item(browser_widget.ListItem)
                repBod.set_details("%s" % fullRepData['content'])
                if fullRepData['user']['id'] == data['user']['id']:
                    repBod.set_thumbnail(image)
                else:
                    image2 = self._app.shotgun.find_one("HumanUser",[['id','is',fullRepData['user']['id']]], ['image'])
                    if image2['image']:
                        repBod.set_thumbnail(image2['image'])