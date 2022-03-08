import datetime

def rsvEmailBodyContent(receiverName:str) -> str:
    return (
"""
尊敬的%s：
    您好！
    您有一份待审核的物品预约，请您及时审核。

                        微未央信息通知
                        %s
""") % (receiverName, str(datetime.date.today()))