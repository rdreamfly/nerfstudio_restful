import pytest
import shutil
from pathlib import Path
import os
import sys
import requests
import utils_db
import utils_bucket


# 将运行目录更改为tests
# 从上个目录引用
os.chdir("D:/Repo/algorithm/ns_api/tests")
sys.path.append("..")
import utils_bucket

usecase = {
    "url": "http://localhost:8080/capture",
    "url_single": "",
    "root_dir": "",
    "data_parent_dir": "",
    "data_dir": "",
    "slug": "test-test-123456",
    "source_url": "",
    "result_url": "",
    "key": "",  # key in bucket, the name of file
}
cwd = Path("D:/Repo/algorithm/ns_api/")
base_name = rf"{str(cwd)}\123213412321341242131"
print(base_name)
archive = Path(rf"C:\Users\future\Desktop\eraLi")
root_dir = Path("C:/User/future/Desktop")
video_path = "../map.jpg"
url = "http://localhost:8080/capture"
url_single = "http://localhost:8080/capture/future-test-123456"


class Test_capture:
    def test_create_capture(self):
        response = requests.post(url, data={"username": "future", "title": "eraLi"})
        # print(response.json())
        capture_data = response.json()
        slug = capture_data["slug"]
        source_url = capture_data["source_url"]

    def test_get_all_captures(self):
        # get all captures
        assert requests.get(url)

    def test_get_single_capture(self):
        # get single capture
        assert requests.get(url_single)

    def test_upload_to_bucket(self):
        slug = "future-test-123456"
        utils_bucket.upload_to_bucket(slug, filename=video_path)

    def test_triger_nerf(self):
        response = requests.post

    def test_download_from_bucket(self):
        slug = "future-test-123456"
        utils_bucket.download_to_local(slug, "test.jpg")
        # 删掉下载的文件
        os.remove("test.jpg")


class Test_job:
    def test_download(self):
        pass

    def test_process(self):
        pass

    def test_train(self):
        pass

    def test_export(self):
        pass

    def upload_to_bucket(self):
        pass
