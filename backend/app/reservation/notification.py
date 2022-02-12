import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

def sendEmailByTHUWY(receiverNum, mailReceiverNames, mailReceiverAddrs, bodyContent) -> dict:
    """
    Args:
        mailReceiversNames: A list of str showing the receivers' names.
        mailReceiversAddrs: A list of str showing the receivers' addresses.
        bodyContent: A str showing the body content of the email. 

    Returns:
        A Json Object:
        {
            "result": str "Email sending succeeded!" or "Email sending failed."
        } 
        
    """
    smtpHost = "smtp.exmail.qq.com"
    
    mailSenderName = "微未央信息通知" # 发件者名字
    mailSenderAddr = "info@thuwy.top" # 发送者邮箱地址
    mailSenderFMAddr = formataddr([mailSenderName, mailSenderAddr]) # 发件者的标准地址："name<xx@xx.xx>"
    mailSenderLicense = "BzB7Ya7TFznGskF6" # 发件者邮箱授权码

    # 收件者的标准地址："name<xx@xx.xx>"
    mailReceiverFMAddrs = []
    for i in range(receiverNum):
        mailReceiverFMAddrs.append(formataddr([mailReceiverNames[i], mailReceiverAddrs[i]]))

    subjectContent = "微未央信息通知" # 邮箱主题
    
    MMMObj = MIMEMultipart('related')
    MMMObj["From"] = mailSenderFMAddr # 发件者
    MMMObj["To"] = ','.join(mailReceiverFMAddrs) # 收件者
    MMMObj["Subject"] = Header(subjectContent, 'utf-8') # 主题
    messageText = MIMEText(bodyContent, "plain", "utf-8") # 文本
    MMMObj.attach(messageText)

    SMTPObj = smtplib.SMTP_SSL(smtpHost, 465)   # 设置发件者邮箱的域名和端口
    SMTPObj.set_debuglevel(1)   # 调试等级：1
    SMTPObj.login(mailSenderAddr, mailSenderLicense) # 登录

    rtn = {}
    try:
        SMTPObj.sendmail(mailSenderAddr, mailReceiverAddrs, MMMObj.as_string()) # 发送邮件
        rtn["result"] = "Email sending succeeded!"
    except smtplib.SMTPResponseException as e:
        print(e)
        rtn["result"] = "Email sending failed."
    
    SMTPObj.quit()  # 退出
    
    return rtn