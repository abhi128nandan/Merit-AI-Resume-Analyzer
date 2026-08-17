import time
from app.matching.evidence import collect_skills_evidence, collect_experience_evidence
from app.schemas.parsed_jd import VerifiedJD, VerifiedJDField
from app.schemas.parsed_resume import VerifiedParsedResume, VerifiedField, VerifiedExperience, VerifiedEducation, VerifiedContact

jd = VerifiedJD(
    job_title=VerifiedJDField(value='Software Engineer', verification_state='Verified'),
    company=VerifiedJDField(value='Tech Corp', verification_state='Verified'),
    location=VerifiedJDField(value='Remote', verification_state='Verified'),
    employment_type=VerifiedJDField(value='Full-time', verification_state='Verified'),
    required_skills=[
        VerifiedJDField(value='Java', verification_state='Verified'),
        VerifiedJDField(value='C++', verification_state='Verified'),
        VerifiedJDField(value='Python', verification_state='Verified'),
        VerifiedJDField(value='Data structures', verification_state='Verified'),
        VerifiedJDField(value='Algorithms', verification_state='Verified'),
        VerifiedJDField(value='Object-oriented programming', verification_state='Verified'),
        VerifiedJDField(value='Software development fundamentals', verification_state='Verified'),
        VerifiedJDField(value='Web services', verification_state='Verified'),
        VerifiedJDField(value='Databases', verification_state='Verified'),
        VerifiedJDField(value='Distributed systems', verification_state='Verified'),
        VerifiedJDField(value='Cloud technologies', verification_state='Verified'),
        VerifiedJDField(value='Linux/Unix environments', verification_state='Verified'),
        VerifiedJDField(value='Git', verification_state='Verified'),
        VerifiedJDField(value='System design', verification_state='Verified'),
        VerifiedJDField(value='Scalable software architecture', verification_state='Verified')
    ],
    preferred_skills=[],
    responsibilities=[],
    qualifications=[],
    experience_requirements=VerifiedJDField(value='3 years', verification_state='Verified'),
    education_requirements=VerifiedJDField(value='BS Computer Science', verification_state='Verified'),
    overall_confidence=100,
    section_confidence={}
)

resume = VerifiedParsedResume(
    contact=VerifiedContact(email=None, phone=None, linkedin=None),
    summary=VerifiedField(value='Experienced backend developer with strong foundations in API design and databases.', verification_state='Verified'),
    skills=[
        VerifiedField(value='REST APIs', verification_state='Verified'),
        VerifiedField(value='PostgreSQL', verification_state='Verified'),
        VerifiedField(value='Spring Boot', verification_state='Verified'),
        VerifiedField(value='DBMS', verification_state='Verified'),
        VerifiedField(value='Git', verification_state='Verified')
    ],
    experience=[VerifiedExperience(
        title=VerifiedField(value='Software Engineering Intern', verification_state='Verified'),
        company=VerifiedField(value='Startup Inc', verification_state='Verified'),
        start_date=VerifiedField(value='Jan 2023', verification_state='Verified'),
        end_date=VerifiedField(value='Dec 2023', verification_state='Verified'),
        responsibilities=[
            VerifiedField(value='Developed scalable web services using Java and Spring Boot.', verification_state='Verified'),
            VerifiedField(value='Optimized PostgreSQL queries improving performance by 20%.', verification_state='Verified')
        ]
    )],
    education=[VerifiedEducation(
        degree=VerifiedField(value='B.S. Computer Science', verification_state='Verified'),
        institution=VerifiedField(value='University of Tech', verification_state='Verified'),
        graduation_year=VerifiedField(value='2024', verification_state='Verified')
    )],
    overall_confidence=100,
    section_confidence={}
)

start = time.perf_counter()
for _ in range(100):
    collect_skills_evidence(resume, jd, True)
    collect_experience_evidence(resume, jd)
end = time.perf_counter()

print(f"Latency per request: {((end - start) / 100) * 1000:.2f} ms")
