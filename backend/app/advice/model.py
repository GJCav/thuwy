from app.models import db
from app.auth.model import User


class Advice(db.Model):
    STATE_WAIT = 1
    STATE_END = 2

    __tablename__ = 'advice'
    id            = db.Column(db.Integer, primary_key = True)
    proponent     = db.Column(db.Text)
    title        = db.Column(db.Text)
    content       = db.Column(db.Text)
    state         = db.Column(db.Integer)
    response      = db.Column(db.Text)

    def queryById(id):
        rst = db.session.query(Advice).filter(Advice.id == id).one_or_none()
        return rst

    def toDict(self, carryContent = False):
        rst = {
            'id': self.id,
            'proponent': User.queryName(self.proponent),
            'title': self.title,
            'state': self.state,
            'response': self.response
        }
        if carryContent:
            rst['content'] = self.content
        return rst
