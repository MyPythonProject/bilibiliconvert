import sys
import os
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import*
import shutil
import json
from Ui_videoConvert import Ui_Form
import re
allfile = []

floor = 0

slm = QStringListModel()

convert_info = {'type': '', 'title': '', 'part': '',
                'video': '', 'audio': '', 'blv': [], 'blv_num': 0, 'm3u8': []}

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|\&\ ]"  # '/ \ : * ? " < > | &  '
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
class WorkThread(QThread):
    trigger = pyqtSignal(int, str, int)

    def __init__(self):
        super(WorkThread, self).__init__()

    def run(self):
        index = 0
        outDir0 = ui.label_dir_out.text()
        outDir0 = outDir0.replace("/", "\\")
        global allfile
        for video_info in allfile:
            # 创建目标目录
            if video_info['part'] != '' and video_info['part'] != video_info['title']:
                if outDir0.endswith('\\'):
                    outDir = outDir0 + video_info['title']
                else:
                    outDir = outDir0 + "\\" + video_info['title']
            else:
                outDir = outDir0
            outDir = outDir.replace(" ", "")
            outDir = outDir.replace("/", "()")
            print('=>'+outDir+'<=')
            if os.path.exists(outDir) == False:
                os.mkdir(outDir)
            windowtitle = ''
            if video_info['part'] != '' and video_info['part'] != video_info['title']:
                windowtitle = video_info['title']+'/'+video_info['part']
            else:
                windowtitle = video_info['title']
            self.trigger.emit(
                1, windowtitle, index)
            if video_info['type'] == 'm4s':

                path1 = video_info['video']
                path2 = video_info['audio']
                name = video_info['part'].replace(' ', '')

                outfile = outDir + '\\' + name
                print(outfile+".mp4开始合并\n")
                ver = os.popen("FFmpeg -i "+path1+" -i "+path2 +
                               " -codec copy "+outfile+".mp4")
                ver.close()

                #shutil.move(outfile + ".mp4", outDir + "\\" + name + ".mp4")
                print(outfile+".mp4合并完成\n")

            elif video_info['type'] == 'blv':
                outfile = outDir + "\\" + video_info['part']
                outfile = outfile.replace(' ', '')
                print(outfile+".mp4开始合并\n")
                if video_info['blv_num'] == 1:  # 单文件直接移动重命名
                    shutil.move(video_info['blv'][0], outfile + ".mp4")
                    print(outfile+".mp4重命名移动完成\n")
                else:  # 多文件合并转换输出
                    if os.path.exists('mergeflv.txt'):
                        os.remove('mergeflv.txt')
                    for blv_file in video_info['blv']:
                        # 将文件重命名为flv文件
                        blv_file_no_ext = os.path.splitext(blv_file)[0]
                        blv_file_add_ext = blv_file_no_ext + '.flv'

                        os.rename(blv_file, blv_file_add_ext)
                        # 追加打开合并脚本，不存在则创建
                        with open('mergeflv.txt', 'a') as f:  # 直接打开一个文件，如果文件不存在则创建文件
                            f.write('file ')
                            blv_file_add_ext = "'" + blv_file_add_ext + "'"
                            f.write(blv_file_add_ext + "\n")
                            f.close()

                    # 多个flv文件合并

                    ver = os.popen("ffmpeg -f concat -safe 0 -i " +
                                   'mergeflv.txt' + " -codec copy " + outfile + ".mp4")
                    ver.close()
                    print(outfile+".mp4合并完成\n")
            elif video_info['type'] == 'm3u8':
                outfile = outDir + "\\" + video_info['title']
                outfile = outfile.replace(' ', '')
                print(outfile+".mp4开始合并\n")
                # 多文件合并转换输出
                if os.path.exists('mergets.txt'):
                    os.remove('mergets.txt')
                for ts_file in video_info['m3u8']:
                    ts_file_add_ext = ts_file
                    if os.path.exists(ts_file+".ts") == False:
                        if os.path.exists(ts_file) == False:
                            continue
                        ext_name = os.path.splitext(ts_file)[1]
                        if ext_name == '':
                            ts_file_add_ext = ts_file_add_ext + '.ts'
                            os.rename(ts_file, ts_file_add_ext)
                        elif ext_name != '.ts':
                            continue
                    else:
                        ts_file_add_ext = ts_file_add_ext + '.ts'
                    # 追加打开合并脚本，不存在则创建
                    with open('mergets.txt', 'a') as f:  # 直接打开一个文件，如果文件不存在则创建文件
                        f.write('file ')
                        ts_file_add_ext = "'" + ts_file_add_ext + "'"
                        f.write(ts_file_add_ext + "\n")
                        f.close()

                # 多个flv文件合并
                if os.path.exists('mergets.txt') == True:
                    ver = os.popen("ffmpeg -f concat -safe 0 -i " +
                                   'mergets.txt' + " -codec copy " + outfile + ".mp4")
                    ver.close()
                    print(outfile+".mp4合并完成\n")
            else:
                self.trigger.emit(4, video_info['type'], index)
                return
            self.trigger.emit(
                2, video_info['title']+'/'+video_info['part'], index)

            index += 1
        # 删除中间文件
        if os.path.exists('mergeflv.txt'):
            os.remove('mergeflv.txt')
        if os.path.exists('mergets.txt'):
            os.remove('mergets.txt')
        self.trigger.emit(3, "转码工作全部完成", index)

# 转码更新 type: 1. 进行中 2. 完成 3. 全部完成，4. 不支持的转码格式 str:转码文件名 index:转码的视频索引


def workUpdate(type, str, index):
    if type == 1 or type == 2:
        qIndex = slm.index(index, 0)
        # 默认选中当前转码行
        ui.list_file.setCurrentIndex(qIndex)
        MainWindow.setWindowTitle(str)
    elif type == 3:
        ui.btn_go.setText("全部转换完成")
        qIndex = slm.index(len(allfile)-1, 0)
        ui.list_file.setCurrentIndex(qIndex)
        MainWindow.setWindowTitle("b站视频转换")
        if ui.chk_delete_source.isChecked() == True:
            if os.path.exists(ui.label_dir_load.text()):
                CleanDir(ui.label_dir_load.text())
        ui.chk_delete_source.setDisabled(False)
        QMessageBox.information(None, "温馨提示", "全部转码任务完成",
                                QMessageBox.Ok, QMessageBox.NoButton)
    elif type == 4:
        QMessageBox.information(None, "警告!致命错误!", "视频格式"+str+"不支持,程序即将退出",
                                QMessageBox.Ok, QMessageBox.NoButton)
        sys.exit(app.exec_())
    ui.progress_convert.setValue(index+1)
    QApplication.processEvents()


def work():
    workThread.start()
    workThread.trigger.connect(workUpdate)

# 删除非空目录及其中文件


def CleanDir(Dir):
    if os.path.isdir(Dir):
        paths = os.listdir(Dir)
        for path in paths:
            filePath = os.path.join(Dir, path)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath, True)
    return True

# 遍历目录下的源视频


def Traversal_Source(path):
    global floor, convert_info, allfile
    allfilelist = os.listdir(path)
    for f in allfilelist:
        filepath = os.path.join(path, f)
        if os.path.isdir(filepath):
            Traversal_Source(filepath)
        else:
            if floor == len(allfile):
                if f == 'entry.json' or f == 'index.json':
                    parse_json(
                        filepath)
                    if f == 'entry.json':
                        print(convert_info['title'] +
                              "  " + convert_info['part'])
                elif f == 'video.m4s':
                    convert_info['video'] = filepath.replace("\\", "/")
                    convert_info['type'] = 'm4s'
                    print(convert_info['video'])
                elif f == 'audio.m4s':
                    convert_info['audio'] = filepath.replace("\\", "/")
                    print(convert_info['audio'])
                elif f.endswith('.blv'):
                    convert_info['blv'].append(filepath.replace("\\", "/"))
                    convert_info['type'] = 'blv'
                elif f.endswith('.m3u8'):
                    convert_info['type'] = 'm3u8'
                    # 寻找同级目录文件夹作为m3u8实际视频存放位置，跟该索引文件的层级关系为index
                    #                                                                  |
                    #                                                                folder->real m3u8 video
                    # 取得m3u8 index之前的路径
                    m3u8_folder = filepath.replace("\\", '/')
                    # :不包括最后一个'/'位置，以得到文件父的路径
                    m3u8_folder = m3u8_folder[0:m3u8_folder.rfind('/')]
                    with open(filepath, 'r') as m3f:
                        lineStrs = m3f.readlines()
                        for lineStr in lineStrs:
                            lineStr = lineStr.replace('\n', '')
                            if lineStr.find('#EXT') == -1:
                                splitStr = lineStr.split('/')
                                # 例如：E:/Quark/Download/1/a (1,a为后补的两个字符串)
                                convert_info['m3u8'].append(
                                    m3u8_folder+'/'+splitStr[len(splitStr)-2]+'/'+splitStr[len(splitStr)-1])

                        convert_info['title'] = os.path.splitext(
                            filepath[filepath.rfind('\\')+1:len(filepath)])[0]  # 获取去除路径与后缀名以后的单独文件名
                        convert_info['title'] = convert_info['title'].replace(
                            ' ', '')
                        if convert_info['title'] != '':
                            allfile.append(convert_info)
                            init_convert_info()
                            floor += 1
                            # 存入m4s文件信息
                if convert_info['type'] == 'm4s' and convert_info['title'] != '' and convert_info['video'] != '' and convert_info['audio'] != '':
                    allfile.append(convert_info)
                    init_convert_info()
                    floor += 1
                # 存入blv文件信息
                elif convert_info['type'] == 'blv' and convert_info['title'] != '' and convert_info['part'] != '' and convert_info['blv_num'] > 0 and len(convert_info['blv']) >= convert_info['blv_num']:
                    allfile.append(convert_info)
                    init_convert_info()
                    floor += 1


def init_convert_info():
    global convert_info
    convert_info = {'type': '', 'title': '', 'part': '',
                    'video': '', 'audio': '', 'blv': [], 'blv_num': 0, 'm3u8': []}

    # 检索json获取视频列表名称与视频名称


def parse_json(jsonname):
    global convert_info
    size = os.path.getsize(jsonname)
    if size == 0:  # 文件为空，已经损坏
        return
    with open(jsonname, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

        if 'entry.json' in jsonname:
            convert_info['title'] = validateTitle(data['title'])
            if 'page_data' in data.keys():
                if 'part' in data['page_data'].keys():
                    convert_info['part'] = data['page_data']['part']
                else:
                    convert_info['part'] = convert_info['title']
            else:
                convert_info['part'] = data['ep']['index']
            convert_info['part'] = validateTitle(convert_info['part'])
        elif 'index.json' in jsonname:
            if 'segment_list' in data.keys():
                convert_info['blv_num'] = len(data['segment_list'])


def click_load():
    global allfile, floor, convert_info, slm
    allfile = []
    floor = 0
    current_path = os.path.dirname(os.path.abspath(__file__))
    path = QFileDialog.getExistingDirectory(
        None, "源文件夹", current_path+"\\download", QFileDialog.ShowDirsOnly)
    if path == "" or os.path.exists(path) == False:
        QMessageBox.information(None, "警告", "请选择合法源视频目录",
                                QMessageBox.Ok, QMessageBox.NoButton)
        return
    path.replace("/", "\\")
    ui.label_dir_load.setText(path)
    init_convert_info()

    Traversal_Source(path)
    print(len(allfile))
    slm = QStringListModel()  # 创建mode
    video_title = []
    for title in allfile:
        if title['part'] != '':
            video_title.append(title['title'] + '/' + title['part'])
        else:
            video_title.append(title['title'])

    slm.setStringList(video_title)
    ui.list_file.setModel(slm)
    if len(allfile) > 0:
        ui.btn_go.setDisabled(False)
        ui.btn_go.setText("点击转码")
        ui.progress_convert.setMinimum(0)
        ui.progress_convert.setValue(0)
        ui.progress_convert.setMaximum(len(allfile))
    else:
        ui.btn_go.setDisabled(True)
        ui.btn_go.setText("没有转码文件")


def click_out():
    current_path = os.path.dirname(os.path.abspath(__file__))
    path = QFileDialog.getExistingDirectory(
        None, "输出文件夹", current_path+"\\outfile", QFileDialog.ShowDirsOnly)

    if path == "" or os.path.exists(path) == False:
        QMessageBox.information(None, "警告", "请选择合法输出目录",
                                QMessageBox.Ok, QMessageBox.NoButton)
        return
    outDir = path.replace("/", "\\")
    ui.label_dir_out.setText(outDir)


def click_go():
    if ui.label_dir_load.text() == "" or ui.label_dir_load.text() == "加载目录" or ui.label_dir_out.text() == "" or ui.label_dir_out.text() == "输出目录" or os.path.exists(ui.label_dir_load.text()) == False or os.path.exists(ui.label_dir_out.text()) == False:
        QMessageBox.information(None, "警告", "请先先择加载和输出目录",
                                QMessageBox.Ok, QMessageBox.NoButton)
        return
    ui.btn_go.setText("转换中")
    ui.btn_go.setDisabled(True)
    ui.chk_delete_source.setDisabled(True)
    work()


def init_ui():
    ui.btn_choice_load.clicked.connect(click_load)
    ui.btn_choice_out.clicked.connect(click_out)
    ui.btn_go.clicked.connect(click_go)
    ui.progress_convert.setValue(0)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_Form()

    ui.setupUi(MainWindow)
    init_ui()
    MainWindow.show()

    QMessageBox.information(None, "温馨提示", "目前支持B站，Quark和UC浏览器",
                            QMessageBox.Ok, QMessageBox.NoButton)
    workThread = WorkThread()

    sys.exit(app.exec_())
