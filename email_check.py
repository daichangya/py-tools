import smtplib
import dns.resolver
from email_validator import validate_email, EmailNotValidError


def check_email_exists(email):
    try:
        # 验证邮箱格式
        valid = validate_email(email)
        email = valid.email
        domain = email.split('@')[-1]

        # 获取邮箱服务器的 MX 记录
        records = dns.resolver.resolve(domain, 'MX')
        mx_records = sorted(records, key=lambda x: x.preference)

        if not mx_records:
            print(f"找不到 {domain} 的 MX 记录")
            return False

        # 尝试连接到第一个 MX 服务器
        mx_server = str(mx_records[0].exchange)
        server = smtplib.SMTP()
        server.set_debuglevel(0)  # 设置为 1 可查看调试信息

        try:
            server.connect(mx_server)
            server.helo(server.local_hostname)
            server.mail('sender@example.com')  # 使用伪造的发件人地址
            code, _ = server.rcpt(str(email))

            # SMTP 250 状态码表示邮箱存在
            if code == 250:
                return True
            else:
                print(f"邮箱不存在或被拒绝 (状态码: {code})")
                return False
        except smtplib.SMTPException as e:
            print(f"SMTP 错误: {e}")
            return False
        finally:
            server.quit()
    except EmailNotValidError as e:
        print(f"邮箱格式无效: {e}")
        return False
    except dns.resolver.NXDOMAIN:
        print(f"域名不存在")
        return False
    except Exception as e:
        print(f"未知错误: {e}")
        return False


# 示例
email = "daichangya@163.com"
print(f"邮箱是否存在: {check_email_exists(email)}")