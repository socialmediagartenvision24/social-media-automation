from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.account import (
    AccountCreate,
    AccountUpdate,
)

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.get("")
async def list_accounts(
    current_user: dict = Depends(get_current_user),
):
    return {
        "items": [],
        "message": "Account-Liste wird im nächsten API-Schritt angeschlossen.",
    }


@router.post("")
async def create_account(
    payload: AccountCreate,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Account-Erstellung wird im nächsten API-Schritt angeschlossen.",
        "data": payload.model_dump(),
    }


@router.patch("/{account_id}")
async def update_account(
    account_id: str,
    payload: AccountUpdate,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Account-Update wird im nächsten API-Schritt angeschlossen.",
        "account_id": account_id,
        "data": payload.model_dump(exclude_unset=True),
    }


@router.delete("/{account_id}")
async def delete_account(
    account_id: str,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Account-Löschung wird im nächsten API-Schritt angeschlossen.",
        "account_id": account_id,
    }
