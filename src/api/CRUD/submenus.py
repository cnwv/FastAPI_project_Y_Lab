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
    def get_menu_json(submenu, session):
        dish_count = session.query(func.count(Dish.id)).join(Submenu).filter(Submenu.id == submenu.id).scalar()
        result = {'id': str(submenu.id),
                  'title': submenu.title,
                  'description': submenu.description,
                  'dishes_count': dish_count}
        return result

    @staticmethod
    def get_submenus(menu_id, session):
        result = {'Submenus': []}
        submenus = session.query(Submenu).where(Submenu.menu_id == menu_id).all()
        if submenus:
            for submenu in submenus:
                submenu_json = CRUDSubmenu.get_menu_json(submenu, session)
                result['Submenus'].append(submenu_json)
            return result
        return []

    @staticmethod
    def create_submenu(target_menu_id, submenu, session):# TODO при одинаковом титуле возращает 500. Исправить psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "uq_submenu_title_menu_id"

        stmt = insert(Submenu).values(menu_id=target_menu_id,
                                      title=submenu.title,
                                      description=submenu.description).returning(Submenu)
        result = CRUDSubmenu.get_menu_json(session.execute(stmt).scalar(), session)
        if result:
            session.commit()
            return result
        return False

    @staticmethod
    def get_target_submenu(menu_id, submenu_id, session):
        query = select(Submenu).where(Submenu.id == submenu_id, Submenu.menu_id == menu_id)
        result = session.execute(query).scalar()
        if result:
            result = CRUDSubmenu.get_menu_json(result, session)
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
            result = CRUDSubmenu.get_menu_json(updated_row, session)
            return result
        return []

    @staticmethod
    def delete_target_submenu(menu_id, submenu_id, session):
        stmt = session.execute(delete(Submenu).where(Submenu.id == submenu_id,
                                                     Submenu.menu_id == menu_id))
        if stmt.rowcount > 0:
            session.commit()
            return f'Dish ID {submenu_id} deleted successfully.'
        return False
