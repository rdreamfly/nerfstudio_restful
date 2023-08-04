import oss2 

from config import *
import requests
import sys

print(oss2.__version__)

auth = oss2.Auth(AccessKey_ID2,AccessKey_Secret2)

bucket = oss2.Bucket(auth, endpoint='http://oss-cn-hangzhou.aliyuncs.com',bucket_name='f-test-bucket')
#等待完成的
# 1.app trigger capture前要把视频更名且放到 data/nerfstudio/<slug>/下
# 2. 上传(阻塞) -> 服务器下载（异步的） ->trigger capture -> 继续 

# 回调进度条
def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

# 签名url上传
def get_sign_url(key):
    url = bucket.sign_url(method='PUT', key=key,expires=600)
    return url

# 签名url下载,一年有效期
def get_sign_url_download(key):
    url = bucket.sign_url(method='GET', key=key,expires=60*60*24*365)
    return url
# with open('eraLi.mp4','rb') as f:
#     r = requests.put(url,data=f)
#     print(r.status_code)
#     print(r.headers)
#     print(r.text)

# 下载到本地
def download_to_local(key,filename):
    bucket.get_object_to_file(key=key,filename=filename,progress_callback=percentage)

# 上传到bucket
def upload_to_bucket(key,filename):
    bucket.put_object_from_file(key=key,filename=filename,progress_callback=percentage)

if __name__ =='__main__':    
    import os
    import shutil
    specific_mesh_dir = '/nerfstudio_restful/data/nerfstudio/future-eraLi-131101/083ddff8-11de-4c4b-9ba7-760dbb1bbeb7'
    shutil.make_archive(base_name =specific_mesh_dir,format='zip',root_dir=specific_mesh_dir) 
    print('test')