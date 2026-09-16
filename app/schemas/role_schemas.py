from pydantic import BaseModel, Field


class RoleRequest(BaseModel):
    name : str
    description : str
    is_active : bool


class RoleResponse(BaseModel):
    id : int
    name : str
    description : str
    is_active : bool


