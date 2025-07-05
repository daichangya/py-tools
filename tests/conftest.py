import os
import sys

# 将项目根目录添加到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# 配置测试环境
def pytest_configure(config):
    """
    pytest配置函数
    """
    # 可以在这里添加自定义的pytest标记
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )

def pytest_sessionstart(session):
    """
    测试会话开始时的处理函数
    """
    # 可以在这里进行测试会话开始前的准备工作
    pass

def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束时的处理函数
    """
    # 可以在这里进行测试会话结束后的清理工作
    pass
