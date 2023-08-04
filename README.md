<p align="center">
    <!-- community badges -->
    <a href="https://discord.gg/uMbNqcraFc"><img src="https://img.shields.io/badge/Join-Discord-blue.svg"/></a>
    <!-- doc badges -->
    <a href='https://plenoptix-nerfstudio.readthedocs-hosted.com/en/latest/?badge=latest'>
        <img src='https://readthedocs.com/projects/plenoptix-nerfstudio/badge/?version=latest' alt='Documentation Status' />
    </a>
    <!-- pi package badge -->
    <a href="https://badge.fury.io/py/nerfstudio"><img src="https://badge.fury.io/py/nerfstudio.svg" alt="PyPI version"></a>
    <!-- code check badges -->
    <a href='https://github.com/nerfstudio-project/nerfstudio/actions/workflows/core_code_checks.yml'>
        <img src='https://github.com/nerfstudio-project/nerfstudio/actions/workflows/core_code_checks.yml/badge.svg' alt='Test Status' />
    </a>
    <a href='https://github.com/nerfstudio-project/nerfstudio/actions/workflows/viewer_build_deploy.yml'>
        <img src='https://github.com/nerfstudio-project/nerfstudio/actions/workflows/viewer_build_deploy.yml/badge.svg' alt='Viewer build Status' />
    </a>
    <!-- license badge -->
    <a href="https://github.com/nerfstudio-project/nerfstudio/blob/master/LICENSE">
        <img alt="License" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">
    </a>
</p>

<p align="center">
    <!-- pypi-strip -->
    <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://docs.nerf.studio/en/latest/_images/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://docs.nerf.studio/en/latest/_images/logo.png">
    <!-- /pypi-strip -->
    <img alt="nerfstudio" src="https://docs.nerf.studio/en/latest/_images/logo.png" width="400">
    <!-- pypi-strip -->
    </picture>
    <!-- /pypi-strip -->
</p>
<!-- Use this for pypi package (and disable above). Hacky workaround -->
<!-- <p align="center">
    <img alt="nerfstudio" src="https://docs.nerf.studio/en/latest/_images/logo.png" width="400">
</p> -->

<p align="center"> A collaboration friendly studio for NeRFs </p>

<p align="center">
    <a href="https://docs.nerf.studio">
        <img alt="documentation" src="https://user-images.githubusercontent.com/3310961/194022638-b591ce16-76e3-4ba6-9d70-3be252b36084.png" width="150">
    </a>
    <a href="https://viewer.nerf.studio/">
        <img alt="viewer" src="https://user-images.githubusercontent.com/3310961/194022636-a9efb85a-14fd-4002-8ed4-4ca434898b5a.png" width="150">
    </a>
    <a href="https://colab.research.google.com/github/nerfstudio-project/nerfstudio/blob/main/colab/demo.ipynb">
        <img alt="colab" src="https://raw.githubusercontent.com/nerfstudio-project/nerfstudio/main/docs/_static/imgs/readme_colab.png" width="150">
    </a>
</p>


- [Quickstart](#quickstart)

# About

_It’s as simple as plug and play with nerfstudio!_

Nerfstudio provides a simple API that allows for a simplified end-to-end process of creating, training, and testing NeRFs.
The library supports a **more interpretable implementation of NeRFs by modularizing each component.**
With more modular NeRFs, we hope to create a more user-friendly experience in exploring the technology.

This is a contributor-friendly repo with the goal of building a community where users can more easily build upon each other's contributions.
Nerfstudio initially launched as an opensource project by Berkeley students in [KAIR lab](https://people.eecs.berkeley.edu/~kanazawa/index.html#kair) at [Berkeley AI Research (BAIR)](https://bair.berkeley.edu/) in October 2022 as a part of a research project ([paper](https://arxiv.org/abs/2302.04264)). It is currently developed by Berkeley students and community contributors.

We are committed to providing learning resources to help you understand the basics of (if you're just getting started), and keep up-to-date with (if you're a seasoned veteran) all things NeRF. As researchers, we know just how hard it is to get onboarded with this next-gen technology. So we're here to help with tutorials, documentation, and more!

Have feature requests? Want to add your brand-spankin'-new NeRF model? Have a new dataset? **We welcome [contributions](https://docs.nerf.studio/en/latest/reference/contributing.html)!** Please do not hesitate to reach out to the nerfstudio team with any questions via [Discord](https://discord.gg/uMbNqcraFc).

We hope nerfstudio enables you to build faster :hammer: learn together :books: and contribute to our NeRF community :sparkling_heart:.

# Quickstart

该项目主要是两个进程，进程1是flask app，监听请求，将训练任务放入redis队列；进程2是worker进程，用于监听队列，当队列有任务，则worker接受并进行处理。

## 1. 安装依赖 ： 设置运行虚拟环境

### 前置程序

主机必须用NVIDIA显卡并安装CUDA。最好是11.8CUDA。在这里看CUDA详细信息。[here](https://docs.nvidia.com/cuda/cuda-quick-start-guide/index.html)

### 创建环境

Nerfstudio 需要 `python >= 3.8`. 

nerfstudio用Conda来管理包，提前下载好 [Conda](https://docs.conda.io/en/latest/miniconda.html) 

```bash
conda create --name nerfstudio -y python=3.8
conda activate nerfstudio
pip install --upgrade pip
```

### 下载依赖包

安装CUDA版Pytorch和  [tiny-cuda-nn](https://github.com/NVlabs/tiny-cuda-nn)。 安装`tiny-cuda-nn`需要安装cuda-toolkit

CUDA 11.7:

```bash
pip install torch==2.0.1+cu117 torchvision==0.15.2+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

conda install -c "nvidia/label/cuda-11.7.1" cuda-toolkit
pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
```

CUDA 11.8:

```bash
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit
pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
```

nerfstudio项目详细的依赖安装文档 [Dependencies](https://github.com/nerfstudio-project/nerfstudio/blob/main/docs/quickstart/installation.md#dependencies)

### 下载 nerfstudio_restful项目

安装好依赖后，克隆项目

```bash
git clone https://github.com/FuturaTino/nerfstudio_restful.git
cd nerfstudio_restful
pip install --upgrade pip setuptools
pip install -e .
```



### 其他选择：Docker部署

后续写







## 2.启动服务： Flask app 和 rq worker

```shell
conda activate nerfstudio
cd nerfstudio_restful
python ns_api/utils_worker.py -q nerf_queue
# 打开一个新的terminal
python ns_api/app.py 
```



## 3. 通过接口访问三维重建服务

假设请求网址为 http://127.0.0.1:8080，

后端语言与框架：python flask

客户端语言： python

### 创建任务

1. 首先向http://127.0.0.1:8080/capture发送POST请求，携带数据`username`与`title`，服务器会初始化一个 **Capture对象**，用以这次三维重建任务的所有信息。POST请求会返回一个Response，其中包含Capture对象的详细信息，即一个 **json文件**，其中包含这次三维重建所需要的所有信息。我们获取Response中的`source_url`和`slug`字段。 Response内容格式[点这里](###Response)。 

```python
import requests

username = "Zhangsan"
capture_title = "table"

response = requests.post("https://createmesh.com/capture",
                         data={'title': capture_title,
                               'username': username})
capture_data = response.json()
upload_url = capture_data['source_url']
slug = capture_data['slug']

print(capture_data)
print("Srouce URL for uploading:", source_url)
print("Capture slug:", slug)
```



### 获取任务信息



### 上传视频

2. 获取Response中的`source_url`字段`https://bucket-storage.com/zhangsan-table-122435`，**向该网址发送PUT请求，上传视频文件**。该请求没有Response，只是单向的文件传输。获得上传成功的code即可。

```python
with open("video.mp4", "rb") as f:
    payload = f.read()

# source_url from step (1)
response = requests.put(source_url,data=payload)

print(response.text)



# curl 
curl -X PUT -T "C:\Users\future\Desktop\eraLi.mp4" "http://f-test-bucket.oss-cn-hangzhou.aliyuncs.com/future-eraLi-102047.mp4?OSSAccessKeyId=LTAI5t6SxcPWVVEm5J48uHZg&Expires=1690857047&Signature=Cfl%2Fmv4Mro%2FirteTIWh%2Be8BKxRM%3D"
```





### **启动训练**

2. 获取 `slug`字段，向 http://127.0.0.1:8080/capture<slug> 发送 POST请求。

```python
# slug from Capture step
response = requests.post(f"http://127.0.0.1:8080/capture/{slug}")

print(response.text) # f"{slug} has enequeued"
```



### 下载模型

4. 通过`slug`获取任务的实时信息。 向 https://createmesh.com/capture/<slug>， 发送GET请求。当任务完成，status字段为变为`Finished`。获取`result_url`的字段，向`result_url`发送GET请求，即可下载mesh文件压缩包。

```python
# slug from Capture step
response = requests.get(f"http://127.0.0.1:8080/capture/{slug}")

print(response.text)
```



### Response

Response中的数据结构

```python
{
    "slug" : "zhangsan-table-122435",
    "title": "table",
    "type" : "reconstruction",
    "date" : "2023.7.28-23:41:43",
    "username": "zhangsan",
    "status": "wait_for_upload",
    "latest_run_status": "wait_for_upload",
    "latest_run_progress": 0,
    "latest_run_current_stage": "wait_for_upload",
    "source_url": "https://bucket-storage.com/zhangsan-table-122435",
    "result_url": ""
}
```

解释如下：

- slug: 任务的唯一标识,表明是用户zhangsan创建的,关于table,创建时间是23:41:43
- title: 任务的标题或名称,这里是"table"
- type: 任务类型,这里是"reconstruction",表示3D重建任务（目前就这一个值）
- date: 任务的创建时间
- username: 创建任务的用户名称
- status: 任务整体状态,这里是"wait_for_upload",表示正在等待用户上传文件
- latest_run_status: 最近一次运行的状态,同样为"wait_for_upload"
- latest_run_progress: 最近一次运行的进度,这里是0,表示刚创建,还没开始处理
- latest_run_current_stage: 最近一次运行的当前执行阶段,同上 为"wait_for_upload"
- source_url: 源文件上传的地址
- result_url: 生成结果文件的地址,现在还为空







# 项目结构

项目主要用到以下组件

| 组件  | 解释                                                        |
| ----- | ----------------------------------------------------------- |
| 主机  | 一个进程flask app和一个worker进程处理长时间任务。           |
| mysql | 目前使用阿里云的mysql服务器，预计到10月15号到期             |
| redis | 同使用阿里云                                                |
| oss   | 目前使用阿里云的oss服务，主要使用上传、下载、签名url三个API |



计划以后一个主机运行flask app ，再使用另外一台主机运行worker进程。通过redis实现进程通信。完全解耦后，可以通过扩展主机数量增加处理任务的能力。项目运行原理如下图

![Flask 集成 Redis Queue 的调用时序图](https://github.com/FuturaTino/TyporaImages/raw/main//images/68747470733a2f2f7465737464726976656e2e696f2f7374617469632f696d616765732f626c6f672f666c61736b2d72712f666c61736b2d72712d666c6f772e706e67)

	## 训练流程图

![ns_train](C:\Users\future\Desktop\ns_train.png)

# Built On

<a href="https://github.com/brentyi/tyro">
<!-- pypi-strip -->
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://brentyi.github.io/tyro/_static/logo-dark.svg" />
<!-- /pypi-strip -->
    <img alt="tyro logo" src="https://brentyi.github.io/tyro/_static/logo-light.svg" width="150px" />
<!-- pypi-strip -->
</picture>
<!-- /pypi-strip -->
</a>

- Easy-to-use config system
- Developed by [Brent Yi](https://brentyi.com/)

<a href="https://github.com/KAIR-BAIR/nerfacc">
<!-- pypi-strip -->

<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/3310961/199083722-881a2372-62c1-4255-8521-31a95a721851.png" />
<!-- /pypi-strip -->
    <img alt="tyro logo" src="https://user-images.githubusercontent.com/3310961/199084143-0d63eb40-3f35-48d2-a9d5-78d1d60b7d66.png" width="250px" />
<!-- pypi-strip -->
</picture>
<!-- /pypi-strip -->
</a>

- Library for accelerating NeRF renders
- Developed by [Ruilong Li](https://www.liruilong.cn/)

# Citation

You can find a paper writeup of the framework on [arXiv](https://arxiv.org/abs/2302.04264).

If you use this library or find the documentation useful for your research, please consider citing:

```
@inproceedings{nerfstudio,
	title        = {Nerfstudio: A Modular Framework for Neural Radiance Field Development},
	author       = {
		Tancik, Matthew and Weber, Ethan and Ng, Evonne and Li, Ruilong and Yi, Brent
		and Kerr, Justin and Wang, Terrance and Kristoffersen, Alexander and Austin,
		Jake and Salahi, Kamyar and Ahuja, Abhik and McAllister, David and Kanazawa,
		Angjoo
	},
	year         = 2023,
	booktitle    = {ACM SIGGRAPH 2023 Conference Proceedings},
	series       = {SIGGRAPH '23}
}
```

# Contributors

<a href="https://github.com/nerfstudio-project/nerfstudio/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=nerfstudio-project/nerfstudio" />
</a>
