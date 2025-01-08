from datetime import datetime
from models import TokenBlocklist
from db import db


def block_jti(jti, ttype, user_id):
    """
    Add the JTI (JWT ID) to the blocklist. This function is used to revoke a token.
    """
    token = TokenBlocklist(
        jti=jti,
        ttype=ttype,
        user_id=user_id,
        created_at=datetime.now(),
    )
    db.session.add(token)
    db.session.commit()
    return token
