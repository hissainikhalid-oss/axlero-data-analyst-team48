from typing import List, Dict, Any
from pydantic import BaseModel

class CSVUploadResponse(BaseModel):
    total_rows: int
    successful_predictions: int
    failed_rows: int
    errors: List[Dict[str, Any]]
