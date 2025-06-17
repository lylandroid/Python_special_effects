import os

def get_curr_dir() -> str:
    """获取当前工作目录"""
    return os.getcwd()

def get_curr_dir(file) -> str:
    """获取路径中的目录名"""
    return os.path.dirname(file)

def get_parent_dir(file) -> str:
    """获取父路径的目录名"""
    curr_dir = os.path.dirname(file)
    parent_dir = os.path.dirname(curr_dir)
    return parent_dir

def get_basename(path : str) -> str:
    """获取路径中的文件名"""
    return os.path.basename(path)

def join_file_uri(_file, file_uri : str) -> str:
    path = join(get_curr_dir(_file), file_uri)
    if not os.path.exists(path):
        print(f"文件不存在：{path}")
    return path

def join(dir, uri) -> str:
    return os.path.join(dir, uri)

def get_create_time(path: str) -> float:
    """获取文件的创建时间"""
    return os.path.getctime(path)

def get_access_time(path: str) -> float:
    """获取文件的最后访问时间"""
    return os.path.getatime(path)

def get_modify_time(path: str) -> float:
    """获取文件的最后修改时间"""
    return os.path.getmtime(path)

def get_file_size(path: str) -> int:
    """获取文件大小（字节为单位）"""
    return os.path.getsize(path)


def is_file(path : str) -> bool:
    """判断路径是否为文件"""
    return os.path.isfile(path)

def is_dir(path : str) -> bool:
    """判断路径是否为目录"""
    return os.path.isdir(path)

# 文件是否存在
def exists(file_path):
    return os.path.exists(file_path)

class _Assets:
    _app_assets_path = None
    _comm_assets_path = None

    def __init__(self, _file):
        self._file = _file

    def get_app_assets_path(self,uri = None, assets_name = "res") -> str:
        if self._app_assets_path is None:
            self._app_assets_path = join(get_parent_dir(self._file), assets_name)
            print(f"Assets._app_assets_path={self._app_assets_path}")

        if uri is None:
            return self._app_assets_path
        else:
            return join(self._app_assets_path, uri)
    
    def get_comm_assets_path(self, uri = None, assets_name = "assets") -> str:
        if self._comm_assets_path is None:
            self._comm_assets_path = join(get_curr_dir(self._file), assets_name)
            print(f"Assets._comm_assets_path={self._comm_assets_path}")

        if uri is None:
            return self._comm_assets_path
        else:
            return join(self._comm_assets_path, uri)