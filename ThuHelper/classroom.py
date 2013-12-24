# coding=utf-8

# classroom.py
# 教室排课信息获取

from database import getclassroomsbyfloor, getcoursebyroom
from utils import getClassSeqNumByDatetime
import datetime

class_sequence = {
    u'一': 1,
    u'二': 2,
    u'三': 3,
    u'四': 4,
    u'五': 5,
    u'六': 6,

    u'壹': 1,
    u'贰': 2,
    u'叁': 3,
    u'肆': 4,
    u'伍': 5,
    u'陆': 6,

    u'貮': 2,

    '1':   1,
    '2':   2,
    '3':   3,
    '4':   4,
    '5':   5,
    '6':   6,
}

buildings = {
    u'一': 1,
    u'二': 2,
    u'三': 3,
    u'四': 4,
    u'五': 5,
    u'六': 6,

    u'壹': 1,
    u'贰': 2,
    u'叁': 3,
    u'肆': 4,
    u'伍': 5,
    u'陆': 6,

    u'貮': 2,

    '1':   1,
    '2':   2,
    '3':   3,
    '4':   4,
    '5':   5,
    '6':   6,
}

cn_num = {
    u'〇': 0,
    u'一': 1,
    u'二': 2,
    u'三': 3,
    u'四': 4,
    u'五': 5,
    u'六': 6,
    u'七': 7,
    u'八': 8,
    u'九': 9,

    u'零': 0,
    u'壹': 1,
    u'贰': 2,
    u'叁': 3,
    u'肆': 4,
    u'伍': 5,
    u'陆': 6,
    u'柒': 7,
    u'捌': 8,
    u'玖': 9,

    u'貮': 2,
    u'两': 2,

    '1':   1,
    '2':   2,
    '3':   3,
    '4':   4,
    '5':   5,
    '6':   6,
    '7':   7,
    '8':   8,
    '9':   9,
    '0':   0,
}

cn_delta = {
    u'前': -2,
    u'昨': -1,
    u'今': 0,
    u'明': 1,
    u'后': 2,
    u'大后': 3,
}

building_storey = {
    '1':  (1, 2),
    '2':  (1, 2),
    '31': (1, 2, 3),
    '32': (1, 3),
    '33': (1, 2, 3, 4),
    '4':  (1, 2, 3, 4),
    '5':  (1, 2, 3),
    '6A': (0, 1, 2, 3, 4),
    '6B': (1, 2, 3, 4),
    '6C': (1, 2, 3),
}

def classroom(query):
    check_result = check_query(query)
    if check_result['is_valid'] == False:
        return check_result['prompt']
    query_dict = query_to_dict(query)
    form_result = formalize(query_dict)
    pre_prompt = form_pre_prompt(query_dict)
    post_prompt = form_result['post_prompt']
    query_list = form_result['query_list']
    ret = pre_prompt
    for q_dict in query_list:
        ret += get_free_classroom(q_dict)
    ret = ret.rstrip('\n')
    ret += post_prompt
    return ret

def get_free_classroom(q_dict):
    room_list = getclassroomsbyfloor(q_dict['building_id'], q_dict['storey'],
                                     q_dict['class_sequence'], q_dict['weekday'])
    ret = building_id_to_name(q_dict['building_id']) + q_dict['storey'] + u'层空闲教室：\n'
    if room_list == []:
        ret += u'无\n'
    else:
        for room in room_list:
            ret = ret + room['roomnumber'].split()[0] + '\n'
    return ret

def form_pre_prompt(query_dict):
    dt = datetime.datetime.now()
    ret = str(dt.month) + u'月' + str(dt.day + int(query_dict['day_delta'])) \
          + u'日' + u'第' + query_dict['class_sequence'] + u'大节\n'
    return ret

def formalize(query_dict):
    dt = datetime.datetime.now()
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday() + int(query_dict['day_delta'])
    is_all_valid = True
    prompt = ''
    q_list = []
    # 指明六教但未指明区
    if query_dict['building_id'] == '6ABC':
        # 未指定楼层
        if query_dict['storey'] == '-':
            for building in ('6A', '6B', '6C'):
                for storey in building_storey[building]:
                    q_list.append({
                        'building_id': building,
                        'storey': str(storey),
                        'weekday': weekday,
                        'class_sequence': int(query_dict['class_sequence']),
                    })
         # 指定了楼层
        else:
            for building in ('6A', '6B', '6C'):
                if int(query_dict['storey']) not in building_storey[building]:
                    is_all_valid = False
                    if building == '6C':
                        prompt += building_id_to_name(building) + u'只有' + \
                                  ''.join(map(lambda x: str(x)+u'、',
                                              building_storey[building])).rstrip(u'、') + u'层\n'
                    else:
                        prompt += building_id_to_name(building) + u'只在' \
                                 + ''.join(map(lambda x: str(x)+u'、',
                                               building_storey[building])).rstrip(u'、') \
                                 + u'层有自习教室\n'
                else:
                    q_list.append({
                        'building_id': building,
                        'storey': query_dict['storey'],
                        'weekday': weekday,
                        'class_sequence': int(query_dict['class_sequence']),
                    })
    # 指明三教但未指明段
    elif query_dict['building_id'] == '3123':
        if query_dict['storey'] == '-':
            for building in ('31', '32', '33'):
                for storey in building_storey[building]:
                    q_list.append({
                        'building_id': building,
                        'storey': str(storey),
                        'weekday': weekday,
                        'class_sequence': int(query_dict['class_sequence']),
                    })
        else:
            for building in ('31', '32', '33'):
                if int(query_dict['storey']) not in building_storey[building]:
                    is_all_valid = False
                    if building != '32':
                        prompt += building_id_to_name(building) + u'只有' + \
                                  ''.join(map(lambda x: str(x)+u'、',
                                              building_storey[str(building)])).rstrip(u'、') + u'层\n'
                    else:
                        prompt += building_id_to_name(building) + u'只在' \
                                 + ''.join(map(lambda x: str(x)+u'、',
                                               building_storey[str(building)])).rstrip(u'、') \
                                 + u'层有自习教室\n'
                else:
                    q_list.append({
                        'building_id': building,
                        'storey': query_dict['storey'],
                        'weekday': weekday,
                        'class_sequence': int(query_dict['class_sequence']),
                    })
    # 指明了不分区段的教学楼，或指明了六教某区，或指明了三教某段
    else:
        # 未指定楼层
        if query_dict['storey'] == '-':
            for storey in building_storey[query_dict['building_id']]:
                q_list.append({
                    'building_id': query_dict['building_id'],
                    'storey': str(storey),
                    'weekday': weekday,
                    'class_sequence': int(query_dict['class_sequence']),
                })
        # 指定了楼层
        else:
            # 指定楼层不正确
            if int(query_dict['storey']) not in building_storey[query_dict['building_id']]:
                is_all_valid = False
                if query_dict['building_id'] in ('6A', '6B', '32'):
                    prompt += building_id_to_name(query_dict['building_id']) + u'只在' \
                             + ''.join(map(lambda x: str(x)+u'、',
                                           building_storey[query_dict['building_id']])).rstrip(u'、') \
                             + u'层有自习教室\n'
                else:
                    prompt += building_id_to_name(query_dict['building_id']) + u'只有' \
                              + ''.join(map(lambda x: str(x)+u'、',
                                            building_storey[query_dict['building_id']])).rstrip(u'、') \
                              + u'层\n'
            # 指定楼层在正确范围内
            else:
                q_list.append({
                    'building_id': query_dict['building_id'],
                    'storey': query_dict['storey'],
                    'weekday': weekday,
                    'class_sequence': int(query_dict['class_sequence']),
                })
    if not is_all_valid:
        prompt = u'\n\n提示：\n' + prompt
    return {
        'post_prompt': prompt,
        'query_list': q_list,
    }

def check_query(query):
    is_valid = True
    prompt = ''
    # 检查天
    if u'天' in query:
        if query[query.index(u'天') - 1] not in cn_delta:
            is_valid = False
            prompt = u'亲～您是想查询哪一天的空闲教室呢？您可以指明“今天”、“明天”或者“后天”，来查询那一天的空闲教室情况^_^'
        elif query[query.index(u'天') - 1] in cn_delta:
            dt = datetime.datetime.now()
            weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
            weekday += cn_delta[query[query.index(u'天') - 1]]
            if weekday not in range(7):
                is_valid = False
                prompt = u'由于数据源的限制，现在只能得到本周的教室空闲情况信息'
    # 检查节
    if is_valid and u'节' in query:
        if query[query.index(u'节') - 1] == u'大':
            if query[query.index(u'节') - 2] not in cn_num:
                is_valid = False
                prompt = u'亲～您的输入的节数有点不对哦～请说明是第几节～举个栗子，您可以指明“第三节”，来查询第三节课时的空闲教室情况^_^'
            elif query[query.index(u'节') - 2] not in class_sequence:
                is_valid = False
                prompt = u'亲～您的输入的节数有点不对哦～一天只有六大节课^_^'
        elif query[query.index(u'节') - 1] not in cn_num:
            is_valid = False
            prompt = u'亲～您的输入的节数有点不对哦～请说明是第几节～举个栗子，您可以指明“第三节”，来查询第三节课时的空闲教室情况^_^'
        elif query[query.index(u'节') - 1] not in class_sequence:
            is_valid = False
            prompt = u'亲～您的输入的节数有点不对哦～一天只有六大节课^_^'
    # 检查教学楼
    if is_valid and u'教' in query:
        if query[query.index(u'教') - 1] not in cn_num:
            is_valid = False
            prompt = u'亲～您想查询哪个教学楼呢？现在支持一到六教。' \
                     u'举个栗子，您可以输入“四教”，来查询四教的空闲教室情况^_^'
        elif query[query.index(u'教') - 1] not in buildings:
            is_valid = False
            prompt = u'亲～教学楼只有一到六教，您想查询哪个教学楼呢？' \
                     u'比如说，您可以输入“四教”，来查询四教的空闲教室情况^_^'
        elif query[query.index(u'教') - 1] in buildings:
            if buildings[query[query.index(u'教') - 1]] == 6:
                if u'区' in query:
                    if query[query.index(u'区') - 1] not in ('a', 'b', 'c', 'A', 'B', 'C'):
                        is_valid = False
                        prompt = u'亲～六教有A区、B区和C区，您的输入似乎有点不对哦～' \
                                 u'举个栗子，您可以输入“六教A区”，来查询六教A区的空闲教室情况^_^'
            if buildings[query[query.index(u'教') - 1]] == 3:
                if u'段' in query:
                    if query[query.index(u'段') - 1] not in \
                            ('1', '2', '3', '一', '二', '三', u'壹', u'贰', u'叁', u'貮'):
                        is_valid = False
                        prompt = u'亲～三教有一段、二段和三段\n您的输入似乎有点不对哦～' \
                                 u'举个栗子，您可以输入“三教三段”，来查询三教三段的空闲教室情况^_^'
    # 检查楼层
    if is_valid and u'层' in query:
        if query[query.index(u'层') - 1] not in cn_num:
            is_valid = False
            prompt = u'亲～您输入的层数似乎有点不对哦～请说明是第几层^_^'
        else:
            building = buildings[query[query.index(u'教') - 1]]
            if building != 6 and building != 3:
                if cn_num[query[query.index(u'层') - 1]] not in building_storey[str(building)]:
                    is_valid = False
                    prompt = building_id_to_name(str(building)) + u'只有' + \
                             ''.join(map(lambda x: str(x)+u'、',
                                         building_storey[str(building)])).rstrip(u'、') \
                             + u'层\n您输入的层数似乎有点不对哦^_^'
            elif building == 6:
                if u'区' not in query:
                    if cn_num[query[query.index(u'层') - 1]] not in (0, 1, 2, 3, 4):
                        is_valid = False
                        prompt = u'亲～您输入的层数似乎有点不对哦～\n' \
                                 u'六教A区只在0、1、2、3、4层有自习教室\n' \
                                 u'六教B区只在1、2、3、4层有自习教室\n六教C区只有1、2、3层^_^'
                if u'区' in query:
                    section = query[query.index(u'区') - 1].upper()
                    building_section = str(building) + section
                    if cn_num[query[query.index(u'层') - 1]] not in building_storey[building_section]:
                        is_valid = False
                        if building_section != '6C':
                            prompt = building_id_to_name(building_section) + u'只在' + \
                                     ''.join(map(lambda x: str(x)+u'、',
                                                 building_storey[building_section])).rstrip(u'、') \
                                     + u'层有自习教室\n您输入的层数似乎有点不对哦^_^'
                        else:
                            prompt = building_id_to_name(building_section) + u'只有' + \
                                     ''.join(map(lambda x: str(x)+u'、',
                                                 building_storey[building_section])).rstrip(u'、') \
                                     + u'层\n您输入的层数似乎有点不对哦^_^'
            elif building == 3:
                if u'段' not in query:
                    if cn_num[query[query.index(u'层') - 1]] not in (1, 2, 3, 4):
                        is_valid = False
                        prompt = u'亲～您输入的层数似乎有点不对哦～\n' \
                                 u'三教一段只有1、2、3层\n' \
                                 u'三教二段只在1、3层有自习教室\n三教三段只有1、2、3、4层^_^'
                if u'段' in query:
                    section = cn_num[query[query.index(u'段') - 1]]
                    building_section = str(building) + str(section)
                    if cn_num[query[query.index(u'层') - 1]] not in building_storey[building_section]:
                        is_valid = False
                        if building_section != '32':
                            prompt = building_id_to_name(building_section) + u'只有' + \
                                     ''.join(map(lambda x: str(x)+u'、',
                                                 building_storey[building_section])).rstrip(u'、') \
                                     + u'层\n您输入的层数似乎有点不对哦^_^'
                        else:
                            prompt = building_id_to_name(building_section) + u'只在' \
                                 + ''.join(map(lambda x: str(x)+u'、',
                                               building_storey[building_section])).rstrip(u'、') \
                                 + u'层有自习教室\n您输入的层数似乎有点不对哦^_^'
    return {
        'is_valid': is_valid,
        'prompt': prompt,
    }

# 返回一个字典，其中各项的值均为字符串
def query_to_dict(query):
    if u'教' in query:
        building_id = toNum(query[query.index(u'教')-1])
    else:
        building_id = 1

    if u'节' in query:
        if query[query.index(u'节')-1] == u'大':
            sequence = toNum(query[query.index(u'节')-2])
        else:
            sequence = toNum(query[query.index(u'节')-1])
    else:
        dt = datetime.datetime.now()
        sequence = getClassSeqNumByDatetime(dt, 20)

    if u'层' in query:
        storey = str(toNum(query[query.index(u'层')-1]))
    else:
        storey = '-'

    if u'天' in query:
        if query[query.index(u'天')-1] == u'后' and query[query.index(u'天')-2] == u'大':
            day_delta = cn_delta[u'大后']
        else:
            day_delta = cn_delta[query[query.index(u'天')-1]]
    else:
        day_delta = 0

    section = ''
    if building_id == 6:
        if u'区' in query:
            section = query[query.index(u'区')-1].upper()
        else:
            section = 'ABC'
    elif building_id == 3:
        if u'段' in query:
            section = str(toNum(query[query.index(u'段')-1]))
        else:
            section = '123'
    building_id = str(building_id) + section
    return {
        'day_delta':   str(day_delta),
        'class_sequence':     str(sequence),
        'building_id': building_id,
        'storey':   storey,
    }

def toNum(word):
    if isinstance(word, int):
        return word
    if word in cn_num:
        return cn_num[word]
    else:
        return word

def building_id_to_name(building):
    building_dict = {
        '1': u'一教',
        '2': u'二教',
        '31': u'三教一段',
        '32': u'三教二段',
        '33': u'三教三段',
        '4': u'四教',
        '5': u'五教',
        '6A': u'六教A区',
        '6B': u'六教B区',
        '6C': u'六教C区',
    }
    return building_dict[building]

# 传入的room如果不是一个教室则原样返回
# 若是一个教室则返回该教室当天的排课信息
def getRoomCourseInfo(room):
    room = room.upper()
    result = getcoursebyroom(room)
    if len(result) != 0:
        return room + formCourseText(result)
    else:
        return room

# 根据六位的01字符序列生成教室占用情况
def formCourseText(sequence):
    text = u'教室今日安排：\n'
    i = 0
    for bit in sequence:
        i += 1
        text += u'第' + str(i) + u'大节'
        if bit == '0':
            text += u'空闲\n'
        else:
            text += u'有课\n'
    return text.rstrip('\n')