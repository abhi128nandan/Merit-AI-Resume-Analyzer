import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from app.main import app
from app.services import analysis_service
from tests.fixtures.golden_data import PAIRS

client = TestClient(app)

@pytest.fixture
def mock_executor():
    with ThreadPoolExecutor(max_workers=4) as executor:
        with patch.object(analysis_service, '_executor', executor):
            yield executor

@pytest.fixture
def mock_parsers():
    with patch('app.services.analysis_service.process_resume') as mock_resume, \
         patch('app.services.analysis_service.process_job_description') as mock_jd:
        yield mock_resume, mock_jd

def test_analyze_endpoint(mock_executor, mock_parsers):
    mock_resume, mock_jd = mock_parsers
    
    # Use one of our fixtures
    resume_ext, resume_raw, jd_ext, jd_raw = PAIRS["fresher"]
    from app.parsers.resume.verifier import verify_resume_data
    from app.parsers.job_description.verifier import verify_jd_data
    
    mock_resume.return_value = verify_resume_data(resume_ext, resume_raw)
    mock_jd.return_value = verify_jd_data(jd_ext, jd_raw)
    
    response = client.post(
        "/api/v1/analyze/",
        files={
            "resume": ("resume.pdf", b"%PDF-" + b" dummy PDF content" * 10, "application/pdf"),
            "jd": ("jd.txt", b"dummy JD content" * 10, "text/plain")
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert "parsed_resume" in data
    assert "parsed_jd" in data
    assert "match_report" in data
    assert "feedback" in data
