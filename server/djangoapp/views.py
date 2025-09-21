from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import json
import logging

# ✅ NEW IMPORTS for Cars API
from .models import CarMake, CarModel        # <-- First task
from .populate import initiate               # <-- If using auto-population

# Logger instance
logger = logging.getLogger(__name__)

# ---------------------- FIRST TASK: GET CARS ---------------------- #
def get_cars(request):
    """
    Returns list of car makes & models.
    - If CarMake is empty, calls populate.initiate() to add default data.
    Response format:
    {
      "CarModels": [
        {"CarModel": "Pathfinder", "CarMake": "NISSAN"},
        {"CarModel": "A-Class", "CarMake": "Mercedes"},
        ...
      ]
    }
    """
    count = CarMake.objects.count()
    if count == 0:
        initiate()  # Populate initial data if empty

    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for cm in car_models:
        cars.append({"CarModel": cm.name, "CarMake": cm.car_make.name})

    return JsonResponse({"CarModels": cars})


# ---------------------- LOGIN VIEW ---------------------- #
@csrf_exempt  # ⚠️ For development only; use CSRF tokens in production
def login_user(request):
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
    logout(request)
    logger.info("User logged out.")
    return JsonResponse({"status": "Logged Out"})


# ---------------------- REGISTRATION VIEW ---------------------- #
@csrf_exempt
def registration(request):
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
