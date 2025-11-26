#!/usr/bin/env python3
"""Test PQA Dashboard API Endpoints"""
import requests
import sys

API_BASE = "http://localhost:8000"

endpoints = [
    "/api/pqa/dashboard/summary",
    "/api/pqa/dashboard/score-distribution",
    "/api/pqa/dashboard/diff-distribution",
    "/api/pqa/dashboard/xpath-patterns?limit=10",
    "/api/pqa/dashboard/phase-breakdown",
]

print("=" * 60)
print("PQA DASHBOARD ENDPOINT TEST")
print("=" * 60)
print(f"\nTesting against: {API_BASE}\n")

results = []
for endpoint in endpoints:
    url = f"{API_BASE}{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        status = "✓ OK" if response.status_code == 200 else f"✗ {response.status_code}"
        results.append({
            'endpoint': endpoint,
            'status': response.status_code,
            'ok': response.status_code == 200,
            'error': None if response.status_code == 200 else response.text[:100]
        })
        print(f"{status:8} | {endpoint}")
        if response.status_code != 200:
            print(f"         | Error: {response.text[:100]}")
    except requests.exceptions.ConnectionError:
        results.append({
            'endpoint': endpoint,
            'status': 0,
            'ok': False,
            'error': 'Connection refused - is the backend running?'
        })
        print(f"✗ FAIL  | {endpoint}")
        print(f"         | Error: Connection refused")
    except Exception as e:
        results.append({
            'endpoint': endpoint,
            'status': 0,
            'ok': False,
            'error': str(e)
        })
        print(f"✗ FAIL  | {endpoint}")
        print(f"         | Error: {e}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
passed = sum(1 for r in results if r['ok'])
total = len(results)
print(f"Passed: {passed}/{total}")
print(f"Failed: {total - passed}/{total}")

if passed < total:
    print("\n⚠️  Some endpoints are not responding!")
    print("Make sure the backend API server is running:")
    print("  cd backend && uvicorn main:app --reload")
    sys.exit(1)
else:
    print("\n✅ All endpoints are working!")
    sys.exit(0)
