import urllib.request
import urllib.parse
import os
import json
import uuid
import pytest

def test_e2e_analyze_flow():
    """End-to-end integration test for full ATS resume analysis API."""
    url = "http://localhost:8000/api/v1/analyze"

    resume_content = "John Doe\nSoftware Engineer\nPython, FastAPI, PostgreSQL"
    jd_content = "Looking for a Senior Software Engineer with strong Python and FastAPI experience."

    with open("temp_resume.txt", "w") as f:
        f.write(resume_content)

    with open("temp_jd.txt", "w") as f:
        f.write(jd_content)

    try:
        boundary = uuid.uuid4().hex
        body = bytearray()
        
        # Resume part
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="resume"; filename="temp_resume.txt"\r\n'.encode())
        body.extend(f"Content-Type: text/plain\r\n\r\n".encode())
        body.extend(open("temp_resume.txt", "rb").read())
        body.extend(b"\r\n")

        # Job description part
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="jd"; filename="temp_jd.txt"\r\n'.encode())
        body.extend(f"Content-Type: text/plain\r\n\r\n".encode())
        body.extend(open("temp_jd.txt", "rb").read())
        body.extend(b"\r\n")
        
        body.extend(f"--{boundary}--\r\n".encode())
        
        req = urllib.request.Request(url, data=body)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        
        try:
            response = urllib.request.urlopen(req)
            assert response.getcode() == 200
            data = json.loads(response.read())
            assert "overall_score" in data or "message" in data or "status" in data
        except urllib.error.URLError:
            pytest.skip("Backend server not running on localhost:8000")
    finally:
        if os.path.exists("temp_resume.txt"):
            os.remove("temp_resume.txt")
        if os.path.exists("temp_jd.txt"):
            os.remove("temp_jd.txt")
