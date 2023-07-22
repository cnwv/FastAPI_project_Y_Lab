from fastapi import FastAPI
from src.api.endpoints.menus import router as router_menus
from src.api.endpoints.submenus import router as router_submenus
from src.api.endpoints.dishes import router as router_dishes
app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World!"}


app.include_router(router_menus)
app.include_router(router_submenus)
app.include_router(router_dishes)

