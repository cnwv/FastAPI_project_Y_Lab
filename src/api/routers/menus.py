from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import get_sync_session
from src.api.services.menus import MenuService

router = APIRouter(prefix='/api/v1/menus', tags=['Menus'])


class MenuBody(BaseModel):
    title: str
    description: str


@router.get('/')
@cache(expire=30)
def get_menus(session: Session = Depends(get_sync_session)):
    return MenuService.get_menus(session)


@router.post('/')
async def create_menu(
        response: Response, menu: MenuBody, session: Session = Depends(get_sync_session)
):
    result = MenuService.create_menu(menu, session)
    response.status_code = status.HTTP_201_CREATED
    return result


@router.get('/{menu_id}')
@cache(expire=30)
async def get_target_menu(menu_id: int, session: Session = Depends(get_sync_session)):
    result = MenuService.get_target_menu(menu_id, session)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='menu not found'
    )


@router.patch('/{menu_id}')
async def update_target_menu(
        menu_id: int, menu: MenuBody, session: Session = Depends(get_sync_session)
):
    result = MenuService.update_target_menu(menu_id, menu, session)
    return result


@router.delete('/{menu_id}')
async def delete_target_menu(menu_id: int, session: Session = Depends(get_sync_session)):
    result = MenuService.delete_target_menu(menu_id, session)
    if result:
        return f'Menu ID {menu_id} deleted successfully.'
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='menu not found'
        )
