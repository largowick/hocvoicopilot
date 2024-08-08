import requests

def get_gemini_data(api_url, params=None):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        return response.json()  # Trả về dữ liệu JSON
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return None