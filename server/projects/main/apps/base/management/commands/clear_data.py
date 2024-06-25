# -*- coding: utf-8 -*-
# Copyright (c) 2021-2024 THL A29 Limited
#
# This source code file is made available under MIT License
# See LICENSE for details
# ==============================================================================

"""
历史数据清理脚本



"""


import logging
import time
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models.deletion import Collector
from datetime import datetime, timedelta
from django.db import connections
from apps.codeproj import models
from util.webclients import AnalyseClient
from util.webclients import FileClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'clear data'

    def handle(self, *args, **options):
        print("执行handle方法")
        # 查找出删除时间已超过一个月的project，记录到列表

        # 获取当前时间
        now = datetime.now()

        # 过滤出 deleted_time 字段不为空且 time 字段与当前时间的差超过一个月的对象
        queryset = models.Project.everything.filter(
            deleted_time__isnull=False,
            #deleted_time__lte=now - timedelta(days=30)
            deleted_time__lte=now - timedelta(seconds=1)
        )

        # 记录需要被清除的project的id
        project_ids = []

        for project in queryset:
            project_ids.append(project.id)
        # project.delete(permanent=True)

        for project_id in project_ids:
            print(project_id)


        # 1、遍历所有需要被清除的project，远程调用analysis服务的删除操作，对project进行软删除。
        # for project_id in project_ids:
        #     print(project_id)
        #
        #     AnalyseClient().api('delete_project', data= None, path_params=(project_id,))


        # 结束后，需要到analysis服务中，执行清理脚本，清除相关数据。 直接在这里执行清除。



        # 2、遍历所有需要被清除的project，远程调用file服务的删除操作，对project相关的数据直接进行清除。
        for project_id in project_ids:
            FileClient.api('delete_project', data=None, path_params=(project_id,))




















        # # Collector 里的删除是有批次的，循环收集也要分批次
        # collector = Collector(using= 'codedog_main')
        # print(2)
        #
        # # 遍历列表，删除所有project相关联的数据cd
        # for project in queryset:
        #     list.append(project)
        #     print(project)
        #     collector.collect(project)
        #     print("收集器当前大小："+ len(collector.data))
        #     # 循环收集收据，到达一定量进行删除，然后休眠。
        #     if len(collector.data)>batch:
        #         collector.delete()
        #         print("休眠5s")
        #         time.sleep(5)
