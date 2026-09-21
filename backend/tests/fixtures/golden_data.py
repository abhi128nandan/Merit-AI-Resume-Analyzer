import json
from pathlib import Path
from app.schemas.parsed_resume import (
    LLMExtractedResume, LLMExtractedContact, LLMExtractedExperience, LLMExtractedEducation
)
from app.schemas.parsed_jd import LLMExtractedJD

# 1. Fresher CS Grad
fresher_resume = LLMExtractedResume(
    contact=LLMExtractedContact(email="fresher@example.com", phone="+91 98765 43210"),
    summary="Recent Computer Science graduate",
    skills=["Python", "Java", "C++", "SQL"],
    experience=[
        LLMExtractedExperience(title="Software Intern", company="Tech Corp", start_date="Jan 2023", end_date="Jun 2023", responsibilities=["Built features"])
    ],
    education=[
        LLMExtractedEducation(degree="B.Tech in Computer Science", institution="Indian Institute of Technology", graduation_year="2023")
    ]
)
fresher_jd = LLMExtractedJD(
    job_title="Junior Software Engineer",
    company="Startup Inc",
    required_skills=["Python", "SQL"],
    experience_requirements="0-1 years",
    education_requirements="Bachelor's degree in Computer Science"
)
fresher_resume_raw = "fresher@example.com +91 98765 43210 Recent Computer Science graduate Python Java C++ SQL Software Intern Tech Corp Jan 2023 Jun 2023 Built features B.Tech in Computer Science Indian Institute of Technology 2023"
fresher_jd_raw = "Junior Software Engineer Startup Inc Python SQL 0-1 years Bachelor's degree in Computer Science"


# 2. Senior Engineer
senior_resume = LLMExtractedResume(
    contact=LLMExtractedContact(email="senior@example.com"),
    summary="Experienced backend engineer",
    skills=["Go", "Python", "Kubernetes", "AWS", "System Design"],
    experience=[
        LLMExtractedExperience(title="Senior Backend Engineer", company="Big Tech", start_date="Jan 2018", end_date="Present", responsibilities=["Led team"]),
        LLMExtractedExperience(title="Software Engineer", company="Old Tech", start_date="Jan 2015", end_date="Dec 2017", responsibilities=["Developed APIs"])
    ],
    education=[
        LLMExtractedEducation(degree="B.S. Computer Science", institution="State Uni", graduation_year="2015")
    ]
)
senior_jd = LLMExtractedJD(
    job_title="Senior Backend Engineer",
    required_skills=["Go", "AWS", "System Design", "Kubernetes"],
    experience_requirements="5+ years",
    education_requirements="Bachelor's degree"
)
senior_resume_raw = "senior@example.com Experienced backend engineer Go Python Kubernetes AWS System Design Senior Backend Engineer Big Tech Jan 2018 Present Led team Software Engineer Old Tech Jan 2015 Dec 2017 Developed APIs B.S. Computer Science State Uni 2015"
senior_jd_raw = "Senior Backend Engineer Go AWS System Design Kubernetes 5+ years Bachelor's degree"

# 3. Career Changer
career_changer_resume = LLMExtractedResume(
    skills=["JavaScript", "React", "Customer Service"],
    experience=[
        LLMExtractedExperience(title="Frontend Developer", company="Freelance", start_date="Jan 2022", end_date="Present", responsibilities=["Web dev"]),
        LLMExtractedExperience(title="Store Manager", company="Retail", start_date="Jan 2015", end_date="Dec 2021", responsibilities=["Managed people"])
    ],
    education=[
        LLMExtractedEducation(degree="B.A. English", institution="Arts Uni", graduation_year="2014")
    ]
)
career_changer_jd = LLMExtractedJD(
    job_title="Junior Frontend Developer",
    required_skills=["JavaScript", "React", "CSS"],
    experience_requirements="1 year",
    education_requirements="Not Specified"
)
career_changer_resume_raw = "changer@example.com Career changer JavaScript React Customer Service Frontend Developer Freelance Jan 2022 Present Web dev Store Manager Retail Jan 2015 Dec 2021 Managed people B.A. English Arts Uni 2014"
career_changer_jd_raw = "Junior Frontend Developer JavaScript React CSS 1 year Not Specified"

# 4. JD that states no experience/education
no_reqs_resume = LLMExtractedResume(
    skills=["HTML", "CSS"],
    experience=[],
    education=[]
)
no_reqs_jd = LLMExtractedJD(
    job_title="Trainee",
    required_skills=["HTML", "CSS"],
    experience_requirements="Not Specified",
    education_requirements="Not Specified"
)
no_reqs_resume_raw = "noreqs@example.com Worker HTML CSS"
no_reqs_jd_raw = "Trainee HTML CSS Not Specified Not Specified"

# 5. JD with "0-1 years" and "Bachelor's degree in Computer Science"
entry_resume = LLMExtractedResume(
    skills=["Java"],
    experience=[
        LLMExtractedExperience(title="Intern", company="Co", start_date="Jan 2022", end_date="May 2022", responsibilities=["Dev"])
    ],
    education=[
        LLMExtractedEducation(degree="BCA", institution="College", graduation_year="2022")
    ]
)
entry_jd = LLMExtractedJD(
    job_title="Entry Level Dev",
    required_skills=["Java"],
    experience_requirements="0-1 years",
    education_requirements="Bachelor's degree in Computer Science"
)
entry_resume_raw = "entry@example.com Student Java Intern Co Jan 2022 May 2022 Dev BCA College 2022"
entry_jd_raw = "Entry Level Dev Java 0-1 years Bachelor's degree in Computer Science"

PAIRS = {
    "fresher": (fresher_resume, fresher_resume_raw, fresher_jd, fresher_jd_raw),
    "senior": (senior_resume, senior_resume_raw, senior_jd, senior_jd_raw),
    "career_changer": (career_changer_resume, career_changer_resume_raw, career_changer_jd, career_changer_jd_raw),
    "no_reqs": (no_reqs_resume, no_reqs_resume_raw, no_reqs_jd, no_reqs_jd_raw),
    "entry": (entry_resume, entry_resume_raw, entry_jd, entry_jd_raw)
}
