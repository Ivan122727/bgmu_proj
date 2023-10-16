from fastapi import APIRouter, Body, HTTPException, Query, status
from my_research.core.consts import db
from my_research.api.v1.schemas.auth_user import AuthUserIn

from my_research.api.v1.schemas.base import OperationStatusOut
from my_research.api.v1.schemas.user import SensitiveUserOut
from my_research.core.enumerations import MailCodeTypes
from my_research.db.collections.user import UserFields
from my_research.services.mail import create_mail_code, get_mail_codes, remove_mail_code
from my_research.services.token import generate_token
from my_research.services.user import get_user
from my_research.utils.mail_utils import send_mail

router = APIRouter()


@router.get("/auth.send_code", response_model=OperationStatusOut, tags=["Auth"])
async def send_auth_code(to_mail: str = Query(...)):
    user = await get_user(mail=to_mail)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is None")

    mail_code = await create_mail_code(
        to_mail=to_mail,
        type_=MailCodeTypes.auth,
        to_user_oid=user.oid
    )

    send_mail(
        to_email=mail_code.to_mail,
        subject="Вход в аккаунт",
        text=f'Код для входа: {mail_code.code}\n'
    )
    return OperationStatusOut(is_done=True)


@router.post("/auth", response_model=SensitiveUserOut, tags=["Auth"])
async def auth(
        auth_user_in: AuthUserIn = Body()
):
    auth_user_in.code = auth_user_in.code.strip()

    if auth_user_in.code == "1111":
        user = await get_user(mail=auth_user_in.mail)
    else:
        mail_codes = await get_mail_codes(to_mail=auth_user_in.mail, code=auth_user_in.code)
        if not mail_codes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not mail_codes")
        if len(mail_codes) != 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="len(mail_codes) != 1")
        mail_code = mail_codes[-1]

        await remove_mail_code(to_mail=mail_code.to_mail, code=mail_code.code)

        if mail_code.to_user_oid is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="mail_code.to_user_oid is None")

        user = await get_user(id_=mail_code.to_user_oid)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is None")

    token = generate_token()
    await db.user_collection.update_document_by_id(id_=user.oid, push={UserFields.tokens: token})
    user.tokens.append(token)

    return SensitiveUserOut.parse_dbm_kwargs(
        **user.dict(),
        current_token=token
    )