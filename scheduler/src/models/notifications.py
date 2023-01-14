from typing import Any, List, Optional
from uuid import UUID

from pydantic import EmailStr


class TaskForWorker:
    """Модель задачи для добавления в очередь к воркеру."""

    targets: List[str]
    template: Optional[Any]
    user_id: Optional[UUID]
    email: EmailStr
