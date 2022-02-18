import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import datetime

from app.reservation.secret import MANAGER_NAMES, MANAGER_EMAILS

def sendEmailByTHUWY(receiverNum, mailReceiverNames:list, mailReceiverAddrs:list) -> dict:
    """
    Args:
        receiverNum: A int showing the number of receivers.
        mailReceiversNames: A list of str showing the receivers' names.
        mailReceiversAddrs: A list of str showing the receivers' addresses.

    Returns:
        A Json Object:{
            "errcode":
            "errmsg:
        }
        
    """
    smtpHost = "smtp.exmail.qq.com"
    
    mailSenderName = "微未央信息通知" # 发件者名字
    mailSenderAddr = "info@thuwy.top" # 发送者邮箱地址
    mailSenderFMAddr = formataddr([mailSenderName, mailSenderAddr]) # 发件者的标准地址："name<xx@xx.xx>"
    mailSenderLicense = "BzB7Ya7TFznGskF6" # 发件者邮箱授权码

    SMTPObj = smtplib.SMTP_SSL(smtpHost, 465)   # 设置发件者邮箱的域名和端口
    SMTPObj.set_debuglevel(1)   # 调试等级：1
    SMTPObj.login(mailSenderAddr, mailSenderLicense) # 登录

    # 收件者的标准地址："name<xx@xx.xx>"
    mailReceiverFMAddrs = []
    for i in range(receiverNum):
        mailReceiverFMAddrs.append(formataddr([mailReceiverNames[i], mailReceiverAddrs[i]]))

        subjectContent = "微未央信息通知" # 邮箱主题

        bodyContent = """
            尊敬的%s：
                您好！
                您有一份待审核的物品预约，请您及时审核。

                                    微未央信息通知
                                    %s
        """ % (mailReceiverNames[i], str(datetime.date.today()) )
        
        
        MMMObj = MIMEMultipart('related')
        MMMObj["From"] = mailSenderFMAddr # 发件者
        MMMObj["To"] = ','.join(mailReceiverFMAddrs[i]) # 收件者
        MMMObj["Subject"] = Header(subjectContent, 'utf-8') # 主题
        messageText = MIMEText(bodyContent, "plain", "utf-8") # 文本
        MMMObj.attach(messageText)

        rtn = {}
        try:
            SMTPObj.sendmail(mailSenderAddr[i], mailReceiverAddrs[i], MMMObj.as_string()) # 发送邮件
        except Exception as e:
            rtn["errcode"] = -1
            rtn["errmsg"] = e
            return rtn
        
        SMTPObj.quit()  # 退出
    
    rtn["errcode"] = 0
    return rtn

