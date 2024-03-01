import pathlib
import os
import re
def get_cloun_root_path():
    return pathlib.Path(r"\\10.236.200.22/")


def get_cloud_path():
    
    return get_cloun_root_path().joinpath("VEoutput").resolve()
a = r"\\10.236.200.22/VEoutput/IBB/IBB0020/cmp/v001/IBB020_cmp_v001_005.png"
c = r"\\10.236.200.22/VEoutput\ISN\ISN0050\CMP\v01"
print(pathlib.Path(a).suffix)
print(os.path.exists(c))
print(os.path.normpath(c))
print(get_cloud_path())
#os.startfile(os.path.normpath(c))
# print(r"\\10.236.200.22\VEoutput\ISN\ISN0020\CMP\001".replace(r"\\", "\\"))
# print(os.path.exists(r"\\10.236.200.22\VEoutput\ISN\ISN0020\CMP\001"))