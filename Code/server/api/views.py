# Standard Library
from datetime import datetime, timedelta
import json
import os
from openai import OpenAI

# Django
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods

# REST Framework
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Local
from .serializers import (
    UserSerializer,
    DaterSerializer,
    CupidSerializer,
    MessageSerializer,
    GigSerializer,
    FeedbackSerializer
)
from .models import (User, Dater, Cupid, Gig, Quest, Message, Feedback)
from . import helpers
from .paypal_service import send_payout_to_cupid

# AI API (pytensor) https://pytensor.readthedocs.io/en/latest/
# Location API (Geolocation) https://pypi.org/project/geolocation-python/
# Speech To Text API (pyttsx3) https://pypi.org/project/pyttsx3/
# Text and Email notifications API (Twilio) https://www.twilio.com/en-us
# Nearby Shops API (yelpapi) https://pypi.org/project/yelpapi/


@api_view(['POST'])
def create_user(request):
    """
    Request the server to create an appropriate dater, cupid, or manager from info given.

    Args:
        request: Information about the request.
            request.post: The json data sent to the server.
               role (str): Dater, Cupid, Manager
               password (str): unhashed password
               confirm_password (str): unhashed password
               username (str)
               email (str)
               first_name (str)
               last_name (str)
               phone_number (str)
               budget (float): the user's default budget
               communication_preference (int): EMAIL = 0, TEXT = 1
               description (str)
               dating_strengths (str)
               dating_weaknesses (str)
               interests (str)
               past (str)
               nerd_type (str)
               relationship_goals (str)
               ai_degree (str)
               cupid_cash_balance (str)
    Returns:
        Response:
            If the user was created successfully, return serialized user and a 200 status code.
            If the user was not created successfully, return an error message and a 400 status code.
    """
    # Prepare data input
    data = request.data
    data['role'] = data['role'].lower()
    # Create user
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid():
        user_serializer.save()
        data['user'] = user_serializer.data['id']
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Create dater or cupid as appropriate
    if data['role'] == User.Role.DATER:
        serializer = DaterSerializer(data=data)
        return helpers.save_profile(request, user_serializer.instance, serializer)
    elif data['role'] == User.Role.CUPID:
        serializer = CupidSerializer(data=data)
        return helpers.save_profile(request, user_serializer.instance, serializer)
    user_serializer.delete()
    return Response({'error': 'invalid user type'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sign_in(request):
    """
    Log in a user

    Args (request.post):
        email(str): The email of the user
        password(str): The password of the user

    Returns:
        Response:
            Dater, Cupid, or Manager serialized
    """
    import logging

    logger = logging.getLogger(__name__)

    data = request.data or {}
    # Safely get fields
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response({'Reason': 'Missing email or password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_obj = User.objects.filter(email__iexact=email).first()
    except Exception as exc:
        logger.exception("Database error while looking up user by email")
        return Response({'Reason': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not user_obj:
        return Response({'Reason': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    username = getattr(user_obj, 'username', None)
    if not username:
        logger.error("User record without username for email=%s", email)
        return Response({'Reason': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        user = authenticate(request, username=username, password=password)
    except Exception:
        logger.exception("Authentication backend raised an exception")
        return Response({'Reason': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if user is None:
        # preserve previous behavior: if email exists but password wrong -> incorrect password
        return Response({'Reason': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

    # successful authentication -> attempt login
    try:
        login(request, user)
    except Exception:
        logger.exception("Error during login()")
        return Response({'Reason': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        if user.role == User.Role.MANAGER:
            return_data = helpers.user_expand(user, UserSerializer(user))
            return Response(return_data, status=status.HTTP_200_OK)
        else:
            serializer = helpers.initialize_serializer(user)
            if serializer is not None:
                return_data = helpers.user_expand(user, serializer)
                return Response(return_data, status=status.HTTP_200_OK)
            else:
                return Response({'Reason': 'Invalid User Type'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        logger.exception("Error preparing sign-in response for user id=%s", getattr(user, 'id', '<unknown>'))
        return Response({'Reason': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request, pk):
    """
    Get a user's information

    Args (URL query string):
        pk(int): The id of the user
    Returns:
        Response:
            Dater, Cupid, or Manager serialized
    """
    if pk != request.user.id and not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(User, id=pk)

    profile_serializer = helpers.initialize_serializer(user)
    if profile_serializer is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return_data = helpers.user_expand(user, profile_serializer)
    return Response(return_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def current_session(request):
    """
    Return basic information about the currently authenticated user.

    This endpoint is intended for client-side route guards to validate the
    server-side session (it does not accept any user-supplied IDs).
    """
    try:
        user = request.user
        return Response({
            'id': user.id,
            'role': getattr(user, 'role', None),
            'is_staff': getattr(user, 'is_staff', False),
            'username': getattr(user, 'username', None),
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    """
    For a manager.
    Delete a user

    Args:
        pk(int): The id of the user

    Returns:
        Response:
            OK
    """
    if pk != request.user.id and request.user.is_staff is False:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = get_object_or_404(User, id=pk)
    user.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def send_chat_message(request):
    """
    For a dater.
    Stores the given message in the database, sends it to the AI, and returns the AI's response.

    Args (request.post):
        message(str): The message

    Returns:
        Response:
            message(str): The AI's response
    """
    data = request.data
    user_id = request.user.id
    message = data['message']
    # save a message to database
    serializer = MessageSerializer(data={'owner': user_id, 'text': message, 'from_ai': False})
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # send a message to AI
    user_messages = Message.objects.filter(owner=user_id).order_by('-id')[:20]
    ai_response = helpers.get_ai_response(user_messages)
    # save AI's response to database
    serializer = MessageSerializer(data={'owner': user_id, 'text': ai_response, 'from_ai': True})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': ai_response}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return AI's response


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_messages(request, pk, count):
    """
    Returns the five most recent messages between user and AI.

    Args:
        request: information about the request
        pk(int): the user_id as included in the URL
        count(int): the number of messages to return. if count is 0, return all messages. if count is greater than the number of messages, return all messages. if count is less than the number of messages, that number of messages will be returned.
    Returns:
        Response:
            The five messages serialized
    """
    if pk != request.user.id:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = get_object_or_404(User, id=pk)
    if user is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        messages = Message.objects.filter(owner=user).order_by('-id')
        new_messages = []
        if count == 0:
            new_messages = messages
        else:
            for i in range(len(messages)):
                m = messages[i]
                new_messages.append(m)
                if i == count - 1:
                    break
    except Message.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = MessageSerializer(new_messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def calendar(request, pk):
    """
    For a dater.
    Returns the dater's scheduled dates.

    GET
    Args:
        pk(int): the user_id as included in the URL
    Returns:
        Response:
            The user's saved dates

    POST
    Args (request.post):
        date_time(str): ISO 8601 timestamp (I fed output back into API, and GPT said that was the date format)
        location(str): Location of date
        description(str): Arbitrary description
        status(str): Date.Status (PLANNED, OCCURING, PAST, or CANCELED)
        budget(decimal): The max budget for the date
    Returns:
        Response:
            The saved date serialized
    """
    if request.method == 'GET':
        return helpers.get_calendar(pk, request)
    elif request.method == 'POST':
        return helpers.save_calendar(request)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def rate_dater(request):
    """
    For a cupid.
    Saves a rating of a dater to the database.

    Args (request.post):
        dater_id(int): The id of the dater
        gig_id(int): The id of the gig
        message(str): Message of feedback
        rating(int): 1-5 stars(hearts)
    Returns:
        Response:
            Saved Feedback serialized
    """
    data = request.data
    owner = request.user.id
    target = data['dater_id']
    gig = data['gig_id']
    if Gig.objects.get(id=gig).dater.user_id != target:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = FeedbackSerializer(
        data={
            'owner': owner,
            'target': target,
            'gig': gig,
            'message': data['message'],
            'star_rating': data['rating'],
            'date_time': make_aware(datetime.now()),
        }
    )
    if serializer.is_valid():
        serializer.save()
        dater = Dater.objects.get(user_id=target)
        dater.rating_count += 1
        dater.rating_sum += data['rating']
        dater.save()

        try:
            helpers.send_email(dater.user.email, "You've been rated by a Cupid!")
        except Exception as e:
            print(f"Failed to send email notification: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_dater_ratings(request, pk):
    """
    For all users.
    Returns the ratings of a specific dater.

    Args:
        request: information about the request
        pk(int): the user_id as included in the URL
    Returns:
        Response:
            Sequence of Feedback objects
    """
    try:
        dater = helpers.authenticated_dater(pk, request.user)
    except PermissionDenied:
        return Response(status=status.HTTP_403_FORBIDDEN)
    ratings = get_list_or_404(Feedback, target=dater.user)
    serializer = FeedbackSerializer(ratings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_dater_balance(request, pk):
    """
    For daters.
    Returns the balance of a specific dater.

    Args:
        request: information about the request
        pk(int): the user_id as included in the URL
    Returns:
        Response:
            balance(int): The balance of the dater
    """
    try:
        dater = helpers.authenticated_dater(pk, request.user)
    except PermissionDenied:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response({'balance': dater.cupid_cash_balance}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def set_dater_profile(request):
    """
    For a dater.
    Saves the profile data of a dater.

    Args (request.post):
        serialized dater
    Returns:
        Response:
            Saved dater serialized
    """
    data = request.data
    data['user'] = request.user.id
    dater = get_object_or_404(Dater, user_id=request.user.id)
    serializer = DaterSerializer(dater, data=data)
    user_serializer = UserSerializer(request.user, data=data, partial=True)
    if serializer.is_valid() and user_serializer.is_valid():
        serializer.save()
        user_serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def rate_cupid(request):
    """
    For a dater.
    Saves a rating of a cupid to the database.

    Args (request.post):
        cupid_id(int): The id of the cupid
        gig_id(int): The id of the gig
        message(str): Message of feedback
        rating(int): 1-5 stars(hearts)
    Returns:
        Response:
            Saved Feedback serialized
    """
    data = request.data
    owner = request.user.id
    target = data['cupid_id']
    gig = get_object_or_404(Gig, id=data['gig_id'])
    if gig.cupid.user_id != target:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = FeedbackSerializer(
        data={
            'owner': owner,
            'target': target,
            'gig': gig.id,
            'message': data['message'],
            'star_rating': data['rating'],
            'date_time': make_aware(datetime.now()),
        }
    )
    if serializer.is_valid():
        serializer.save()
        cupid = get_object_or_404(Cupid, user_id=data['cupid_id'])
        cupid.rating_count += 1
        cupid.rating_sum += data['rating']
        cupid.save()

        try:
            helpers.send_email(cupid.user.email, "You've been rated by a Dater!")
        except Exception as e:
            print(f"Failed to send email notification: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_cupid_ratings(request, pk):
    """
    For all users.
    Returns the ratings of a specific cupid.

    Args:
        request: information about the request
        pk(int): the user_id as included in the URL
    Returns:
        Response:
            Sequence of Feedback objects
    """
    ratings = get_list_or_404(Feedback, target=request.user)
    serializer = FeedbackSerializer(ratings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_cupid_avg_rating(request, pk):
    """
    Return the average rating for the requested Cupid.

    Args:
        request: Information about the request.

        pk (int): ID for the requested user
    Returns:
        Response:
            Average rating from the user's record (int).
            If the account could not be found, return a 400 status code.
    """
    cupid = helpers.authenticated_cupid(pk, request.user)
    return Response({'rating:': cupid.rating_sum / cupid.rating_count}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def set_cupid_profile(request):
    """
    Creates or changes data in a Cupid's profile.

    Args:
        request: Information about the request.
            request.post: The json data sent to the server.
                data (json): The data to create or change in the Cupid's profile.
    Returns:
        Response:
            If the profile was created or changed successfully, return a 200 status code.
            If the profile failed to be created or changed (insufficent permissions, bad data, or error), return a 400 status code.
    """
    data = request.data
    data['user'] = request.user.id
    cupid = get_object_or_404(Cupid, user_id=request.user.id)
    serializer = CupidSerializer(cupid, data=data)
    user_serializer = UserSerializer(request.user, data=data, partial=True)
    if serializer.is_valid() and user_serializer.is_valid():
        serializer.save()
        user_serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_gig(request):
    """
    Creates a gig.

    Args:
        request: Information about the request.
            request.post: The json data sent to the server.
                quest (json): The quest that the gig is for.
                    quest['budget'] (float): The budget for the gig.
                    quest['items_requested'] (str): The items requested for the gig.
                    quest['pickup_location'] (str): The location to pick up the items for the gig.

    Returns:
        Response:
            If the gig was created correctly, return a 200 status code.
            If the gig was failed to be created, return a 400 status code.
    """
    data = request.data
    dater = get_object_or_404(Dater, user_id=request.user.id)
    quest = Quest(budget=data['budget'], pickup_location=data['pickup_location'], items_requested=data['items_requested'], dropoff_location=data['dropoff_location'])
    quest.save()
    gig = Gig(dater=dater, quest=quest, status=Gig.Status.UNCLAIMED, dropped_count=0, accepted_count=0)
    gig.save()
    return Response(GigSerializer(gig).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def accept_gig(request):
    """
    Assign the requesting Cupid to an unclaimed Gig, mark it as CLAIMED, and send immediate payout.

    Authentication:
        Requires an authenticated Cupid (request.user must be a Cupid).

    Request JSON:
        gig_id (int): ID of the Gig to accept.

    Behavior:
        - Fails if the gig does not exist (404).
        - Fails if the Cupid doesn't have a PayPal email configured.
        - Sends full gig budget (10% reward) to Cupid immediately via PayPal.
        - Increments the Gig's accepted_count.
        - Stamps the current (timezone–aware) datetime as date_time_of_claim.
        - Sets the cupid field to the requesting user's id.
        - Updates status to CLAIMED.

    Responses:
        200 OK: Gig claimed and payout sent successfully.
        400 BAD REQUEST: Validation failure or missing PayPal email.
        404 NOT FOUND: Gig or Cupid not found.
        500 INTERNAL SERVER ERROR: Payout failed.
    """
    try:
        user = request.user
        
        # Get the cupid profile
        try:
            cupid = Cupid.objects.get(user=user)
        except Cupid.DoesNotExist:
            return Response(
                {'error': 'Cupid profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if cupid has PayPal email set
        if not cupid.paypal_email:
            return Response(
                {'error': 'Please add a PayPal email to your profile before accepting gigs'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        gig_id = request.data.get('gig_id')
        gig = get_object_or_404(Gig, id=gig_id)
        
        # Check if gig is available
        if gig.status != Gig.Status.UNCLAIMED:
            return Response(
                {'error': 'This gig is no longer available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate reward (10% of budget)
        reward = gig.quest.budget / 10
        
        # Send PayPal payout immediately
        payout_result = send_payout_to_cupid(cupid, reward, gig_id)
        
        if not payout_result['success']:
            return Response(
                {
                    'error': 'Failed to process payout',
                    'details': payout_result.get('error', 'Unknown error')
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Update gig with claim information and payout details
        gig.cupid = cupid
        gig.status = Gig.Status.CLAIMED
        gig.date_time_of_claim = make_aware(datetime.now())
        gig.accepted_count += 1
        gig.payout_id = payout_result['payout_batch_id']
        gig.payout_status = 'processing'
        gig.save()
        
        # Update cupid's balance
        cupid.cupid_cash_balance += reward
        cupid.save()

        try:
            helpers.send_email(gig.dater.user.email, "Your gig has been claimed by a Cupid!")
        except Exception as e:
            print(f"Failed to send email notification: {e}")
        
        serializer = GigSerializer(gig)
        return Response(
            {
                'message': 'Gig claimed successfully and payment sent!',
                'gig': serializer.data,
                'reward': float(reward),
                'payout_id': payout_result['payout_batch_id']
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def complete_gig(request):
    """
    Marks a gig as complete, updates related user stats, and returns serialized gig data.

    This view function handles the completion of a gig by:
      - Retrieving the gig using the provided `gig_id` in the request data.
      - Updating the gig's status to `COMPLETE` and recording the completion timestamp.
      - Calculating and awarding a reward (10% of the quest's budget) to the Cupid who completed the gig.
      - Updating the Cupid's cash balance and completed gigs count.
      - Returning the updated gig data along with the reward amount.

    Args:
        request (Request): The incoming HTTP request containing gig data and metadata.
            Expected keys in `request.data`:
                - gig_id (int): The ID of the gig to complete.

    Returns:
        Response: 
            - 201 Created: If the gig was successfully completed, returns the serialized gig data and reward amount.
            - 400 Bad Request: If the serializer validation fails, returns validation errors.

    Side Effects:
        - Modifies the `Gig` and associated `Cupid` models in the database.
        - Adds a location string to the request data using the client's IP address.

    Example:
        >>> POST /api/gigs/complete/
        >>> { "gig_id": 42 }
        Returns:
        {
            "id": 42,
            "status": "COMPLETE",
            "date_time_of_completion": "2025-10-14T15:22:00Z",
            "reward": 50.0
        }
    """
    data = request.data
    gig = get_object_or_404(Gig, id=data['gig_id'])
    serializer = GigSerializer(
        gig,
        data={
            'status': Gig.Status.COMPLETE,
            'date_time_of_completion': make_aware(datetime.now()),
        },
        partial=True,
    )
    if serializer.is_valid():
        serializer.save()
        reward = gig.quest.budget / 10
        gig.cupid.cupid_cash_balance += reward
        gig.cupid.gigs_completed += 1
        gig.cupid.save()
        return_data = serializer.data
        return_data['reward'] = reward

        try:
            helpers.send_email(gig.dater.user.email, "Your gig has been completed by a Cupid!")
        except Exception as e:
            print(f"Failed to send email notification: {e}")
        
        return Response(return_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def drop_gig(request):
    """
    Modifies the gig to show that it is no longer claimed by a Cupid. Cupid is no longer in charge of the gig.

    Args:
        request: Information about the request.
            request.post: The json data sent to the server.
                gig_id (int): The id of the gig to drop.
    Returns:
        Response:
            If the gig was successfully dropped, return a 200 status code.
            If the gig could not be dropped, was already dropped, or does not have a Cupid assigned, return a 400 status code.
    """
    data = request.data
    gig = get_object_or_404(Gig, id=data['gig_id'])
    if gig.cupid != request.user.cupid:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    # Update gig with drop information
    gig.status = Gig.Status.UNCLAIMED
    gig.cupid = None
    gig.dropped_count += 1
    gig.date_time_of_drop = make_aware(datetime.now())  # Set drop timestamp
    gig.save()
    
    # Update cupid stats
    request.user.cupid.gigs_failed += 1
    request.user.cupid.save()

    try:
        helpers.send_email(gig.dater.user.email, "Your gig has been dropped by a Cupid!")
    except Exception as e:
        print(f"Failed to send email notification: {e}")
    
    serializer = GigSerializer(gig)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cancel_gig(request):
    """
    Deletes the gig.

    Args:
        request: Information about the request.
            request.post: The json data sent to the server.
                gig_id (int): The id of the gig to drop.
    Returns:
        Response:
            If the gig was successfully dropped, return a 200 status code.
            If the gig could not be dropped, was already dropped, or does not have a Cupid assigned, return a 400 status code.
    """
    data = request.data
    gig = get_object_or_404(Gig, id=data['gig_id'])
    if gig.dater != request.user.dater:
        return Response(status=status.HTTP_403_FORBIDDEN)
    gig.delete()
    return Response(GigSerializer(gig).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_cupid_gigs(request, pk):
    """
    For a cupid.
    Returns all gigs that the cupid has been assigned.

    Args:
        request: Information about the request.
        pk (int): The id of the cupid
        query string:
            complete(bool): Should return cupid's completed or cupid's claimed
    Returns:
        Response:
            A list of gigs (JSON)
    """
    cupid = get_object_or_404(Cupid, user_id=pk)
    gigs = get_list_or_404(Gig, cupid=cupid)
    target = Gig.Status.COMPLETE if request.GET['complete'] == 'true' else Gig.Status.CLAIMED
    current_gigs = []
    for gig in gigs:
        if gig.status == target:
            current_gigs.append(gig)
    serializer = GigSerializer(current_gigs, many=True)
    for gig in serializer.data:
        user = User.objects.get(id=gig['dater'])
        gig['dater'] = f'{user.first_name} {user.last_name}'
        gig['dater_id'] = user.id
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_dater_gigs(request, pk):
    """
    For a dater.
    Returns all gigs that the dater has created.

    Args:
        request: Information about the request.
        pk (int): The id of the cupid
    Returns:
        Response:
            A list of gigs (JSON)
    """
    dater = get_object_or_404(Dater, user_id=pk)
    gigs = get_list_or_404(Gig, dater=dater)
    serializer = GigSerializer(gigs, many=True)
    for gig in serializer.data:
        try:
            user = User.objects.get(id=gig['cupid'])
            gig['cupid'] = f'{user.first_name} {user.last_name}'
            gig['cupid_id'] = user.id
        except User.DoesNotExist:
            gig['cupid'] = ''  # Leave blank for frontend code
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_gigs(request, pk, count):
    """
    Returns a list of gigs, up to the number of `count`.

    Args:
        request: Information about the request.
        pk (int): The user_id as included in the URL
        count (int): The number of gigs to return and display.
    Returns:
        Response:
            A list of gigs (JSON)
    """
    cupid = get_object_or_404(Cupid, user_id=pk)
    gigs = Gig.objects.all()
    near_gigs = []
    for gig in gigs:
        quest = gig.quest
        if gig.status == Gig.Status.UNCLAIMED:
            near_gigs.append(gig)
    if count != 0:
        near_gigs = near_gigs[:count]
    serializer = GigSerializer(near_gigs, many=True)
    
    # Add dater names to the serialized data
    for gig in serializer.data:
        user = User.objects.get(id=gig['dater'])
        gig['dater'] = f'{user.first_name} {user.last_name}'
        gig['dater_id'] = user.id
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_cupids(request):
    """
    A manager can get all the cupid profiles.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the cupid profiles were retrieved successfully, return the serialized cupids and a 200 status code.
            If the cupid profiles were not retrieved successfully, return an error message and a 400 status code.
    """
    cupids = Cupid.objects.all()
    if cupids is None:
        return Response(data={"error": "database query failed"}, status=status.HTTP_400_BAD_REQUEST)
    data = {}
    for cupid in cupids:
        return_data = helpers.user_expand(cupid.user, CupidSerializer(cupid))
        data[cupid.user_id] = return_data
    return JsonResponse(data, safe=False)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_daters(request):
    """
    A manager can get all the dater profiles.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the dater profiles were retrieved successfully, return the serialized daters and a 200 status code.
            If the dater profiles were not retrieved successfully, return an error message and a 400 status code.
    """
    daters = Dater.objects.all()
    if daters is None:
        return Response(data={"error": "database query failed"}, status=status.HTTP_400_BAD_REQUEST)
    data = {}
    for dater in daters:
        return_data = helpers.user_expand(dater.user, DaterSerializer(dater))
        data[dater.user_id] = return_data
    return JsonResponse(data, safe=False)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_dater_count(request):
    """
    A manager can get the number of total daters.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the number of daters that are currently active was retrieved successfully, return the number of daters and a 200 status code.
            If the number of daters that are currently active was not retrieved successfully, return an error message and a 400 status code.
    """
    try:
        number_of_daters = Dater.objects.all().count()
        if number_of_daters is None:
            return Response({'error': 'no response'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'count': number_of_daters}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_cupid_count(request):
    """
    A manager can get the number of total cupids.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the number of cupids that are currently active was retrieved successfully, return the cupid count and a 200 status code.
            If the number of cupids that are currently active was not retrieved successfully, return an error message and a 400 status code.
    """
    try:
        number_of_cupids = Cupid.objects.all().count()
        if number_of_cupids is None:
            return Response({'count': None}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'count': number_of_cupids}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_active_cupids(request):
    """
    A manager can get the number of active cupids.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the number of active cupids was retrieved successfully, return the number of active cupids and a 200 status code.
            If the number of active cupids was not retrieved successfully, return an error message and a 400 status code.
    """
    try:
        active_cupids = helpers.get_sessions(User.Role.CUPID)  # Fixed: was DATER, changed to CUPID
        if active_cupids is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Fixed: added status=
        return Response(active_cupids, status=status.HTTP_200_OK)  # Fixed: added status=
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_active_daters(request):
    """
    A manager can get the number of active daters.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the number of active daters was retrieved successfully, return the number of active daters and a 200 status code.
            If the number of active daters was not retrieved successfully, return an error message and a 400 status code.
    """
    try:
        active_daters = helpers.get_sessions(User.Role.DATER)
        if active_daters is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Fixed: added status=
        return Response(active_daters, status=status.HTTP_200_OK)  # Fixed: added status=
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_gig_rate(request):
    """
    A manager can get the rate of gigs per hour.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the rate of gigs per hour was retrieved successfully, return the gig rate and a 200 status code.
            If the rate of gigs per hour was not retrieved successfully, return an error message and a 400 status code.
    """
    try:
        yesterday = datetime.now() - timedelta(days=1)  # Fixed: removed datetime. prefix
        gigs_from_past_day = Gig.objects.filter(date_time_of_request__range=(yesterday, datetime.now()))
        if gigs_from_past_day is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        gig_rate = gigs_from_past_day.count() / 24
        return Response(data={"gig_rate": gig_rate}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_gig_count(request):
    """
    A manager can get the number of gigs that are currently active.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the number of gigs that are currently active was retrieved successfully, return the gig count and a 200 status code.
            If the number of gigs that are currently active was not retrieved successfully, return an error message and a 400 status code.
    """
    try:
        number_of_gigs = Gig.objects.all().count()
        if number_of_gigs is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'count': number_of_gigs}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_gig_drop_rate(request):
    """
    A manager can get the rate of gigs that are dropped.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the rate of gigs that are dropped was retrieved successfully, return the gig drop rate and a 200 status code.
            If the rate of gigs that are dropped was not retrieved successfully, return an error message and a 400 status code.
    """
    try:
        number_of_drops = 0
        yesterday = datetime.now() - timedelta(days=1)  # Fixed: removed datetime. prefix
        gigs_from_past_day = Gig.objects.filter(date_time_of_request__range=(yesterday, datetime.now()))
        if gigs_from_past_day is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Fixed: added status=
        for gig in gigs_from_past_day:
            number_of_drops += gig.dropped_count
        drop_rate = number_of_drops / 24
        return Response(data={"drop_rate": drop_rate}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_gig_complete_rate(request):
    """
    A manager can get the rate of gigs that are completed.

    Args:
        request: Information about the request.
    Returns:
        Response:
            If the rate of gigs that are completed was retrieved successfully, return the gig complete rate and a 200 status code.
            If the rate of gigs that are completed was not retrieved successfully, return an error message and a 400 status code.
    """
    try:
        yesterday = datetime.now() - timedelta(days=1)  # Fixed: removed datetime. prefix
        gigs_from_past_day = Gig.objects.filter(date_time_of_request__range=(yesterday, datetime.now()))
        if gigs_from_past_day is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Fixed: added status=
        number_of_completed_gigs = gigs_from_past_day.filter(status=2).count()
        number_of_gigs = Gig.objects.all().count()
        gig_complete_rate = number_of_completed_gigs / number_of_gigs
        return Response(data={"gig_complete_rate": gig_complete_rate}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def suspend(request):
    """
    Manager can suspend a user.

    Args:
        request: Information about the request.
            request.post: The json data sent to the server.
                user_id (int): The id of the user to suspend.
    Returns:
        Response:
            If the user was suspended successfully, return a 200 status code.
            If the user was not suspended successfully, return an error message and a 400 status code.
    """
    user_data = request.data
    if user_data['role'] == 'Dater':
        dater = get_object_or_404(Dater, user_id=user_data['user_id'])
        serializer = DaterSerializer(dater, data={'is_suspended': True}, partial=True)
    elif user_data['role'] == 'Cupid':
        cupid = get_object_or_404(Cupid, user_id=user_data['user_id'])
        serializer = CupidSerializer(cupid, data={'is_suspended': True}, partial=True)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return helpers.retrieved_response(serializer)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def unsuspend(request):
    """
    Manager can unsuspend a user.

    Args:
        request: Information about the request.
            request.post: The json data sent to the server.
                user_id (int): The id of the user to unsuspend.
    Returns:
        Response:
            If the user was unsuspended successfully, return a 200 status code.
            If the user was not unsuspended successfully, return an error message and a 400 status code.
    """
    user_data = request.data
    if user_data['role'] == 'Dater':
        dater = get_object_or_404(Dater, user_id=user_data['user_id'])
        serializer = DaterSerializer(dater, data={'is_suspended': False}, partial=True)
    elif user_data['role'] == 'Cupid':
        cupid = get_object_or_404(Cupid, user_id=user_data['user_id'])
        serializer = CupidSerializer(cupid, data={'is_suspended': False}, partial=True)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return helpers.retrieved_response(serializer)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_notifications(request, pk):
    """
    Long poll for real-time popup notifications.
    
    Args:
        pk (int): The user id from URL
        query params:
            last_check (str): ISO timestamp of last check (optional)
            timeout (int): Max seconds to wait (default: 30, max: 60)
    """
    import time
    try: 
        user_id = pk
        timeout = min(int(request.GET.get('timeout', 30)), 60)
        start_time = time.time()
        
        if user_id != request.user.id and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # Parse last check timestamp or start from now
        last_check = request.GET.get('last_check')
        if last_check:
            try:
                last_check_time = make_aware(datetime.fromisoformat(last_check.replace('Z', '+00:00')))
                
            except ValueError:
                last_check_time = make_aware(datetime.now())
        else:
            last_check_time = make_aware(datetime.now())
        
        # Long poll loop
        while time.time() - start_time < timeout:
            notifications = []
            
            # Check for new feedback
            new_feedback = Feedback.objects.filter(
                target_id=user_id,
                date_time__gt=last_check_time
            )
            
            for feedback in new_feedback:
                notifications.append({
                    'type': 'feedback',
                    'message': f"You received a {feedback.star_rating}-star rating!",
                    'timestamp': feedback.date_time.isoformat()
                })
            
            # Check for gig status changes
            if request.user.role == User.Role.DATER:
                gigs = Gig.objects.filter(dater__user_id=user_id)
                for gig in gigs:
                    if (gig.date_time_of_claim and gig.date_time_of_claim > last_check_time):
                        notifications.append({
                            'type': 'gig_claimed',
                            'message': f"Your gig has been claimed by a Cupid!",
                            'timestamp': gig.date_time_of_claim.isoformat()
                        })
                    elif (gig.date_time_of_completion and gig.date_time_of_completion > last_check_time):
                        notifications.append({
                            'type': 'gig_completed', 
                            'message': f"Your gig has been completed!",
                            'timestamp': gig.date_time_of_completion.isoformat()
                        })
                    elif (gig.date_time_of_drop and gig.date_time_of_drop > last_check_time):
                        # Use the actual drop timestamp for proper notification timing
                        notifications.append({
                            'type': 'gig_dropped',
                            'message': f"Your gig was dropped and is now available for other Cupids!",
                            'timestamp': gig.date_time_of_drop.isoformat()
                        })
            
            # Check for gig notifications for cupids too
            elif request.user.role == User.Role.CUPID:
                # Cupids could get notifications about new gigs in their area, etc.
                pass
            
            # Return notifications if found
            if notifications:
                return Response({
                    'notifications': notifications,
                    'current_time': make_aware(datetime.now()).isoformat()
                }, status=status.HTTP_200_OK)
            
            # Wait 2 seconds before checking again
            time.sleep(2)
        
        # Timeout - return empty
        return Response({
            'notifications': [],
            'current_time': make_aware(datetime.now()).isoformat(),
            'timeout': True
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_google_maps_config(request):
    """
    Get Google Maps API configuration.
    
    Returns:
        Response:
            GOOGLE_MAPS_API_KEY: The Google Maps API key from environment variables
    """
    return Response({
        'GOOGLE_MAPS_API_KEY': os.getenv('GOOGLE_MAPS_API_KEY', '')
    })

@api_view(["GET"])
def paypal_config(request):
    """Return PayPal configuration for client-side SDK initialization"""
    return Response({
        'CLIENT_ID': os.environ.get('VITE_PAYPAL_CLIENT_ID', ''),
        'CURRENCY': os.environ.get('VITE_PAYPAL_CURRENCY', 'USD'),
        'MODE': os.environ.get('PAYPAL_MODE', 'sandbox')
    })

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def check_speech_for_word(request):
    transcript = request.data.get('transcript', '')
    
    # Add logging for debugging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Processing transcript: '{transcript}'")
    
    try:
        client = OpenAI(api_key=os.getenv('AI_API_KEY', ''))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a product detection assistant. Your job is to identify any sellable products mentioned in speech.
                    
                    Products include: food, drinks, flowers, books, electronics, clothing, jewelry, toys, household items, gifts, etc.
                    
                    IMPORTANT: Respond ONLY with valid JSON. No other text."""
                },
                {
                    "role": "user", 
                    "content": f"""Analyze this text for any products someone could buy from a store: "{transcript}"
                    
                    Respond with JSON:
                    {{
                        "word_detected": true/false,
                        "detected_word": "product name" or null,
                        "confidence": 0.0-1.0
                    }}
                    
                    Examples of products: pizza, coffee, flowers, phone, shirt, book, chocolate
                    """
                }
            ],
            temperature=0.2,  # Lower temperature for more consistent results
            max_tokens=100    # Reduced tokens since we just need simple JSON
        )
        
        # Parse OpenAI response
        ai_response = response.choices[0].message.content.strip()
        logger.info(f"OpenAI response: '{ai_response}'")
        
        # Try to parse as JSON
        try:
            import json
            
            # Clean up the response in case there's extra text
            if ai_response.startswith('```json'):
                ai_response = ai_response.replace('```json', '').replace('```', '').strip()
            elif ai_response.startswith('```'):
                ai_response = ai_response.replace('```', '').strip()
                
            parsed_response = json.loads(ai_response)
            logger.info(f"Parsed response: {parsed_response}")
            
            # Validate the response structure
            if not isinstance(parsed_response, dict):
                raise ValueError("Response is not a dictionary")
                
            # Ensure required fields exist
            parsed_response.setdefault('word_detected', False)
            parsed_response.setdefault('detected_word', None)
            parsed_response.setdefault('confidence', 0.0)
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"JSON parsing failed: {e}. Raw response: '{ai_response}'")
            
            # Fallback: simple keyword detection for common products
            common_products = [
                'pizza', 'coffee', 'flowers', 'flower', 'book', 'books', 'phone', 'shirt', 'shoes',
                'chocolate', 'candy', 'wine', 'beer', 'bread', 'milk', 'eggs', 'cheese',
                'laptop', 'computer', 'headphones', 'watch', 'jewelry', 'necklace', 'ring',
                'toy', 'toys', 'game', 'games', 'food', 'drink', 'clothes', 'clothing'
            ]
            
            transcript_lower = transcript.lower()
            detected_product = None
            
            for product in common_products:
                if product in transcript_lower:
                    detected_product = product
                    break
            
            parsed_response = {
                "word_detected": detected_product is not None,
                "detected_word": detected_product,
                "confidence": 0.8 if detected_product else 0.0,
                "fallback_used": True
            }
            logger.info(f"Using fallback detection: {parsed_response}")
        
        return Response(parsed_response)
        
    except Exception as e:
        logger.error(f"Error in check_speech_for_word: {e}")
        return Response(
            {
                "word_detected": False,
                "detected_word": None,
                "confidence": 0.0,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_ai_gig(request):
    """
    Create a gig using AI with Google Places API to find pickup locations
    """
    try:
        data = request.data
        keyword = data.get('keyword')
        user_location = data.get('user_location', {})  # {lat, lng}
        dater = get_object_or_404(Dater, user_id=request.user.id)
        
        places = helpers.find_places_for_keyword(keyword, user_location)

        print(f"Keyword: {keyword}")
        print(f"User location: {user_location}")
        print(f"Found {len(places)} places")
        if places:
            print(f"First place keys: {places[0].keys()}")
            print(f"First place: {places[0]}")
        
        if not places:
            return Response({
                'success': False, 
                'error': 'No places found for this item'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Use the closest/best place
        best_place = places[0]
        geometry = best_place.get('geometry', {})
        location_data = geometry.get('location', {})
        pickup_location = (
            best_place.get('formatted_address') or 
            best_place.get('vicinity') or 
            best_place.get('name') or 
            'Unknown Location'
        )
        
        gig_data = {
            'keyword': keyword,
            'pickup_location': pickup_location,
            'pickup_place_id': best_place.get('place_id'),
            'pickup_coords': {
                'lat': location_data.get('lat', 0),
                'lng': location_data.get('lng', 0)
            },
            'dropoff_location': f"{user_location.get('lat', '')},{user_location.get('lng', '')}" if user_location.get('lat') and user_location.get('lng') else None,
            'budget': dater.budget or 0, 
            'place_name': best_place.get('name', 'Unknown Business'),
            'place_rating': best_place.get('rating')
        }
        
        return Response({
            'success': True,
            'gig_data': gig_data,
            'message': f"Found {gig_data['place_name']} for {keyword}!"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        print(f"Error in create_ai_gig: {e}")
        print(traceback.format_exc())  # This will help debug the exact error
        
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)