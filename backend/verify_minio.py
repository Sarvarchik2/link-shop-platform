import os
import sys

# Add the parent directory of backend to sys.path
sys.path.append('/Users/ula/Documents/link-shop-platform-1/backend')

from app.core.storage import storage
import requests

def test_minio():
    print("Testing Minio integration...")
    try:
        # Create a dummy image content
        dummy_content = b"fake-image-binary-content"
        filename = "test-image.jpg"
        content_type = "image/jpeg"
        
        print(f"Uploading {filename} to Minio...")
        url = storage.upload_file(filename, dummy_content, content_type)
        print(f"Successfully uploaded! URL: {url}")
        
        print(f"Verifying URL accessibility...")
        response = requests.get(url)
        if response.status_code == 200:
            print("URL is accessible and returned 200 OK.")
        else:
            print(f"URL returned status code: {response.status_code}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_minio()
