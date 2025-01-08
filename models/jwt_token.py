from db import db

## Ref: https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking.html
class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    ttype = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey("users.id"),
        nullable=False,
    )
    created_at = db.Column(db.DateTime, nullable=False)
