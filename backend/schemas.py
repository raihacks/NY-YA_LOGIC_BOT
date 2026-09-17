from pydantic import BaseModel


class ArgumentRequest(BaseModel):
    text: str


class NyayaResult(BaseModel):
    pratijna: str
    hetu: str
    udaharana: str
    upanaya: str
    nigamana: str
    explanation: str
    validity: str