from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import get_sync_session
from src.api.services.submenus import SubmenuService

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenus'])


class SubmenuBody(BaseModel):
    title: str
    description: str


@router.get('/')
@cache(expire=30)
async def get_submenus(menu_id: int, session: Session = Depends(get_sync_session)):
    result = SubmenuService.get_submenus(menu_id, session)
    return result if result else []


@router.post('/')
async def create_submenu(
    response: Response,
    menu_id: int,
    submenu: SubmenuBody,
    session: Session = Depends(get_sync_session),
):
    result = SubmenuService.create_submenu(menu_id, submenu, session)
    if result:
        response.status_code = status.HTTP_201_CREATED
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='a menu with that title already exists',
    )


@router.get('/{submenu_id}')
@cache(expire=30)
async def get_target_submenu(
    menu_id: int, submenu_id: int, session: Session = Depends(get_sync_session)
):
    result = SubmenuService.get_target_submenu(menu_id, submenu_id, session)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found'
    )


@router.patch('/{submenu_id}')
async def update_target_menu(
    menu_id: int,
    submenu_id: int,
    submenu: SubmenuBody,
    session: Session = Depends(get_sync_session),
):
    result = SubmenuService.update_target_submenu(menu_id, submenu_id, submenu, session)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found'
    )


@router.delete('/{submenu_id}')
async def delete_target_submenu(
    menu_id: int, submenu_id: int, session: Session = Depends(get_sync_session)
):
    result = SubmenuService.delete_target_submenu(menu_id, submenu_id, session)
    if result:
        return f'Menu ID {submenu_id} deleted successfully.'
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found'
    )
