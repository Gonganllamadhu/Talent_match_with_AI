import os
from pydantic import BaseModel, Field
from langchain_mistralai import ChatMistralAI

from app.prompt.resume_parser_prompt import parser_prompt
from app.prompt.resume_analyze_prompt import resume_analyzer_prompt
class ResumeEvaluation(BaseModel):
    match_score: int = Field( ge=0, le=100, description="Overall resume-job match score from 0 to 100.", )
    is_match: bool = Field( description=( "True when the candidate meets the configured " "minimum matching criteria." ) )
    recommendation: str = Field( description=( "One of: STRONG_MATCH, REVIEW, NOT_A_MATCH." ) )
    summary: str
    matched_skills: list[str]
    missing_skills: list[str]
    experience_analysis: str
    education_analysis: str
    pros: list[str]
    cons: list[str]
    detailed_analysis: dict



def get_llm ():
    model = os.getenv("MISTRAL_MODEL")
    temperature = "0.2"

    return ChatMistralAI(model_name=model, temperature=temperature)


def evaluate_resume(
        resume_input : str
):
    prompt = parser_prompt(resume_input=resume_input)
    llm = get_llm()
    result = llm.invoke(prompt)
    return result


def evaluate_resume_with_job(
    resume_input: str,
    job_profile_input: str,
):
    prompt = resume_analyzer_prompt(
        resume_input=resume_input,
        job_profile_input=job_profile_input,
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(ResumeEvaluation)

    result = structured_llm.invoke(prompt)

    return result