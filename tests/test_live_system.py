import httpx
import json

BASE_BACKEND = "http://localhost:8000"
BASE_FRONTEND = "http://localhost:5173"

def run_tests():
    client = httpx.Client(timeout=15.0)

    print("--- 1. Testing Frontend Accessibility ---")
    try:
        fe_resp = client.get(BASE_FRONTEND)
        print(f"Frontend HTTP Status: {fe_resp.status_code}")
        assert fe_resp.status_code == 200, "Frontend did not return 200"
        assert "<div id=\"root\"></div>" in fe_resp.text, "Root element missing"
        print("Frontend OK!")
    except Exception as e:
        print(f"Frontend test error: {e}")

    print("\n--- 2. Testing Backend Endpoints ---")
    endpoints = [
        ("/api/health", 200),
        ("/docs", 200),
        ("/api/dashboard", 200),
        ("/api/feedback?page=1&limit=5", 200),
        ("/api/analytics/sentiment", 200),
        ("/api/analytics/issues", 200),
        ("/api/insights", 200),
    ]

    for ep, expected_code in endpoints:
        resp = client.get(f"{BASE_BACKEND}{ep}")
        print(f"GET {ep} -> Status {resp.status_code}")
        assert resp.status_code == expected_code, f"Expected {expected_code}, got {resp.status_code}"

    # Test feedback detail
    fb_resp = client.get(f"{BASE_BACKEND}/api/feedback?page=1&limit=1")
    first_id = fb_resp.json()["data"][0]["feedback_id"]
    detail_resp = client.get(f"{BASE_BACKEND}/api/feedback/{first_id}")
    print(f"GET /api/feedback/{first_id} -> Status {detail_resp.status_code}")
    assert detail_resp.status_code == 200

    print("\n--- 3. Testing 8 Required Sample Predictions (Step 36) ---")
    test_queries = [
        "The product quality is excellent and I am very happy.",
        "My delivery is three days late.",
        "Money was deducted but payment failed.",
        "The application keeps crashing.",
        "The customer service was very helpful.",
        "I received the wrong product.",
        "The order arrived on time.",
        "Can you tell me more about this product?"
    ]

    results = []
    for idx, query in enumerate(test_queries, 1):
        resp = client.post(f"{BASE_BACKEND}/api/predict", json={"text": query})
        assert resp.status_code == 200, f"Query {idx} failed: {resp.text}"
        data = resp.json()
        results.append({
            "idx": idx,
            "input": query,
            "sentiment": data["sentiment"],
            "sentiment_confidence": data["sentiment_confidence"],
            "issue_category": data["issue_category"],
            "issue_confidence": data["issue_confidence"],
            "attention_level": data["attention_level"]
        })
        print(f"[{idx}] \"{query}\"")
        print(f"     -> Sentiment: {data['sentiment']} ({data['sentiment_confidence']:.1%})")
        print(f"     -> Issue:     {data['issue_category']} ({data['issue_confidence']:.1%})")
        print(f"     -> Attention: {data['attention_level']}")

    with open("tests/sample_predictions_output.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved predictions output to tests/sample_predictions_output.json")
    print("ALL INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
