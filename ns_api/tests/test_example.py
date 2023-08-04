import pytest
import shutil
from pathlib import Path
import os 
import sys
import requests

# 将运行目录更改为tests
# 从上个目录引用
os.chdir('D:/Repo/algorithm/ns_api/tests')
sys.path.append('..')
import utils_bucket


cwd = Path('D:/Repo/algorithm/ns_api/')
base_name = fr'{str(cwd)}\123213412321341242131'
print(base_name)
archive = Path(rf'C:\Users\future\Desktop\eraLi')
root_dir = Path('C:/User/future/Desktop')
video_path = '../map.jpg'


url = 'http://localhost:8080/capture'
url_single = 'http://localhost:8080/capture/future-test-123456'
class Test_capture:
    def test_create_capture(self):
        response = requests.post(url,data={'username':'future','title':'eraLi'})
        # print(response.json())
        capture_data = response.json()
        slug = capture_data['slug']
        source_url = capture_data['source_url']
    def test_get_all_captures(self):
        # get all captures
        assert requests.get(url)
    def test_get_single_capture(self):
        # get single capture
        assert requests.get(url_single)
    def test_upload_to_bucket(self):
        slug = 'future-test-123456'
        utils_bucket.upload_to_bucket(slug,filename=video_path)
    def test_triger_nerf(self):
        response = requests.post
    def test_download_from_bucket(self):
        slug = 'future-test-123456'
        utils_bucket.download_to_local(slug,'test.jpg')
        # 删掉下载的文件
        os.remove('test.jpg')

class Test_job:
    def test_train_export_upload():
        slug = 'future-eraLi-131101'
        # mkdir
        data_dir = data_parent_dir / f'{slug}'
        video_path = data_dir / f'{slug}.mp4'
        data_dir.mkdir(parents=True, exist_ok=True)
        output_dir = cwd / 'outputs'
        # 2. Start training
        info = {
            'latest_run_current_stage': 'Training',
        }
        utils_db.update_capture(slug,**info)
        subprocess.run(f"ns-train nerfacto --data {data_dir}  --output-dir {output_dir} --pipeline.model.predict-normals True --max-num-iterations {200} --save-only-latest-checkpoint True --vis tensorboard  ",shell=True,cwd='/nerfstudio_restful')

        # 3. Start exporting mesh
        specific_output_dir = cwd / 'outputs' / slug
        config_path = next(specific_output_dir.glob('**/config.yml'), None)
        if config_path is None:
            return 'config_path doesnt exist',1
        info = {
            'latest_run_current_stage': 'Exporting',
        }
        utils_db.update_capture(slug,**info)
        job_id = utils_db.get_a_capture(slug)['job_id']
        specific_mesh_dir = data_dir / job_id
        subprocess.run(f"ns-export poisson --load-config {config_path} --output-dir {specific_mesh_dir} --num-pixels-per-side 1024--target-num-faces 1000",shell=True)

        # 4. Upload mesh to bucket
        key = f'{job_id}.zip'
        shutil.make_archive(base_name=str(specific_mesh_dir), format='zip', base_dir=specific_mesh_dir)
        filename = specific_mesh_dir.with_suffix('.zip')
        utils_bucket.upload_to_bucket(key,filename)
        # 5. Update result_url and status
        result_url = utils_bucket.get_sign_url_download(key=key)
        info = {
            'status':'Finished',
            'latest_run_current_stage': 'Finished',
            'latest_run_progress': 100,
            'result_url':result_url,
            'job_id': ""
        }
        utils_db.update_capture(slug,**info)
        print('job finished')
        # # 6. Delete data directory
        # shutil.rmtree(data_dir)