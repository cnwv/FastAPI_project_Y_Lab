from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1/menus',
    tags=["Menus"]
)


@router.get("/")
def get_menus():
    return


@router.post("/")
def create_menu(menu_id):
    return


@router.get("/{menu_id}")
def get_target_menu(menu_id):
    return


@router.patch("/{menu_id}")
def update_target_menu(menu_id):
    return


@router.delete("/{menu_id}")
def delete_target_menu(menu_id):
    return
