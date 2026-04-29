from pydantic import BaseModel
from typing import List
from app.dataset.CaseData import Study as InternalStudy, Case as InternalCase

class Study(BaseModel):
    study_id: str
    study_description: str
    study_date: str

class Case(BaseModel):
    case_id: str
    patient_id: str
    patient_name: str
    current_study: Study
    prior_studies: List[Study]

class CaseRequest(BaseModel):
    challenge_id: str
    schema_version: int
    generated_at: str
    cases: List[Case]

def to_internal_cases(case_request: CaseRequest) -> List[InternalCase]:
    cases = []
    for case in case_request.cases:
        current = InternalStudy(
            study_id=case.current_study.study_id,
            description=case.current_study.study_description,
            date=case.current_study.study_date,
        )
        priors = [
            InternalStudy(
                study_id=s.study_id,
                description=s.study_description,
                date=s.study_date,
            )
            for s in case.prior_studies
        ]
        cases.append(InternalCase(case.case_id, current, priors))
    return cases
