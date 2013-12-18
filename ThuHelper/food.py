# coding=utf-8

import random
import datetime

foods = [
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

    u'桃李地下清青休闲餐厅',
    u'桃李一层铁板',
    u'桃李一层麻辣烫',
    u'桃李一层沙县小吃',
    u'桃李一层米线',
    u'桃李二层自选',
    u'桃李三层火锅',
    u'桃李三层点餐餐厅',

    u'芝兰二层自助',
    u'芝兰一层小火锅',
    u'芝兰一层自选',

    u'听涛陕西窗口',
    u'听涛香锅',
    u'听涛山西面食',
    u'听涛自选窗口',

    u'闻馨香锅',
    u'闻馨瓦罐汤',
    u'闻馨煎饼',
    u'闻馨自选窗口',

    u'清青快餐',

    u'万人一层涮羊肉',
    u'万人一层麻辣烫',
    u'万人一层饺子',
    u'万人一层火锅面',
    u'万人一层滑蛋饭',
    u'万人一层煎鸡饭',
    u'万人二层自选',
    u'万人三层点餐餐厅',

    u'清青时代咖啡厅',

    u'清青永和',

    u'荷园一层自选',
    u'荷园二层点餐餐厅',

    u'澜园三层陕西窗口',
    u'澜园三层自选窗口',

    u'丁香鱼锅',
    u'丁香小炒',
    u'丁香名厨窗口',
    u'丁香香锅',
    u'丁香瓦罐汤',
    u'丁香石锅饭'
]

num_cn = {
    '1': u'一',
    '2': u'二',
    '3': u'三',
    '4': u'四',
    '5': u'五',
    '6': u'六',
    '7': u'天',
}

ranges = {
    'lunch_end': datetime.time(hour=13, second=0),
    'supper_end': datetime.time(hour=19, second=0),
}

def get_food():
    lenth = len(foods)
    index = random.randint(0, lenth - 1)
    dt = datetime.datetime.now()
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    t = datetime.time(hour=dt.hour, second=dt.second)
    meal = ''
    if t < ranges['lunch_end']:
        meal = u'午饭'
    elif t < ranges['supper_end']:
        meal = u'晚饭'
    return u'今天是星期' + num_cn[str(weekday+1)]+ u'\n' + meal + u'我们向您推荐:\n' \
        + tuple(foods)[index] + u'\n快去尝尝吧o(∩_∩)o'