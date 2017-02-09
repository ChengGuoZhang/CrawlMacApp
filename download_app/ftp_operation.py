import json
import sys
import time
from ftplib import FTP

from compress_7z import *

reload(sys)
sys.setdefaultencoding('utf-8')

url_json_file = "soft_macx_cn_items.json"
ftp_setting_file = "ftp_setting.json"

def ftp_upload(ftp_upload_file):
    with open(ftp_setting_file, 'r') as fetch_items:
        items = json.load(fetch_items)

    ftp_host_address = items[0]['ftp_host_address']
    ftp_port = items[0]['ftp_port']
    ftp_username = items[0]['ftp_username']
    ftp_pass = items[0]['ftp_pass']

    ftp = FTP()
    ftp.set_debuglevel(0)
    ftp.connect(ftp_host_address, ftp_port)
    ftp.login(ftp_username, ftp_pass)
    print "Uploading to Ftp. Please wait......."

    ftp.cwd('/samples/CRAWLER_MACXCN/')

    bufsize = 8192

    file_handler = open(ftp_upload_file, "rb")
    ftp.storbinary('STOR %s' % os.path.basename(ftp_upload_file), file_handler, bufsize)
    file_handler.close()
    print "\t[Success]" + ftp_upload_file + " Upload into FTP Success!"
    ftp.quit()


def UploadFtp(file_name,item):
    try:
        ftp_upload(file_name)
    except Exception, ex:
        print "[FAILED]   Upload Failed file [" + item['upload_file_name'] + "]            " + str(ex)
    else:
        item['is_upload_ftp'] = True
        item['upload_time'] = time.strftime('%Y-%m-%d %X', time.localtime())
        # delete the local file
        os.remove(file_name)


def UpdateJson(items):
    len_items = len(items)
    with open(url_json_file, 'w+') as jsonFile:
        jsonFile.write('[\n')
        i = 0
        for item in items:
            i += 1
            jsonFile.write(json.dumps(item, ensure_ascii=False))
            if (i != len_items):
                jsonFile.write(',\n')
            else:
                jsonFile.write('\n')
        jsonFile.write(']')
    print "Updating Json File......"
    print "\t[Success]\tUpdate JsonFile Success"