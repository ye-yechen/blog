# _*_ coding:utf-8 -*-

from django import template

#  自定义过滤器
register = template.Library()  # 自定义filter时必须加上


@register.filter(is_safe=True)  # 注册template filter
def get_dict_item(dictionary, key):     # 自定义在template中根据key取dict的value的过滤器
    return dictionary.get(key)