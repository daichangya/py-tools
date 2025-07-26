import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """
    邮件发送服务
    """
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        """
        初始化邮件服务

        Args:
            smtp_server: SMTP服务器地址
            smtp_port: SMTP服务器端口
            username: 邮箱用户名
            password: 邮箱密码
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
        is_html: bool = False,
        send_individually: bool = False
    ) -> Dict[str, Any]:
        """
        发送邮件

        Args:
            to_emails: 收件人邮箱列表
            subject: 邮件主题
            body: 邮件正文
            cc_emails: 抄送邮箱列表
            bcc_emails: 密送邮箱列表
            attachments: 附件路径列表
            is_html: 是否为HTML格式
            send_individually: 是否单独发送给每个收件人（默认为False）
                              当为True时，系统会为每个收件人单独发送邮件，
                              收件人不会看到其他人的邮箱地址

        Returns:
            Dict: 包含发送结果的字典，包括成功/失败状态和详细信息
        """
        if not to_emails:
            return {"success": False, "message": "收件人不能为空"}

        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject

            # 添加抄送
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)

            # 添加邮件正文
            content_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(body, content_type, 'utf-8'))

            # 添加附件
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            attachment = MIMEApplication(f.read())
                            attachment.add_header(
                                'Content-Disposition',
                                'attachment',
                                filename=os.path.basename(file_path)
                            )
                            msg.attach(attachment)
                    else:
                        logger.warning(f"附件不存在: {file_path}")

            # 所有收件人列表（包括抄送和密送）
            all_recipients = to_emails.copy()
            if cc_emails:
                all_recipients.extend(cc_emails)
            if bcc_emails:
                all_recipients.extend(bcc_emails)

            # 连接SMTP服务器
            try:
                if self.smtp_port == 465:
                    # 使用SSL连接
                    server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
                else:
                    # 使用普通连接，然后启用TLS
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                    server.starttls()  # 启用TLS加密
                
                server.login(self.username, self.password)
                
                # 根据发送模式选择发送方式
                if send_individually and to_emails:
                    # 单独发送模式 - 为每个收件人单独建立连接
                    successful_count = 0
                    failed_recipients = []
                    error_messages = []
                    
                    # 关闭当前连接，为每个收件人创建新连接
                    server.quit()
                    
                    import time
                    
                    for recipient in to_emails:
                        try:
                            # 为每个收件人创建单独的邮件
                            individual_msg = MIMEMultipart()
                            individual_msg['From'] = self.username
                            individual_msg['To'] = recipient
                            individual_msg['Subject'] = subject
                            
                            # 添加抄送和密送（如果有）
                            if cc_emails:
                                individual_msg['Cc'] = ', '.join(cc_emails)
                            
                            # 添加邮件正文
                            content_type = 'html' if is_html else 'plain'
                            individual_msg.attach(MIMEText(body, content_type, 'utf-8'))
                            
                            # 添加附件（如果有）
                            if attachments:
                                for file_path in attachments:
                                    if os.path.exists(file_path):
                                        with open(file_path, 'rb') as f:
                                            attachment = MIMEApplication(f.read())
                                            attachment.add_header(
                                                'Content-Disposition',
                                                'attachment',
                                                filename=os.path.basename(file_path)
                                            )
                                            individual_msg.attach(attachment)
                            
                            # 构建收件人列表（主收件人 + 抄送 + 密送）
                            individual_recipients = [recipient]
                            if cc_emails:
                                individual_recipients.extend(cc_emails)
                            if bcc_emails:
                                individual_recipients.extend(bcc_emails)
                            
                            # 添加更长的延迟，避免触发邮件服务器的频率限制
                            time.sleep(2)
                            
                            # 为每个收件人创建新的SMTP连接
                            individual_server = None
                            try:
                                logger.info(f"正在为收件人 {recipient} 创建SMTP连接...")
                                
                                if self.smtp_port == 465:
                                    individual_server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=30)
                                else:
                                    individual_server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
                                    individual_server.ehlo()  # 明确发送EHLO命令
                                    individual_server.starttls()
                                    individual_server.ehlo()  # TLS后再次发送EHLO
                                
                                logger.info(f"正在登录SMTP服务器...")
                                individual_server.login(self.username, self.password)
                                
                                logger.info(f"正在发送邮件给 {recipient}...")
                                # 发送邮件
                                individual_server.sendmail(self.username, individual_recipients, individual_msg.as_string())
                                logger.info(f"邮件已成功发送给 {recipient}")
                                
                                successful_count += 1
                            finally:
                                # 确保无论如何都关闭连接
                                if individual_server:
                                    try:
                                        # 检查连接是否已建立
                                        if hasattr(individual_server, 'sock') and individual_server.sock:
                                            individual_server.quit()
                                            logger.info("SMTP连接已关闭")
                                        else:
                                            logger.info("SMTP连接已不存在，无需关闭")
                                    except Exception as close_error:
                                        logger.warning(f"关闭SMTP连接时出错: {str(close_error)}")
                            
                        except smtplib.SMTPResponseException as e:
                            error_code = e.smtp_code
                            error_message = e.smtp_error.decode('utf-8') if isinstance(e.smtp_error, bytes) else str(e.smtp_error)
                            error_detail = f"SMTP错误 {error_code}: {error_message}"
                            logger.error(f"向 {recipient} 发送邮件时出错: {error_detail}")
                            failed_recipients.append(recipient)
                            error_messages.append(f"向 {recipient} 发送邮件时出错: {error_detail}")
                            
                            # 对于特定错误码提供更具体的建议
                            if error_code == 503:
                                logger.info("检测到503错误(bad sequence of commands)，增加延迟时间...")
                                time.sleep(5)  # 遇到503错误时增加更长的延迟
                            elif error_code == 451:
                                logger.info("检测到451错误(可能是频率限制)，增加延迟时间...")
                                time.sleep(10)  # 遇到451错误时增加更长的延迟
                            elif error_code == 550:
                                logger.info("检测到550错误(可能是垃圾邮件拦截)，记录详细信息...")
                                # 550错误通常表示邮件被拒绝，可能是因为被识别为垃圾邮件
                                # 这种情况下增加延迟通常没有帮助，但我们记录详细信息以便分析
                        except Exception as e:
                            error_detail = str(e)
                            logger.error(f"向 {recipient} 发送邮件时出错: {error_detail}")
                            failed_recipients.append(recipient)
                            error_messages.append(f"向 {recipient} 发送邮件时出错: {error_detail}")
                    
                    # 构建结果消息
                    if successful_count == len(to_emails):
                        return {
                            "success": True,
                            "message": f"已成功单独发送邮件给所有 {successful_count} 位收件人"
                        }
                    elif successful_count > 0:
                        # 分析错误模式，提供针对性建议
                        suggestions = []
                        if any("503" in msg for msg in error_messages):
                            suggestions.append("检测到'bad sequence of commands'错误，这通常是由于163邮箱对连续发送邮件的限制。建议减少收件人数量或分批发送。")
                        
                        if any("451" in msg for msg in error_messages):
                            suggestions.append("检测到频率限制错误，这表明您可能触发了邮件服务器的反垃圾邮件机制。建议等待10-30分钟后再尝试发送。")
                        
                        if any("550" in msg for msg in error_messages):
                            suggestions.append("检测到550错误，这表明您的邮件可能被识别为垃圾邮件。建议检查以下几点：\n"
                                             "  - 邮件主题不要使用过于营销化的词语\n"
                                             "  - 邮件内容不要包含过多链接或敏感词\n"
                                             "  - 尝试修改邮件格式，减少HTML元素\n"
                                             "  - 确认您的发件邮箱没有被用于发送垃圾邮件")
                        
                        if not suggestions:
                            suggestions.append("如果继续遇到问题，请尝试使用批量发送模式或减少收件人数量。")
                        
                        suggestion_text = "\n\n建议：\n" + "\n".join(f"- {s}" for s in suggestions)
                        
                        return {
                            "success": True,
                            "message": f"已成功单独发送邮件给 {successful_count}/{len(to_emails)} 位收件人。\n\n失败的收件人: {', '.join(failed_recipients)}\n\n错误信息: {'; '.join(error_messages)}{suggestion_text}"
                        }
                    else:
                        # 所有邮件都发送失败
                        suggestions = []
                        if any("503" in msg for msg in error_messages):
                            suggestions.append('尝试使用批量发送模式（不勾选"单独发送"选项）')
                        if any("451" in msg for msg in error_messages):
                            suggestions.append("等待10-30分钟后再尝试发送")
                        if any("550" in msg for msg in error_messages):
                            suggestions.append("修改邮件内容，避免使用可能触发垃圾邮件过滤的词语")
                            suggestions.append("减少邮件中的链接数量和图片")
                            suggestions.append("尝试使用纯文本格式而非HTML格式")
                        suggestions.append("检查SMTP服务器设置和授权码是否正确")
                        suggestions.append("尝试使用其他邮箱服务（如Gmail、QQ邮箱）")
                        
                        suggestion_text = "\n\n请尝试以下解决方法：\n" + "\n".join(f"- {s}" for s in suggestions)
                        
                        return {
                            "success": False,
                            "message": f"发送邮件失败。\n\n错误信息: {'; '.join(error_messages)}{suggestion_text}"
                        }
                else:
                    # 批量发送模式
                    try:
                        logger.info(f"正在批量发送邮件给 {len(all_recipients)} 位收件人...")
                        server.sendmail(self.username, all_recipients, msg.as_string())
                        logger.info("邮件发送成功")
                        # 安全关闭连接
                        try:
                            if hasattr(server, 'sock') and server.sock:
                                server.quit()
                                logger.info("批量发送模式：SMTP连接已成功关闭")
                            else:
                                logger.info("批量发送模式：SMTP连接已不存在，无需关闭")
                        except Exception as close_error:
                            logger.warning(f"批量发送模式：关闭SMTP连接时出错: {str(close_error)}")
                        
                        return {
                            "success": True,
                            "message": f"邮件已成功发送给 {len(all_recipients)} 位收件人"
                        }
                    except smtplib.SMTPResponseException as e:
                        error_code = e.smtp_code
                        error_message = e.smtp_error.decode('utf-8') if isinstance(e.smtp_error, bytes) else str(e.smtp_error)
                        error_detail = f"SMTP错误 {error_code}: {error_message}"
                        
                        # 为常见错误提供更有用的建议
                        suggestion = ""
                        if error_code == 503:
                            suggestion = "建议：尝试使用单独发送模式，或减少收件人数量。"
                        elif error_code == 451:
                            suggestion = "建议：您可能触发了邮件服务器的频率限制，请稍后再试或减少收件人数量。"
                        elif error_code == 550:
                            suggestion = "建议：邮件被识别为垃圾邮件。请尝试以下解决方法：\n" + \
                                        "1. 检查邮件主题，避免使用营销类词语\n" + \
                                        "2. 减少邮件中的链接数量\n" + \
                                        "3. 避免使用大量图片或附件\n" + \
                                        "4. 如果使用HTML格式，尝试切换到纯文本格式\n" + \
                                        "5. 查看163邮箱的反垃圾邮件规则：http://mail.163.com/help/help_spam_16.htm"
                        
                        # 安全关闭连接
                        try:
                            if hasattr(server, 'sock') and server.sock:
                                server.quit()
                                logger.info("批量发送模式：SMTP连接已关闭")
                            else:
                                logger.info("批量发送模式：SMTP连接已不存在，无需关闭")
                        except Exception as close_error:
                            logger.warning(f"批量发送模式：关闭SMTP连接时出错: {str(close_error)}")
                        
                        logger.error(f"批量发送邮件时出错: {error_detail}")
                        return {
                            "success": False,
                            "message": f"批量发送邮件时出错: {error_detail}\n{suggestion}"
                        }
                    except Exception as e:
                        error_detail = str(e)
                        # 安全关闭连接
                        try:
                            if hasattr(server, 'sock') and server.sock:
                                server.quit()
                                logger.info("批量发送模式：SMTP连接已关闭（异常处理）")
                            else:
                                logger.info("批量发送模式：SMTP连接已不存在，无需关闭（异常处理）")
                        except Exception as close_error:
                            logger.warning(f"批量发送模式：关闭SMTP连接时出错: {str(close_error)}")
                        
                        logger.error(f"批量发送邮件时出错: {error_detail}")
                        return {
                            "success": False,
                            "message": f"批量发送邮件时出错: {error_detail}\n建议：请检查您的网络连接和SMTP服务器设置。"
                        }
            except Exception as e:
                if 'server' in locals():
                    # 安全关闭连接
                    try:
                        if hasattr(server, 'sock') and server.sock:
                            server.quit()
                            logger.info("SMTP连接已关闭（外层异常处理）")
                        else:
                            logger.info("SMTP连接已不存在，无需关闭（外层异常处理）")
                    except Exception as close_error:
                        logger.warning(f"关闭SMTP连接时出错: {str(close_error)}")
                raise e

        except Exception as e:
            error_msg = f"发送邮件时出错: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    def validate_email(self, email: str) -> bool:
        """
        简单验证邮箱格式是否正确

        Args:
            email: 邮箱地址

        Returns:
            bool: 邮箱格式是否正确
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
