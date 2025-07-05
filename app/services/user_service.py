#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, List
from datetime import datetime
import hashlib
import secrets
from sqlalchemy.exc import IntegrityError
from app.database.db_manager import db_session
from app.models.user import User

class UserService:
    """用户服务类"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        对密码进行哈希处理
        :param password: 原始密码
        :return: 哈希后的密码
        """
        salt = secrets.token_hex(8)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}${hash_obj.hexdigest()}"

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """
        验证密码
        :param stored_password: 存储的哈希密码
        :param provided_password: 提供的原始密码
        :return: 验证是否通过
        """
        salt, hash_value = stored_password.split('$')
        hash_obj = hashlib.sha256((provided_password + salt).encode())
        return hash_obj.hexdigest() == hash_value

    @staticmethod
    def create_user(username: str, password: str, email: str, phone: str = None, 
                   id_card: str = None, full_name: str = None, additional_info: dict = None) -> User:
        """
        创建新用户
        :param username: 用户名
        :param password: 密码
        :param email: 邮箱
        :param phone: 手机号（可选）
        :param id_card: 身份证号（可选）
        :param full_name: 全名（可选）
        :param additional_info: 附加信息（可选，JSON格式）
        :return: 创建的用户对象
        """
        try:
            hashed_password = UserService.hash_password(password)
            user = User(
                username=username,
                password=hashed_password,
                email=email,
                phone=phone,
                id_card=id_card,
                full_name=full_name,
                additional_info=additional_info or {}
            )
            db_session.add(user)
            db_session.commit()
            return user
        except IntegrityError:
            db_session.rollback()
            raise ValueError("Username or email already exists")
        except Exception as e:
            db_session.rollback()
            raise e

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        通过ID获取用户
        :param user_id: 用户ID
        :return: 用户对象或None
        """
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username: str) -> List[User]:
        """
        通过用户名获取用户
        :param username: 用户名
        :return: 用户对象列表
        """
        return User.query.filter(User.username.ilike(f"{username}")).all()

    @staticmethod
    def get_user_by_email(email: str) -> List[User]:
        """
        通过邮箱获取用户
        :param email: 邮箱
        :return: 用户对象列表
        """
        return User.query.filter(User.email.ilike(f"{email}")).all()

    @staticmethod
    def get_user_by_phone(phone: str) -> List[User]:
        """
        通过手机号获取用户
        :param phone: 手机号
        :return: 用户对象列表
        """
        return User.query.filter(User.phone.ilike(f"{phone}")).all()

    @staticmethod
    def get_user_by_full_name(full_name: str) -> List[User]:
        """
        通过用户姓名获取用户
        :param full_name: 用户姓名
        :return: 用户对象列表
        """
        return User.query.filter(User.full_name.ilike(f"{full_name}")).all()

    @staticmethod
    def get_user_by_id_card(id_card: str) -> List[User]:
        """
        通过身份证号获取用户
        :param id_card: 身份证号
        :return: 用户对象列表
        """
        return User.query.filter(User.id_card.ilike(f"{id_card}")).all()

    @staticmethod
    def get_all_users() -> List[User]:
        """
        获取所有用户
        :return: 用户列表
        """
        return User.query.all()
        
    @staticmethod
    def count_users() -> int:
        """
        获取用户总数
        :return: 用户数量
        """
        return User.query.count()

    @staticmethod
    def update_user(user_id: int, **kwargs) -> Optional[User]:
        """
        更新用户信息
        :param user_id: 用户ID
        :param kwargs: 要更新的字段
        :return: 更新后的用户对象或None
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None

            # 如果更新密码，需要进行哈希处理
            if 'password' in kwargs:
                kwargs['password'] = UserService.hash_password(kwargs['password'])

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            user.updated_at = datetime.utcnow()
            db_session.commit()
            return user
        except IntegrityError:
            db_session.rollback()
            raise ValueError("Username or email already exists")
        except Exception as e:
            db_session.rollback()
            raise e

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        删除用户
        :param user_id: 用户ID
        :return: 是否删除成功
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            db_session.delete(user)
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()
            raise e

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        """
        用户认证
        :param username: 用户名
        :param password: 密码
        :return: 认证成功返回用户对象，失败返回None
        """
        user = UserService.get_user_by_username(username)
        if user and UserService.verify_password(user.password, password):
            return user
        return None

    @staticmethod
    def update_additional_info(user_id: int, info: dict = None, key: str = None, 
                             value: any = None, delete_key: str = None) -> Optional[User]:
        """
        更新用户的附加信息
        :param user_id: 用户ID
        :param info: 要更新的完整附加信息字典（会替换现有的）
        :param key: 要更新的特定键
        :param value: 要更新的特定值
        :param delete_key: 要删除的键
        :return: 更新后的用户对象或None
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None

            if info is not None:
                # 更新整个附加信息字典
                user.additional_info = info
            elif key is not None and value is not None:
                # 更新特定的键值对
                user.set_additional_info(key, value)
            elif delete_key is not None:
                # 删除特定的键
                if user.additional_info and delete_key in user.additional_info:
                    del user.additional_info[delete_key]

            user.updated_at = datetime.utcnow()
            db_session.commit()
            return user
        except Exception as e:
            db_session.rollback()
            raise e
