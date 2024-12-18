from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Type, TypeVar, cast
from fastapi import HTTPException, status, UploadFile

DBModelT = TypeVar("DBModelT")

async def find_instance_or_fail(
    db: AsyncSession,
    model: Type[DBModelT],
    *args,
    message_404: Optional[str] = None,
) -> DBModelT:
    if message_404 is None:
        message_404 = f"Not found for {model.__name__}"

    instance: Optional[DBModelT] = await db.scalar(select(model).where(*args))

    if instance is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            message_404,
        )

    return cast(DBModelT, instance)

# await db.delete(
#     await find_instance_or_fail(
#         db,
#         User,
#         User.user_id == user_id,
#         message_404=f"Not found for user with user_id {user_id}",
#     )
# )
# await db.commit()