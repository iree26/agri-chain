"""AgriChain AI - FastAPI endpoint"""

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agrichain.ai.agents.orchestrator import OrchestratorAgent

app = FastAPI(title="AgriChain AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OrchestrateRequest(BaseModel):
    language: str
    soil_type: str
    fertilization_method: str
    farm_size: float
    name: str
    state: str
    lga: str
    crop: str


orchestrator = OrchestratorAgent()


@app.post("/orchestrate")
async def orchestrate(request: OrchestrateRequest):
    result = await orchestrator.orchestrate(
        name=request.name,
        state=request.state,
        lga=request.lga,
        crop=request.crop,
        farm_size=str(request.farm_size),
        language=request.language,
        soil_type=request.soil_type,
        fertilization_method=request.fertilization_method
    )
    return {
        "success": result["success"],
        "farm_plan": result.get("farm_plan", "")
       
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
