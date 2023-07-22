from sqlalchemy import select, insert, update, delete, func
from .schemas import Menu, Submenu, Dish
from pydantic import BaseModel


class MenuModel(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        orm_mode = True


class CRUDMenu():

    @staticmethod
    def prepare_response(menu):
        response = dict()
        response['id'] = str(menu.id)
        response['title'] = str(menu.title)
        response['description'] = str(menu.description)
        return response

    @staticmethod
    def get_submenu_and_dish_count(menu_id, session):
        submenu_count = session.query(func.count(Submenu.id)).filter(Submenu.menu_id == menu_id).scalar()
        dish_count = session.query(func.count(Dish.id)).join(Submenu).filter(Submenu.menu_id == menu_id).scalar()
        return submenu_count, dish_count

    @staticmethod
    def get_menus(session):
        result = {'result': []}
        menus = session.query(Menu).all()
        if menus:
            for menu in menus:
                submenu_count, dish_count = CRUDMenu.get_submenu_and_dish_count(menu.id, session)
                result['result'].append(
                    {'Menu ID': menu.id, 'Title': menu.title, 'Submenu Count': submenu_count, 'Dish Count': dish_count}
                )
            return result
        return []

    @staticmethod
    def create_menu(menu, session):
        stmt = insert(Menu).values(title=menu.title, description=menu.description).returning(Menu)
        result = CRUDMenu.prepare_response(session.execute(stmt).scalar())
        session.commit()
        return result

    @staticmethod
    def get_target_menu(menu_id, session):
        query = select(Menu).where(Menu.id == menu_id)
        result = session.execute(query).scalar()
        if result:
            result = CRUDMenu.prepare_response(result)
            return result
        else:
            return False

    @staticmethod
    def update_target_menu(menu_id, menu, session):
        stmt = session.execute(update(Menu).where(Menu.id == menu_id).values(**menu.dict()).returning(Menu))
        updated_row = stmt.scalar()
        if updated_row:
            session.commit()
            result = CRUDMenu.prepare_response(updated_row)
            return result

    @staticmethod
    def delete_target_menu(menu_id, session):
        stmt = session.execute(delete(Menu).where(Menu.id == menu_id))
        if stmt.rowcount > 0:
            session.commit()
            return True
        return []
