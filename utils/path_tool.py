import os

#获取根目录
def get_project_root():#从一个完整的文件路径中，提取出【所在的文件夹路径】，自动去掉最后的文件名
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#由相对获取绝对路径
#os.path.join把多个路径片段智能拼接成一个完整、合法的路径
def get_abs_path(relative_path):
    return os.path.join(get_project_root(), relative_path)