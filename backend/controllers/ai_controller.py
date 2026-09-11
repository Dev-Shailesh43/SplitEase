"""
AI Controller — Gemini Multimodal OCR and Financial Copilot.
"""

from ..services.gemini_service import scan_receipt_image, ask_copilot, generate_insights
from ..middleware.error_handler import make_success_response, make_error_response

def handle_ai_chat(body):
    user_prompt = body.get('prompt', '')
    pod_context = body.get('context', {})
    if not user_prompt:
        return make_error_response("Missing prompt in request body", 400)
    reply = ask_copilot(user_prompt, pod_context)
    return make_success_response({"reply": reply})

def handle_ai_scan_receipt(body):
    image_base64 = body.get('imageBase64', '')
    mime_type = body.get('mimeType', 'image/jpeg')
    if not image_base64:
        return make_error_response("Missing imageBase64 data", 400)
    parsed_data = scan_receipt_image(image_base64, mime_type)
    return make_success_response({"data": parsed_data})

def handle_ai_insights(body):
    pod_context = body.get('context', {})
    insights = generate_insights(pod_context)
    return make_success_response({"insights": insights})
