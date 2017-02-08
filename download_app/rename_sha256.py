import hashlib
import os


def calc_sha256(filename):
    block_size = 64 * 1024
    with open(filename, 'rb') as fp:
        file_hash = hashlib.sha256()
        while (True):
            buf = fp.read(block_size)
            if not buf:
                break
            file_hash.update(buf)
    file_hash_value = file_hash.hexdigest()
    return file_hash_value


def rename_sha256(filename, zip_done):
    file_suffix = filename.split(".")[-1]
    if (zip_done):
        file_sha256 = calc_sha256(filename)
    else:
        file_sha256 = "[ERROR]" + filename[:-4]
    new_name = file_sha256 + "." + file_suffix
    os.rename(filename, new_name)
    result = [file_sha256, new_name]
    return result