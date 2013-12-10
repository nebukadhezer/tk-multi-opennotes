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
        #self.ui.right_browser.action_requested.connect( self.set_context )
        #self.ui.change_context.clicked.connect( self.set_context )

        #self.toggle_load_button_enabled()
        #self.ui.left_browser.selection_changed.connect( self.toggle_load_button_enabled )
        #self.ui.right_browser.selection_changed.connect( self.toggle_load_button_enabled )

        # create
        #types_to_load = self._app.get_setting("sg_entity_types", [])

        # now resolve the entity types into display names
        #types_nice_names = [ tank.util.get_entity_type_display_name(self._app.tank, x) for x in types_to_load ]

#         plural_types = [ "%ss" % x for x in types_nice_names] # no fanciness (sheep, box, nucleus etc)
#         if len(plural_types) == 1:
#             # "Shots"
#             types_str = plural_types[0]
#         else:
#             # "Shots, Assets & Sequences"
#             types_str = ", ".join(plural_types[:-1])
#             types_str += " & %s" % plural_types[-1]

        self.ui.left_browser.set_label("Overview")
        self.ui.right_browser.set_label("Dialog")

        # refresh when the checkbox is clicked
        #self.ui.hide_tasks.toggled.connect( self.setup_entity_list )
        #self.ui.hide_tasks.toggled.connect( self.remember_checkbox )


        # load data from shotgun
        self.setup_entity_list()
        self.ui.right_browser.set_message("Please select an item in the listing to the left.")

        # remember state of checkbox
        # this qsettings stuff seems super flaky on different platforms
#         try:
#             # this qsettings stuff seems super flaky on different platforms
#             # - although setting is saved as an int, it can get loaded as either an
#             # int or a string, hence the double casting to int and then bool.
#             prev_hide_tasks = bool(int(self._settings.value("hide_tasks", True)))
#             self.ui.hide_tasks.setChecked(prev_hide_tasks)
#         except Exception, e:
#             self._app.log_warning("Cannot restore state of hide tasks checkbox: %s" % e)


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


    def toggle_load_button_enabled(self):
        """
        Control the enabled state of the load button
        """
        curr_selection = self.ui.right_browser.get_selected_item()
        if curr_selection is None:
            self.ui.change_context.setEnabled(False)
        else:
            self.ui.change_context.setEnabled(True)


    def remember_checkbox(self):
        pass
        # remember setting - save value as an int as this
        # can be handled across all operating systems!
        # - on Windows & Linux, boolean & int settings are
        # returned as strings when queried!
        #settings_val = self.ui.hide_tasks.isChecked()
        #self._settings.setValue("hide_tasks", int(settings_val))

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