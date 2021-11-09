import os
import json
#songs  歌曲列表
#colections 歌曲目录目录

#category_info 视频素材目录
#effect_item_list 视频素材列表



path = 'Sessions.json'
file = open(path,'r')

jsonp = file.read().replace("\n","").replace(" ","").replace("}{","}\n{").replace('"{','{').replace('}"','}').split("\n")
for i in jsonp:
    # x=i.encode('utf-8').decode('unicode_escape')
    try:
        s=json.loads(i)
    except:
        print(i)
    # if x.get('response_data') :
        # print(x.get('response_data').get('data','no'))



file.close()