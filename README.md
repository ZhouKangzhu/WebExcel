## 前言
本篇使用Python Web框架Django以及MySQL数据库，实现对Excel文件的在线读取和修改

## 开发环境
- 开发工具：Pycharm 2020.3
- 开发语言：Python 3.8.5
- Web框架：Django 3.0.6
- 数据库：MySQL8.021
- 操作系统：Windows 10

- Python类库
django
pymysql
sqlalchemy
pandas
xlrd
# WebExcel

## 思路
从前端读取Excel文件至后端
后端将Excel文件的数据写入MySQL数据库
通过将MySQL数据库的内容显示在前端，并提供增删改的功能

## 本地配置
在sims/views.py中配置MySQL数据库的信息


### 数据库信息（以MySQL为例）
DB_username = 'XXXXX'
DB_password = 'XXXXX'

### 数据库端口和名字
DB_port = 3306
DB_name = 'test'

填入数据库的用户以及密码
test的数据库也要先创建
