from pydantic import BaseModel, ConfigDict

class ModelSource(BaseModel):
    name: str
    theme: str
    url: str
    model_config = ConfigDict(from_attributes=True)


class ModelSourceWithID(ModelSource):
    id: int
    model_config = ConfigDict(from_attributes=True)