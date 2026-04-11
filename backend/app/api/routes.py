from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.analyzer import AnalysisService

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Analyze a German news article.

    - **input**: URL or article text
    - **mode**: 'auto', 'url', or 'text'
    - **summary_length**: 'short', 'medium', or 'detailed'
    """
    if not request.input or not request.input.strip():
        raise HTTPException(status_code=400, detail="Input cannot be empty")

    try:
        result = AnalysisService.analyze(
            input_text=request.input,
            mode=request.mode,
            summary_length=request.summary_length,
        )
        return AnalyzeResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
