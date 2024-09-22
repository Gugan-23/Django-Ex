from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .utils import get_mongo_client
from bson import ObjectId
import bcrypt
# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import send_email  # Make sure to import here

@method_decorator(csrf_exempt, name='dispatch')
class AuthView(View):
    def post(self, request):
        client = get_mongo_client()
        if not client:
            return HttpResponse("Failed to connect to MongoDB")

        db = client['test']
        collection = db['users']
        action = request.POST.get('action')

        if action == "signup":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not username or not email or not password:
                return HttpResponseBadRequest("Missing required fields")

            try:
                if collection.find_one({"email": email}):
                    return HttpResponse(f"User with email {email} already exists!")

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                collection.insert_one({
                    "_id": ObjectId(),
                    "username": username,
                    "email": email,
                    "password": hashed_password
                })

                return HttpResponse("Signup successful! <a href='/auth/?action=login'>Login</a>")

            except Exception as e:
                return HttpResponse(f"Failed to interact with MongoDB: {e}")

        # Login logic
        elif action == "login":
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
                return HttpResponseBadRequest("Missing required fields")

            try:
                user = collection.find_one({"email": email})

                if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                    request.session['user_id'] = str(user['_id'])  
                    send_email(email, "You loggined","Thank you for loggini")

                    return redirect('/home/')  

                return HttpResponse("Invalid email or password")

            except Exception as e:
                return HttpResponse(f"Failed to interact with MongoDB: {e}")
            
    def get(self, request):
        # If user is already authenticated, redirect to home
        if request.user.is_authenticated:
            return redirect('/home/')

        action = request.GET.get('action', 'signup')
        
        # Show the login or signup form
        return render(request, 'auth.html', {'action': action})

# Global home function
def home(request):
    client = get_mongo_client()
    if not client:
        return HttpResponse("Failed to connect to MongoDB")

    db = client['test']
    collection = db['users']

    try:
        user_list = list(collection.find({}, {'username': 1, 'email': 1, '_id': 1}))
        formatted_user_list = [{
            'username': u.get('username'),
            'email': u.get('email'),
            'user_id': str(u.get('_id'))
        } for u in user_list]

        return render(request, 'index.html', {'users': formatted_user_list})  # Render the home page

    except Exception as e:
        return HttpResponse(f"Failed to interact with MongoDB: {e}")

def profile(request):
    user_id = request.session.get('user_id')  # Get user ID from session
    if not user_id:
        return redirect('/auth/?action=login')  # Redirect to login if not authenticated

    client = get_mongo_client()
    if not client:
        return HttpResponse("Failed to connect to MongoDB")

    db = client['test']
    collection = db['users']

    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user_details = {
                'username': user.get('username'),
                'email': user.get('email'),
                'user_id': str(user.get('_id')),
            }
            # Render the profile page with user details
            return render(request, 'profile.html', {'user': user_details, 'username': user_details['username']})
        else:
            return HttpResponse("User not found")

    except Exception as e:
        return HttpResponse(f"Failed to interact with MongoDB: {e}")
    
from django.http import HttpResponse
from django.shortcuts import redirect, render
from bson import ObjectId
from .utils import get_mongo_client  
from django.http import HttpResponse
from .utils import send_email
def caretaker(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/auth/?action=login')

    client = get_mongo_client()
    if not client:
        return HttpResponse("Failed to connect to MongoDB")

    db = client['test']
    collection = db['users']
    caretakers_collection = db['caretakers']

    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user_details = {
                'username': user.get('username'),
                'email': user.get('email'),
                'user_id': str(user.get('_id')),
            }
            users = list(collection.find({}, {'username': 1, 'email': 1, '_id': 1}))

            formatted_users = [{
                'username': u.get('username'),
                'email': u.get('email'),
                'user_id': str(u.get('_id'))
            } for u in users]

            if request.method == 'POST':
                caretaker_email = request.POST.get('caretaker_email')

                # Send email after booking
                
                # Insert booking into database
                caretakers_collection.insert_one({
                    "user_id": ObjectId(user_id),
                    "email": user.get('email'),
                    "caretaker_email": caretaker_email,
                    "status": "Requested"
                })

                user_email = user.get('email')
                send_email(caretaker_email, "Booking Request",{user_email})

                return HttpResponse("Booking successful")

            return render(request, 'list_caretakers.html', {'users': formatted_users, 'user_details': user_details})

    except Exception as e:
        return HttpResponse(f"Failed to interact with MongoDB: {e}")

def user_list_view(request):
    client = get_mongo_client()
    if not client:
        return HttpResponse("Failed to connect to MongoDB")

    db = client['test']
    collection = db['users']

    # Retrieve users from the database
    users = list(collection.find({}, {'username': 1, 'email': 1, '_id': 1}))

    # Format users for display
    formatted_users = [{
        'username': user.get('username'),
        'email': user.get('email'),
        'user_id': str(user.get('_id'))
    } for user in users]

    return render(request, 'users_list.html', {'users': formatted_users})
def profile(request):
    user_id = request.session.get('user_id')  # Get user ID from session
    if not user_id:
        return redirect('/auth/?action=login')  # Redirect to login if not authenticated

    client = get_mongo_client()
    if not client:
        return HttpResponse("Failed to connect to MongoDB")

    db = client['test']
    collection = db['users']

    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user_details = {
                'username': user.get('username'),
                'email': user.get('email'),
                'user_id': str(user.get('_id')),
            }
            # Render the profile page with user details
            return render(request, 'profile.html', {'user': user_details, 'username': user_details['username']})
        else:
            return HttpResponse("User not found")

    except Exception as e:
        return HttpResponse(f"Failed to interact with MongoDB: {e}")

def about(request):
    
    return render(request, 'aboutus.html')

class AdminView(View):
    def get(self, request):
        client = get_mongo_client()
        if not client:
            return HttpResponse("Failed to connect to MongoDB")

        db = client['test']
        collection = db['users']

        try:
            # Fetch all users
            user_list = list(collection.find({}, {'username': 1, 'email': 1, '_id': 1}))
            formatted_user_list = [{
                'username': u.get('username'),
                'email': u.get('email'),
                'user_id': str(u.get('_id'))
            } for u in user_list]

            return render(request, 'users_list.html', {'users': formatted_user_list})

        except Exception as e:
            return HttpResponse(f"Failed to interact with MongoDB: {e}")

    def post(self, request):
        client = get_mongo_client()
        if not client:
            return HttpResponse("Failed to connect to MongoDB")

        db = client['test']
        collection = db['users']
        action = request.POST.get('action')

        if action == 'delete_user':
            user_id = request.POST.get('user_id')

            if not user_id:
                return HttpResponseBadRequest("User ID is missing")

            try:
                # Delete user by ObjectId
                result = collection.delete_one({"_id": ObjectId(user_id)})

                if result.deleted_count == 1:
                    return HttpResponse("User deleted successfully")
                else:
                    return HttpResponse("User not found")

            except Exception as e:
                return HttpResponse(f"Failed to interact with MongoDB: {e}")

        return redirect('/admin')
