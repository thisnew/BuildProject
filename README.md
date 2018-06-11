# BuildProject
## 增量打包工具，目前仅支持非maven等框架 使用javac编译 自动生成zip包 不能生成META_INF文件夹 内部使用工具
pip freeze > requirements.txt

### 使用方法：
    需要配置tomcat环境变量
    需要配置conf文件中部分（大部分不需要更改）
    
    data.txt文件名目前不能更改名称 加入后续
    data 文件格式
        配置需要更改的增量
    
### 运行命令:
```
    python zipProject.py -p [ProjectName]

    ./firstChackOut.sh [ProjectName]
```


### 后续
    配置文件更新
    
    todo
ok

