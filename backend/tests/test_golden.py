import json
from pathlib import Path
from app.parsers.resume.verifier import verify_resume_data
from app.parsers.job_description.verifier import verify_jd_data
from app.matching.engine import evaluate_match
from app.matching.policies import DEFAULT_POLICY
from tests.fixtures.golden_data import PAIRS

GOLDEN_DIR = Path(__file__).parent / "golden"

def test_golden_snapshots():
    GOLDEN_DIR.mkdir(exist_ok=True, parents=True)
    
    for name, (resume_ext, resume_raw, jd_ext, jd_raw) in PAIRS.items():
        v_resume = verify_resume_data(resume_ext, resume_raw)
        v_jd = verify_jd_data(jd_ext, jd_raw)
        report = evaluate_match(v_resume, v_jd, DEFAULT_POLICY)
        
        report_dict = json.loads(report.model_dump_json())
        golden_file = GOLDEN_DIR / f"{name}.json"
        
        if not golden_file.exists():
            with open(golden_file, "w") as f:
                json.dump(report_dict, f, indent=2)
        else:
            with open(golden_file, "r") as f:
                golden_dict = json.load(f)
            assert report_dict == golden_dict, f"Golden snapshot mismatch for {name}"
