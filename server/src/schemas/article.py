from pydantic import BaseModel, ConfigDict

class ModelArticle(BaseModel):
    name: str
    id_source: int
    content: str
    url: str
    theme_name: str
    model_config = ConfigDict(from_attributes=True)


class ModelArticleWithID(ModelArticle):
    id: int
    model_config = ConfigDict(from_attributes=True)