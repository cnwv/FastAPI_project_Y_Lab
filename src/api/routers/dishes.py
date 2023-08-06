from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_cache.decorator import cache
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from config import get_sync_session
from src.api.services.dishes import DishService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes']
)


class BodyDish(BaseModel):
    title: str
    description: str
    price: float = Field(ge=0)


@router.get('/')
@cache(expire=30)
async def get_dishes(
    menu_id: int, submenu_id: int, session: Session = Depends(get_sync_session)
):
    result = DishService.get_dishes(menu_id, submenu_id, session)
    return result


@router.post('/')
async def create_dish(
    response: Response,
    menu_id: int,
    submenu_id: int,
    dish: BodyDish,
    session: Session = Depends(get_sync_session),
):
    result = DishService.create_dish(menu_id, submenu_id, dish, session)
    if result:
        response.status_code = status.HTTP_201_CREATED
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='menu or submenu not found'
        )


@router.get('/{dish_id}')
@cache(expire=30)
async def get_target_dish(
    menu_id: int, submenu_id, dish_id, session: Session = Depends(get_sync_session)
):
    pass
    result = DishService.get_dish(menu_id, submenu_id, dish_id, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='dish not found'
        )


@router.patch('/{dish_id}')
async def update_target_dish(
    menu_id: int,
    submenu_id,
    dish: BodyDish,
    dish_id,
    session: Session = Depends(get_sync_session),
):
    result = DishService.update_dish(menu_id, submenu_id, dish_id, dish, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='dish not found'
        )


@router.delete('/{dish_id}')
async def delete_target_dish(
    menu_id: int, submenu_id, dish_id, session: Session = Depends(get_sync_session)
):
    result = DishService.delete_dish(menu_id, submenu_id, dish_id, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='menu or submenu not found'
        )
