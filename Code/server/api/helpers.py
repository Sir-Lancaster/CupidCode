# Standard Library
from math import radians, sin, cos, sqrt, atan2
import base64
import wave
import os

# Django
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, get_list_or_404

# Rest Framework
from rest_framework.response import Response
from rest_framework import status

# Miscellaneous Utils
try:
    from geopy.geocoders import Nominatim
except Exception:
    Nominatim = None

try:
    import geoip2.database
except Exception:
    geoip2 = None

try:
    from yelpapi import YelpAPI
except Exception:
    YelpAPI = None

from openai import OpenAI

from operator import contains

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
except Exception:
    SendGridAPIClient = Mail = None

try:
    from twilio.rest import Client
except Exception:
    Client = None

try:
    import speech_recognition as sr
except Exception:
    sr = None

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


def authenticated_cupid(pk, user):
    """
    Retrieve a Cupid object only if the authenticated user matches the requested primary key.

    Ensures that users can only access their own Cupid profile. If the provided primary key
    does not match the authenticated user's ID, a PermissionDenied exception is raised.

    Args:
        pk (int): The primary key of the user to retrieve.
        user (User): The currently authenticated user.

    Returns:
        Cupid: The Cupid object associated with the given user ID.

    Raises:
        PermissionDenied: If the provided primary key does not match the authenticated user.
        Http404: If no matching Cupid object exists.
    """
    if pk != user.id:
        raise PermissionDenied()
    return get_object_or_404(Cupid, user_id=pk)


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
    client = OpenAI(api_key=os.getenv('AI_API_KEY', ''))

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
        data['location'] = get_location_string(request.META['REMOTE_ADDR'])
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


def update_user_location(user, addr):
    """
    Update a user's stored location based on their IP address or physical address.

    Uses get_location_string() to determine the location from the given address.
    If a valid location is found, it updates the user's `location` field and saves
    the user instance to the database.

    Args:
        user (User): The user whose location should be updated.
        addr (str): The IP address or address string used to determine location.
    """
    user.location = get_location_string(addr)
    if user.location is not None:
        user.save()


def get_location_string(ip_address):
    """
    Convert an IP address into a formatted latitude-longitude string.

    If the IP address is localhost (127.0.0.1), returns a fixed default coordinate.
    Otherwise, uses get_location_from_ip_address() to determine latitude and longitude.
    Returns None if no valid coordinates are found.

    Args:
        ip_address (str): The IP address to convert into a location string.

    Returns:
        str | None: A space-separated string "latitude longitude" if found,
        otherwise None.
    """
    if ip_address is None:
        return None
    if ip_address == "127.0.0.1" or ip_address == "localhost":
        return "430909.36611535 4621007.2874155"
    latitude, longitude = get_location_from_ip_address(ip_address)
    if latitude is None or longitude is None:
        return None
    return f"{latitude} {longitude}"


def get_location_from_address(address):
    """
    Retrieve latitude and longitude coordinates from a physical address string.

    Uses the Nominatim geocoding API (via geopy) to look up geographic coordinates.
    Returns None, None if the address cannot be resolved.

    Args:
        address (str): The address string to geocode.

    Returns:
        tuple[float | None, float | None]: A tuple containing (latitude, longitude),
        or (None, None) if the address could not be located.
    """
    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="geoapiExercises")
    # Getting location details
    location = geolocator.geocode(address)
    if location:
        # Extracting latitude and longitude
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None


def get_location_from_ip_address(ip_address):
    # ...existing docstring...
    if ip_address is None:
        return None, None
    if ip_address in ("127.0.0.1", "localhost"):
        # keep format consistent: return tuple of floats for coordinates
        return 430909.36611535, 4621007.2874155

    # Use absolute path relative to this module
    base = os.path.dirname(os.path.abspath(__file__))
    geoip_database_path = os.path.join(base, "geodata", "GeoLite2-City_20240227", "GeoLite2-City.mmdb")
    if geoip2 is None:
        return None, None
    if not os.path.exists(geoip_database_path):
        return None, None

    try:
        with geoip2.database.Reader(geoip_database_path) as reader:
            try:
                response = reader.city(ip_address)
                latitude = response.location.latitude
                longitude = response.location.longitude
                return latitude, longitude
            except geoip2.errors.AddressNotFoundError:
                return None, None
    except Exception:
        return None, None


def locations_are_near(location1, location2, max_distance_miles):
    """
    Determine whether two locations are within a given distance of each other.

    Parses two latitude-longitude strings and compares their distance using
    within_distance(). Returns True if the locations are within the specified
    maximum distance in miles, False otherwise.

    Args:
        location1 (str): The first location string in the format "latitude longitude".
        location2 (str): The second location string in the format "latitude longitude".
        max_distance_miles (float): The maximum allowed distance in miles.

    Returns:
        bool: True if the two locations are within max_distance_miles, else False.
    """
    latitude1, longitude1 = location1.split(" ")
    latitude1 = latitude1.strip(',')
    latitude2, longitude2 = location2.split(" ")
    latitude2 = latitude2.strip(',')
    # TODO: Expand quest or give frontend an api for getting quests.
    return within_distance(
        float(latitude1), float(longitude1), float(latitude2), float(longitude2), float(max_distance_miles)
    )


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two geographic points in miles.

    Implements the Haversine formula to compute distance based on latitude and
    longitude values provided in degrees. Assumes Earth’s radius as 3958.8 miles.

    Args:
        lat1 (float): Latitude of the first point.
        lon1 (float): Longitude of the first point.
        lat2 (float): Latitude of the second point.
        lon2 (float): Longitude of the second point.

    Returns:
        float: The distance between the two points in miles.
    """
    # Radius of the Earth in miles
    r = 3958.8  # miles

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c

    return distance


def within_distance(lat1, lon1, lat2, lon2, max_distance_miles):
    """
    Check whether two geographic coordinates are within a specified distance.

    Uses the haversine_distance() function to calculate the great-circle distance
    between two points on Earth and compares it to the given maximum distance.

    Args:
        lat1 (float): Latitude of the first location.
        lon1 (float): Longitude of the first location.
        lat2 (float): Latitude of the second location.
        lon2 (float): Longitude of the second location.
        max_distance_miles (float): The maximum allowed distance in miles.

    Returns:
        bool: True if the distance between the two points is less than or equal
        to max_distance_miles, otherwise False.
    """
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return distance <= max_distance_miles


def call_yelp_api(pk, search):
    # defensive: ensure YelpAPI library present and api key available
    if YelpAPI is None:
        return None
    dater = get_object_or_404(Dater, user_id=pk)
    if not dater.location:
        return None
    try:
        latitude, longitude = dater.location.split(" ")
    except Exception:
        return None
    api_key = get_yelp_api_key()
    if not api_key:
        return None
    try:
        y = YelpAPI(api_key, timeout_s=5.0)
        return y.search_query(term=search, latitude=latitude, longitude=longitude, limit=10)
    except Exception:
        return None


def get_yelp_api_key():
    """
    Prefer env var YELP_API_KEY. Fallback to absolute yelp_api_key.txt near this module.
    Return None if not found or malformed.
    """
    key = os.environ.get("YELP_API_KEY")
    if key:
        return key
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "yelp_api_key.txt")
    try:
        with open(path, "r") as file:
            lines = file.readlines()
            if not lines:
                return None
            # best-effort: first line contains key at last token
            parts = lines[0].strip().split()
            return parts[-1] if parts else None
    except Exception:
        return None


def get_twilio_account_sid():
    """
    Retrieve the Twilio Account SID from the configuration file.

    Reads the 'yelp_api_key.txt' file and extracts the Twilio Account SID
    from the second line.

    Returns:
        str: The Twilio Account SID as a string.
    """
    with open('yelp_api_key.txt', 'r') as file:
        lines = file.readlines()
        return lines[1].split(" ")[2].strip()


def get_twilio_auth_token():
    """
    Retrieve the Twilio Auth Token from the configuration file.

    Reads the 'yelp_api_key.txt' file and extracts the Twilio authentication
    token from the second line.

    Returns:
        str: The Twilio Auth Token as a string.
    """
    with open('yelp_api_key.txt', 'r') as file:
        lines = file.readlines()
        return lines[1].split(" ")[4].strip()


def get_twilio_authenticated_sender_email():
    """
    Retrieve the authenticated Twilio sender email address.

    Reads the 'yelp_api_key.txt' file and extracts the verified sender email
    address from the sixth line.

    Returns:
        str: The authenticated sender email address as a string.
    """
    with open('yelp_api_key.txt', 'r') as file:
        lines = file.readlines()
        return lines[5].split(" ")[1].strip()


def get_grid_api_key():
    """
    Retrieve the SendGrid API key from the configuration file.

    Reads the 'yelp_api_key.txt' file and extracts the SendGrid API key
    from the third line.

    Returns:
        str: The SendGrid API key as a string.
    """
    with open('yelp_api_key.txt', 'r') as file:
        lines = file.readlines()
        return lines[2].split(" ")[2].strip()


def get_twilio_authenticated_reserve_phone_number():
    """
    Retrieve the Twilio reserved phone number for message sending.

    Reads the 'yelp_api_key.txt' file and extracts the reserved Twilio phone
    number from the fifth line.

    Returns:
        str: The reserved Twilio phone number as a string.
    """
    with open('yelp_api_key.txt', 'r') as file:
        lines = file.readlines()
        return lines[4].split(" ")[1].strip()


def get_twilio_authenticated_sender_phone_number():
    """
    Retrieve the Twilio verified sender phone number.

    Reads the 'yelp_api_key.txt' file and extracts the authenticated sender
    phone number from the sixth line.

    Returns:
        str: The Twilio sender phone number as a string.
    """
    with open('yelp_api_key.txt', 'r') as file:
        lines = file.readlines()
        return lines[5].split(" ")[1].strip()


def process_ai_response(dater, response):
    """
    Process an AI-generated response to determine whether a new gig should be created.

    If the AI response contains the phrase 'Create gig: True', initiates gig creation
    through create_new_gig(). Otherwise, returns a message indicating that gig creation
    was not needed.

    Args:
        dater (Dater): The Dater instance associated with the request.
        response (str): The AI-generated response message.

    Returns:
        Response: A DRF Response indicating whether a gig was created or skipped.
    """
    if contains('Create gig: True', response):
        return create_new_gig(dater, response)
    else:
        return Response(
            {'message': 'gig creation not needed', 'gig_created': False},
            status=status.HTTP_200_OK,
        )


def create_new_gig(dater, response):
    requested_items = 'NA'
    for line in response.split('\n'):
        if contains('Items requested:', line):
            parts = line.split(':', 1)
            if len(parts) > 1:
                requested_items = parts[1].strip()
    if requested_items == 'NA':
        return Response(
            {
                'error': 'gig creation failed. no specified pickup items',
                'gig_created': False,
            },
            status=status.HTTP_200_OK,
        )
    # call_yelp_api expects user id (pk), not a location string
    locations = call_yelp_api(dater.user.id, requested_items)
    if not locations or 'businesses' not in locations or len(locations.get('businesses', [])) == 0:
        return Response(
            {'error': 'gig creation failed. no yelp locations found', 'gig_created': False},
            status=status.HTTP_200_OK,
        )
    first = locations['businesses'][0]
    pickup_address = first.get('location', {}).get('address1') or first.get('name') or 'unknown'
    quest_data = {
        'budget': dater.budget,
        'items_requested': requested_items,
        'pickup_location': pickup_address,
    }
    serializer = QuestSerializer(data=quest_data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(
            {'error': 'gig creation failed. could not serialize quest.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    gig_data = {'dater': dater.id if hasattr(dater, 'id') else dater, 'quest': serializer.data}
    serializer = GigSerializer(data=gig_data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'gig was created', 'gig_created': True},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {'error': 'gig creation failed. could not serialize.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

def send_text(account_sid, auth_token, message):
    """
    Send an SMS message using the Twilio API.

    Uses authenticated Twilio credentials and verified phone numbers to send
    a text message. Returns a Response containing the Twilio message SID.

    Args:
        account_sid (str): The Twilio Account SID for authentication.
        auth_token (str): The Twilio authentication token.
        message (str): The text message content to send.

    Returns:
        Response: A DRF Response containing the Twilio message SID on success.
    """
    # We are hard-coding the number since only verified numbers can be used
    to_phone_number = get_twilio_authenticated_reserve_phone_number()
    from_phone_number = get_twilio_authenticated_sender_phone_number()
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_phone_number,
        body=message,
        to=to_phone_number
    )
    return Response(message.sid, status=status.HTTP_200_OK)


def send_email(dater, message):
    """
    Send an email notification to a Dater using SendGrid.

    Composes and sends an HTML email from the verified Twilio SendGrid sender
    address to the Dater’s registered email. Handles exceptions raised during
    email transmission.

    Args:
        dater (Dater): The Dater instance to send the email to.
        message (str): The email body content (HTML format).

    Returns:
        Response: A DRF Response indicating success or containing an error message.
    """
    dater_email = dater.email
    from_email = get_twilio_authenticated_sender_email()
    mail = Mail(
        from_email=from_email,
        to_emails=dater_email,
        subject='Notification from Cupid Code',
        html_content=message,
    )
    try:
        grid_api_key = get_grid_api_key()
        sg = SendGridAPIClient(grid_api_key)
        response = sg.send(mail)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
    return Response(response, status=status.HTTP_200_OK)


def get_message_from_audio(audio_data, dater):
    """
    Convert base64-encoded audio data into text and construct an AI prompt.

    Decodes a base64 audio string, writes it to a temporary WAV file, transcribes
    it into text using CMU Sphinx, and formats the transcription into a structured
    prompt for AI analysis. Deletes the temporary file after processing.

    Args:
        audio_data (str): The base64-encoded audio data from the client.
        dater (Dater): The Dater instance whose context (budget) informs the AI prompt.

    Returns:
        str: A formatted text prompt containing transcribed audio and gig instructions,
        or an error message if processing fails.
    """
    recognizer = sr.Recognizer()
    # Convert base64 audio data to bytes
    audio_bytes = base64.b64decode(audio_data)
    file_path = "temp_audio_storage/file.wav"
    try:
        # Convert bytes to audio file
        with wave.open(file_path, 'wb') as file:
            file.setnchannels(1)  # Mono audio
            file.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
            file.setframerate(44100)  # Sample rate (adjust as needed)
            file.writeframes(audio_bytes)

        # Transcribe audio
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_sphinx(audio_data)
            prompt = f"""
                          The following text is transcribed from an audio file. 
                          Analyze the text to determine if a gig should be created. 
                          A gig can be created by saying 'create gig'. 
                          The purpose of a gig is to tell a Cupid what to do to save the date. 
                          If a gig is created, the Cupid will be able to see the gig and accept it. 
                          A gig will need to know what items are requested for the date. 
                          The budget for the gig will be the amount of money the Dater is willing to spend on the date.
                          Budget: {dater.budget}
                          Please give your response in the following form:
                              Create gig: True or False
                              Items requested: Flowers, Chocolate, etc. or NA if no items are requested
                          The text is: 

                          """
            message = prompt + text
            return message
    except Exception as e:
        print("Error processing audio:", e)
        return "Error processing audio"
    finally:
        # Delete the temporary WAV file
        if os.path.exists(file_path):
            os.remove(file_path)


def get_response_from_yelp_api(pk, request, search):
    """
    Handle an authenticated Yelp API query request for a specific user.

    Validates that the user making the request matches the provided primary key.
    If authorized, performs a Yelp API search and returns the results.

    Args:
        pk (int): The user ID making the request.
        request (HttpRequest): The current HTTP request object.
        search (str): The search term to use for the Yelp query.

    Returns:
        Response: A DRF Response containing Yelp data (200 OK), or an error status
        (403 FORBIDDEN or 400 BAD REQUEST) on failure.
    """
    if pk != request.user.id:
        return Response(status=status.HTTP_403_FORBIDDEN)
    response = call_yelp_api(pk, search)
    if response:
        return Response(response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


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
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    if active_sessions is None:
        return Response({'error': 'No active sessions'}, status=status.HTTP_400_BAD_REQUEST)
    number_dater_sessions = 0
    for session in active_sessions:
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if User.objects.get(id=user_id).role == role:
            number_dater_sessions += 1
    return Response({'active_sessions': number_dater_sessions}, status=status.HTTP_200_OK)
