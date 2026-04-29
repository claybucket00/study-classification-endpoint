import json
from datetime import datetime
import re

class CaseDataset:
    def __init__(self, path):
        self.case_data, self.study_to_truth = process_data(path)

    def __len__(self):
        return len(self.case_data)
    
    def __getitem__(self, idx):
        case = self.case_data[idx]
        priors_with_labels = [
            (prior.description, self.study_to_truth[(case.case_id, prior.study_id)])
            for prior in case.prior_studies
        ]
        return case.current_study.description, priors_with_labels

    @staticmethod
    def collate_fn(batch):
        """Training collate: candidate pool contains only positive priors (in-batch negatives)."""
        currents = []
        priors = []
        pos_indices = []

        for current, priors_with_labels in batch:
            currents.append(current)
            indices = []
            for p, is_relevant in priors_with_labels:
                if is_relevant:
                    indices.append(len(priors))
                    priors.append(p)
            pos_indices.append(indices)

        return currents, priors, pos_indices

    @staticmethod
    def eval_collate_fn(batch):
        """Eval collate: candidate pool contains all priors (positive and negative)."""
        currents = []
        priors = []
        pos_indices = []

        for current, priors_with_labels in batch:
            currents.append(current)
            indices = []
            for p, is_relevant in priors_with_labels:
                if is_relevant:
                    indices.append(len(priors))
                priors.append(p)
            pos_indices.append(indices)

        return currents, priors, pos_indices

class Study:
    def __init__(self, study_id, description, date):
        self.study_id = study_id
        self.description = normalize_text(description)
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
    
    def days_between(self, other):
        return abs((self.date - other.date).days)

class Case:
    def __init__(self, case_id, current_study, prior_studies):
        self.case_id = case_id
        self.current_study = current_study
        self.prior_studies = prior_studies

    def __str__(self):
        return f"Case ID: {self.case_id}, Current Study: {self.current_study.study_id}, Prior Studies: {[(study.study_id, study.description, study.date) for study in self.prior_studies]}"

ABBREVIATIONS = {
    "XR": "Xray",
    "CT": "Computed Tomography Scan",
    "MR": "Magnetic Resonance Imaging",
    "MRI": "Magnetic Resonance Imaging", 
    "NM": "Nuclear Medicine",
    "PET": "Positron Emission Tomography",
    "ECHO": "Echocardiogram",
    "LUM TTE": "heart Transthoracic Echocardiogram",
    "VAS": "Visual Analogue Scale",
    "ULTRASOUND": "Ultrasound",
    "US": "Ultrasound",
    "EEG": "Electroencephalogram",
    "TOMO": "Tomosynthesis",
    "CAD": "Computer-Aided Detection",
    "LT": "left",
    "RT": "right",
    "3V": "3 views",
    "2V": "2 views",
    "1V": "1 view",
    "MYO": "Myocardial Perfusion Imaging",
    "MAM": "Mammography",
    "MAMMO": "Mammography",
    "DIGITAL SCREENER W CAD": "mammography",
    "ABD": "abdomen",
    "BI": "bilateral",
    "PEL": "pelvis",
    "PELVIC": "pelvis",
    "ABDOMINAL": "abdomen",
    "SKULLTHIGH": "skull to thigh"
}

def normalize_text(text: str) -> str:
    for k, v in ABBREVIATIONS.items():
        text = re.sub(rf"\b{k}\b", v, text, flags=re.IGNORECASE)
    return text


def process_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    truths = data.get('truth', [])

    study_to_truth = {}

    for truth in truths:
        study_id = truth.get('study_id')
        current_id = truth.get('case_id')
        if study_id:
            study_to_truth[(current_id, study_id)] = truth['is_relevant_to_current']
    
    cases = data.get('cases', [])

    case_data = []

    for case in cases:
        case_id = case.get('case_id')
        current_study_data = case.get('current_study', {})
        current_study = Study(
            study_id=current_study_data.get('study_id'),
            description=current_study_data.get('study_description'),
            date=current_study_data.get('study_date')
        )
        priors = case.get('prior_studies', [])
        prior_studies = []

        for prior in priors:
            study_id = prior.get('study_id')
            study_description = prior.get('study_description')
            study_date = prior.get('study_date')
            prior_studies.append(Study(study_id, study_description, study_date))
        
        case_data.append(Case(case_id, current_study, prior_studies))
    
    return case_data, study_to_truth