from pydantic import BaseModel, Field


class QueryRequestBody(BaseModel):
    query: str = Field('Greetings!', description='User input text')
