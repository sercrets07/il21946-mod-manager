import requests

# Flask server URL (Change if running on a different machine)
SERVER_URL = "http://127.0.0.1:5100"  # If remote, use "http://your-server-ip:5000"

# Test file paths
UPLOAD_FILE_PATH = "mod_pack.json"  # Make sure this file exists before testing
DOWNLOAD_FILE_NAME = "mod_pack.json"
SAVE_DOWNLOAD_PATH = "downloaded_mod_pack.json"  # Where to save downloaded file

def test_upload():
    """Tests file upload to Flask server."""
    url = f"{SERVER_URL}/upload_file"
    try:
        with open(UPLOAD_FILE_PATH, "rb") as file:
            files = {"file": file}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            print(f"✅ Upload successful: {response.json()}")
        else:
            print(f"❌ Upload failed: {response.json()}")
    except Exception as e:
        print(f"❌ Error during upload: {e}")

def test_download():
    """Tests file download from Flask server."""
    url = f"{SERVER_URL}/download/{DOWNLOAD_FILE_NAME}"
    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(SAVE_DOWNLOAD_PATH, "wb") as file:
                for chunk in response.iter_content(1024):  # Download in chunks
                    file.write(chunk)
            print(f"✅ Download successful: {SAVE_DOWNLOAD_PATH}")
        else:
            print(f"❌ Download failed: {response.json()}")
    except Exception as e:
        print(f"❌ Error during download: {e}")

if __name__ == "__main__":
    print("🔄 Running Flask server tests...")
    test_upload()
    test_download()
