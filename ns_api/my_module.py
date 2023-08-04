import subprocess
import zipfile
from sqlalchemy import text
from pathlib import Path
import utils_db
from config import *
import utils_bucket
import shutil
import os
# config
cwd = Path('/nerfstudio_restful')
data_parent_dir = cwd / f'data/nerfstudio'

output_dir = cwd / f'outputs'

# # test_meta
# test_slug = 'future-eraLi-123456'
# slug = test_slug
# data_dir = data_parent_dir / f'{slug}'


def download_video_to_dir_from_bucket(slug):
    key = f'{slug}.mp4'
    filename = data_parent_dir / slug /f'{slug}.mp4' # be careful
    utils_bucket.download_to_local(key,filename)
    return filename
def create_nerf(slug):
<<<<<<< HEAD
    # 0. Download video from bucket
    info = {
        'status':'downloading',
        'latest_run_status':'downloading',
        'latest_run_current_stage':'downloading',
    }
    utils_db.update_capture(slug,**info) # 下载中
    download_video_to_dir_from_bucket(slug)

=======
    # mkdir
    data_dir = data_parent_dir / f'{slug}'
    video_path = data_dir / f'{slug}.mp4'
    data_dir.mkdir(parents=True, exist_ok=True)
    if not video_path.exists():
    # 0. Download video from bucket
        info = {
            'status':'Downloading',
            'latest_run_status':'Downloading',
            'latest_run_current_stage':'Downloading',
        }
        utils_db.update_capture(slug,**info) # 下载中
        download_video_to_dir_from_bucket(slug)
        print('Downloaded')
>>>>>>> e58ba6ade247ab5158b4d662dd927b641f06816e
    # 1. Started processing
    info = {
        'status':'Started',
        'latest_run_status':'Started',
        'latest_run_current_stage': 'Preprocessing',
    }
    utils_db.update_capture(slug,**info)
    data_dir = data_parent_dir / f'{slug}'
    subprocess.run(f"ns-process-data video --data {video_path} --output-dir {data_dir}",shell=True)

    # 2. Start training
    info = {
        'latest_run_current_stage': 'Training',
    }
    utils_db.update_capture(slug,**info)
    subprocess.run(f"ns-train nerfacto --data {data_dir}  --output-dir {output_dir} --pipeline.model.predict-normals True \
        --max-num-iterations {200} --save-only-latest-checkpoint True --vis tensorboard  ",shell=True,cwd='/nerfstudio_restful')

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
    subprocess.run(f"ns-export poisson --load-config {config_path} --output-dir {specific_mesh_dir}",shell=True)

    # 4. Upload mesh to bucket
    key = f'{job_id}.zip'
    shutil.make_archive(base_name=job_id, format='zip', root_dir=specific_mesh_dir)
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
    # 5. Delete data directory
    shutil.rmtree(data_dir)

def test_create_nerf_with_data(slug):
    # mkdir
    data_dir = data_parent_dir / f'{slug}'
    video_path = data_dir / f'{slug}.mp4'
    data_dir.mkdir(parents=True, exist_ok=True)

    # # 3. Start exporting mesh
    # specific_output_dir = cwd / 'outputs' / slug
    # config_path = next(specific_output_dir.glob('**/config.yml'), None)
    # if config_path is None:
    #     return 'config_path doesnt exist',1
    # info = {
    #     'latest_run_current_stage': 'Exporting',
    # }
    # utils_db.update_capture(slug,**info)
    # # job_id = utils_db.get_a_capture(slug)['job_id']
    job_id = '38bfe0fa-d611-478b-8d51-6186a95707ef'
    title = slug.split('-')[1]
    specific_mesh_dir = data_dir / job_id / title
    # subprocess.run(f"ns-export poisson --load-config {config_path} --output-dir {specific_mesh_dir} --num-pixels-per-side 1024 --target-num-faces 1000 --num-points 10000" ,shell=True)

    # 4. Upload mesh to bucket
    os.chdir(data_dir)
    key = f'{job_id}.zip'
    print('zip')
    shutil.make_archive(base_name=job_id, format='zip', root_dir=specific_mesh_dir)

    # filename = specific_mesh_dir.with_suffix('.zip')
    filename = specific_mesh_dir.with_suffix('.zip')
    print('upload')
    utils_bucket.upload_to_bucket(key,filename)
    # 5. Update result_url and status
    print('get url')
    result_url = utils_bucket.get_sign_url_download(key=key)
    print(result_url)
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
if __name__ == "__main__":
    test_slug = 'future-eraLi-131101'
    test_create_nerf_with_data(test_slug)