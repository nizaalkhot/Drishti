import os
import asyncio
from typing import Optional, Any
from dotenv import load_dotenv
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.agents import BaseAgent
from google.genai import Client, types

# Load local .env if present
load_dotenv()

class DrishtiGemini(Gemini):
    """
    Drishti Google ADK Model Provider.
    Prioritizes GEMINI_API_KEY from environment, with seamless fallback to Vertex AI.
    """
    @property
    def api_client(self) -> Client:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            return Client(api_key=api_key)
        
        project = os.getenv("GCP_PROJECT", "team-gain")
        region = os.getenv("REGION", "us-central1")
        try:
            return Client(vertexai=True, project=project, location=region)
        except Exception:
            return Client()

def get_adk_model(model_name: str = "gemini-2.0-flash") -> Gemini:
    """Returns an initialized Google ADK Gemini model instance."""
    return DrishtiGemini(model=model_name)

async def execute_adk_agent(
    agent: BaseAgent,
    input_text: str,
    user_id: str = "drishti-analyst"
) -> str:
    """
    Executes a Google ADK agent or workflow agent (ParallelAgent, SequentialAgent, LoopAgent)
    using InMemoryRunner and returns the final generated text output.
    """
    runner = InMemoryRunner(agent=agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id
    )
    
    new_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=input_text)]
    )

    final_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=new_message
    ):
        # Event content extraction
        if hasattr(event, "content") and event.content:
            for part in getattr(event.content, "parts", []):
                if hasattr(part, "text") and part.text:
                    final_text += part.text
        elif hasattr(event, "output") and event.output:
            final_text += str(event.output)

    return final_text.strip()
