from app.routers.users import router as users_router
from app.routers.services import router as services_router
from app.routers.sales import router as sales_router
from app.routers.enquiries import router as enquiries_router
from app.routers.appointments import router as appointments_router

api_routers = [
    users_router,
    services_router,
    sales_router,
    enquiries_router,
    appointments_router,
]