from sentence_transformers import SentenceTransformer
import numpy as np
import joblib
from pathlib import Path

_MODELS_DIR = Path(__file__).parent.parent.parent / "models"

model = SentenceTransformer(str(_MODELS_DIR / "sbert_finetuned/final"))
def embed(texts):
    return model.encode(texts, normalize_embeddings=True)

classifier = joblib.load(_MODELS_DIR / "study_classifier.joblib")
_THRESHOLD = 0.3939 # Determined from validation set

def build_embeddings(pairs):
    study_to_embedding = {}
    for current, prior in pairs:
        if current.study_id not in study_to_embedding:
            study_to_embedding[current.study_id] = embed(current.description)
        if prior.study_id not in study_to_embedding:
            study_to_embedding[prior.study_id] = embed(prior.description)
    return study_to_embedding

body_parts = [
    'heart',
    'breast',
    'chest',
    'knee',
    'spine',
    'abdomen',
    'thyroid',
    'shoulder',
    'brain',
    'wrist',
    'hip',
    'face',
    'head',
    'ankle'
]
body_parts_mapping = {}
for i, part in enumerate(body_parts):
    body_parts_mapping[part] = i

laterality = [
    'left',
    'right',
    'bilateral',
    'frontal',
    'full',
    'lumbar',
    'cervical'
]
lat_mapping = {}
for i, lat in enumerate(laterality):
    lat_mapping[lat] = i

def multi_hot(study_text, mapping):
    vec = np.zeros(len(mapping))
    
    for key, val in mapping.items():
        if key in study_text.lower():
            vec[val] = 1
    return vec

def build_features(pairs, embed_mapping):
    X = []
    for current, prior in pairs:
        current_emb = embed_mapping[current.study_id]
        prior_emb = embed_mapping[prior.study_id]

        sim = prior_emb @ current_emb
        time_diff = current.days_between(prior)
        exp_decay = np.exp(-time_diff / 90)

        bp_curr = multi_hot(current.description, body_parts_mapping)
        bp_prior = multi_hot(prior.description, body_parts_mapping)

        same_body_part = int(np.dot(bp_curr, bp_prior) == np.sum(bp_curr) == np.sum(bp_prior))
        overlap = np.dot(bp_curr, bp_prior) / max(np.sum(bp_curr), 1)
        has_overlap = int(np.dot(bp_curr, bp_prior) > 0)

        lat_curr = multi_hot(current.description, lat_mapping)
        lat_prior = multi_hot(prior.description, lat_mapping)

        same_laterality = int(np.dot(lat_curr, lat_prior) == np.sum(lat_curr) == np.sum(lat_prior))
        lat_overlap = np.dot(lat_curr, lat_prior) / max(np.sum(lat_curr), 1)
        has_lat_overlap = int(np.dot(lat_curr, lat_prior) > 0)

        features = np.concatenate([
            [sim, time_diff, exp_decay],
            [same_body_part, overlap, has_overlap],
            [same_laterality, lat_overlap, has_lat_overlap]
        ])
        X.append(features)
    return np.array(X)

def infer(cases):
    pairs = []
    case_ids = []
    for case in cases:
        current = case.current_study
        for prior in case.prior_studies:
            pairs.append((current, prior))
            case_ids.append(case.case_id)
    study_to_embedding = build_embeddings(pairs)

    X = build_features(pairs, study_to_embedding)
    # Load saved model and infer
    probs = classifier.predict_proba(X)[:, 1]
    predictions = (probs > _THRESHOLD).astype(int)
    return case_ids, pairs, predictions
