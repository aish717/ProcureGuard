from tools import calculate_percentage_difference, verify_numeric_findings

assert calculate_percentage_difference(387000, 327000) == 18.35
r = verify_numeric_findings(387000, 327000, 5)
assert r["threshold_exceeded"] is True
print("Smoke test passed.")
