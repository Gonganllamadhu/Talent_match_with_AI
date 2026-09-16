from pydantic import BaseModel, Field


class DepartmentRequest(BaseModel):
    name : str
    description : str
    is_active : bool


class DepartmentResponse(BaseModel):
    id : int
    name : str
    description : str
    is_active : bool