from datetime import datetime
from flask import Flask, Request, Response
from flask.json.tag import TaggedJSONSerializer
from flask.sessions import SecureCookieSession
from flask.sessions import SessionInterface, SessionMixin
import hashlib
from itsdangerous import BadSignature, URLSafeTimedSerializer

session_json_serializer = TaggedJSONSerializer()

class HeaderSession(SessionInterface):
    """
    仿照 SecureCookieSessionInterface 实现在header中保存session信息，避免跨域等问题
    """

    salt = "cookie-session"
    digest_method = staticmethod(hashlib.sha1)
    key_derivation = "hmac"
    header_name = "Session"

    def get_signing_serializer(self, app: "Flask"):
        if not app.secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation, 
            digest_method=self.digest_method,
        )
        return URLSafeTimedSerializer(
            app.secret_key,
            salt=self.salt,
            serializer=session_json_serializer,
            signer_kwargs=signer_kwargs,
        )

    def open_session(self, app: "Flask", request: "Request"):
        s = self.get_signing_serializer(app)
        if s is None:
            return None
        val = request.headers.get(self.header_name)
        if not val:
            return SecureCookieSession()
        max_age = int(app.permanent_session_lifetime.total_seconds())
        try:
            data = s.loads(val, max_age=max_age)
            if data.get("expire_at", 0) < datetime.now().timestamp():
                return SecureCookieSession()
            return SecureCookieSession(data.get("data", {}))
        except BadSignature:
            return SecureCookieSession()


    def save_session(
        self, app: "Flask", session: SessionMixin, response: "Response"
    ) -> None:
        if not session:
            if session.modified:
                response.headers.add(self.header_name, "")
            return

        if session.accessed:
            response.vary.add(self.header_name)

        if not self.should_set_cookie(app, session):
            return

        expire_at = self.get_expiration_time(app, session)
        expire_at = expire_at.timestamp() if expire_at else 0
        val = self.get_signing_serializer(app).dumps({
            "expire_at": expire_at,
            "data": dict(session)
        })
        response.headers[self.header_name] = val


def patch_session(app):
    app.session_interface = HeaderSession()