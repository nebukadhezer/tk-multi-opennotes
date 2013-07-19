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
        
        self._settings = QtCore.QSettings("Shotgun Software", "tk-multi-setcontext")
        
        # set up the browsers
        self.ui.left_browser.set_app(self._app)        
        self.ui.right_browser.set_app(self._app)
        
        self.ui.left_browser.selection_changed.connect( self.setup_task_list )
        self.ui.right_browser.action_requested.connect( self.set_context )
        self.ui.change_context.clicked.connect( self.set_context )
        
        self.toggle_load_button_enabled()
        self.ui.left_browser.selection_changed.connect( self.toggle_load_button_enabled )
        self.ui.right_browser.selection_changed.connect( self.toggle_load_button_enabled )        
        
        # create 
        types_to_load = self._app.get_setting("sg_entity_types", [])
        
        # now resolve the entity types into display names
        types_nice_names = [ tank.util.get_entity_type_display_name(self._app.tank, x) for x in types_to_load ]
        
        plural_types = [ "%ss" % x for x in types_nice_names] # no fanciness (sheep, box, nucleus etc)
        if len(plural_types) == 1:
            # "Shots"
            types_str = plural_types[0]
        else:
            # "Shots, Assets & Sequences"
            types_str = ", ".join(plural_types[:-1])
            types_str += " & %s" % plural_types[-1]
            
        self.ui.left_browser.set_label(types_str)
        self.ui.right_browser.set_label("Tasks")
        
        # refresh when the checkbox is clicked
        self.ui.hide_tasks.toggled.connect( self.setup_entity_list )
        self.ui.hide_tasks.toggled.connect( self.remember_checkbox )
        
        # should we show create tasks?
        create_tasks = self._app.get_setting("enable_create_tasks", False)

        if create_tasks:
            self.ui.new_task.clicked.connect( self.create_new_task )
        else:
            self.ui.new_task.setVisible(False)
        
        # load data from shotgun
        self.setup_entity_list()
        self.ui.right_browser.set_message("Please select an item in the listing to the left.")        

        # remember state of checkbox        
        # this qsettings stuff seems super flaky on different platforms
        try:
            prev_hide_tasks = bool(self._settings.value("hide_tasks", True))
            self.ui.hide_tasks.setChecked(prev_hide_tasks)
        except Exception, e:
            self._app.log_warning("Cannot restore state of hide tasks checkbox: %s" % e)
        
        
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
        
    def create_new_task(self):

        curr_selection = self.ui.left_browser.get_selected_item()
        if curr_selection is None:
                QtGui.QMessageBox.warning(self, 
                                          "Please select an Entity!", 
                                          "Please select an Entity that you want to add a Task to.")
                return
            
        # do new task
        new_task = NewTaskDialog(self._app, curr_selection.sg_data, self)
        # need to keep the reference alive otherwise the window is destroyed
        if new_task.exec_() == QtGui.QDialog.Accepted:
            # do it!
            task_id = new_task.create_task()
            
            # refresh - in case they cancel the context set, the dialog is up to date.
            self.setup_task_list()
        
            # and set the context to point here!
            self._set_context(task_id)
            
    def remember_checkbox(self):        
        settings_val = self.ui.hide_tasks.isChecked()
        self._settings.setValue("hide_tasks", settings_val)
        
    def setup_entity_list(self): 
        self.ui.left_browser.clear()
        self.ui.right_browser.clear()
        d = {}
        d["own_tasks_only"] = self.ui.hide_tasks.isChecked()
        self.ui.left_browser.load(d)
        
    def setup_task_list(self):
        self.ui.right_browser.clear()
        curr_selection = self.ui.left_browser.get_selected_item()
        if curr_selection is None:
            return
        
        # pass in data to task retreiver
        d = {}
        d["own_tasks_only"] = self.ui.hide_tasks.isChecked()
        d["entity"] = curr_selection.sg_data
        # pass in the sg data dump for the entity to the task loader code
        self.ui.right_browser.load(d)
        
        
    def set_context(self):
        """
        Set context based on selected task
        """
        curr_selection = self.ui.right_browser.get_selected_item()
        if curr_selection is None:
            return

        self._set_context(curr_selection.sg_data.get("id"))


    def _clear_current_scene_maya(self):
        """
        Clears the current scene. Does a file -> new.
        Maya implementation.
        returns False on cancel, true on success.
        """
        
        import pymel.core as pm
        import maya.cmds as cmds

        status = True
        
        if cmds.file(query=True, modified=True):
            
            # changes have been made to the scene
            res = QtGui.QMessageBox.question(self,
                                             "Save your scene?",
                                             "Your scene has unsaved changes. Save before proceeding?",
                                             QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
            
            if res == QtGui.QMessageBox.Cancel:
                status = False

            elif res == QtGui.QMessageBox.No:
                # don't save!
                cmds.file(newFile=True, force=True)
            
            else:
                # save before!
                
                if pm.sceneName() != "":
                    # scene has a name!
                    # normal save
                    cmds.file(save=True, force=True)
                    cmds.file(newFile=True, force=True)
                else:
                    # scene does not have a name. 
                    # save as dialog
                    cmds.SaveSceneAs()
                    # not sure about return value here, so check the scene!
                    if cmds.file(query=True, modified=True):
                        # still unsaved changes
                        # assume user clicked cancel in dialog
                        status = False

        return status
        
        
        
        
        
        
    def _clear_current_scene_motionbuilder(self):
        """
        Clears the current scene. Does a file -> new.
        Motionbuilder implementation.
        returns False on cancel, true on success.
        """
        from pyfbsdk import FBApplication
        status = True

        fb_app = FBApplication()

        res = QtGui.QMessageBox.question(self,
                                         "Save your scene?",
                                         "Your scene has unsaved changes. Save before proceeding?",
                                         QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)

        if res == QtGui.QMessageBox.Cancel:
            status = False
            
        elif res == QtGui.QMessageBox.No:
            # don't save!
            fb_app.FileNew()
            
        else:
            # save before!
            fb_app.FileSave()
            fb_app.FileNew()

        return status
        



    def _set_context(self, task_id):
        """
        Set context based on selected task
        """

        try:
            ctx = self._app.tank.context_from_entity("Task", task_id)
        except Exception, e:            
            QtGui.QMessageBox.critical(self, 
                                       "Cannot Resolve Task!", 
                                       "Cannot resolve this task into a context: %s" % e)
            return


        res = QtGui.QMessageBox.question(self,
                                         "Change work area?",
                                         "This will switch your work area to the "
                                         "selected Task. Are you sure you want to continue?",
                                         QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)

        if res == QtGui.QMessageBox.Ok:            
            
            # first clear the scene
            if self._app.engine.name == "tk-maya":
                
                if not self._clear_current_scene_maya():
                    # return back to dialog
                    return
            
            elif self._app.engine.name == "tk-3dsmax":
                
                from Py3dsMax import mxs
                
                if mxs.getSaveRequired():
                    # not an empty scene
                    # this will ask the user if they want to reset
                    mxs.resetMaxFile()
                    
                if mxs.getSaveRequired():
                    # if save is still required, this means that the user answered No
                    # when asked to reset. So now, exit and don't carry out the switch
                    return
                
            
            elif self._app.engine.name == "tk-motionbuilder":
                if not self._clear_current_scene_motionbuilder():
                    # return back to dialog
                    return
                
                
            # note - on nuke, we always start from a clean scene, so no need to check.
                
            # ok scene is clear. Now switch!
            
            # Try to create path for the context.  
            try:
                self._app.tank.create_filesystem_structure("Task", task_id, engine=self._app.engine.name)
                current_engine_name = self._app.engine.name            
                if tank.platform.current_engine(): 
                    tank.platform.current_engine().destroy()
                tank.platform.start_engine(current_engine_name, ctx.tank, ctx)
            except Exception, e:
                QtGui.QMessageBox.critical(self, 
                                           "Could not Switch!", 
                                           "Could not change work area and start a new " 
                                           "engine. This can be because the task doesn't "
                                           "have a step. Details: %s" % e)
                return
            
            
            # close dialog
            self.close()
        
        
        
        
        