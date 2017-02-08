import os

from pip._vendor import requests

from download_app.compress_7z import archive
from rename_sha256 import rename_sha256


def file_length(url):
    headers = {
        'Range':'byte=0-4'
    }
    try:
        r = requests.head(url,headers=headers)
        length = int(r.headers['content-length'])
    except Exception,ex:
        print "[ERROR]\tget file length fail\t\t\t" + str(ex)
    return length


def download_file(url):
    #  extract the real url for the redirect page when receive the 302 Http Response Code
    #tmp_page = requests.get(url, allow_redirects=False)
    #if tmp_page.status_code == 302:
     #   url = tmp_page.headers.get('location')

    local_filename = url.split('/')[-1]

    r = requests.get(url,stream=True)

    file_size_current = 0
    file_size = file_length(url)

    print "Downing loading: [%s]  Total Bytes: [%s]  :            " % (local_filename, file_size),
    with open(local_filename,'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
            file_size_current += len(chunk)
            status = r"%10d [%3.2f%%]" % (file_size_current, file_size_current * 100. / file_size)
            print status,
            print (chr(8) * (len(status) + 2)),
        print ''
    print "\t[Success] Download file " + local_filename + " successfully!"

    # using 7z to compress and encrypt the original file
    # add _ at the header of the zip_file_name to prevent the situation that the source file is a zip file.
    zip_file_name = "_"+local_filename[:-4] + ".zip"
    print "Compressing the File ......"
    result = archive(zip_file_name, local_filename)
    if (result[0] == False):
        print "\t[Error]\tCompress File Error\t" + zip_file_name+ "\t"+result
    else:
        print "\t[Success]\tCompress File Success\t" + zip_file_name
        os.remove(local_filename)
    return rename_sha256(zip_file_name, zip_done=result[0])  # return sha256

