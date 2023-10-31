import requests
import json
from datetime import datetime

class APIHandler:

    def __init__(self, base_url="BASE_URL"):
        self.base_url = base_url
        self.token_file = "tokens.json"

    def authenticate_user(self, credentials):
        endpoint = f"{self.base_url}/OAUTH_2.0_ENDPOINT"
        payload = {
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'code': credentials.authorization_code,
            'redirect_uri': credentials.redirect_uri
        }
        response = requests.post(endpoint, data=payload).json()
        if 'access_token' in response:
            self.save_tokens(response['access_token'], response['refresh_token'])
        else:
            self.handle_api_errors(response)

    def refresh_token(self):
        endpoint = f"{self.base_url}/TOKEN_REFRESH_ENDPOINT"
        refresh_token = self.get_refresh_token()
        payload = {
            'client_id': 'CLIENT_ID',
            'client_secret': 'CLIENT_SECRET',
            'refresh_token': refresh_token
        }
        response = requests.post(endpoint, data=payload).json()
        if 'access_token' in response:
            self.save_access_token(response['access_token'])
        else:
            self.handle_api_errors(response)

    def upload_video(self, video_path, video_description):
        media_upload_response = self.upload_media(video_path)
        if 'media_id' in media_upload_response:
            media_id = media_upload_response['media_id']
            endpoint = f"{self.base_url}/video/upload/"
            headers = {'Authorization': f"Bearer {self.get_access_token()}"}
            payload = {
                'media_id': media_id,
                'text': video_description
            }
            response = requests.post(endpoint, headers=headers, json=payload).json()
            self.handle_api_errors(response)
            return response
        else:
            self.handle_api_errors(media_upload_response)

    def upload_media(self, media_path):
        endpoint = f"{self.base_url}/image/upload/"
        headers = {'Authorization': f"Bearer {self.get_access_token()}"}
        files = {'media': open(media_path, 'rb')}
        response = requests.post(endpoint, headers=headers, files=files).json()
        self.handle_api_errors(response)
        return response

    def get_user_info(self, user_id):
        endpoint = f"{self.base_url}/user/info/{user_id}"
        headers = {'Authorization': f"Bearer {self.get_access_token()}"}
        response = requests.get(endpoint, headers=headers).json()
        self.handle_api_errors(response)
        return response

    def handle_api_errors(self, response):
        if 'error' in response:
            error_code = response.get('error_code')
            error_message = response.get('error_msg')
            print(f"Error {error_code}: {error_message}")
        elif 'data' not in response:
            print("Unexpected Response:")
            print(response)

    def check_rate_limits(self, response_headers):
        remaining_calls = response_headers.get('X-RateLimit-Remaining')
        if remaining_calls is not None and int(remaining_calls) < 1:
            print("Rate limit reached. Please wait and try again later.")

    def parse_date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Define the token handling methods like save_tokens, save_access_token, and get_refresh_token here.

    # def Method: get_video_data():
    #     pass
    # def Method: get_user_data():
    #     pass
