import requests

BASE_URL = "http://localhost:8000"
SHOP_SLUG = "premium-eyewear"

def test_endpoints():
    endpoints = [
        f"/banner?shop_slug={SHOP_SLUG}",
        # Requesting subscription request requires Auth token usually, but let's see if we get 401 instead of 500
        f"/shop/{SHOP_SLUG}/subscription/request"
    ]

    for ep in endpoints:
        url = f"{BASE_URL}{ep}"
        print(f"Testing {url}...")
        try:
            resp = requests.get(url)
            print(f"Status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"Response: {resp.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_endpoints()
