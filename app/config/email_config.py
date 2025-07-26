import os

# 邮件服务配置
EMAIL_CONFIG = {
    'SMTP_SERVER': os.environ.get('SMTP_SERVER', 'smtp.example.com'),
    'SMTP_PORT': int(os.environ.get('SMTP_PORT', 587)),
    'SMTP_USERNAME': os.environ.get('SMTP_USERNAME', 'your_email@example.com'),
    'SMTP_PASSWORD': os.environ.get('SMTP_PASSWORD', 'your_password'),
}
