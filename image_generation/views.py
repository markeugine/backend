from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.conf import settings
import os, requests, base64
from dotenv import load_dotenv
import time

load_dotenv()
class ImageGenerationViewset(viewsets.ViewSet):
    """
    ViewSet to handle AI image generation requests using Stability AI API.

    Provides a POST endpoint 'generate-image' to generate an image from a text prompt.
    """

    @action(detail=False, methods=['post'], url_path='generate-image')
    def generate_image(self, request):
        """
        Generate an image based on a text prompt sent in the request.

        Expected JSON payload:
            {
                "prompt": "a description of the desired image"
            }

        Returns:
            - Base64 encoded image string
            - URL to the saved image file accessible via MEDIA_URL
        """

        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Load API key from environment variables
        STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
        API_HOST = "https://api.stability.ai"
        ENGINE_ID = "stable-diffusion-xl-1024-v1-0"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        }

        # Define the payload according to Stability AI API spec
        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 896,
            "width": 1152,
            "samples": 1,
            "steps": 30
        }

        # Make the API request to generate the image
        response = requests.post(f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image",
                                 headers=headers, json=payload)

        if response.status_code != 200:
            # Return error response from API if generation failed
            return Response({"error": response.text}, status=response.status_code)

        data = response.json()
        image_base64 = data.get("artifacts", [])[0].get("base64")

        # Decode the base64 image data
        image_data = base64.b64decode(image_base64)

        # Create unique filename based on current timestamp
        file_name = f"generated_image_{int(time.time())}.png"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Ensure MEDIA_ROOT directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save image to disk
        with open(file_path, "wb") as f:
            f.write(image_data)

        # Construct full URL for frontend access
        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)

        # Respond with base64 image and accessible URL
        return Response({
            "image": image_base64,
            "file_url": file_url,
        })
