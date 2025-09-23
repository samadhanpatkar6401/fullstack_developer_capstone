from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import json
import logging

# External API helpers
from .restapis import get_request, analyze_review_sentiments, post_review

# Models for Cars API
from .models import CarMake, CarModel
from .populate import initiate   # Used to auto-populate car data if empty

# Logger
logger = logging.getLogger(__name__)


# ---------------------- CARS API ---------------------- #
def get_cars(request):
    """
    Returns list of car makes & models.
    If CarMake is empty, populate it with default data.
    Response:
    {
      "CarModels": [
        {"CarModel": "Pathfinder", "CarMake": "NISSAN"},
        {"CarModel": "A-Class", "CarMake": "Mercedes"},
        ...
      ]
    }
    """
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})


# ---------------------- AUTH: LOGIN ---------------------- #
@csrf_exempt   # ⚠️ Use CSRF tokens in production
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


# ---------------------- AUTH: LOGOUT ---------------------- #
@csrf_exempt
def logout_request(request):
    logout(request)
    logger.info("User logged out.")
    return JsonResponse({"status": "Logged Out"})


# ---------------------- AUTH: REGISTRATION ---------------------- #
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


# ---------------------- DEALERSHIPS ---------------------- #
def get_dealerships(request, state="All"):
    """
    Returns list of dealerships.
    - state="All" -> fetch all dealers
    - state="XX"  -> fetch dealers for a given state code
    """
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    """
    Return details for a specific dealer.
    """
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": [dealership]})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    """
    Fetch reviews for a specific dealer and analyze sentiment.
    """
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if reviews is None:
            return JsonResponse({"status": 500, "message": "Failed to fetch reviews from external service."})

        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail.get("review", ""))
            review_detail["sentiment"] = response.get("sentiment", "neutral") if response else "neutral"

        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


# ---------------------- ADD REVIEW ---------------------- #
@csrf_exempt
def add_review(request):
    """
    Add a review for a dealer. User must be authenticated.
    """
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body.decode("utf-8"))
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Error posting review: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
