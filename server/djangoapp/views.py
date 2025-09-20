from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import json
import logging

# Logger instance
logger = logging.getLogger(__name__)

# ---------------------- LOGIN VIEW ---------------------- #
@csrf_exempt  # ⚠️ For development only; use CSRF tokens in production
def login_user(request):
    """
    JSON login endpoint for React/JS fetch.
    Expects POST JSON:
      { "username": "...", "password": "..." }
    Returns:
      { "userName": "...", "status": "Authenticated" | "Failed" }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username") or data.get("userName")
        password = data.get("password")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        logger.info(f"User '{username}' logged in successfully.")
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        logger.warning(f"Failed login attempt for username '{username}'.")
        return JsonResponse({"userName": username, "status": "Failed"}, status=401)


# ---------------------- LOGOUT VIEW ---------------------- #
@csrf_exempt
def logout_request(request):
    """
    Logs out the current user and returns JSON status.
    GET or POST is accepted.
    """
    logout(request)
    logger.info("User logged out.")
    return JsonResponse({"status": "Logged Out"})


# ---------------------- REGISTRATION VIEW ---------------------- #
@csrf_exempt
def registration(request):
    """
    Register a new user (JSON only).
    Expects POST JSON:
      { "username": "...", "password": "...", "email": "..." (optional) }
    Returns:
      { "userName": "...", "status": "Registered" }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email if email else ""
    )

    logger.info(f"New user registered: {username}")
    return JsonResponse({"userName": user.username, "status": "Registered"})
