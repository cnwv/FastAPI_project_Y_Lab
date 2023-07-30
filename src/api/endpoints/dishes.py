from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.orm import Session

from config import get_sync_session
from src.api.CRUD.dishes import CRUDDish

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["Dishes"]
)


class BodyDish(BaseModel):
    title: str
    description: str
    price: float = Field(ge=0)


@router.get("/")
def get_dishes(
    menu_id: int, submenu_id: int, session: Session = Depends(get_sync_session)
):
    result = CRUDDish.get_dishes(menu_id, submenu_id, session)
    return result


@router.post("/")
def create_dish(
    response: Response,
    menu_id: int,
    submenu_id: int,
    dish: BodyDish,
    session: Session = Depends(get_sync_session),
):
    result = CRUDDish.create_dish(menu_id, submenu_id, dish, session)
    if result:
        response.status_code = status.HTTP_201_CREATED
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu or submenu not found"
        )


@router.get("/{dish_id}")
def get_target_dish(
    menu_id: int, submenu_id, dish_id, session: Session = Depends(get_sync_session)
):
    pass
    result = CRUDDish.get_dish(menu_id, submenu_id, dish_id, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )


@router.patch("/{dish_id}")
def update_target_dish(
    menu_id: int,
    submenu_id,
    dish: BodyDish,
    dish_id,
    session: Session = Depends(get_sync_session),
):
    result = CRUDDish.update_dish(menu_id, submenu_id, dish_id, dish, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )


@router.delete("/{dish_id}")
def delete_target_dish(
    menu_id: int, submenu_id, dish_id, session: Session = Depends(get_sync_session)
):
    result = CRUDDish.delete_dish(menu_id, submenu_id, dish_id, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu or submenu not found"
        )
