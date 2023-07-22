from sqlalchemy import select, insert, update, delete, func
from .schemas import Submenu, Dish
from pydantic import BaseModel


class SubmenuModel(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        orm_mode = True


class CRUDSubmenu():
    @staticmethod
    def prepare_response(submenu, menu_id):
        response = dict()
        response['id'] = str(submenu.id)
        response['title'] = str(submenu.title)
        response['description'] = str(submenu.description)
        response['menu_id'] = str(menu_id)
        return response

    @staticmethod
    def get_submenu_and_dish_count(submenu_id, session):
        dish_count = session.query(func.count(Dish.id)).join(Submenu).filter(Submenu.id == submenu_id).scalar()
        return dish_count

    @staticmethod
    def get_submenus(menu_id, session):
        result = {'Submenus': []}
        submenus = session.query(Submenu).where(Submenu.menu_id == menu_id).all()
        if submenus:
            for submenu in submenus:
                dish_count = CRUDSubmenu.get_submenu_and_dish_count(submenu.id, session)
                result['Submenus'].append(
                    {'Submenu ID': submenu.id, 'Title': submenu.title, 'Dish Count': dish_count}
                )
            return result
        return []

    @staticmethod
    def create_submenu(target_menu_id, submenu, session):
        stmt = insert(Submenu).values(menu_id=target_menu_id,
                                      title=submenu.title,
                                      description=submenu.description).returning(Submenu)
        result = CRUDSubmenu.prepare_response(session.execute(stmt).scalar(), target_menu_id)
        session.commit()
        return result

    @staticmethod
    def get_target_submenu(menu_id, submenu_id, session):
        query = select(Submenu).where(Submenu.id == submenu_id, Submenu.menu_id == menu_id)
        result = session.execute(query).scalar()
        if result:
            result = CRUDSubmenu.prepare_response(result, menu_id)
            return result
        else:
            return []

    @staticmethod
    def update_target_submenu(menu_id, submenu_id, submenu, session):
        stmt = session.execute(update(Submenu).where(Submenu.id == submenu_id,
                                                     Submenu.menu_id == menu_id).values(**submenu.dict()).returning(
            Submenu))
        updated_row = stmt.scalar()
        if updated_row:
            session.commit()
            result = CRUDSubmenu.prepare_response(updated_row, menu_id)
            return result
        return []

    @staticmethod
    def delete_target_submenu(menu_id, submenu_id, session):
        stmt = session.execute(delete(Submenu).where(Submenu.id == submenu_id,
                                                     Submenu.menu_id == menu_id))
        if stmt.rowcount > 0:
            session.commit()
            return True
        return False
