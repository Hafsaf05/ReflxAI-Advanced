"""
metrics.py — ReflxAI-Advanced
Code Quality Metrics Calculator: computes complexity, coverage, and ratings.
"""

import re
from typing import Dict, Tuple


def calculate_complexity(code: str) -> Dict[str, float]:
    """
    Calculate cyclomatic and cognitive complexity metrics for the code.

    Args:
        code: The source code.

    Returns:
        A dict with complexity metrics.
    """
    lines = code.split("\n")
    
    cyclomatic = 1
    cognitive = 0
    
    for line in lines:
        stripped = line.strip()
        if any(keyword in stripped for keyword in ["if ", "elif ", "for ", "while ", "except", "and ", "or "]):
            cyclomatic += 1
            cognitive += 1
        if "def " in stripped or "class " in stripped:
            if cognitive > 0:
                cognitive += 1
    
    return {
        "cyclomatic_complexity": cyclomatic,
        "cognitive_complexity": max(cognitive, 1),
        "lines_of_code": len([l for l in lines if l.strip() and not l.strip().startswith("#")])
    }


def estimate_test_coverage(code: str, tests: str) -> float:
    """
    Estimate test coverage based on functions/classes defined vs tested.

    Args:
        code: The source code.
        tests: The test code.

    Returns:
        Estimated coverage percentage (0-100).
    """
    # Count functions in main code
    main_functions = len(re.findall(r"^\s*def\s+\w+", code, re.MULTILINE))
    main_classes = len(re.findall(r"^\s*class\s+\w+", code, re.MULTILINE))
    main_items = max(main_functions + main_classes, 1)
    
    # Count test functions
    test_functions = len(re.findall(r"def\s+test_\w+", tests))
    
    coverage = min(100, (test_functions / max(main_items * 1.5, 1)) * 100)
    return coverage


def calculate_security_score(audit_result: str) -> float:
    """
    Calculate security score based on audit results.

    Args:
        audit_result: The security audit output.

    Returns:
        Security score (0-100).
    """
    if audit_result.strip().upper() == "SECURE":
        return 100.0
    
    high_issues = len(re.findall(r"HIGH|CRITICAL", audit_result))
    medium_issues = len(re.findall(r"MEDIUM", audit_result))
    low_issues = len(re.findall(r"LOW", audit_result))
    
    score = 100 - (high_issues * 25 + medium_issues * 10 + low_issues * 5)
    return max(0, score)


def calculate_performance_score(performance_analysis: str) -> float:
    """
    Calculate performance score based on analysis.

    Args:
        performance_analysis: The performance analysis output.

    Returns:
        Performance score (0-100).
    """
    if performance_analysis.strip().upper() == "OPTIMIZED":
        return 100.0
    
    # Count optimization opportunities
    optimizations = len(re.findall(r"^\d+\.", performance_analysis, re.MULTILINE))
    score = max(60, 100 - (optimizations * 8))
    
    return score


def generate_quality_report(
    code: str,
    tests: str,
    security_audit: str,
    performance_analysis: str,
    approval_status: bool
) -> Dict[str, any]:
    """
    Generate a comprehensive quality report for the code.

    Args:
        code: The generated code.
        tests: The generated tests.
        security_audit: The security audit results.
        performance_analysis: The performance analysis results.
        approval_status: Whether code passed critic review.

    Returns:
        A comprehensive quality report dictionary.
    """
    complexity = calculate_complexity(code)
    coverage = estimate_test_coverage(code, tests)
    security = calculate_security_score(security_audit)
    performance = calculate_performance_score(performance_analysis)
    
    overall_score = (security + performance + coverage + (100 if approval_status else 50)) / 4
    
    return {
        "overall_score": round(overall_score, 1),
        "complexity": complexity,
        "test_coverage": round(coverage, 1),
        "security_score": round(security, 1),
        "performance_score": round(performance, 1),
        "approval_status": "✅ APPROVED" if approval_status else "⚠️ NEEDS REVIEW",
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }
