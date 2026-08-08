import json

from groq import Groq

from app.core.config import settings
from app.core.logging import logger
from app.exceptions.custom_exceptions import LLMIntegrationException
from app.schemas.parsed_resume import LLMExtractedResume


def parse_resume_with_llm(cleaned_text: str) -> LLMExtractedResume:
    """Uses Groq LLM to semantically structure the cleaned resume text.

    Args:
        cleaned_text: The pristine, normalized text extracted from the document.

    Returns:
        LLMExtractedResume: Pydantic model containing the structured data.

    Raises:
        LLMIntegrationException: If the LLM times out or returns malformed JSON.
    """
    logger.info("Calling Groq LLM to structure resume text...")

    if not settings.GROQ_API_KEY:
        raise LLMIntegrationException(
            details={"reason": "GROQ_API_KEY is not configured."}
        )

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)

        schema = LLMExtractedResume.model_json_schema()

        system_prompt = f"""You are an expert ATS (Applicant Tracking System) parser.
Your task is to extract information from the provided resume text and output it strictly as a JSON object matching this exact schema:
{json.dumps(schema, indent=2)}

Rules:
1. Return ONLY valid JSON. No markdown formatting, no explanation.
2. If a field is not found in the resume, omit it or return null (if optional) or an empty array/string based on the schema.
3. Be objective. Do not hallucinate information not present in the text."""

        user_prompt = f"<resume_text>\n{cleaned_text}\n</resume_text>"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )

        json_output = response.choices[0].message.content
        if json_output is None:
            raise ValueError("LLM returned empty content")
        extracted_resume = LLMExtractedResume.model_validate_json(json_output)
        return extracted_resume

    except Exception as e:
        logger.error(f"LLM integration failed: {str(e)}")
        raise LLMIntegrationException(details={"reason": str(e)})
