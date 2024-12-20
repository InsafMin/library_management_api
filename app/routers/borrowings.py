from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper
from crud import borrowing as crud_borrowing
from dependencies import borrowing_by_id
from schemas import Borrowing, BorrowingUpdatePartial, BorrowingUpdate, BorrowingCreate

router = APIRouter()


@router.get("/", response_model=list[Borrowing])
async def get_borrowings(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud_borrowing.get_all_borrowings(session=session)


@router.post("/", response_model=Borrowing, status_code=status.HTTP_201_CREATED)
async def create_borrowing(
    borrowing_create: BorrowingCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud_borrowing.create_borrowing(
        session=session, borrowing_create=borrowing_create
    )


@router.get("/{borrowing_id}/", response_model=Borrowing)
async def get_borrowing(
    borrowing: Borrowing = Depends(borrowing_by_id),
):
    return borrowing


@router.put("/{borrowing_id}/")
async def update_borrowing(
    borrowing_update: BorrowingUpdate,
    borrowing: Borrowing = Depends(borrowing_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud_borrowing.update_borrowing(
        session=session,
        borrowing=borrowing,
        borrowing_update=borrowing_update,
    )


@router.patch("/{borrowing_id}/")
async def update_borrowing_partial(
    borrowing_update: BorrowingUpdatePartial,
    borrowing: Borrowing = Depends(borrowing_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud_borrowing.update_borrowing(
        session=session,
        borrowing=borrowing,
        borrowing_update=borrowing_update,
        partial=True,
    )


@router.delete("/{borrowing_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reader(
    borrowing: Borrowing = Depends(borrowing_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await crud_borrowing.delete_borrowing(session=session, borrowing=borrowing)
