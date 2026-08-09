import asyncio
from app.services.analysis_service import execute_analysis_workflow

resume_content = b"""John Doe
Senior Backend Engineer
Email: john.doe@example.com | Location: San Francisco, CA

SUMMARY
Senior Software Engineer with 6+ years of experience designing high-throughput REST APIs in Python and FastAPI.

EXPERIENCE
Software Engineering Intern at Amazon (2020)
- Built internal tools using Java and AWS.

TECHNICAL SKILLS
Python, FastAPI, SQL, Docker, Kubernetes, AWS, REST APIs, PostgreSQL, DSA Coursework, OOP Coursework, C++

EDUCATION
Bachelor of Science in Computer Science - UC Berkeley (2021)
"""

jd_content = b"""Job Title: Software Development Engineer (SDE)
Employment Type: Full-time

Requirements:
- Experience in software development using Java or C++.
- Deep expertise in Databases.
- Knowledge of Web Services.
- Strong understanding of Data Structures.
- Strong understanding of Object Oriented Programming.

Responsibilities:
- Architect and deploy scalable microservices.
- Qualifications: Bachelor's degree in Computer Science."""


async def main():
    print("Running ATS Engine trace...")
    response = await execute_analysis_workflow(
        resume_bytes=resume_content,
        resume_filename="resume.txt",
        jd_bytes=jd_content,
        jd_filename="amazon_sde_jd.txt",
    )
    
    report = response.match_report
    print(f"\nOverall Score: {report.overall_score}\n")
    print(f"JD Parsed Experience Req: {response.parsed_jd.experience_requirements.value}")
    
    print("Skills Evaluation Evidence:")
    for ev in report.skills_evaluation.evidence:
        print(f"Req: {ev.requirement} -> Level: {ev.match_level.name} | Found: {ev.evidence_found}")
        
    print("\nExperience Evaluation Evidence:")
    for ev in report.experience_evaluation.evidence:
        print(f"Req: {ev.requirement} -> Level: {ev.match_level.name} | Found: {ev.evidence_found}")

if __name__ == "__main__":
    asyncio.run(main())
