# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_task.ui'
#
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_NewTask(object):
    def setupUi(self, NewTask):
        NewTask.setObjectName("NewTask")
        NewTask.resize(676, 415)
        self.gridLayout = QtGui.QGridLayout(NewTask)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(NewTask)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.label_2 = QtGui.QLabel(NewTask)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.attachment = QtGui.QLineEdit(NewTask)
        self.attachment.setObjectName("attachment")
        self.gridLayout.addWidget(self.attachment, 1, 1, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.thumbnail_frame = QtGui.QFrame(NewTask)
        self.thumbnail_frame.setStyleSheet("#thumbnail_frame {\n"
"border-style: solid;\n"
"border-color: rgb(32,32,32);\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"background: rgb(117,117,117);\n"
"}")
        self.thumbnail_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.thumbnail_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.thumbnail_frame.setObjectName("thumbnail_frame")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.thumbnail_frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.thumbnail_widget = ThumbnailWidget(self.thumbnail_frame)
        self.thumbnail_widget.setMinimumSize(QtCore.QSize(200, 130))
        self.thumbnail_widget.setMaximumSize(QtCore.QSize(200, 130))
        self.thumbnail_widget.setStyleSheet("")
        self.thumbnail_widget.setObjectName("thumbnail_widget")
        self.horizontalLayout_3.addWidget(self.thumbnail_widget)
        self.horizontalLayout_6.addWidget(self.thumbnail_frame)
        spacerItem = QtGui.QSpacerItem(0, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_6, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(NewTask)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(NewTask)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewTask.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewTask.reject)
        QtCore.QMetaObject.connectSlotsByName(NewTask)

    def retranslateUi(self, NewTask):
        NewTask.setWindowTitle(QtGui.QApplication.translate("NewTask", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewTask", "<html><head/><body><p><span style=\" font-size:large; font-weight:600;\">Reply</span><br/><br/>Add a thumbnail if you want or add a path to a local file.<br/><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewTask", "Attachment", None, QtGui.QApplication.UnicodeUTF8))

from ..dialog import ThumbnailWidget
