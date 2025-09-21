from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .restapis import get_request, analyze_review_sentiments, post_review

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

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})