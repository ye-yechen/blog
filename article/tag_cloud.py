# -*- coding:utf-8 -*-


class TagCloud(object):  # 标签云
    MIN_FONT_SIZE = 12   # 最小尺寸
    MAX_FONT_SIZE = 45   # 最大尺寸
    FONT_SIZES = [MIN_FONT_SIZE, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, MAX_FONT_SIZE]
    COLORS = ['#bf242a', "#96514d", '#e6b422', '#006e54', '#895b8a', '#e7e7eb',
              '#47585c', '#f09199', '#007bbb', '#16160e', '#fdeff2', '#622a1d']

    def __init__(self, min_ref_count, max_ref_count):
        TagCloud.min_ref_count = min_ref_count
        # 如果最大标签和最小标签相等,那么认为两者的步长为0,所有标签取同样的font-size.
        if max_ref_count == min_ref_count:
            TagCloud.step = 0
        else:
            TagCloud.step = (TagCloud.MAX_FONT_SIZE - TagCloud.MIN_FONT_SIZE) / (max_ref_count - min_ref_count)

    def get_tag_font_size(self, tag_ref_count):     # 计算标签字大小
        font_size = TagCloud.MIN_FONT_SIZE + (tag_ref_count - TagCloud.min_ref_count) * TagCloud.step
        # 上面计算出来的font_size并不一定刚好是FONT_SIZES中的某个元素, 可以能某两个元素之间的某个值
        # 因此要取最接近FONT_SIZES中某个元素
        font_size = min(TagCloud.FONT_SIZES, key=lambda x: abs(font_size - x))
        return font_size

    def get_tag_color(self, tag_ref_count):     # 根据标签引用次数计算标签颜色
        return TagCloud.COLORS[(TagCloud.FONT_SIZES.index(self.get_tag_font_size(tag_ref_count)))]


'''
MIN_FONT_SIZE + n*step = MAX_FONT_SIZE，step是步长，
    n是指引用次数最多的标签减去引用次数最少的标签，表示两者之间总共有多少步step，
    根据此根式可以算出每一步的step值是多少，知道了步长后，就可以计算出任意一个标签的font-size了，
    任何一个标签到最小标签的步数是两者之差，
    因此每一个标签的font-size为 MIN_FONT_SIZE + (tag_ref_count-min_ref_count)*step.
'''


class TagInfo(object):  # tag信息类
    def __init__(self, tag_name, tag_size, tag_color, article_nums):
        self.tag_name = tag_name
        self.tag_size = tag_size
        self.tag_color = tag_color
        self.article_nums = article_nums
