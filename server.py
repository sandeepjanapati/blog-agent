"""
FastAPI backend for the AI Blog Writing Agent.

Endpoints:
- GET /health: Basic health check.
- POST /v1/generate: Generate blog content and SEO metadata.

Run locally:
  uvicorn server:app --host 0.0.0.0 --port 8000
"""

import os
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from main import run_blog_agent


class GenerateRequest(BaseModel):
    topic: str = Field(..., description="Main topic for the blog post")
    tone: Optional[str] = Field("informative", description="Desired writing tone")
    output_dir: Optional[str] = Field("output", description="Directory to save generated files")


class GenerateResponse(BaseModel):
    content: str
    metadata: Dict[str, Any]


app = FastAPI(title="AI Blog Agent API", version="1.0.0")

# Allow all origins by default; tighten for production as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest) -> GenerateResponse:
    try:
        markdown_content, metadata = await run_blog_agent(
            topic=req.topic,
            tone=req.tone or "informative",
            output_dir=req.output_dir or "output",
            run_mode="cli",
        )
        if not markdown_content or not metadata:
            raise HTTPException(status_code=500, detail="Generation failed. Check server logs for details.")

        return GenerateResponse(content=markdown_content, metadata=metadata)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )

