from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=["Dishes"]
)


@router.get("/")
def get_dishes():
    return ''


@router.post("/")
def create_dish():
    return


@router.get("/{dish_id}")
def get_target_dish(dish_id):
    return


@router.patch("/{dish_id}")
def update_target_dish(dish_id):
    return


@router.delete("/{dish_id}")
def delete_target_dish(dish_id):
    return