from fastapi import APIRouter
from src.api.CRUD.menus import CRUDMenu
from config import get_sync_session
from sqlalchemy.orm import Session
from fastapi import Depends, Response, status
from pydantic import BaseModel
from fastapi import HTTPException

router = APIRouter(
    prefix='/api/v1/menus',
    tags=["Menus"]
)


class MenusBody(BaseModel):
    title: str
    description: str


@router.get("/")
def get_menus(session: Session = Depends(get_sync_session)):
    result = CRUDMenu.get_menus(session)
    return result


@router.post("/")
def create_menu(response: Response,
                menu: MenusBody,
                session: Session = Depends(get_sync_session)):
    result = CRUDMenu.create_menu(menu, session)
    response.status_code = status.HTTP_201_CREATED
    return result


@router.get("/{menu_id}")
def get_target_menu(menu_id: int,
                    session: Session = Depends(get_sync_session)):
    result = CRUDMenu.get_target_menu(menu_id, session)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found.")


@router.patch("/{menu_id}")
def update_target_menu(menu_id: int,
                       menu: MenusBody,
                       session: Session = Depends(get_sync_session)):
    result = CRUDMenu.update_target_menu(menu_id, menu, session)
    return result


@router.delete("/{menu_id}")
def delete_target_menu(menu_id: int,
                       session: Session = Depends(get_sync_session)):
    result = CRUDMenu.delete_target_menu(menu_id, session)
    if result:
        return f'Menu ID {menu_id} deleted successfully.'
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found.")
