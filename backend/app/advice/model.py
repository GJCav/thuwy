from app.models import db
from app.auth.model import User

from sqlalchemy import INTEGER, VARCHAR, TEXT
from app.models import SNOWFLAKE_ID, WECHAT_OPENID


class Advice(db.Model):
    STATE_WAIT = 1
    STATE_END = 2

    __tablename__ = "advice"
    id = db.Column(SNOWFLAKE_ID, primary_key=True)  # 建议ID
    proponent = db.Column(WECHAT_OPENID)  # 提出者openid
    title = db.Column(VARCHAR(128))  # 建议标题
    content = db.Column(TEXT)  # 内容
    state = db.Column(INTEGER)  # 建议状态
    response = db.Column(TEXT)  # 回应

    def queryById(id):
        rst = db.session.query(Advice).filter(Advice.id == id).one_or_none()
        return rst

    def toDict(self, carryContent=False):
        rst = {
            "id": self.id,
            "proponent": User.queryName(self.proponent),
            "title": self.title,
            "state": self.state,
            "response": self.response,
        }
        if carryContent:
            rst["content"] = self.content
        return rst
