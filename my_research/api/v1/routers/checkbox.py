from typing import Optional
from fastapi import APIRouter

from my_research.core.enumerations import ResearchTypes, UserRoles

router = APIRouter()

@router.get('/user.roles', tags=['Data'])
async def site_user_roles():
    return UserRoles.set()

@router.get('/research.types', tags=['Data'])
async def research_types():
    return ResearchTypes.set()
