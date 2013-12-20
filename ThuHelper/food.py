# coding=utf-8

# food.py
# 食堂推荐功能

import random
import datetime
from .settings import URL_FOOD_IMAGE_PREF as IMAGE_PREF

food_filename = {
    u'紫荆一层木桶饭': '1mutong.jpg',
    u'紫荆一层原清芬香锅': '1xiangguo.jpg',
    u'紫荆一层湖南窗口': 'zijing.jpg',
    u'紫荆二层铁板': '2tieban.jpg',
    u'紫荆二层海南鸡饭': '2hainanjifan.jpg',
    u'紫荆二层云南米线': '2yunnanmixian.jpg',
    u'紫荆二层熟食': '2shushi.jpg',
    u'紫荆二层低糖少盐窗口': '2ditangshaoyan.jpg',
    u'紫荆二层淮扬菜': '2huaiyang.jpg',
    u'紫荆三层东北菜': '3dongbei.jpg',
    u'紫荆四层砂锅': '4shaguo.jpg',
    u'紫荆四层名厨窗口': '4mingchu.jpg',
    u'紫荆四层盖饭': '4gaifan.jpg',
    u'紫荆地下清青披萨': 'pizza.jpg',

    u'桃李地下清青休闲餐厅': 'taoli.jpg',
    u'桃李一层铁板': '1tieban.jpg',
    u'桃李一层麻辣烫': '1malatang.jpg',
    u'桃李一层沙县小吃': '1shaxianxiaochi.jpg',
    u'桃李一层米线': '1mixian.jpg',
    u'桃李二层自选': '2zixuan.jpg',
    u'桃李三层火锅': '3huoguo.jpg',
    u'桃李三层点餐餐厅': '3diancan.jpg',

    u'芝兰二层自助': '2zizhu.jpg',
    u'芝兰一层小火锅': '1huoguo.jpg',
    u'芝兰一层自选': 'zhilan.jpg',

    u'听涛陕西窗口': 'shannxi.jpg',
    u'听涛香锅': 'xiangguo.jpg',
    u'听涛山西面食': 'shanximianshi.jpg',
    u'听涛自选窗口': 'zixuan.jpg',

    u'闻馨香锅': 'xiangguo.jpg',
    u'闻馨瓦罐汤': 'waguantang.jpg',
    u'闻馨煎饼': 'jianbing.jpg',
    u'闻馨自选窗口': 'wenxin.jpg',

    u'清青快餐': 'kuaican.jpg',

    u'万人一层涮羊肉': 'shuanyangrou.jpg',
    u'万人一层麻辣烫': 'malatang.jpg',
    u'万人一层饺子': 'jiaozi.jpg',
    u'万人一层火锅面': 'guanchou.jpg',
    u'万人一层滑蛋饭': 'huadan.jpg',
    u'万人一层煎鸡饭': 'jianjifan.jpg',
    u'万人二层自选': '2zixuan.jpg',
    u'万人三层点餐餐厅': '3diancan.jpg',

    u'清青永和': 'yonghe.jpg',

    u'清青面吧': 'mianba.jpg',

    u'荷园一层自选': '1zixuan.jpg',
    u'荷园二层点餐餐厅': '2canting.jpg',

    u'澜园三层陕西窗口': 'lanyuan.jpg',
    u'澜园三层自选窗口': 'lanyuan.jpg',

    u'丁香鱼锅': 'dingxiang.jpg',
    u'丁香小炒': 'xiaochao.jpg',
    u'丁香名厨窗口': 'dingxiang.jpg',
    u'丁香香锅': 'xiangguo.jpg',
    u'丁香瓦罐汤': 'waguantang.jpg',
    u'丁香石锅饭': 'shiguofan.jpg',
}

refectory_food = {
    'zijing': [
        u'紫荆一层木桶饭',
        u'紫荆一层原清芬香锅',
        u'紫荆一层湖南窗口',
        u'紫荆二层铁板',
        u'紫荆二层海南鸡饭',
        u'紫荆二层云南米线',
        u'紫荆二层熟食',
        u'紫荆二层低糖少盐窗口',
        u'紫荆三层淮扬菜',
        u'紫荆三层东北菜',
        u'紫荆四层砂锅',
        u'紫荆四层名厨窗口',
        u'紫荆四层盖饭',
        u'紫荆地下清青披萨',
    ],
    'taoli': [
        u'桃李地下清青休闲餐厅',
        u'桃李一层铁板',
        u'桃李一层麻辣烫',
        u'桃李一层沙县小吃',
        u'桃李一层米线',
        u'桃李二层自选',
        u'桃李三层火锅',
        u'桃李三层点餐餐厅',
    ],
    'zhilan': [
        u'芝兰二层自助',
        u'芝兰一层小火锅',
        u'芝兰一层自选',
    ],
    'tingtao': [
        u'听涛陕西窗口',
        u'听涛香锅',
        u'听涛山西面食',
        u'听涛自选窗口',
    ],
    'wenxin': [
        u'闻馨香锅',
        u'闻馨瓦罐汤',
        u'闻馨煎饼',
        u'闻馨自选窗口',
    ],
    'kuaicai': [
        u'清青快餐',
    ],
    'wanren': [
        u'万人一层涮羊肉',
        u'万人一层麻辣烫',
        u'万人一层饺子',
        u'万人一层火锅面',
        u'万人一层滑蛋饭',
        u'万人一层煎鸡饭',
        u'万人二层自选',
        u'万人三层点餐餐厅',
    ],
    'yonghe': [
        u'清青永和',
    ],
    'mianba': [
         u'清青面吧',
    ],
    'heyuan': [
        u'荷园一层自选',
        u'荷园二层点餐餐厅',
    ],
    'lanyuan': [
        u'澜园三层陕西窗口',
        u'澜园三层自选窗口',
    ],
    'dingxiang': [
        u'丁香鱼锅',
        u'丁香小炒',
        u'丁香名厨窗口',
        u'丁香香锅',
        u'丁香瓦罐汤',
        u'丁香石锅饭'
    ],
}

refectory_weight = {
    'zijing': 50,
    'taoli': 50,
    'zhilan': 5,
    'tingtao': 40,
    'wenxin': 30,
    'kuaican': 10,
    'wanren': 50,
    'yonghe': 10,
    'mianba': 10,
    'heyuan': 5,
    'lanyuan': 5,
    'dingxiang': 50,
}

num_cn = {
    '1': u'一',
    '2': u'二',
    '3': u'三',
    '4': u'四',
    '5': u'五',
    '6': u'六',
    '7': u'天',
}

time_ranges = {
    'lunch_end': datetime.time(hour=13, second=0),
    'supper_end': datetime.time(hour=19, second=0),
}

def get_refectory():
    total = 0
    for key in refectory_weight:
        total += refectory_weight[key]
    num = random.randint(1, total)

    ret = ''
    refectories = sorted(refectory_weight)
    for key in refectories:
        if num - refectory_weight[key] <= 0:
            ret = key
            break
        else:
            num -= refectory_weight[key]
    return ret

def get_food(refectory):
    food_list = refectory_food[refectory]
    index = random.randint(0, len(food_list) - 1)
    return food_list[index]

def get_picture_url(refectory, food):
    return IMAGE_PREF + refectory + '/' + food_filename[food]

def food_articles():
    dt = datetime.datetime.now()
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    t = datetime.time(hour=dt.hour, second=dt.second)
    meal = ''
    if t < time_ranges['lunch_end']:
        meal = u'午饭'
    elif t < time_ranges['supper_end']:
        meal = u'晚饭'
    refectory = get_refectory()
    food = get_food(refectory)
    picture = get_picture_url(refectory, food)
    description = u'今天是星期' + num_cn[str(weekday + 1)] + u'\n' + meal + u'我们向您推荐:\n' \
               + food + u'\n去尝尝吧o(∩_∩)o'
    return [{
        'Title': food,
        'PicUrl': picture,
        'Url': ''
            }, {
        'Title': description,
        'Url': ''
    }]
