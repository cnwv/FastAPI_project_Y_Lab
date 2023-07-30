from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import get_sync_session
from src.api.CRUD.menus import CRUDMenu

router = APIRouter(prefix="/api/v1/menus", tags=["Menus"])


class MenuBody(BaseModel):
    title: str
    description: str


@router.get("/")
def get_menus(session: Session = Depends(get_sync_session)):
    result = CRUDMenu.get_menus(session)
    return result


@router.post("/")
def create_menu(
    response: Response, menu: MenuBody, session: Session = Depends(get_sync_session)
):
    result = CRUDMenu.create_menu(menu, session)
    response.status_code = status.HTTP_201_CREATED
    return result


@router.get("/{menu_id}")
def get_target_menu(menu_id: int, session: Session = Depends(get_sync_session)):
    result = CRUDMenu.get_target_menu(menu_id, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )


@router.patch("/{menu_id}")
def update_target_menu(
    menu_id: int, menu: MenuBody, session: Session = Depends(get_sync_session)
):
    result = CRUDMenu.update_target_menu(menu_id, menu, session)
    return result


@router.delete("/{menu_id}")
def delete_target_menu(menu_id: int, session: Session = Depends(get_sync_session)):
    result = CRUDMenu.delete_target_menu(menu_id, session)
    if result:
        return f"Menu ID {menu_id} deleted successfully."
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
