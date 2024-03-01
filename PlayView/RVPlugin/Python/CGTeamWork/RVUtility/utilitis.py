import os
import re
from RVControllers import RVnoteControll, RVsearchTControll, RVdataControll
from PySide2 import QtGui
from rv import commands as rvc
import time

def readQSS(fileName):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Styles', fileName)
    with open(path) as f:
        data = f.read()
    return data

def getTextResult(content, imageList):
    results = []
    pResult = re.findall(r"<p[\s\S].*?>([\s\S].*)</p>",content)
    if pResult:
        for result in pResult:
            cResult = re.sub(r'<img[\s\S].*? />', '#Image#', result)
            sResults = [i for i in cResult.split("#") if i]
            sResults.append('\n')
            results.extend(sResults)
        for image in imageList:
            for index, value in enumerate(results):
                if results[index] == 'Image':
                    results[index] = image
                    break
        return results
    else:
        return []

def getMousePos():
    cursor = QtGui.QCursor.pos()
    return [cursor.x(), cursor.y()]

def deleteFiles(files):
    try:
        for file in files:
            os.remove(file)
    except Exception as e:
        print(str(e))
        
def getImagePath(imageName):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Resources/icons/' + imageName)


def setWidgetSize(widget, a,b):
    cursor = QtGui.QCursor.pos()
    window = QtGui.QGuiApplication.screenAt(cursor)

    size = window.size()
    widget.resize(a*size.width(), b*size.height())

def getLatestVersion(path):
    if os.path.exists(path):
        versions = listDir(path)
        versions.sort()
        if versions:
            return [True, os.path.join(path, versions[-1])]
        else:
            return [False, path]
    else:
        return [False, path]


def listDir(path):
    return [i for i in os.listdir(path) if i != 'Thumbs.db']

def create_temp_dir(dir_name):
    dir_path = os.path.join(os.getenv('TEMP'), dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def getSequenceString(path):
    file_list = listDir(path)
    if len(file_list) > 1:
        return splitFileSequence(file_list[0], file_list[-1])
    else:
        return file_list[0]


def splitFileSequence(firstFile, lastFile):
    first_digit = re.findall(r'\d+', firstFile)
    last_digit = re.findall(r'\d+', lastFile)
    result = [i for i in zip(first_digit, last_digit) if i[0] != i[1]][0]
    rule_str, frame = (firstFile, result[0])if firstFile.count(result[0]) <= 1 else (lastFile, result[1])
    start_index = rule_str.find(frame)
    src_list = list(rule_str)
    if result.index(frame):
        src_list.insert(start_index + len(frame), '#')
        src_list.insert(start_index, result[0] + '-')
    else:
        src_list.insert(start_index + len(frame), '-' + result[-1] + '#')
    sequenceFrame = ''.join(src_list)
    return sequenceFrame


def getControll(name):
    controllMap = {
                    "noteControll": RVnoteControll.NoteControll,
                    "searchTControll": RVsearchTControll.SearchTControll,
                    "dataControll": RVdataControll.DataList
                  }
    return controllMap.get(name)()


def export_current_frame():
    image_dir_path = create_temp_dir("FrameImages")
    image_path = os.path.join(image_dir_path, str(time.time()) + '.jpg')
    rvc.exportCurrentFrame(image_path)
    return image_path