from pydantic import BaseModel
from typing import List

class Prediction(BaseModel):
    case_id: str
    study_id: str
    predicted_is_relevant: bool

class InferenceResponse(BaseModel):
    predictions: List[Prediction]