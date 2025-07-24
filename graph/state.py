from typing import TypedDict, List, Optional, Any

class State(TypedDict):
    request_id: str
    extracted_text: str
    embeddings: List[float]
    # metadata: Optional[dict[str, Any]]  # Optional metadata for additional information
    summary: str
    
    mode: str # either user_query or summarize_news mode 
    user_input: Optional[str]
    agent_response: Optional[str]   
    prompt: Optional[str]
    