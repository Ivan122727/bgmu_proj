from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from my_research.api.v1.schemas.base import OperationStatusOut

from my_research.api.v1.schemas.user import UserExistsStatusOut, UserOut
from my_research.core.enumerations import UserRoles
from my_research.db.collections.user import UserFields
from my_research.deps.user_deps import get_strict_current_user, make_strict_depends_on_roles
from my_research.models.user import User
from my_research.services.user import get_user, get_users
from my_research.core.consts import db

router = APIRouter()

@router.get('/user.mail_exists', response_model=UserExistsStatusOut, tags=['User'])
async def user_mail_exists(mail: str = Query(...)):
    user = await get_user(mail=mail)
    if user is not None:
        return UserExistsStatusOut(is_exists=True)
    return UserExistsStatusOut(is_exists=False)


@router.get('/user.all', response_model=list[UserOut], tags=['User'])
async def get_all_users(user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.dev]))):
    return [UserOut.parse_dbm_kwargs(**user.dict()) for user in await get_users()]


@router.get('/user.by_id', response_model=Optional[UserOut], tags=['User'])
async def get_user_by_int_id(int_id: int, user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.dev]))):
    user = await get_user(id_=int_id)
    if user is None:
        raise HTTPException(status_code=400, detail="user is none")
    return UserOut.parse_dbm_kwargs(**user.dict())


@router.get('/user.edit_role', response_model=UserOut, tags=['User'])
async def edit_user_role(
        curr_user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.dev])),
        user_int_id: int = Query(...),
        role: str = Query(...)
):
    user = await get_user(id_=user_int_id)
    if user is None:
        raise HTTPException(status_code=400, detail="user is none")
    if not role in UserRoles.set():
        raise HTTPException(status_code=400, detail="invalid role")
    await db.user_collection.update_document_by_id(id_=user.oid, set_={UserFields.roles: [role]})
    return UserOut.parse_dbm_kwargs(**(await get_user(id_=user.oid)).dict())



@router.get('/user.delete', response_model=OperationStatusOut, tags=['User'])
async def delete_user(
        curr_user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.dev])),
        user_int_id: int = Query(...),
):
    user = await get_user(id_=user_int_id)
    if user is None:
        raise HTTPException(status_code=400, detail="user is none")
    await db.user_collection.remove_document({UserFields.int_id: user_int_id})
    return OperationStatusOut(is_done=True)    



@router.get('/user.me', response_model=UserOut, tags=['User'])
async def user_me(user: User = Depends(get_strict_current_user)):
    return UserOut.parse_dbm_kwargs(**user.dict()) 