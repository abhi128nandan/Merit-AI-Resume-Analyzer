from typing import List, Optional, Set
from dataclasses import dataclass
from enum import IntEnum

from app.matching.similarity import evaluate_similarity, extract_months_of_experience
from app.schemas.match_report import EvidenceResult, MatchLevel
from app.schemas.parsed_jd import VerifiedJD
from app.schemas.parsed_resume import VerifiedParsedResume
from app.matching.normalizer import normalize_term
from app.matching.providers import concept_provider
import re

class EvidencePriority(IntEnum):
    VERIFIED = 50
    ALIAS = 40
    TECHNOLOGY = 30
    COURSEWORK = 20
    CONTEXT = 10
    MISSING = 0

@dataclass
class InternalEvidenceResult:
    requirement: str
    match_level: MatchLevel
    match_type: str 
    confidence: str 
    evidence_found: Optional[str]
    priority: EvidencePriority
    source: str

def map_to_public(internal: InternalEvidenceResult) -> EvidenceResult:
    if internal.evidence_found:
        if internal.match_level not in [MatchLevel.MISSING, MatchLevel.HALLUCINATED]:
            formatted = f"{internal.evidence_found} [Type: {internal.match_type}, Conf: {internal.confidence}]"
        else:
            formatted = internal.evidence_found
    else:
        formatted = None
        
    return EvidenceResult(
        requirement=internal.requirement,
        match_level=internal.match_level,
        evidence_found=formatted
    )

def check_text_for_requirement(
    text: str, source: str, req_value: str, norm_req: str, req_aliases: Set[str]
) -> List[InternalEvidenceResult]:
    results = []
    norm_text = normalize_term(text)
    
    # 1. Exact Match / Alias Match
    if norm_text in req_aliases:
        priority = EvidencePriority.VERIFIED if norm_text == norm_req else EvidencePriority.ALIAS
        match_type = "Verified" if norm_text == norm_req else "Alias"
        results.append(InternalEvidenceResult(
            req_value, MatchLevel.EXACT, match_type, "High", text, priority, source
        ))
        return results # Highest possible, no need to keep checking this text

    for alias in req_aliases:
        boundary_start = r'(?:^|[^\w+#])'
        boundary_end = r'(?:$|[^\w+#])'
        pattern = boundary_start + re.escape(alias) + boundary_end
        if re.search(pattern, norm_text):
            priority = EvidencePriority.VERIFIED if alias == norm_req else EvidencePriority.ALIAS
            match_type = "Verified" if alias == norm_req else "Alias"
            results.append(InternalEvidenceResult(
                req_value, MatchLevel.EXACT, match_type, "High", text, priority, source
            ))
            return results

    # 2. Technology Evidence
    techs = concept_provider.get_technologies_for_concept(norm_req)
    for tech in techs:
        boundary_start = r'(?:^|[^\w+#])'
        boundary_end = r'(?:$|[^\w+#])'
        pattern = boundary_start + re.escape(tech) + boundary_end
        if re.search(pattern, norm_text):
            results.append(InternalEvidenceResult(
                req_value, MatchLevel.SEMANTIC, "Technology", "Medium", text, EvidencePriority.TECHNOLOGY, source
            ))
            break # Once we found one tech, we can stop for this text

    # 3. Contextual Fallback
    if not results:
        level = evaluate_similarity(text, req_value)
        if level in [MatchLevel.EXACT, MatchLevel.SEMANTIC, MatchLevel.PARTIAL]:
            results.append(InternalEvidenceResult(
                req_value, level, "Context", "Low", text, EvidencePriority.CONTEXT, source
            ))
            
    return results

def resolve_evidence_conflicts(results: List[InternalEvidenceResult]) -> InternalEvidenceResult:
    """
    Deterministic conflict resolution:
    1. Highest Priority (Verified > Alias > Technology > Coursework > Context > Missing)
    2. Highest Confidence (High > Medium > Low) mapped by Priority mostly.
    3. Shortest Evidence (More concise is usually a better targeted extraction)
    """
    if not results:
        return None
        
    def sort_key(res: InternalEvidenceResult):
        evidence_len = len(res.evidence_found) if res.evidence_found else 9999
        return (res.priority, -evidence_len)
        
    results.sort(key=sort_key, reverse=True)
    return results[0]

def collect_skills_evidence(
    resume: VerifiedParsedResume, jd: VerifiedJD, is_required: bool
) -> List[EvidenceResult]:
    evidence_list = []
    jd_skills = jd.required_skills if is_required else jd.preferred_skills

    for req in jd_skills:
        if req.verification_state == "Hallucinated":
            continue

        norm_req = normalize_term(req.value)
        req_aliases = concept_provider.get_aliases(norm_req)
        
        all_results: List[InternalEvidenceResult] = []
        
        # Check Skills Section
        for s in resume.skills:
            if s.verification_state != "Hallucinated":
                all_results.extend(check_text_for_requirement(s.value, "Skills", req.value, norm_req, req_aliases))
                
        # Check Experience Section
        for exp in resume.experience:
            if exp.title.verification_state != "Hallucinated":
                all_results.extend(check_text_for_requirement(exp.title.value, "Experience Title", req.value, norm_req, req_aliases))
            for resp in exp.responsibilities:
                if resp.verification_state != "Hallucinated":
                    all_results.extend(check_text_for_requirement(resp.value, "Experience Details", req.value, norm_req, req_aliases))
                    
        # Check Summary
        if resume.summary and resume.summary.verification_state != "Hallucinated":
            all_results.extend(check_text_for_requirement(resume.summary.value, "Summary", req.value, norm_req, req_aliases))

        # Check Coursework
        # A coursework match specifically looks at degree texts
        for edu in resume.education:
            if edu.degree.verification_state != "Hallucinated":
                # Check if the degree text contains a mapped coursework string for the required concept
                concepts = concept_provider.get_concepts_for_coursework(edu.degree.value)
                if norm_req in concepts or any(a in concepts for a in req_aliases):
                    all_results.append(InternalEvidenceResult(
                        req.value, MatchLevel.SEMANTIC, "Coursework", "Medium", f"Course: {edu.degree.value}", EvidencePriority.COURSEWORK, "Education"
                    ))

        if not all_results:
            best = InternalEvidenceResult(
                req.value, MatchLevel.MISSING, "Missing", "Low", None, EvidencePriority.MISSING, "None"
            )
        else:
            best = resolve_evidence_conflicts(all_results)
            
        evidence_list.append(map_to_public(best))

    return evidence_list


def collect_experience_evidence(
    resume: VerifiedParsedResume, jd: VerifiedJD
) -> List[EvidenceResult]:
    if jd.experience_requirements.verification_state == "Hallucinated":
        return []

    req_months = extract_months_of_experience(jd.experience_requirements.value)
    candidate_months = 0
    evidence_texts = []

    for exp in resume.experience:
        if exp.title.verification_state != "Hallucinated":
            start_month = extract_months_of_experience(exp.start_date.value, is_date=True)
            end_month = extract_months_of_experience(exp.end_date.value, is_date=True, is_end=True)
            
            if start_month > 0 and end_month >= start_month:
                months_spent = end_month - start_month
            else:
                months_spent = 0
            
            # Minimum 1 month if same month
            if start_month > 0 and start_month == end_month:
                months_spent = 1
                
            if months_spent > 0 and months_spent < (50 * 12):
                candidate_months += months_spent
                years_display = round(months_spent / 12, 1)
                evidence_texts.append(f"{exp.title.value} ({years_display} yrs)")

    match_level = MatchLevel.MISSING
    if candidate_months >= req_months:
        match_level = MatchLevel.EXACT
    elif candidate_months >= req_months - 12 and req_months > 12:
        match_level = MatchLevel.PARTIAL
    elif candidate_months > 0:
        match_level = MatchLevel.WEAK

    best = InternalEvidenceResult(
        requirement=jd.experience_requirements.value,
        match_level=match_level,
        match_type="Experience Calculation",
        confidence="High" if candidate_months > 0 else "Low",
        evidence_found=", ".join(evidence_texts) if evidence_texts else None,
        priority=EvidencePriority.VERIFIED if match_level == MatchLevel.EXACT else EvidencePriority.MISSING,
        source="Experience"
    )
    
    return [map_to_public(best)]


def collect_education_evidence(
    resume: VerifiedParsedResume, jd: VerifiedJD
) -> List[EvidenceResult]:
    if jd.education_requirements.verification_state == "Hallucinated":
        return []

    best = InternalEvidenceResult(
        requirement=jd.education_requirements.value,
        match_level=MatchLevel.MISSING,
        match_type="None",
        confidence="Low",
        evidence_found=None,
        priority=EvidencePriority.MISSING,
        source="None"
    )

    for edu in resume.education:
        if edu.degree.verification_state != "Hallucinated":
            level = evaluate_similarity(edu.degree.value, jd.education_requirements.value)
            if level in [MatchLevel.EXACT, MatchLevel.SEMANTIC]:
                best = InternalEvidenceResult(jd.education_requirements.value, level, "Semantic", "High", edu.degree.value, EvidencePriority.CONTEXT, "Education")
                break
            elif level == MatchLevel.PARTIAL and best.match_level == MatchLevel.MISSING:
                best = InternalEvidenceResult(jd.education_requirements.value, level, "Partial", "Medium", edu.degree.value, EvidencePriority.CONTEXT, "Education")

    return [map_to_public(best)]


def collect_title_evidence(
    resume: VerifiedParsedResume, jd: VerifiedJD
) -> List[EvidenceResult]:
    if jd.job_title.verification_state == "Hallucinated":
        return []

    best = InternalEvidenceResult(
        requirement=jd.job_title.value,
        match_level=MatchLevel.MISSING,
        match_type="None",
        confidence="Low",
        evidence_found=None,
        priority=EvidencePriority.MISSING,
        source="None"
    )

    for exp in resume.experience:
        if exp.title.verification_state != "Hallucinated":
            level = evaluate_similarity(exp.title.value, jd.job_title.value)
            if level in [MatchLevel.EXACT, MatchLevel.SEMANTIC]:
                best = InternalEvidenceResult(jd.job_title.value, level, "Semantic", "High", exp.title.value, EvidencePriority.CONTEXT, "Experience")
                break
            elif level == MatchLevel.PARTIAL and best.match_level == MatchLevel.MISSING:
                best = InternalEvidenceResult(jd.job_title.value, level, "Partial", "Medium", exp.title.value, EvidencePriority.CONTEXT, "Experience")

    return [map_to_public(best)]
