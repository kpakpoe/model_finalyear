from typing import List
from datetime import date
from pydantic import BaseModel

class data_to_be_used_for_prediction(BaseModel):
    Date: List[date]
    Close: List[float]
    
class prediction(BaseModel):
    Prediction: List[float]