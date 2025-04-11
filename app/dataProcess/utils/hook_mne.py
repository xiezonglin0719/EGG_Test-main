from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 收集 mne 库的数据文件，但不包括存根文件
datas = collect_data_files('mne', include_py_files=False)
hiddenimports = collect_submodules('mne')

# 排除存根文件
excluded_files = ['__init__.pyi', 'utils/__init__.pyi']
for file in excluded_files:
    datas = [data for data in datas if not data[0].endswith(file)]