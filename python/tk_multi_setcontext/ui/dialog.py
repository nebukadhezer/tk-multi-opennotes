# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Tue Sep 25 13:44:30 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(749, 546)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.new_task = QtGui.QToolButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/icon_Task.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.new_task.setIcon(icon)
        self.new_task.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.new_task.setObjectName("new_task")
        self.horizontalLayout_2.addWidget(self.new_task)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.left_browser = EntityBrowserWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_browser.sizePolicy().hasHeightForWidth())
        self.left_browser.setSizePolicy(sizePolicy)
        self.left_browser.setObjectName("left_browser")
        self.gridLayout.addWidget(self.left_browser, 0, 0, 1, 1)
        self.right_browser = TaskBrowserWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right_browser.sizePolicy().hasHeightForWidth())
        self.right_browser.setSizePolicy(sizePolicy)
        self.right_browser.setObjectName("right_browser")
        self.gridLayout.addWidget(self.right_browser, 0, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.change_context = QtGui.QPushButton(Dialog)
        self.change_context.setObjectName("change_context")
        self.horizontalLayout_3.addWidget(self.change_context)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hide_tasks = QtGui.QCheckBox(Dialog)
        self.hide_tasks.setChecked(True)
        self.hide_tasks.setObjectName("hide_tasks")
        self.horizontalLayout.addWidget(self.hide_tasks)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Change your Work Area", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "<b><big>Where will you be working today?</big></b>", None, QtGui.QApplication.UnicodeUTF8))
        self.new_task.setText(QtGui.QApplication.translate("Dialog", "Create New Task...", None, QtGui.QApplication.UnicodeUTF8))
        self.change_context.setText(QtGui.QApplication.translate("Dialog", "Switch Work Area", None, QtGui.QApplication.UnicodeUTF8))
        self.hide_tasks.setText(QtGui.QApplication.translate("Dialog", "Show My Tasks Only", None, QtGui.QApplication.UnicodeUTF8))

from ..entity_browser import EntityBrowserWidget
from ..task_browser import TaskBrowserWidget
from . import resources_rc
