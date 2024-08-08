from typing import Optional  
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.model.orm import Citizen
from app.api.deps import (
    SessionDep, get_current_active_superuser, get_current_user
)
from app.data.peru_data import apiNetPe
from app.dto.optimizer import OptimizationRequest, OptimizationResult
from scripts.optimizers.maximal_covering_location import MaximalCoveringLocation

from app.dto.utils import Message

router = APIRouter()



@router.post("/optimize-covering-location", response_model=OptimizationResult)
async def web_service_optimize_covering_location(request: OptimizationRequest):
    try:
        optimizer = MaximalCoveringLocation(
            points=request.points,
            demands=request.demands,
            facilities=request.facilities,
            max_facilities=request.max_facilities,
            coverage_radius=request.coverage_radius
        )
        result = optimizer.solve()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))