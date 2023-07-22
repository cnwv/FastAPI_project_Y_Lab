from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=["Submenus"]
)


@router.get("/")
def get_submenus():
    return


@router.post("/")
def create_submenu(submenu_id):
    return


@router.get("/{submenu_id}")
def get_target_submenu(submenu_id):
    return


@router.patch("/{submenu_id}")
def update_target_menu(submenu_id):
    return


@router.delete("/{submenu_id}")
def delete_target_submenu(menu_id):
    return
