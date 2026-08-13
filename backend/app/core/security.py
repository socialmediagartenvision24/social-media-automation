from typing import Any

from fastapi import Header, HTTPException, status


async def get_current_user(
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """
    Temporary authentication dependency.

    The production implementation will validate the Supabase JWT
    and return the authenticated user's information.
    """

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header fehlt.",
        )

    if not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültiger Authorization Header.",
        )

    token = authorization[7:].strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer Token fehlt.",
        )

    # TODO:
    # Validate Supabase JWT here.
    #
    # We intentionally do not trust a client-provided user ID.
    #
    # Production:
    #   token -> Supabase JWT validation -> authenticated user ID

    return {
        "id": None,
        "token": token,
    }
