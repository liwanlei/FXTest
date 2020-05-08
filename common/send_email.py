'''
邮件发送测试报告
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send_emails(sender, receivers, password, smtp, port, fujian1, fujian2, subject, url):
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
    att1 = MIMEText(open(fujian1, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="%s"' % fujian1
    message.attach(att1)
    att2 = MIMEText(open(fujian2, 'rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="%s"' % fujian2
    message.attach(att2)
    try:
        smtpObj = smtplib.SMTP_SSL(smtp, port)
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except Exception as e:
        return False
