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


class TaskBrowserWidget(browser_widget.BrowserWidget):

    
    def __init__(self, parent=None):
        browser_widget.BrowserWidget.__init__(self, parent)
        
        # only load this once!
        self._current_user = None
        self._current_user_loaded = False
        
        # create an action for grabbing tasks
        
    def grab_task(self):
        
        try:
            task_id = self.sender().parent().sg_data["id"]
            task_assignees = self.sender().parent().sg_data["task_assignees"]
        except:
            QtGui.QMessageBox.critical(self, "Cannot Resolve Task!", "Cannot resolve this task!")            
            return
            
        res = QtGui.QMessageBox.question(self, 
                                         "Assign yourself to this task?", 
                                         "Assign yourself to this task?",
                                         QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)
        if res == QtGui.QMessageBox.Ok:
            task_assignees.append(self._current_user)
            self._app.shotgun.update("Task", task_id, {"task_assignees": task_assignees})
        
        # ask widget to refresh itself
        self.clear()
        self.load(self._current_data)
        
        

    def get_data(self, data):
        
        self._current_data = data
        
#         if not self._current_user_loaded:
#             self._current_user = tank.util.get_shotgun_user(self._app.shotgun)
#             self._current_user_loaded = True
#         
        
        # start building output data structure        
        output = {}
        output["sgData"] = data["entity"]

        
        return output
                    
    def process_result(self, result):
        
        data = result["sgData"]
        print data
        entity_str = "%s wrote on %s" % (data["user"]["name"], data.get("created_at", "Unknonwn"))

        t = self.add_item(browser_widget.ListHeader)
        t.set_title("%s" % entity_str)
        i = self.add_item(browser_widget.ListItem)
        
        details = []
        details.append("%s" % data.get("content", ""))
        #details.append("Status: %s" % d.get("sg_status_list"))
        #names = [ x.get("name", "Unknown") for x in d.get("task_assignees", []) ]
        #names_str = ", ".join(names)
        #details.append("Assigned to: %s" % names_str)
        i.set_details("<br>".join(details))
    
        i.sg_data = data
        if "replies" in data:
            if data["replies"]:
                for rep in data["replies"]:
                    fullRepData = self._app.shotgun.find_one(rep['type'],[['id','is',rep['id']]],['user','created_at'])
                    repHead = self.add_item(browser_widget.ListHeader)
                    repHead.set_title("%s wrote on %s" % (fullRepData['user']['name'],fullRepData['created_at']))
                    repBod = self.add_item(browser_widget.ListItem)
                    repBod.set_details("%s" % rep['name'])