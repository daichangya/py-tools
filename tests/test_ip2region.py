import os
import sys
import time
import pytest
from utils.ip2region import XdbSearcher, Ip2Region, get_ip2region

class TestIp2Region:
    """IP2Region测试类"""

    @pytest.fixture
    def ip2region(self):
        """创建IP2Region实例"""
        instance = get_ip2region()
        assert instance is not None
        yield instance

    def test_basic_search(self, ip2region):
        """测试基本的IP查询功能"""
        # 测试公共DNS服务器IP
        test_cases = [
            {
                'ip': '1.1.1.1',  # Cloudflare DNS
                'expected_country': '澳大利亚'
            },
            {
                'ip': '114.114.114.114',  # 114 DNS
                'expected_country': '中国'
            },
            {
                'ip': '8.8.8.8',  # Google DNS
                'expected_country': '美国'
            }
        ]

        for case in test_cases:
            result = ip2region.search(case['ip'])
            print(f"查询结果: {result}")
            assert result is not None
            assert result['country'] == case['expected_country']

    def test_invalid_ip(self, ip2region):
        """测试无效IP地址"""
        invalid_ips = [
            '256.256.256.256',  # 超出范围
            '1.2.3',            # 格式错误
            'abc.def.ghi.jkl',  # 非数字
            '192.168.1',        # 不完整
            '',                 # 空字符串
            '127.0.0.256',      # 部分无效
        ]

        for ip in invalid_ips:
            assert not ip2region.is_valid_ip(ip)
            result = ip2region.search(ip)
            assert result['country'] == '未知'

    def test_private_ip(self, ip2region):
        """测试私有IP地址"""
        private_ips = [
            '127.0.0.1',        # 本地回环
            '192.168.1.1',      # 私有网络
            '10.0.0.1',         # 私有网络
            '172.16.0.1',       # 私有网络
            '169.254.0.1',      # 链路本地
        ]

        for ip in private_ips:
            assert ip2region.is_valid_ip(ip)
            result = ip2region.search(ip)
            # 私有IP可能返回内网或未知
            assert result is not None

    def test_cache(self, ip2region):
        """测试缓存功能"""
        test_ip = '114.114.114.114'

        # 第一次查询
        start_time = time.time()
        result1 = ip2region.search(test_ip)
        first_query_time = time.time() - start_time

        # 第二次查询（应该使用缓存）
        start_time = time.time()
        result2 = ip2region.search(test_ip)
        second_query_time = time.time() - start_time

        # 验证结果一致
        assert result1 == result2
        # 验证缓存查询更快
        assert second_query_time < first_query_time

    def test_performance(self, ip2region):
        """测试查询性能"""
        # 生成测试IP
        test_ips = [f"{i}.{i}.{i}.{i}" for i in range(1, 255, 10)]

        # 批量查询测试
        start_time = time.time()
        for ip in test_ips:
            ip2region.search(ip)
        total_time = time.time() - start_time

        # 计算平均查询时间
        avg_time = total_time / len(test_ips)
        print(f"\n性能测试结果:")
        print(f"总查询数: {len(test_ips)}")
        print(f"总耗时: {total_time:.4f}秒")
        print(f"平均查询时间: {avg_time:.4f}秒")

        # 验证性能满足要求（平均查询时间应小于1ms）
        assert avg_time < 0.001

    def test_memory_usage(self, ip2region):
        """测试内存使用"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss

        # 执行大量查询
        test_ips = [f"{i}.{i}.{i}.{i}" for i in range(1, 255)]
        for ip in test_ips:
            ip2region.search(ip)

        end_memory = process.memory_info().rss
        memory_increase = end_memory - start_memory

        print(f"\n内存使用测试结果:")
        print(f"初始内存: {start_memory / 1024 / 1024:.2f}MB")
        print(f"最终内存: {end_memory / 1024 / 1024:.2f}MB")
        print(f"内存增长: {memory_increase / 1024 / 1024:.2f}MB")

        # 验证内存增长在合理范围内（小于10MB）
        assert memory_increase < 10 * 1024 * 1024

    def test_concurrent_access(self, ip2region):
        """测试并发访问"""
        import threading
        import queue

        # 创建结果队列
        results = queue.Queue()
        test_ip = '114.114.114.114'
        thread_count = 10

        def worker():
            try:
                result = ip2region.search(test_ip)
                results.put(('success', result))
            except Exception as e:
                results.put(('error', str(e)))

        # 创建并启动线程
        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        # 等待所有线程完成
        for t in threads:
            t.join()

        # 检查结果
        success_count = 0
        error_count = 0
        first_result = None

        while not results.empty():
            status, result = results.get()
            if status == 'success':
                success_count += 1
                if first_result is None:
                    first_result = result
                else:
                    # 验证所有成功的查询结果一致
                    assert result == first_result
            else:
                error_count += 1

        # 验证所有查询都成功
        assert success_count == thread_count
        assert error_count == 0

if __name__ == '__main__':
    pytest.main([__file__])
