"""
通过API进行：
1. 上传视频
2. 处理视频
3. 开启nerf训练
4. 输出结果

"""

from flask import Flask, request,jsonify
from flask_restful import reqparse, abort, Api, Resource
from pathlib import Path
from capture import Capture
from utils_db import *
import json
import time
import redis,rq
import utils_redis
import utils_db
import utils_bucket
from my_module import create_nerf
from config import *
import os

from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

CORS(app)  # 允许所有来源的跨域请求

# meta
parser = reqparse.RequestParser()

parser.add_argument("title", type=str)
parser.add_argument("type", type=str)
parser.add_argument("date", type=str)
parser.add_argument("username")
parser.add_argument("slug", type=str)
parser.add_argument("latestRun", type=dict)

# cache list
cache_dict = {}


# Capture
class Caputures_Management(Resource):
    # get all captures or search
    def get(self):
        # cache list
        cache_dict = {}
        # 搜索
        title = None
        username = None
        # 没有参数
        if not request.form: # 无参数
            # 获取所有的Capture的状态，返回一个json，包含所有的信息
            cache_dict = get_all_captures()
            return cache_dict, 200
        elif request.form:
            # 获取参数
            if request.form.__contains__("title"):
                title = request.form["title"]
            if request.form.__contains__("username"):
                username = request.form["username"]
            cache_dict = search_captures(title,username)
            return cache_dict, 200
        return "no data",400
    # create a capture
    def post(self):
        if request.form:
            print(request.form)
            title = request.form["title"]
            username = request.form["username"]
        elif request.json:
            # 数据为json格式 , REST_FUL API开发的接口，一般用json格式传数据 , 这很重要
            args = parser.parse_args()
            title = args["title"]
            username = args["username"]
        elif request.data:
            # 处理二进制数据， 内容类型为form-data
            pass
        else: 
            return "No data", 400

        # 补充信息，根据参数,添加slug,source
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        random_num_str = date.split(' ')[1].replace(':','')
        slug = username + "-" + title + "-" + random_num_str # username-title-103119
        key_video = f'{slug}.mp4'
        source = utils_bucket.get_sign_url(key=key_video)
        # source = Path.cwd() / "video_data" / slug 
        # 准备输出，到cache中，数据库中
        source = str(source)
        capture =create_capture(title,username,slug=slug,source_url=source) # 创建实例，并添加到数据库中
        cache_dict[capture.slug] = capture.__dict__
        return capture.__dict__,200
    
    def delete(self):
        delete_all_captures()
        return 201

class single_Capture(Resource):
    # get a single capture
    def get(self, slug):
        target = get_a_capture(slug)
        # 获取单个Capture的状态，返回一个json，包含其信息
        if target:
            return target, 200
        else:
            return f'no {slug}', 200
    
    # trigger a capture
    def post(self, slug):
        # 判断是否已经在训练或队列中
        status = utils_db.get_a_capture(slug)['status']
        print(status)
        print(type(status))
        if status =='Started' or status == 'Enqueued':
            return f"{slug} is already {status},Triger fail" , 201

            
        if 1:
            # 1. Enqueued job
            info = {
                'status': "Enqueued",
                'latest_run_status': "Enqueued",
                'latest_run_current_stage': "Enqueued",
                'latest_run_progress': 0
            }
            utils_db.update_capture(slug, **info)    
            q_nerf = utils_redis.get_queue(queue_name='nerf_queue') # q.name = 'nerf_queue'

            # job失败后，直接抛弃，不重试
            job = q_nerf.enqueue(create_nerf, slug,job_timeout='2h',failure_ttl=0, on_failure=utils_db.on_failure)
            job_id = job.get_id()
            update_capture(slug,job_id=job_id)


            return f"{slug} is enqueued" , 201
        else:
            return f"{slug} is not enqueueed", 400
    def delete(self, slug):
        # 删除数据库中的记录，删除bucket中的文件
        delete_capture(slug)
        return f"secessfully deleted {slug}", 201

api.add_resource(Caputures_Management, "/capture")
api.add_resource(single_Capture, "/capture/<slug>")
if __name__ == "__main__":
    # 工作目录读写权限
    app.run(debug=True,host='0.0.0.0',port=8080)
