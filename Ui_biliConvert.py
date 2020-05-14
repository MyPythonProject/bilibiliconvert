# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\UserData\Personal\GitHub\Python\biliConvert\biliConvert.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(304, 567)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        Form.setFont(font)
        self.progress_convert = QtWidgets.QProgressBar(Form)
        self.progress_convert.setGeometry(QtCore.QRect(10, 420, 271, 71))
        self.progress_convert.setProperty("value", 24)
        self.progress_convert.setObjectName("progress_convert")
        self.label_dir_out = QtWidgets.QLabel(Form)
        self.label_dir_out.setGeometry(QtCore.QRect(100, 69, 161, 31))
        self.label_dir_out.setMaximumSize(QtCore.QSize(161, 31))
        self.label_dir_out.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dir_out.setObjectName("label_dir_out")
        self.btn_choice_out = QtWidgets.QPushButton(Form)
        self.btn_choice_out.setGeometry(QtCore.QRect(10, 70, 82, 31))
        self.btn_choice_out.setMaximumSize(QtCore.QSize(91, 31))
        self.btn_choice_out.setAutoFillBackground(False)
        self.btn_choice_out.setObjectName("btn_choice_out")
        self.btn_choice_load = QtWidgets.QPushButton(Form)
        self.btn_choice_load.setGeometry(QtCore.QRect(10, 10, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_choice_load.sizePolicy().hasHeightForWidth())
        self.btn_choice_load.setSizePolicy(sizePolicy)
        self.btn_choice_load.setMaximumSize(QtCore.QSize(91, 31))
        self.btn_choice_load.setAutoFillBackground(False)
        self.btn_choice_load.setObjectName("btn_choice_load")
        self.label_dir_load = QtWidgets.QLabel(Form)
        self.label_dir_load.setGeometry(QtCore.QRect(100, 15, 161, 31))
        self.label_dir_load.setMaximumSize(QtCore.QSize(161, 31))
        self.label_dir_load.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dir_load.setObjectName("label_dir_load")
        self.list_file = QtWidgets.QListView(Form)
        self.list_file.setGeometry(QtCore.QRect(10, 150, 256, 241))
        self.list_file.setMaximumSize(QtCore.QSize(256, 281))
        self.list_file.setObjectName("list_file")
        self.btn_go = QtWidgets.QPushButton(Form)
        self.btn_go.setGeometry(QtCore.QRect(13, 506, 241, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_go.sizePolicy().hasHeightForWidth())
        self.btn_go.setSizePolicy(sizePolicy)
        self.btn_go.setMaximumSize(QtCore.QSize(300, 75))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.btn_go.setFont(font)
        self.btn_go.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_go.setObjectName("btn_go")
        self.chk_delete_source = QtWidgets.QCheckBox(Form)
        self.chk_delete_source.setGeometry(QtCore.QRect(20, 120, 241, 17))
        self.chk_delete_source.setObjectName("chk_delete_source")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "b站视频转换"))
        self.label_dir_out.setText(_translate("Form", "输出目录"))
        self.btn_choice_out.setToolTip(_translate("Form", "选择要转码的视频文件目录"))
        self.btn_choice_out.setText(_translate("Form", "选择输出目录"))
        self.btn_choice_load.setToolTip(_translate("Form", "选择要转码的视频文件目录"))
        self.btn_choice_load.setText(_translate("Form", "加载转换目录"))
        self.label_dir_load.setText(_translate("Form", "加载目录"))
        self.btn_go.setText(_translate("Form", "开始转换"))
        self.chk_delete_source.setText(_translate("Form", "转换完成后删除源文件"))
