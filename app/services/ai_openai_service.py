import base64
import os
from openai import OpenAI, OpenAIError
from PIL import Image
import io

class OpenAIService:
    def __init__(self, db_service):
        self.db = db_service
        self.client = None
        self.api_key = self.db.get_setting("openai_api_key", "")
        self.base_url = self.db.get_setting("openai_base_url", "https://api.openai.com/v1")
        self.model = self.db.get_setting("openai_model", "gpt-4o")
        
        if self.api_key:
            self._init_client()

    def _init_client(self):
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url if self.base_url else "https://api.openai.com/v1"
            )
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            self.client = None

    def update_settings(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.db.save_setting("openai_api_key", api_key)
        self.db.save_setting("openai_base_url", base_url)
        self.db.save_setting("openai_model", model)
        self._init_client()

    def test_connection(self):
        if not self.client: return False, "Client not initialized (Missing API Key)"
        try:
            self.client.models.list()
            return True, "Connection Successful"
        except OpenAIError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def _encode_image(self, pil_image):
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Resize if too large to save token/bandwidth (max 2048px)
        max_size = 2048
        if max(pil_image.size) > max_size:
            pil_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def extract_text_ocr(self, pil_image):
        if not self.client: return "Error: API Key not configured."
        
        base64_image = self._encode_image(pil_image)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract all text from this image exactly as it appears. Do not add any commentary."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during OCR: {str(e)}"

    def smart_rename(self, pil_image):
        if not self.client: return "Scan_Error"
        
        base64_image = self._encode_image(pil_image)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Suggest a concise, descriptive filename for this document (e.g., 'Invoice_12345', 'Meeting_Notes_Oct2023'). Output ONLY the filename, no extension, no spaces (use underscores)."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=20
            )
            name = response.choices[0].message.content.strip().replace(" ", "_")
            # Remove extension if AI added it
            if "." in name: name = name.rsplit(".", 1)[0]
            return name
        except Exception as e:
            print(f"Smart rename error: {e}")
            return "Scan_AutoRename_Error"

    def analyze_document(self, pil_image):
        if not self.client: return "Error: API Key not configured."
        
        base64_image = self._encode_image(pil_image)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this document. Provide a Summary and key extracted fields (like dates, names, amounts) in a structured format."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during analysis: {str(e)}"

    def chat_with_content(self, message, history, pil_image=None):
        if not self.client: return "Error: API Key not configured."
        
        messages = [{"role": m["role"], "content": m["content"]} for m in history]
        
        user_content = [{"type": "text", "text": message}]
        
        if pil_image:
            base64_image = self._encode_image(pil_image)
            user_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
            
        messages.append({"role": "user", "content": user_content})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during chat: {str(e)}"
