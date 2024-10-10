from .server import app
from .routers import auth, items

app.include_router(auth.router)
app.include_router(items.router)