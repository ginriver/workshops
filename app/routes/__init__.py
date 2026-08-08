"""API route modules."""
from app.routes.instruments import router as instruments_router
from app.routes.calibrations import router as calibrations_router

__all__ = ["instruments_router", "calibrations_router"]
