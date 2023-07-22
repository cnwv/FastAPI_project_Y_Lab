from fastapi import APIRouter
from src.api.CRUD.submenus import CRUDSubmenu
from config import get_sync_session
from sqlalchemy.orm import Session
from fastapi import Depends, Response, status
from pydantic import BaseModel
from fastapi import HTTPException

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=["Submenus"]
)


class SubmenuBody(BaseModel):
    title: str
    description: str


@router.get("/")
def get_submenus(menu_id: int,
                 session: Session = Depends(get_sync_session)):
    result = CRUDSubmenu.get_submenus(menu_id, session)
    if result:
        return result
    return []


@router.post("/")
def create_submenu(response: Response,
                   menu_id: int, submenu: SubmenuBody,
                   session: Session = Depends(get_sync_session)):
    result = CRUDSubmenu.create_submenu(menu_id, submenu, session)
    response.status_code = status.HTTP_201_CREATED
    return result


@router.get("/{submenu_id}")
def get_target_submenu(menu_id: int,
                       submenu_id: int,
                       session: Session = Depends(get_sync_session)):
    result = CRUDSubmenu.get_target_submenu(menu_id, submenu_id, session)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")


@router.patch("/{submenu_id}")
def update_target_menu(menu_id: int,
                       submenu_id: int,
                       submenu: SubmenuBody,
                       session: Session = Depends(get_sync_session)):
    result = CRUDSubmenu.update_target_submenu(menu_id, submenu_id, submenu, session)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")


@router.delete("/{submenu_id}")
def delete_target_submenu(menu_id: int,
                          submenu_id: int,
                          session: Session = Depends(get_sync_session)):
    result = CRUDSubmenu.delete_target_submenu(menu_id, submenu_id, session)
    if result:
        return f'Menu ID {submenu_id} deleted successfully.'
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
