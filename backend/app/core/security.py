from typing import Any

import jwt
from fastapi import Header, HTTPException, status

from app.core.config import settings


def _unauthorized(detail: str = "Nicht authentifiziert.") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """
    Validate the Supabase access token and return the authenticated user.

    The frontend sends:

        Authorization: Bearer <supabase-access-token>

    The backend validates the JWT and extracts the Supabase user ID.

    IMPORTANT:
    The Service Role Key is never used as the user's authentication token.
    """

    if not authorization:
        raise _unauthorized("Authorization Header fehlt.")

    if not authorization.lower().startswith("bearer "):
        raise _unauthorized("Ungültiger Authorization Header.")

    token = authorization[7:].strip()

    if not token:
        raise _unauthorized("Bearer Token fehlt.")

    try:
        # ------------------------------------------------------------------
        # Supabase JWT
        # ------------------------------------------------------------------
        #
        # Supabase projects created with the newer JWT configuration expose
        # their signing secret through the project configuration.
        #
        # We support HS256 here when JWT_SECRET is configured.
        # ------------------------------------------------------------------

        if not settings.jwt_secret:
            raise _unauthorized(
                "JWT_SECRET ist im Backend nicht konfiguriert."
            )

        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            options={
                "verify_exp": True,
            },
        )

    except jwt.ExpiredSignatureError:
        raise _unauthorized("Access Token ist abgelaufen.")

    except jwt.InvalidTokenError:
        raise _unauthorized("Ungültiger Access Token.")

    user_id = payload.get("sub")

    if not user_id:
        raise _unauthorized("Token enthält keine User-ID.")

    return {
        "id": user_id,
        "email": payload.get("email"),
        "role": payload.get("role"),
        "token": token,
        "claims": payload,
    }
