from django.shortcuts import render, redirect
import pandas as pd
from sqlalchemy import create_engine

# 数据库信息（以MySQL为例）
DB_username = 'root'
DB_password = 'ghjk45628'

# 数据库端口和名字
DB_port = 3306
DB_name = 'test'

# 创建管理池
engine = create_engine(f"mysql+pymysql://{DB_username}:{DB_password}@localhost:{DB_port}/{DB_name}", encoding='utf-8')
# engine = create_engine("sqlite:///test.db")
# 连接数据库
con = engine.connect()

# 上传excel文件,并将文件内容写入数据库中
def upload(request):
    if "GET" == request.method:
        return render(request, 'webPage/upload.html')
    else:
        excel_file = request.FILES["excel_file"]
        global filename
        filename = excel_file.name
        if not (filename.endswith('.xls') or filename.endswith('.xlsx')):
            return render(request, 'webPage/index.html')
        data = pd.read_excel(excel_file)
        try:
            # 清除之前文件的数据（删除数据表）
            pd.read_sql_query("drop table tempexcel", con=con)
        except:
            data.to_sql(name='tempexcel', con=con, if_exists='append', index=True)
    # 重定向刷新页面
    return redirect('../')

# 主页面（index）页面显示文件内容
def index(request):
    try:
        global data
        data = pd.read_sql_query("select * from tempexcel", con=con)
        global col_name
        col_name = list(data)
        global number
        number = len(list(data))
        return render(request, 'webPage/index.html', {'data':data.values, 'col_names':col_name})
    except:
        print('查询失败')
        return render(request, 'webPage/index.html')

# 删除数据行
def delete(request):
    # 根据传回的id删除指定数据行
    id = request.GET.get("id")
    try:
        pd.read_sql_query(f"delete from tempexcel where `index` = {id}", con=con)
    except:
        print('删除')
    return  redirect('../')

# 添加数据行
def add(request):
    if request.method == 'GET':
        try:
            data = pd.read_sql_query("select * from tempexcel", con=con)
            return render(request, 'webPage/add.html', {'col_names': list(data)[1:]})
        except:
            print('查询失败')
    else:
        # 构建新数据行
        inputdata = []
        for i in range(number - 1):
            inputdata.append(request.POST.get('inputdata' + str(i + 1), ''))
        # print(inputdata)
        test = pd.read_sql_query("select * from tempexcel", con=con)
        newdata = pd.DataFrame(dict(zip(col_name[1:], inputdata)), index = [len(test)])
        # print(newdata)
        newdata.to_sql(name='tempexcel', con=con, if_exists='append', index=True)
        return redirect('../')


# 修改数据行
def edit(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        try:
            row = data.values[int(id)]
            return render(request, 'webPage/edit.html', {'id':id, 'col_names': list(data), 'values':row})
        except:
            print('查询失败')
    else:
        id = request.POST.get("id")
        inputdata = []
        for i in range(number):
            inputdata.append(request.POST.get('inputdata' + str(i + 1), ''))
        # print(inputdata)
        try:
            int(inputdata[1])
            newdata = col_name[1] + "=" + inputdata[1]
        except:
            newdata = col_name[1] + "='" + inputdata[1] + "'"
        for i in range(2, len(inputdata)):
            try:
                int(inputdata[i])
                newdata += ',' + col_name[i] + "=" + inputdata[i]
            except:
                newdata += ',' + col_name[i] + "='" + inputdata[i] + "'"
        print(newdata)
        try:
            pd.read_sql_query(f"update tempexcel set {newdata} where `index` = {id}", con=con)
        except:
            print('修改')
        return redirect('../')

# 将数据库内容写入excel
def write(request):
    try:
        data = pd.read_sql_query("select * from tempexcel", con=con)
        data.to_excel(f'{filename}')
    except:
        print('写入失败')
    return redirect('../')


