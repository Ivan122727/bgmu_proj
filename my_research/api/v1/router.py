from fastapi import APIRouter

from my_research.api.v1.routers import auth, reg
from my_research.api.v1.routers import user, patient, research, conlusion, checkbox


api_v1_router = APIRouter()

api_v1_router.include_router(router=reg.router, prefix="/reg", tags=["Reg"])
api_v1_router.include_router(router=auth.router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(router=user.router, prefix="/user", tags=["User"])
api_v1_router.include_router(router=patient.router, prefix="/patient", tags=["Patient"])
api_v1_router.include_router(router=research.router, prefix="/research", tags=["Research"])
api_v1_router.include_router(router=conlusion.router, prefix="/conlusion", tags=["Research"])
api_v1_router.include_router(router=checkbox.router, prefix="/data", tags=["Data"])