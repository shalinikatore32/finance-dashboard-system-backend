from fastapi import APIRouter
from app.services.dashboard_service import get_dashboard_summary
from app.routers.deps import RequireAnalyst

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
async def get_summary(current_user = RequireAnalyst):
    """Get dashboard summary. Analyst and Admin only."""
    return await get_dashboard_summary()
