#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.user_service import UserService
from app.database import init_db, db_session

class TestUserService(unittest.TestCase):
    """用户服务测试类"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        init_db()

    def setUp(self):
        """每个测试用例开始前的设置"""
        # 清理数据库中的测试数据
        db_session.query(UserService.get_user_by_username("testuser").delete())
        db_session.commit()

    def tearDown(self):
        """每个测试用例结束后的清理"""
        # 清理数据库中的测试数据
        db_session.query(UserService.get_user_by_username("testuser").delete())
        db_session.commit()

    def test_create_user(self):
        """测试创建用户"""
        user = UserService.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com",
            full_name="Test User"
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.full_name, "Test User")

    def test_get_user(self):
        """测试获取用户"""
        # 创建测试用户
        created_user = UserService.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com"
        )

        # 通过ID获取用户
        user_by_id = UserService.get_user_by_id(created_user.id)
        self.assertIsNotNone(user_by_id)
        self.assertEqual(user_by_id.username, "testuser")

        # 通过用户名获取用户
        user_by_username = UserService.get_user_by_username("testuser")
        self.assertIsNotNone(user_by_username)
        self.assertEqual(user_by_username.email, "test@example.com")

        # 通过邮箱获取用户
        user_by_email = UserService.get_user_by_email("test@example.com")
        self.assertIsNotNone(user_by_email)
        self.assertEqual(user_by_email.username, "testuser")

    def test_update_user(self):
        """测试更新用户"""
        # 创建测试用户
        user = UserService.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com"
        )

        # 更新用户信息
        updated_user = UserService.update_user(
            user.id,
            full_name="Updated Name",
            email="updated@example.com"
        )

        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.full_name, "Updated Name")
        self.assertEqual(updated_user.email, "updated@example.com")

    def test_delete_user(self):
        """测试删除用户"""
        # 创建测试用户
        user = UserService.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com"
        )

        # 删除用户
        result = UserService.delete_user(user.id)
        self.assertTrue(result)

        # 验证用户已被删除
        deleted_user = UserService.get_user_by_id(user.id)
        self.assertIsNone(deleted_user)

    def test_authenticate_user(self):
        """测试用户认证"""
        # 创建测试用户
        UserService.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com"
        )

        # 测试正确的认证
        authenticated_user = UserService.authenticate_user("testuser", "testpass")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, "testuser")

        # 测试错误的密码
        wrong_auth_user = UserService.authenticate_user("testuser", "wrongpass")
        self.assertIsNone(wrong_auth_user)

        # 测试不存在的用户
        nonexistent_user = UserService.authenticate_user("nonexistent", "testpass")
        self.assertIsNone(nonexistent_user)

if __name__ == '__main__':
    unittest.main()
