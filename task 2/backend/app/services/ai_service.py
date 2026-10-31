import httpx
from typing import Optional
from app.core.config import settings
from app.schemas.ai import AIRequest, AIResponse


class AIService:
    def __init__(self):
        self.provider = settings.ai_provider
        self.api_key = settings.ai_api_key
        self.model = settings.ai_model
        self.base_url = settings.ai_base_url
        self.timeout = settings.ai_timeout_seconds

    def _build_prompt(self, request: AIRequest) -> str:
        return f"""You are producing an informational explanation for a software assessment demonstration, not a medical diagnosis.
Review only the supplied blood-test values:
Glucose: {request.glucose}
Haemoglobin: {request.haemoglobin}
Cholesterol: {request.cholesterol}

The units, laboratory reference intervals, fasting status, sex, medical history and clinical context may be missing.
Return:
- A cautious, plain-language observation.
- A clear statement of important missing context.
- A suggestion to discuss results with a qualified clinician.

Do not diagnose a disease.
Do not prescribe medication or treatment.
Do not invent units, normal ranges, probabilities or certainty.
If interpretation is limited by missing units/context, say so.
Keep the response concise and suitable for a patient record."""

    async def analyze(self, request: AIRequest) -> AIResponse:
        if not self.api_key:
            return AIResponse(
                remarks=None,
                status="unavailable",
                provider=None,
                model=None
            )

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if self.provider.lower() == "openai":
                    return await self._call_openai(client, request)
                else:
                    # Generic HTTP-based provider
                    return await self._call_generic_provider(client, request)
        except httpx.TimeoutException:
            return AIResponse(
                remarks=None,
                status="failed",
                provider=self.provider,
                model=self.model
            )
        except Exception as e:
            return AIResponse(
                remarks=None,
                status="failed",
                provider=self.provider,
                model=self.model
            )

    async def _call_openai(self, client: httpx.AsyncClient, request: AIRequest) -> AIResponse:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": self._build_prompt(request)}
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        response = await client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            return AIResponse(
                remarks=None,
                status="failed",
                provider=self.provider,
                model=self.model
            )
        
        data = response.json()
        remarks = data["choices"][0]["message"]["content"].strip()
        
        if not remarks or len(remarks) > 2000:
            return AIResponse(
                remarks=None,
                status="failed",
                provider=self.provider,
                model=self.model
            )
        
        return AIResponse(
            remarks=remarks,
            status="completed",
            provider=self.provider,
            model=self.model
        )

    async def _call_generic_provider(self, client: httpx.AsyncClient, request: AIRequest) -> AIResponse:
        # Generic provider interface - can be extended
        return AIResponse(
            remarks=None,
            status="unavailable",
            provider=self.provider,
            model=self.model
        )
