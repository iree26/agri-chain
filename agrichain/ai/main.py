"""
AgriChain AI - Main entry point
"""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

from agrichain.ai.agents.orchestrator import OrchestratorAgent


def main():
    """Main function for AgriChain AI system."""
    orchestrator = OrchestratorAgent()
    
    # Run with sample data
    result = asyncio.run(
        orchestrator.orchestrate(
            name="Chukwuemeka",
            state="Kebbi",
            lga="Ngaski",
            crop="Rice",
            farm_size="2",
            language="Hausa",
            soil_type="Loamy",
            fertilization_method="Mixed (both organic and inorganic)"
        )
    )
    
    if result["success"]:
        print("\n" + "="*60)
        print("AGRICHAIN WEEKLY FARM PLAN")
        print("="*60)
        print(f"Farmer: {result['farmer_name']}")
        print(f"Location: {result['lga']}, {result['state']}")
        print(f"Crop: {result['crop']}")
        print(f"Farm Size: {result['farm_size']} hectares")
        print(f"Soil Type: {result.get('soil_type', 'N/A')}")
        print(f"Fertilization: {result.get('fertilization_method', 'N/A')}")
        print(f"Language: {result['language']}")
        print("="*60)
        print(result["farm_plan"])
        print("="*60)
        print(f"Execution time: {result['execution_times']['total']}")
        exported = result.get("exported_files", {})
        if exported:
            print(f"Files exported: {exported.get('docx', 'N/A')}, {exported.get('pdf', 'N/A')}")
    else:
        print(f"Error: {result['error']}")
        print(result.get("details", {}))


if __name__ == "__main__":
    main()
