from fastapi import APIRouter
from .inference import infer
from app.schemas.CaseRequest import CaseRequest, to_internal_cases
from app.schemas.InferenceResponse import InferenceResponse, Prediction

router = APIRouter()

@router.post("/inference")
def run_inference(case_request: CaseRequest):
    cases = to_internal_cases(case_request)
    case_ids, pairs, predictions = infer(cases)
    
    response_predictions = []
    for i, ((_, prior), pred) in enumerate(zip(pairs, predictions)):
        response_predictions.append(Prediction(
            case_id=case_ids[i], 
            study_id=prior.study_id,
            predicted_is_relevant=bool(pred)
        ))

    return InferenceResponse(predictions=response_predictions)