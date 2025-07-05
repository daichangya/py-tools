from app.utils.ip_utils import get_ip_utils
import time

def test_basic_query():
    """基本查询测试"""
    print("\n=== 基本查询测试 ===")
    ip_util = get_ip_utils()
    if not ip_util:
        print("IP工具初始化失败")
        return

    test_ips = [
        '1.1.1.1',          # Cloudflare DNS
        '114.114.114.114',  # 114 DNS
        '223.5.5.5',        # 阿里 DNS
        '8.8.8.8',          # Google DNS
        '119.29.29.29',     # DNSPod DNS
        '180.76.76.76'      # 百度 DNS
    ]

    for ip in test_ips:
        try:
            print(f"\n查询IP: {ip}")
            result = ip_util.search(ip)
            for key, value in result.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"查询失败: {e}")

def test_invalid_ips():
    """无效IP测试"""
    print("\n=== 无效IP测试 ===")
    ip_util = get_ip_utils()
    if not ip_util:
        print("IP工具初始化失败")
        return

    invalid_ips = [
        '256.256.256.256',  # 超出范围
        '1.2.3',            # 格式错误
        'abc.def.ghi.jkl',  # 非数字
        '192.168.1',        # 不完整
        '',                 # 空字符串
        '127.0.0.256',      # 部分无效
    ]

    for ip in invalid_ips:
        try:
            print(f"\n测试无效IP: {ip}")
            if ip_util.is_valid_ip(ip):
                print("IP格式验证错误：应该是无效的")
            else:
                print("IP格式验证正确：检测为无效")

            result = ip_util.search(ip)
            print("查询结果:", result)
        except Exception as e:
            print(f"预期的错误: {e}")

def test_special_ips():
    """特殊IP测试"""
    print("\n=== 特殊IP测试 ===")
    ip_util = get_ip_utils()
    if not ip_util:
        print("IP工具初始化失败")
        return

    special_ips = [
        '127.0.0.1',        # 本地回环
        '192.168.1.1',      # 私有网络
        '10.0.0.1',         # 私有网络
        '172.16.0.1',       # 私有网络
        '169.254.0.1',      # 链路本地
        '224.0.0.1',        # 组播地址
    ]

    for ip in special_ips:
        try:
            print(f"\n查询特殊IP: {ip}")
            result = ip_util.search(ip)
            for key, value in result.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"查询失败: {e}")

def test_performance():
    """性能测试"""
    print("\n=== 性能测试 ===")
    ip_util = get_ip_utils()
    if not ip_util:
        print("IP工具初始化失败")
        return

    # 生成测试IP
    test_ips = [f"{i}.{i}.{i}.{i}" for i in range(1, 255, 10)]

    # 首次查询（无缓存）
    print("\n首次查询性能测试（无缓存）:")
    start_time = time.time()
    for ip in test_ips[:10]:  # 测试前10个IP
        ip_util.search(ip)
    elapsed = time.time() - start_time
    print(f"查询10个IP耗时: {elapsed:.4f}秒")
    print(f"平均每次查询耗时: {(elapsed/10):.4f}秒")

    # 缓存查询
    print("\n缓存查询性能测试:")
    start_time = time.time()
    for ip in test_ips[:10]:  # 再次查询相同的IP
        ip_util.search(ip)
    elapsed = time.time() - start_time
    print(f"查询10个IP耗时: {elapsed:.4f}秒")
    print(f"平均每次查询耗时: {(elapsed/10):.4f}秒")

def main():
    """运行所有测试"""
    print("开始测试IP地址查询工具...")

    test_basic_query()
    test_invalid_ips()
    test_special_ips()
    test_performance()

    print("\n测试完成!")

if __name__ == '__main__':
    main()
