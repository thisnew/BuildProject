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
try:
    import configparser as ConfigParser
except Exception as e:
    import ConfigParser as ConfigParser
    pass


def update_svn(p_path):
    os.system('svn update '+p_path)


if __name__ == '__main__':

    # argv check
    if '-h' in sys.argv:
        print("\033[1;31m     "
              "     -p  项目名称 (必填) \n"
              "     -c  手动配置 conf.ini  \n"
              "     -cl rm -rf all project build .class file \n"
              "\033[0m")
        sys.exit(0)
    if len(sys.argv) < 3 or '-p' not in sys.argv:
        print("\033[1;31m     "
              "     -p  项目名称 (必填) \n"
              "     -c  手动配置 conf.ini  \n"
              "     -cl rm -rf all project build .class file \n"
              "\033[0m")
        sys.exit(0)
    if not os.path.exists(sys.argv[sys.argv.index('-p')+1]):
        print(" make sure the project file >"+sys.argv[sys.argv.index('-p')+1]+"< exists !!!")
        sys.exit(0)
    if '-cl' in sys.argv:
        print("\033[1;31m 这个操作一般不需要执行，只有才不确定是否有.class文件存留的情况下使用 请谨慎! \033[0m")
        ans = input("Enter (yes) to continue:")
        if ans == 'yes':
            os.system('''find '''+sys.argv[sys.argv.index('-p')+1]+''' -name '*.class' -exec rm -rf {} \;''')
            print("\033[1;31m done \033[0m")
        sys.exit(0)
    PROJECTNAME = None
    List_javaFile = list()
    List_otherFile = list()
    PROJECTNAME = sys.argv[sys.argv.index('-p')+1]
    PROJECTNAME = str(PROJECTNAME).replace('/', ' ').strip()
    print ("\033[1;31m  当前项目名称："+PROJECTNAME+"\033[0m")

    ConfPath = sys.argv[sys.argv.index('-c')+1]
    print ("\033[1;31m  当前conf.ini：" + ConfPath + "\033[0m")
    conf = ConfigParser.ConfigParser()
    conf.read('conf.ini')
    # todo
    update_svn(PROJECTNAME)
    CHAR = 'utf-8'
    # todo
    if str(conf.get("data", "datadir")).strip() == "":
        DATAFileName = 'data.txt'
    else:
        DATAFileName = conf.get("data", "datadir")
    if str(conf.get("custom", "CATALINA_HOME")).strip() == "":
        try:
            CATALINA_HOME = str(os.environ.get('CATALINA_HOME'))
        except Exception as e:
            print('no tomcat lib')
            CATALINA_HOME = None
            pass
    else:
        CATALINA_HOME = conf.get("custom", "CATALINA_HOME")
        print('CATALINA_HOME:'+CATALINA_HOME)
    if CATALINA_HOME == 'None':
        print('\033[1;31m 当前未设置Tomcat环境的jar包 如:servlet.jar等 如编译错误请配置CATALINA_HOME环境变量 \033[0m')
        EXJARPATH = PROJECTNAME + '/'+'WebRoot/WEB-INF/lib:'
    else:
        EXJARPATH = PROJECTNAME + '/'+'WebRoot/WEB-INF/lib:' + CATALINA_HOME + '/lib:'
    CLASSPATH = str()
    for path in os.listdir(PROJECTNAME):
        if not path.startswith(".") and '.' not in path:
            CLASSPATH += PROJECTNAME+'/'+path+':'
    CLASSPATH = '.:'+CLASSPATH
    print("\033[1;31m 使用默认 ClassPath:"+CLASSPATH+"\033[0m")
    with open(DATAFileName, 'r') as fileList:
        for line in fileList.readlines():
            if line.strip() == '' or line.strip().startswith('#') or line.strip().endswith('/'):
                pass
            else:
                if line.strip().endswith('java'):
                    List_javaFile.append(line.strip())
                else:
                    List_otherFile.append(line.strip())
    fileList.close()
    BUILDCMD = "javac -encoding " + CHAR \
               + " -Djava.ext.dirs=" + EXJARPATH\
               + " -cp " + CLASSPATH + " "+"-d "\
               + PROJECTNAME + "/WebRoot/WEB-INF/classes"
    nowTime = PROJECTNAME + '_' + time.strftime("%Y%m%d_%H%M%S") + '.zip'
    zf = zipfile.ZipFile(nowTime, "w", zipfile.zlib.DEFLATED)
    for JavaPath in List_javaFile:
        print('\033[1;32m')
        print('执行编译 >>>>'+BUILDCMD + JavaPath+'\033[0m ')
        os.system(BUILDCMD + JavaPath)
        #classpath = JavaPath.replace('.java', '.class')
        # print('\033[1;34m')
        # print("正在压缩 .class ...  "+classpath+'\033[0m ')
        # os.system('rm -rf '+classpath)
    print('\033[1;34m')
    print('正在压缩 .class ... >> WEB-INF/classes \033[0m ')
    zf.write(PROJECTNAME + "/WebRoot/WEB-INF/classes/")
    os.system('rm -rf ' + PROJECTNAME + "/WebRoot/WEB-INF/classes/*")
    for OtherPath in List_otherFile:
        # if not OtherPath.endswith('.java'):
        zf.write(OtherPath)
        print('\033[1;36m')
        print("正在压缩 其他文件 ...  "+OtherPath+'\033[0m')
    zf.close()
    print('\033[5;30;41m'+">"*8 + "打包完成----"+nowTime+"!"+"<"*8+'\033[0m')
    sys.exit(0)
