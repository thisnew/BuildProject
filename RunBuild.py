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
import configparser


def update_svn(p_path):
    os.system('svn update '+p_path)


if __name__ == '__main__':

    # argv check
    if '-h' in sys.argv:
        print("     -p  projectname \n     -c  conf.ini path \n     -d  project output path \n")
        sys.exit(0)
    if len(sys.argv) < 3 or '-p' not in sys.argv:
        print('not -p met')
        sys.exit(0)
    if not os.path.exists(sys.argv[sys.argv.index('-p')+1]):
        print(" make sure the project file >"+sys.argv[sys.argv.index('-p')+1]+"< exists !!!")
        sys.exit(0)
    conf = configparser.ConfigParser()
    conf.read('conf.ini')
    PROJECTNAME = None
    List_javaFile = list()
    List_otherFile = list()
    PROJECTNAME = sys.argv[sys.argv.index('-p')+1]
    update_svn(PROJECTNAME)
    CHAR = 'utf-8'
    DATAFileName = 'data.txt'
    if conf.get("custom", "CATALINA_HOME") is not None:
        CATALINA_HOME = str(conf.get("custom", "CATALINA_HOME"))
    else:
        try:
            CATALINA_HOME = str(os.environ.get('CATALINA_HOME'))
        except Exception as e:
            print()
            CATALINA_HOME = None
            pass
    if CATALINA_HOME is None:
        print('\033[1;31m There is no Tomcat CATALINA_HOME. if build wrong ,please set CATALINA_HOME \033[0m')
        EXJARPATH = PROJECTNAME + '/'+'WebRoot/WEB-INF/lib:'
    else:
        EXJARPATH = PROJECTNAME + '/'+'WebRoot/WEB-INF/lib:' + CATALINA_HOME + '/lib:'
    SOURCEPATH = ' .:src/ '
    CLASSPATH = '.:'+PROJECTNAME+'/WebRoot/WEB-INF/lib:'
    with open(DATAFileName, 'r') as fileList:
        for line in fileList.readlines():
            if line.strip().endswith('java'):
                List_javaFile.append(line.strip())
            else:
                List_otherFile.append(line.strip())
    fileList.close()
    BUILDCMD = "javac -encoding " + CHAR + " -Djava.ext.dirs=" + EXJARPATH + " -cp " + CLASSPATH + " -sourcepath " + SOURCEPATH + " "
    nowTime = PROJECTNAME + '_' + time.strftime("%Y%m%d_%H%M%S") + '.zip'
    zf = zipfile.ZipFile(nowTime, "w", zipfile.zlib.DEFLATED)
    for JavaPath in List_javaFile:
        print(BUILDCMD + JavaPath)
        os.system(BUILDCMD + JavaPath)
        classpath = JavaPath.replace('.java', '.class')
        zf.write(classpath)
        print("zipping .class ...  "+classpath)
        os.system('rm -rf '+classpath)
    for OtherPath in List_otherFile:
        #if not OtherPath.endswith('.java'):
        zf.write(OtherPath)
        print("zipping other ...  "+OtherPath)
    zf.close()
    print("zip all done !! >>>>>>>>>"+nowTime)
    sys.exit(0)