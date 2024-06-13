
'''from pydantic import BaseModel
from typing import Dict

class ConfigurationCreate(BaseModel):
    country_code: str  # Use 'str' instead of 'String'
    requirements: Dict[str, str]

class ConfigurationUpdate(BaseModel):
    requirements: Dict[str, str]

class ConfigurationResponse(ConfigurationCreate):
    id: int

    class Config:
        orm_mode = True
'''
'''
from pydantic import BaseModel
from typing import Dict, Optional

class ConfigurationCreate(BaseModel):
    country_code: str
    requirements: Dict[str, str]

class ConfigurationUpdate(BaseModel):
    requirements: Dict[str, str]

class ConfigurationResponse(BaseModel):
    id: int
    country_code: str
    requirements: Dict[str, str]

class ConfigurationUpdate(BaseModel):
    requirements: Dict[str, str]

class ConfigurationResponse(ConfigurationCreate):
    id: int

    class Config:
        orm_mode = True


'''



from pydantic import BaseModel
from typing import Dict

class ConfigurationCreate(BaseModel):
    country_code: str
    requirements: Dict[str, str]

class ConfigurationResponse(BaseModel):
    id: int
    country_code: str
    requirements: Dict[str, str]

class ConfigurationUpdate(BaseModel):
    requirements: Dict[str, str]
