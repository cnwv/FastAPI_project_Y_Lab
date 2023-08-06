from pydantic import BaseModel
from sqlalchemy import delete, func, insert, select, update

from src.api.models import Dish, Menu, Submenu


class MenuModel(BaseModel):
    id: str
    title: str
    description: str


class MenuService:
    @staticmethod
    def prepare_response(menu):
        response = dict()
        response['id'] = str(menu.id)
        response['title'] = str(menu.title)
        response['description'] = str(menu.description)
        return response

    @staticmethod
    def get_menu_json(menu, session):
        submenu_count = (
            session.query(func.count(Submenu.id))
            .filter(Submenu.menu_id == menu.id)
            .scalar()
        )
        dish_count = (
            session.query(func.count(Dish.id))
            .join(Submenu)
            .filter(Submenu.menu_id == menu.id)
            .scalar()
        )
        result = {
            'id': str(menu.id),
            'title': menu.title,
            'description': menu.description,
            'submenus_count': submenu_count,
            'dishes_count': dish_count,
        }
        return result

    @staticmethod
    def get_menus(session):
        result = {'result': []}
        menus = session.query(Menu).all()
        if menus:
            for menu in menus:
                menu_json = MenuService.get_menu_json(menu, session)
                result['result'].append(menu_json)
            return result
        return []

    @staticmethod
    def create_menu(menu, session):
        stmt = (
            insert(Menu)
            .values(title=menu.title, description=menu.description)
            .returning(Menu)
        )
        result = MenuService.get_menu_json(session.execute(stmt).scalar(), session)
        session.commit()
        return result

    @staticmethod
    def get_target_menu(menu_id, session):
        query = select(Menu).where(Menu.id == menu_id)
        result = session.execute(query).scalar()
        if result:
            result = MenuService.get_menu_json(result, session)
            return result
        else:
            return False

    @staticmethod
    def update_target_menu(menu_id, menu, session):
        stmt = session.execute(
            update(Menu).where(Menu.id == menu_id).values(**menu.dict()).returning(Menu)
        )
        updated_row = stmt.scalar()
        if updated_row:
            session.commit()
            result = MenuService.prepare_response(updated_row)
            return result

    @staticmethod
    def delete_target_menu(menu_id, session):
        stmt = session.execute(delete(Menu).where(Menu.id == menu_id))
        if stmt.rowcount > 0:
            session.commit()
            return True
        return []
