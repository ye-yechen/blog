# -*- coding:utf-8 -*-
import sys
import redis
import configparser
import json
import datetime
from collections import OrderedDict
import MySQLdb as mdb

from blog import settings


class Analyze(object):
    config = ''
    db_cursor = ''

    def __init__(self):
        # conf_dir = settings.STATIC_URL + 'config/conf.ini'
        # self.config = configparser.ConfigParser()
        # self.config.read(conf_dir)
        try:
            db_host = "127.0.0.1"
            db_port = 3306
            db_user = "root"
            db_pass = "340818"
            db_db = "blog"
            db_charset = "utf8"
            # db_host = self.config.get("db", "host")
            # db_port = int(self.config.get("db", "port"))
            # db_user = self.config.get("db", "user")
            # db_pass = self.config.get("db", "password")
            # db_db = self.config.get("db", "db")
            # db_charset = self.config.get("db", "charset")
            self.db = mdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_pass, db=db_db,
                                  charset=db_charset)
            self.db_cursor = self.db.cursor()
        except:
            print("请检查数据库配置")
            sys.exit()

            # 初始化redis连接
            # try:
            #     # redis_host = self.config.get("redis", "host")
            #     # redis_port = self.config.get("redis", "port")
            #     redis_host = "127.0.0.1"
            #     redis_port = 6379
            #     self.redis_con = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
            # except:
            #     print("请安装redis或检查redis连接配置")
            #     sys.exit()

    def get_user_num(self):  # 获取用户总数
        # 检查是否缓存
        try:
            result = None
            # result = json.loads(self.redis_con.get("user_num").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                            SELECT COUNT(*) FROM zhihu_user
                        '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取用户数量失败")
                return None
            data = self.db_cursor.fetchone()
            result = {'已统计的用户总数': data[0], '更新时间': datetime.datetime.now()}

            # 保存到redis
            # self.redis_con.set("user_num", result, 9600)

            return result
        else:
            return result

    def get_sex(self):  # 获取用户性别数量等数据
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("sex_num").decode('utf-8'))
        except Exception as err:
            print(err)
            result = None
        if not result:
            sql = '''SELECT
                        (SELECT COUNT(*) FROM zhihu_user WHERE gender = 1) AS male,
                        (SELECT COUNT(*) FROM zhihu_user WHERE gender = 0) AS female,
                        (SELECT COUNT(*) FROM zhihu_user WHERE gender = -1) AS other,
                        (SELECT COUNT(*) FROM zhihu_user) AS total
                    '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取性别比例失败")
                return None
            data = self.db_cursor.fetchone()
            result = OrderedDict([('男性', data[0]), ('女性', data[1]), ('未知', data[2])])
            # 保存到redis
            # self.redis_con.set("sex_num", result)
            return result
        else:
            return result

    # 学校人数统计
    def get_school_count(self):
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("school_count").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                     SELECT school,COUNT(*) FROM zhihu_user
                     WHERE school NOT LIKE '%本科%' AND LENGTH(school) > 8
                     GROUP BY school
                     ORDER BY COUNT(*) DESC
                     LIMIT 10
                 '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取学校统计失败")
                return None
            data = self.db_cursor.fetchall()
            result = OrderedDict()
            for row in data:
                result[row[0]] = row[1]

            # 保存到redis
            # self.redis_con.set("school_count", result)

            return result
        else:
            return result

    # 行业统计
    def get_business_count(self):
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("business_count").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                    SELECT business,COUNT(*) FROM zhihu_user
                    WHERE business <> ''
                    GROUP BY business
                    ORDER BY COUNT(*) DESC
                    LIMIT 10
                '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取行业比例失败")
                return None
            data = self.db_cursor.fetchall()
            result = OrderedDict()
            for row in data:
                result[row[0]] = row[1]

            # 保存到redis
            # self.redis_con.set("business_count", result)
            return result
        else:
            return result

    # 地域统计
    def get_location_count(self):
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("location_count").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                    SELECT location,COUNT(*) FROM zhihu_user
                     WHERE location <> '' AND location NOT LIKE "%美国%"
                     GROUP BY location
                     ORDER BY COUNT(*) DESC
                     LIMIT 10
                '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取位置分布失败")
                return None
            data = self.db_cursor.fetchall()
            result = OrderedDict()
            for row in data:
                result[row[0]] = row[1]

            # 保存到redis
            # self.redis_con.set("location_count", result, 9600)

            return result
        else:
            return result

    # 公司统计
    def get_company_count(self):
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("company_count").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                     SELECT company,COUNT(*) FROM zhihu_user
                     WHERE company <> '' AND company NOT LIKE "%学生%" AND company <> '无' AND company <> '自由职业' AND company <> '待业'
                     GROUP BY company
                     ORDER BY COUNT(*) DESC
                     LIMIT 10
                 '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取公司统计失败")
                return None
            data = self.db_cursor.fetchall()
            result = OrderedDict()
            for row in data:
                result[row[0]] = row[1]

            # 保存到redis
            # self.redis_con.set("company_count", result, 9600)
            return result
        else:
            return result

    # 获取赞同数统计数据
    def get_voteup_count(self):
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("agree_count").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                   SELECT
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 1000000) AS zero,
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 100000 AND voteup_count < 1000000) AS FIRST,
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 50000 AND voteup_count <100000) AS SECOND,
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 10000 AND voteup_count <50000) AS third,
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 5000 AND voteup_count <10000) AS fourth,
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 1000 AND voteup_count <5000) AS fifth,
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 500 AND voteup_count <1000) AS sixth,
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 100 AND voteup_count <500) AS seventh,
                (SELECT COUNT(*) FROM zhihu_user WHERE voteup_count >= 0 AND voteup_count <100) AS eighth     
                '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取赞同数统计失败")
                return None
            data = self.db_cursor.fetchone()

            result = OrderedDict(
                    [('>1000000', data[0]),
                     ('100000-1000000', data[1]),
                     ('50000-100000', data[2]),
                     ('10000-50000', data[3]),
                     ('5000-10000', data[4]),
                     ('1000-5000', data[5]),
                     ('500-1000', data[6]),
                     ('100-500', data[7]),
                     # ('0-100', data[8])
                     ])

            # 保存到redis
            # self.redis_con.set("agree_count", result, 9600)

            return result
        else:
            return result

    # 获取粉丝数统计数据
    def get_follower_count(self):
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("follower_count").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                    SELECT
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 1000000) AS zero,
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 100000 AND follower_count < 1000000) AS first,
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 50000 AND follower_count <100000) AS second,
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 10000 AND follower_count <50000) AS third,
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 5000 AND follower_count <10000) AS fourth,
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 1000 AND follower_count <5000) AS fifth,
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 500 AND follower_count <1000) AS sixth,
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 100 AND follower_count <500) AS seventh,
                    (SELECT COUNT(*) FROM zhihu_user WHERE follower_count >= 0 AND follower_count <100) AS eighth
                 '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取粉丝数统计失败")
                return None
            data = self.db_cursor.fetchone()
            result = OrderedDict(
                    [('>1000000', data[0]),
                     ('100000-1000000', data[1]),
                     ('50000-100000', data[2]),
                     ('10000-50000', data[3]),
                     ('5000-10000', data[4]),
                     ('1000-5000', data[5]),
                     ('500-100', data[6]),
                     ('100-500', data[7]),
                     # ('0-100', data[8])
                     ])

            # 保存到redis
            # self.redis_con.set("follower_count", result, 9600)

            return result
        else:
            return result

    # 获取回答问题数统计数据
    def get_answer_count(self):
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("agree_count").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                       SELECT
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 600) AS zero,
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 500 AND answer_count < 600) AS FIRST,
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 400 AND answer_count <500) AS SECOND,
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 300 AND answer_count <400) AS third,
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 200 AND answer_count <300) AS fourth,
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 150 AND answer_count <200) AS fifth,
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 100 AND answer_count <150) AS sixth,
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 50 AND answer_count <100) AS seventh,
                    (SELECT COUNT(*) FROM zhihu_user WHERE answer_count >= 0 AND answer_count <50) AS eighth   '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                print("获取答案数统计失败")
                return None
            data = self.db_cursor.fetchone()

            result = OrderedDict(
                    [('>600', data[0]),
                     ('500-600', data[1]),
                     ('400-500', data[2]),
                     ('300-400', data[3]),
                     ('200-300', data[4]),
                     ('150-200', data[5]),
                     ('100-150', data[6]),
                     ('50-100', data[7]),
                     # ('0-50', data[8])
                     ])

            # 保存到redis
            # self.redis_con.set("agree_count", result, 9600)

            return result
        else:
            return result

    # 用户昵称中英文统计
    def get_name_count(self):
        # 检查是否缓存
        try:
            result = None
            # result = eval(self.redis_con.get("business_count").decode('utf-8'))
        except:
            result = None
        if not result:
            sql = '''
                         SELECT (SELECT COUNT(*) FROM zhihu_user WHERE LENGTH(username) = CHAR_LENGTH(username) ) AS eng,
                         (SELECT COUNT(*) FROM zhihu_user WHERE LENGTH(username) <> CHAR_LENGTH(username) ) AS chn,
                         (SELECT COUNT(*) FROM zhihu_user) AS total
                    '''
            try:
                self.db_cursor.execute(sql)
            except Exception as err:
                print(err)
                return None
            data = self.db_cursor.fetchone()
            result = OrderedDict([('英文昵称比例', 100*data[0]/data[2])])
            # 保存到redis
            # self.redis_con.set("business_count", result)
            return result
        else:
            return result

    def __del__(self):
        self.db_cursor.close()
        self.db.commit()
        self.db.close()
