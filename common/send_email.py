'''
邮件发送测试报告
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from common.system_log import logger


def send_emails(sender, receivers, password, smtp,
                port, annexone, annextwo, subject, url):
    message = MIMEMultipart()
    mail_msg = """
		<h1>接口测试报告</h1>
	<p>您提交的接口测试已经测试完毕，附件中存放您的测试报告和测试日志，定时测试报告链接如下</p>
	<p>
	<a href="%s">这是一个链接</a>
	</p>
	""" % url
    message['From'] = sender
    message['To'] = ','.join(receivers)
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(mail_msg, 'html', 'utf-8'))
    try:
        with open(annexone, 'rb') as f1:
            att1 = MIMEText(f1.read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="%s"' % annexone
        message.attach(att1)
        with open(annextwo, 'rb') as f2:
            att2 = MIMEText(f2.read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="%s"' % annextwo
        message.attach(att2)
    except Exception as e:
        logger.exception('读取邮件附件失败: %s' % e)
        return False
    try:
        smtpObj = smtplib.SMTP_SSL(smtp, port)
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except Exception as e:
        logger.exception('邮件发送失败: %s' % e)
        return False
