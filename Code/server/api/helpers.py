# Standard Library
import os

# Django
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings

# Rest Framework
from rest_framework.response import Response
from rest_framework import status

# Miscellaneous Utils

from openai import OpenAI

from operator import contains

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Local
from .models import User, Dater, Cupid, Date
from .serializers import UserSerializer, DaterSerializer, CupidSerializer, QuestSerializer, GigSerializer, \
    DateSerializer


def initialize_serializer(user):
    """
    Initialize and return the appropriate serializer for a given user based on their role.

    If the user is a Dater, returns a DaterSerializer instance for the related Dater object.
    If the user is a Cupid, returns a CupidSerializer instance for the related Cupid object.

    Args:
        user (User): The user instance whose role determines which serializer to initialize.

    Returns:
        Serializer: An instance of either DaterSerializer or CupidSerializer corresponding
        to the user's role.

    Raises:
        Dater.DoesNotExist: If the user's role is DATER but no related Dater object exists.
        Cupid.DoesNotExist: If the user's role is CUPID but no related Cupid object exists.
    """
    if user.role == User.Role.DATER:
        dater = Dater.objects.get(user=user)
        return DaterSerializer(dater)
    elif user.role == User.Role.CUPID:
        cupid = Cupid.objects.get(user=user)
        return CupidSerializer(cupid)


def authenticated_dater(pk, user):
    """
    Retrieve a Dater object only if the authenticated user matches the requested primary key.

    Ensures that users can only access their own Dater profile. If the provided primary key
    does not match the authenticated user's ID, a PermissionDenied exception is raised.

    Args:
        pk (int): The primary key of the user to retrieve.
        user (User): The currently authenticated user.

    Returns:
        Dater: The Dater object associated with the given user ID.

    Raises:
        PermissionDenied: If the provided primary key does not match the authenticated user.
        Http404: If no matching Dater object exists.
    """
    if pk != user.id:
        raise PermissionDenied()
    return get_object_or_404(Dater, user_id=pk)


def save_profile(request, user, serializer):
    """
    Validate, save, and authenticate a user profile based on the provided serializer.

    If the serializer is valid, the user's profile is saved, the user is logged in, and
    a response containing serialized user data is returned with a 201 Created status.
    If the serializer is invalid, the user instance is deleted and a 400 Bad Request
    response is returned containing validation errors.

    Args:
        request (HttpRequest): The current HTTP request object.
        user (User): The user being saved and authenticated.
        serializer (Serializer): The serializer containing the user's profile data.

    Returns:
        Response: A DRF Response object with serialized user data on success,
        or error details on failure.
    """
    if serializer.is_valid():
        serializer.save()
        login(request, user)

        return_data = user_expand(user, serializer)
        return Response(return_data, status=status.HTTP_201_CREATED)
    user.delete()
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_expand(user, other_serializer):
    """
    Expand serialized user data with additional nested user information.

    Constructs a response dictionary that combines the provided serializer data
    with serialized user information. For manager roles, embeds the user data
    directly from the same serializer. For other roles, it uses UserSerializer
    to serialize the user separately and removes the password field for security.

    Args:
        user (User): The user whose data is being expanded.
        other_serializer (Serializer): A serializer containing additional profile data.

    Returns:
        dict | Response: A dictionary of combined user and profile data on success,
        or a 400 Bad Request Response on error.
    """
    try:
        return_data = other_serializer.data
        if user.role == User.Role.MANAGER:
            return_data['user'] = other_serializer.data
        else:
            user_serializer = UserSerializer(user)
            return_data['user'] = user_serializer.data
        del return_data['user']['password']
        return return_data
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def retrieved_response(serializer):
    """
    Validate and save a serializer, returning an HTTP 200 OK or 400 Bad Request response.

    If the serializer is valid, its data is saved and returned with a 200 status code.
    Otherwise, the function returns the serializer's validation errors with a 400 status code.

    Args:
        serializer (Serializer): The serializer instance to validate and save.

    Returns:
        Response: A DRF Response object containing serialized data on success,
        or validation errors on failure.
    """
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def save_serializer(serializer):
    """
    Validate and save a serializer, returning an HTTP 201 Created or 400 Bad Request response.

    If the serializer is valid, its data is saved and returned with a 201 status code.
    Otherwise, the function returns the serializer's validation errors with a 400 status code.

    Args:
        serializer (Serializer): The serializer instance to validate and save.

    Returns:
        Response: A DRF Response object containing serialized data on success,
        or validation errors on failure.
    """
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_ai_response(user_messages: str):
    try:
        #client = OpenAI(api_key='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')
        client = OpenAI(api_key = os.getenv('AI_API_KEY', ''))

        messages = [
            {
                "role": "system",
                "content": "You are a dating coach. You give thoughtful, supportive, and practical advice on relationships, dating, and communication. Respond with raw text only. Do NOT use Markdown, bullet points, or code blocks."
            },
        ]

        for msg in reversed(user_messages):
            role = "user" if not msg.from_ai else "assistant"
            messages.append({
                "role": role,
                "content": msg.text
            })

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )

        return response.choices[0].message.content
    except Exception as e:
        return Response({'error': f'An error occurred while processing your message: {str(e)}', "api_key": os.getenv('AI_API_KEY', '')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def save_calendar(request):
    """
    Create and save a new Date entry associated with the authenticated user.

    Extracts data from the request, determines the user's location based on their
    IP address, and sets the current user's ID as the associated dater. Uses the
    DateSerializer to validate and save the data, returning the result of
    save_serializer().

    Args:
        request (HttpRequest): The current HTTP request containing date information.

    Returns:
        Response: A DRF Response object indicating success (201 Created) or failure
        (400 Bad Request).
    """
    try:
        data = request.data
        # TODO: Either us or the frontend needs to determine a planned location, then save the geo coords
        data['dater'] = request.user.id
        serializer = DateSerializer(data=data)
        return save_serializer(serializer)
    except Dater.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def get_calendar(pk, request):
    """
    Retrieve all scheduled Date entries for the authenticated Dater user.

    Verifies that the provided primary key matches the authenticated user, then
    fetches all Date objects associated with that Dater. Returns serialized date
    data with a 200 status code if successful, or a 400 status code if the Dater
    does not exist.

    Args:
        pk (int): The primary key of the user requesting their calendar.
        request (HttpRequest): The current HTTP request object.

    Returns:
        Response: A DRF Response containing serialized date data on success,
        or a 400 Bad Request response if the Dater does not exist.
    """
    try:
        dater = authenticated_dater(pk, request.user)
        dates = get_list_or_404(Date, dater=dater)
        serializer = DateSerializer(dates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Dater.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def send_email(recipient_email, message):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                background: linear-gradient(135deg, #FB3640 0%, #1F487E 100%);
                padding: 30px;
                text-align: center;
            }}
            .email-header h1 {{
                color: #ffffff;
                margin: 0;
                font-size: 28px;
                font-weight: bold;
            }}
            .email-body {{
                padding: 40px 30px;
                color: #333333;
                line-height: 1.6;
            }}
            .notification-icon {{
                text-align: center;
                font-size: 48px;
                margin-bottom: 20px;
            }}
            .message-content {{
                background-color: #f9f9f9;
                border-left: 4px solid #09A129;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .email-footer {{
                background-color: #1F487E;
                padding: 20px;
                text-align: center;
                color: #ffffff;
                font-size: 14px;
            }}
            .email-footer a {{
                color: #00CCFF;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>💘 Cupid Code</h1>
            </div>
            <div class="email-body">
                <div class="notification-icon">🔔</div>
                <h2 style="color: #1F487E; text-align: center;">You have a new notification!</h2>
                <div class="message-content">
                    {message}
                </div>
                <p style="text-align: center; margin-top: 30px;">
                    Log in to your Cupid Code account to see more details.
                </p>
            </div>
            <div class="email-footer">
                <p>© 2025 Cupid Code. All rights reserved.</p>
                <p>This is an automated notification. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    mail = Mail(
        from_email=os.getenv('SEND_EMAIL', ''),
        to_emails=recipient_email,
        subject='Cupid Code Notification',
        html_content=html_content)

    SendGridAPIClient(os.getenv('GRID_API_KEY', '')).send(mail)



def get_sessions(role):
    """
    Count the number of active user sessions for a specific role.

    Iterates over all active Django sessions, decodes each session to identify
    the user, and counts how many users have the specified role. Returns the
    count as a JSON response.

    Args:
        role (str): The user role to count active sessions for (e.g., 'DATER', 'CUPID').

    Returns:
        Response: A DRF Response containing the number of active sessions for
        the specified role, or an error response if none are found.
    """
    try:
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        if not active_sessions.exists():
            return {'data': 0}  # Return dict with data key, not Response object
        
        number_role_sessions = 0
        for session in active_sessions:
            try:
                session_data = session.get_decoded()
                user_id = session_data.get('_auth_user_id')
                if user_id:  # Check if user_id exists
                    try:
                        user = User.objects.get(id=user_id)
                        if user.role == role:
                            number_role_sessions += 1
                    except User.DoesNotExist:
                        # Skip sessions for deleted users
                        continue
            except Exception:
                # Skip sessions that can't be decoded
                continue
        
        return {'data': number_role_sessions}  # Return dict with data key
    except Exception as e:
        return {'error': str(e), 'data': 0}  # Return error but still include data key



def find_places_for_keyword(keyword, user_location):
    """
    Find places that sell the given keyword using Google Places API
    """
    try:
        import googlemaps
        
        # Get Google Maps API key
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            raise Exception('Google Maps API key not configured')
        
        gmaps = googlemaps.Client(key=api_key)
        
        # Search for places
        location = (user_location.get('lat', 40.7128), user_location.get('lng', -74.0060))
        radius = 10000  # 10km radius
        
        # Expand search queries to include broader terms
        search_queries = [
            keyword,
            f"{keyword} store",
            
            f"{keyword} shop"
        ]
        
        print(f"Searching for '{keyword}' with queries: {search_queries}")
        
        all_results = []
        
        for query in search_queries:
            try:
                # Try both keyword search and text search
                result = gmaps.places_nearby(
                    location=location,
                    radius=radius,
                    keyword=query,
                    type='store'
                )
                
                if result.get('results'):
                    all_results.extend(result['results'])
                    print(f"Query '{query}' found {len(result['results'])} results")
                
                # Also try text search for broader coverage
                text_result = gmaps.places(
                    query=f"{query} near me",
                    location=location,
                    radius=radius
                )
                
                if text_result.get('results'):
                    all_results.extend(text_result['results'])
                    print(f"Text search for '{query}' found {len(text_result['results'])} results")
                    
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
        
        unique_places = {}
        for place in all_results:
            place_id = place.get('place_id')
            if place_id not in unique_places:
                # Enrich place data with formatted address
                try:
                    place_details = gmaps.place(
                        place_id=place_id,
                        fields=['formatted_address', 'name', 'rating', 'user_ratings_total', 'geometry']
                    )
                    
                    if place_details.get('result'):
                        enriched_place = {**place, **place_details['result']}
                        unique_places[place_id] = enriched_place
                    else:
                        place['formatted_address'] = place.get('vicinity', place.get('name', 'Unknown Location'))
                        unique_places[place_id] = place
                        
                except Exception as e:
                    print(f"Error getting place details for {place_id}: {e}")
                    place['formatted_address'] = place.get('vicinity', place.get('name', 'Unknown Location'))
                    unique_places[place_id] = place
        
        def calculate_relevance_score(place, search_keyword):
            """Calculate relevance score based on multiple factors"""
            score = 0
            name = place.get('name', '').lower()
            types = place.get('types', [])
            keyword_lower = search_keyword.lower()
            
            # Name matching (highest weight)
            if keyword_lower in name:
                if name.startswith(keyword_lower):
                    score += 100  # Exact start match
                elif name.endswith(keyword_lower):
                    score += 80   # Exact end match
                else:
                    score += 60   # Contains keyword
            
            # Type matching
            relevant_types = ['store', 'establishment', 'point_of_interest']
            for place_type in types:
                if keyword_lower in place_type.lower():
                    score += 50
                elif place_type in relevant_types:
                    score += 20
            
            # Distance factor (closer is more relevant)
            # Google Places returns results roughly ordered by distance, so use index as proxy
            # This will be refined by the original order from Google's algorithm
            
            # Rating bonus (but lower weight than name/type matching)
            rating = place.get('rating', 0)
            if rating >= 4.0:
                score += 15
            elif rating >= 3.0:
                score += 10
            elif rating >= 2.0:
                score += 5
            
            # Popular places bonus
            user_ratings_total = place.get('user_ratings_total', 0)
            if user_ratings_total > 100:
                score += 10
            elif user_ratings_total > 50:
                score += 5
            
            return score
        
        # Sort by relevance score (highest first)
        sorted_places = sorted(
            unique_places.values(),
            key=lambda x: calculate_relevance_score(x, keyword),
            reverse=True
        )

        print(f"Total unique places found: {len(unique_places)}")
        for place in sorted_places[:10]:  # Show top 10 instead of just 5
            relevance_score = calculate_relevance_score(place, keyword)
            print(f"  - {place.get('name')} (Relevance: {relevance_score}, Rating: {place.get('rating', 'N/A')}, Type: {place.get('types', [])})")
        
        return sorted_places[:5] 

    except Exception as e:
        print(f"Error in find_places_for_keyword: {e}")
        return []