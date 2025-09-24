from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},   
)