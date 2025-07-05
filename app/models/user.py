#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, Text
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import validates
import re
from app.database.db_manager import Base

class User(Base):
    """用户模型"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30),  nullable=False)
    password = Column(String(50), nullable=True)  # 存储加密后的密码
    email = Column(String(50),  nullable=False)
    phone = Column(String(11),  nullable=True, index=True)  # 手机号
    id_card = Column(String(18), nullable=True)  # 身份证号
    full_name = Column(String(10),  nullable=True)  # 姓名
    _additional_info = Column('additional_info', Text, nullable=True)  # 附加信息，存储为JSON字符串

    # # 联合唯一约束：同一用户的同一email只能存在一条记录
    # __table_args__ = (
    #     UniqueConstraint('username', 'email', name='uq_user_device'),
    # )

    @property
    def additional_info(self):
        """获取附加信息字典"""
        if self._additional_info is None:
            return {}
        try:
            return json.loads(self._additional_info)
        except json.JSONDecodeError:
            return {}

    @additional_info.setter
    def additional_info(self, value):
        """设置附加信息字典"""
        if value is None:
            self._additional_info = None
        else:
            self._additional_info = json.dumps(value)
            
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates('email')
    def validate_email(self, key, email):
        # 为空直接返回
        if not email:  # 可以为空
            return None
        email = email.replace(' ', '')
        """验证邮箱格式"""
        if not email:
            raise ValueError('Email is required')

        # pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # if not re.match(pattern, email):
        #     raise ValueError('Invalid email format')

        return email

    @validates('username')
    def validate_username(self, key, username):
        """验证用户名"""
        if not username:
            raise ValueError('Username is required')

        # if len(username) < 3:
        #     raise ValueError('Username must be at least 3 characters long')

        # if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        #     raise ValueError('Username can only contain letters, numbers, underscores and hyphens')

        return username
        
    @validates('phone')
    def validate_phone(self, key, phone):
        # 手机号为空直接返回
        if not phone:  # 手机号可以为空
            # raise ValueError('phone is required')
            return None
        phone = phone.replace(' ', '')
        """验证手机号格式"""
        if phone:  # 手机号可以为空
            if not re.match(r'^1[3-9]\d{9}$', phone):
                # raise ValueError('Invalid phone number format')
                return None

        return phone
        
    @validates('id_card')
    def validate_id_card(self, key, id_card):
        # 为空直接返回
        if not id_card:  # 可以为空
            return None
        id_card = id_card.replace(' ', '')
        """验证身份证号格式"""
        if id_card:  # 身份证号可以为空
            if not re.match(r'^\d{17}[\dXx]$', id_card):
                # raise ValueError('Invalid ID card format')
                return None
        return id_card

    def __repr__(self):
        """返回用户实例的字符串表示"""
        return f'<User {self.username}>'

    def to_dict(self):
        """将用户对象转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'id_card': self.id_card,
            'full_name': self.full_name,
            'additional_info': self.additional_info,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
    def get_additional_info(self, key=None, default=None):
        """
        获取附加信息
        :param key: 键名，如果为None则返回整个附加信息字典
        :param default: 如果键不存在，返回的默认值
        :return: 附加信息或指定键的值
        """
        if self.additional_info is None:
            self.additional_info = {}
            
        if key is None:
            return self.additional_info
        return self.additional_info.get(key, default)
        
    def set_additional_info(self, key, value):
        """
        设置附加信息
        :param key: 键名
        :param value: 值
        """
        if self.additional_info is None:
            self.additional_info = {}
            
        self.additional_info[key] = value
        return self
