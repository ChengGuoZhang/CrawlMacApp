import json
import re
import sys
import time

from download_app.ftp_operation import UpdateJson,UploadFtp
from download_app.download import download_file

reload(sys)
sys.setdefaultencoding('utf-8')
url_json_file = "soft_macx_cn_items.json"


def main():
    # download software from the internet and store them on local temparaily
    # after upload them to Ftp server ,delete them
    with open(url_json_file, 'r') as fetch_items:
        items = json.load(fetch_items)

    len_items = len(items)

    for item in items:
        if item['is_download'] == True and item['is_upload_ftp'] == True or item['download_http_error'] == True:
            continue
        elif item['is_download'] == False:
            download_link = item['download_link']
            try:
                print "________________________________________________________________________________________________________________"
                # some download link provided by ther website is illegal which contains illegal character will down the program
                # As a result, extract the download link with regex just in ascii
                p = re.compile(r'[\x00-\xff]+')
                m = p.search(download_link)
                download_link = m.group()
                result = download_file(download_link)
            except Exception, ex:
                item['download_http_error'] = True

                print "[FAILED]   Downloading Failed url [" + download_link + "]            " + str(ex)
                UpdateJson(items)
            else:
                item['is_download'] = True
                item['download_time'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['soft_sha256'] = result[0]
                item['upload_file_name'] = result[1]
                UpdateJson(items)
                # when finish download , upload them to the ftp server immidetely
                UploadFtp(result[1], item)
                UpdateJson(items)
        elif item['is_upload_ftp'] == False:
            print "________________________________________________________________________________________________________________"
            UploadFtp(item['upload_file_name'],item)
            UpdateJson(items)


if __name__ == '__main__':
    main()