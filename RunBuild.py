#!/usr/bin/env python
# coding=utf-8
"""
    环境 java
        svn
        Tomcat

    变量说明
          VERSION svn 导出版本
          CHAR 字符集
          EXJARPATH 依赖jar包环境
          SOURCEPATH 源文件
          PROJECTNAME 项目名称
          CATALINA_HOME tomcat lib依赖
"""
import os
import zipfile
import time
import sys
import re


def main(argv):
    print(argv)
    CATALINA_HOME = str(os.environ.get('CATALINA_HOME'))
    VERSION = str(argv)
    CHAR = 'utf-8'

    if CATALINA_HOME is None:
        print('\033[1;31m There is no Tomcat CATALINA_HOME. if build wrong ,please set CATALINA_HOME \033[0m')
        EXJARPATH = 'WebRoot\WEB-INF\lib;'
    else:
        EXJARPATH = 'WebRoot\WEB-INF\lib;' + CATALINA_HOME + '\lib;'

    SOURCEPATH = ' .;src\ '
    CLASSPATH = '.;WebRoot\WEB-INF\lib;'
    PROJECTNAME = 'jrbs_report'
    os.system("chcp 65001")
    try:
        os.system("del diff.list")
    except e:
        pass
    DIFF = "svn diff --summarize -r" + VERSION + " >> diff.list"
    print(DIFF)
    os.system(DIFF)
    result = list()
    buildJavaList = list()
    # read file path
    file = open('diff.list', 'r')
    for i in file.readlines():
        result.append(str(i.rsplit('\n')[0]).split('       ')[1])

    # per build java file
    for row in result:
        if row.endswith('.java'):
            buildJavaList.append(row)
    # java build path

    BUILDCMD = "javac -encoding " + CHAR + " -Djava.ext.dirs=" + EXJARPATH + " -cp " + CLASSPATH + " -sourcepath " + SOURCEPATH + " "
    nowTime = time.strftime("%Y%m%d_%H%M%S_") + PROJECTNAME + '_' + VERSION.replace(':', 'To') + '.zip'
    print(nowTime)
    zf = zipfile.ZipFile(nowTime, "w", zipfile.zlib.DEFLATED)
    for JavaPath in buildJavaList:
        print(BUILDCMD + JavaPath)
        os.system(BUILDCMD + JavaPath)
        classpath = JavaPath.replace('.java', '.class')
        zf.write(classpath)
        os.system("del " + classpath)
    for OtherPath in result:
        if not OtherPath.endswith('.java'):
            print(OtherPath)
            zf.write(OtherPath)
    zf.close()
    file.close()

    # os.system("del diff.list")
    print(result)
    print(buildJavaList)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("example : python runbuild.py 20:30")
        sys.exit(0)
    else:
        if not re.match(r'^[0-9]*:[0-9]*$', str(sys.argv[1])):
            print('VersionNum like --> 20:22 ')
            sys.exit(0)
        else:
            main(sys.argv[1])