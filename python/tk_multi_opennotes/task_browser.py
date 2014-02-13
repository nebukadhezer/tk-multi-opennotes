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
        
        output = {}
        
        data = data["entity"]

        ### Todo if the timedelta is older than a minute requery for replies and attachments
        ### although the refresh button does the job already
#         newReply = self._app.shotgun.find_one(data['type'],
#                                                [['id','is',data['id']]],
#                                                ['replies'])
#         data['replies']= newReply['replies']
        replies = dict()
        attach = dict()
        sortList = list()
        
        if "replies" in data:
            if data["replies"]:
                for rep in data["replies"]:
                    fullRepData = self._app.shotgun.find_one(rep['type'],
                                                             [['id','is',rep['id']]],
                                                             ['user','created_at','content'])
                    replies[fullRepData['created_at']]= fullRepData
                    sortList.append(fullRepData['created_at'])
                    
        if "attachments" in data:
            if data["attachments"]:
                for att in data["attachments"]:
                    attachData = self._app.shotgun.find_one(att['type'],
                                                             [['id','is',att['id']]],
                                                             ['created_at','this_file','file_extension', 'filename','image'])
                                                             #[{'field_name':'created_at','direction':'asc'}])
                    attach[attachData['created_at']]= attachData
                    sortList.append(attachData['created_at'])

        sortList.sort()
        
        output['data'] = data
        output['replies'] = replies
        output['attach'] = attach
        output['sortList'] = sortList
        
        return output
                    
    def process_result(self, result):
        
        data = result['data']
        replies = result['replies']
        attach = result['attach']
        sortList = result['sortList']
        
        start = self.add_item(browser_widget.ListHeader)
        start.set_title("%s wrote on %s" % (data["user"]["name"], data.get("created_at", "Unknonwn")))
        body = self.add_item(browser_widget.ListItem)
        body.set_details("%s" % data['content'])
        image = data['user']['image']
        if image:
            body.set_thumbnail(image)
        if sortList:
            for i in sortList:
                if i in replies:
                    fullRepData = replies[i]
                    repHead = self.add_item(browser_widget.ListHeader)
                    repHead.set_title("%s wrote on %s" % (fullRepData['user']['name'],fullRepData['created_at']))

                    repBod = self.add_item(browser_widget.ListItem)
                    repBod.set_details("%s" % fullRepData['content'])
                    
                    if fullRepData['user']['id'] == data['user']['id']:
                        if image:
                            repBod.set_thumbnail(image)
                    else:
                        repImage = self._app.shotgun.find_one("HumanUser",[['id','is',fullRepData['user']['id']]], ['image'])
                        if repImage['image']:
                            repBod.set_thumbnail(repImage['image'])

                elif i in attach:
                    fullAttData = attach[i]
                    attBod = self.add_item(browser_widget.ListItem)
                    attBod.set_details("<i>Attachment:\n%s</i>" % fullAttData['filename'])
                    if fullAttData['image']:
                        attBod.set_thumbnail(fullAttData['image'])