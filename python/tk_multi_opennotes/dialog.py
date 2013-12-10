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

thumbnail_widget = tank.platform.import_framework("tk-framework-widget", "thumbnail_widget")
class ThumbnailWidget(thumbnail_widget.ThumbnailWidget):
    pass

from .ui.dialog import Ui_Dialog
from .new_task import NewTaskDialog



class AppDialog(QtGui.QWidget):


    def __init__(self, app):
        QtGui.QWidget.__init__(self)
        # set up the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self._app = app

        self._settings = QtCore.QSettings("Shotgun Software", "tk-multi-opennotes")

        # set up the browsers
        self.ui.left_browser.set_app(self._app)
        self.ui.right_browser.set_app(self._app)

        self.ui.left_browser.selection_changed.connect( self.setup_task_list )
        self.ui.left_browser.set_label("Overview")
        self.ui.right_browser.set_label("Dialog")

        self.setup_entity_list()
        self.ui.right_browser.set_message("Please select an item in the listing to the left.")
        self.ui.reply.clicked.connect( self.openReply )
        self.ui.refresh.clicked.connect( self.refresh )
        self.ui.reply.hide()

    def openReply(self):
        
        
        curr_selection = self.ui.left_browser.get_selected_item()
        if curr_selection is None:
                QtGui.QMessageBox.warning(self,
                                          "Please select an Entity!",
                                          "Please select an Entity that you want to add a Task to.")
                return
        reply = NewTaskDialog(self._app, curr_selection.sg_data, self)
        # need to keep the reference alive otherwise the window is destroyed
        if reply.exec_() == QtGui.QDialog.Accepted:
            # do it!
            pass
            print 'yes'
            #task_id = new_task.create_task()

            # refresh - in case they cancel the context set, the dialog is up to date.
            #self.setup_task_list()

            # and set the context to point here!
            #self._set_context(task_id)
    ########################################################################################
    # make sure we trap when the dialog is closed so that we can shut down
    # our threads. Maya does not do proper cleanup on exit.

    def closeEvent(self, event):
        self.ui.left_browser.destroy()
        self.ui.right_browser.destroy()
        # okay to close!
        event.accept()

    ########################################################################################
    # basic business logic


    def refresh(self):
        self.setup_entity_list()

    def setup_entity_list(self):
        self.ui.left_browser.clear()
        self.ui.right_browser.clear()
        d = {}
        #d["own_tasks_only"] = self.ui.hide_tasks.isChecked()
        self.ui.left_browser.load(d)

    def setup_task_list(self):
        self.ui.right_browser.clear()
        curr_selection = self.ui.left_browser.get_selected_item()

        if curr_selection is None:
            return

        # pass in data to task retreiver
        d = {}
        #d["own_tasks_only"] = self.ui.hide_tasks.isChecked()
        d["entity"] = curr_selection.sg_data
        # pass in the sg data dump for the entity to the task loader code
        self.ui.right_browser.load(d)