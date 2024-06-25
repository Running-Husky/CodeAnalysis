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
from apps.codemetric import codemetricmodels

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'clear data'

    def handle(self, *args, **options):
        print("执行handle方法")
        # 查找出删除时间已超过一个月的project，记录到列表

        # 过滤出 deleted_time 字段不为空且 time 字段与当前时间的差超过一个月的对象
        queryset = models.Project.everything.filter(
            deleted_time__isnull=False
        )

        # 每一批次删除数据的条数
        batch=100

        for project in queryset:
            id=project.id

            # 先把数据量大的库单独进行删除
            # 1、codemetric_duplicateBlock 表  对应DuplicateBlock 类
            duplicateblock=codemetricmodels.DuplicateBlock.filter(project_id=id)
            count=duplicateblock.count()
            cur=0
            while queryset.exists():
                batch = queryset[:batch]  # 获取100个对象
                batch.delete()
                cur+=batch
                print("重复代码问题数据正在进行删除"+cur+"/"+count)

            # 2、codemetric_clocFile 表  对应 ClocFile 类




            # 3、codemetric_clocDir 表  对应 ClocDir 类


            # 4、codelint_issue 表  对应  Issue 类


            # 5、codemetric_duplicateFile 表  对应  DuplicateFile 类


            # 6、codemetric_iuplicateIssue  表  对应 DuplicateIssue 类



            # # 剩余数据删除
            # project.delete(permanent=True)
