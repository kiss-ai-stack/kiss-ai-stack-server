from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field


class DocumentsRequestBody(BaseModel):
    """
    Structured request for document upload
    """
    files: List[Dict[str, Any]] = Field(
        ...,
        description="List of files to upload. Each file is a dictionary with name and base64-encoded content"
    )
    query: Optional[str] = Field(
        None,
        description='Optional user inputs upon storing documents'
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional metadata for the upload"
    )
