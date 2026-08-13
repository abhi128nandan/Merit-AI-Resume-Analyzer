
from app.matching.similarity import evaluate_similarity
from app.schemas.match_report import MatchLevel


def test_sql_vs_nosql():
    # Should not match
    level = evaluate_similarity("SQL", "NoSQL")
    assert level == MatchLevel.MISSING


def test_c_vs_cpp():
    # Should not match
    level = evaluate_similarity("C", "C++")
    assert level == MatchLevel.MISSING


def test_cpp_vs_c():
    # Should not match
    level = evaluate_similarity("C++", "C")
    assert level == MatchLevel.MISSING


def test_html_vs_java():
    # Should not match
    level = evaluate_similarity("HTML", "Java")
    assert level == MatchLevel.MISSING


def test_react_native_vs_reactjs():
    # Should be partial at best, definitely not EXACT
    level = evaluate_similarity("React Native", "React.js")
    assert level in [MatchLevel.PARTIAL, MatchLevel.WEAK, MatchLevel.MISSING]
