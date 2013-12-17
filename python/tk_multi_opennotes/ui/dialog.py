# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1058, 732)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.openInSg = QtGui.QPushButton(Dialog)
        self.openInSg.setObjectName("openInSg")
        self.horizontalLayout_2.addWidget(self.openInSg)
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
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.reply = QtGui.QPushButton(Dialog)
        self.reply.setObjectName("reply")
        self.horizontalLayout_3.addWidget(self.reply)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.refresh = QtGui.QPushButton(Dialog)
        self.refresh.setObjectName("refresh")
        self.horizontalLayout.addWidget(self.refresh)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Change your Work Area", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "All open notes, linked to the current context. Latest changes on top.", None, QtGui.QApplication.UnicodeUTF8))
        self.openInSg.setText(QtGui.QApplication.translate("Dialog", "open in SG", None, QtGui.QApplication.UnicodeUTF8))
        self.reply.setText(QtGui.QApplication.translate("Dialog", "reply", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh.setText(QtGui.QApplication.translate("Dialog", "refresh", None, QtGui.QApplication.UnicodeUTF8))

from ..entity_browser import EntityBrowserWidget
from ..task_browser import TaskBrowserWidget
from . import resources_rc
