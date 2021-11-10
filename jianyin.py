import requests
import json
import math
import os

# songs  歌曲列表
# colections 歌曲目录目录

# category_info 视频素材目录
# effect_item_list 视频素材列表
歌曲分类 = {}
视频素材分类 = {}

path = 'Sessions.json'
file = open(path, 'r')

jsonp = file.read().encode('utf-8').decode('unicode_escape').replace("\n", "").replace(" ", "").replace("}{",
                                                                                                        "}\n{").replace(
    '"{', '{').replace('}"', '}').replace("\t", "").replace('\\"', '"').replace('\\n', '').split("\n")


def down(url, path, lx):
    if lx == 'm4a':
        headers = {
            'x-kss-meta-mm': '-|unknown-MediaName=mp4a'
        }
    elif lx == 'mp4':
        headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Cronet/TTNetVersion:60c657ad 2021-03-17 QuicVersion:47946d2a 2020-10-14',
            'x-tt-trace-id':'00-08aa736a0d8306dd0c039f7433170e78-08aa736a0d8306dd-01'
        }

    file_name = str(path.split('/')[-1])
    if os.path.exists('/'.join(path.split('/')[:3])) is False:
        os.makedirs('/'.join(path.split('/')[:3]))
    if os.path.exists(path) is False:
        try:
            print(file_name + "开始下载")
            down_file = requests.get(url, headers=headers, stream=True)
            print(down_file)
            with open(path, 'wb') as f:
                for chunk in down_file.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(file_name + '下载完成')
        except requests.exceptions.ConnectionError:
            if os.path.exists(path) is True:
                os.remove(path)
            print(file_name + '下载失败')


for i in jsonp:
    try:
        s = json.loads(i)
        if 'data' in list(s.get('response_data').keys()):
            if 'collections' in s.get('response_data').get('data'):
                for col in s.get('response_data').get('data').get('collections'):
                    歌曲分类[math.floor(int(col.get('id')) / 1000000) * 1000000] = col.get('name')
            elif 'songs' in s.get('response_data').get('data'):
                for son in s.get('response_data').get('data').get('songs'):
                    音乐名字 = son.get('title')
                    if '/' in 音乐名字:
                        音乐名字 = 音乐名字.replace('/', ' ')
                    # 音乐作者 = son.get('author')
                    下载链接 = son.get('preview_url')
                    music_path = os.path.join('./音乐',
                                              歌曲分类.get(math.floor(s.get('request_body').get('id') / 1000000) * 1000000),
                                              音乐名字 + '.m4a')
                    down(下载链接, music_path, 'm4a')
            # elif 'category_info' in s.get('response_data').get('data'):
            #     for cat in s.get('response_data').get('data').get('category_info').get("201"):
            #         视频素材分类[cat.get('category_id')] = cat.get('category_name')
            # elif 'effect_item_list' in s.get('response_data').get('data'):
            #     for eff in s.get('response_data').get('data').get('effect_item_list'):
            #         素材名称 = eff.get('author').get('name')
            #         if '/' in 素材名称:
            #             素材名称 = 素材名称.replace('/', ' ')
            #         素材下载链接 = eff.get('video').get('origin_video').get('video_url')
            #
            #         video_path = os.path.join('./视频素材',
            #                                   视频素材分类.get(s.get('request_body').get('category_id')),
            #                                   素材名称 + '.mp4')
            #         print(video_path)
            #         # down(素材下载链接, video_path, 'mp4')


    except Exception as e:
        print(e)
file.close()
