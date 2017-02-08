# -*- encoding: utf-8 -*-
import os
import subprocess


def archive(dest_zip_file, source_file, level='-mx9', create_always=True, pwd='-pvirus'):
    """
    对7z压缩命令进行封装
    :param dest_zip_file: 压缩文件的文件名
    :param source_file:   待压缩的文件
    :param level:         压缩等级
    :param create_always: 每次都创建新的压缩文件
    :param pwd:            压缩文档的密码
    :return:
    """
    if create_always and os.path.exists(dest_zip_file):
        os.remove(dest_zip_file)

    cmd = "7z a {dest_zip_file} {source_file} {level} {pwd}".format(
        dest_zip_file=dest_zip_file,
        source_file=source_file,
        level=level,
        pwd=pwd
    )

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode == 0, err, cmd


def unarchive(zip_file, pwd='-pvirus'):
    """
    对7z解压命令进行封装
    :param zip_file:
    :param pwd:
    :return:
    """
    cmd = "7z x {zip_file} {pwd} -y".format(
        zip_file=zip_file,
        pwd=pwd
    )
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode == 0, err, cmd

