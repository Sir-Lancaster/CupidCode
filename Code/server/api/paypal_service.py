import os
import requests
import base64
import logging
from decimal import Decimal
import datetime

logger = logging.getLogger(__name__)

def get_paypal_access_token():
    """
    Get OAuth access token from PayPal using client credentials.
    
    Returns:
        str: Access token if successful, None otherwise
    """
    client_id = os.getenv('VITE_PAYPAL_CLIENT_ID')
    client_secret = os.getenv('PAYPAL_SECRET')
    mode = os.getenv('PAYPAL_MODE', 'sandbox')
    
    if not client_id or not client_secret:
        logger.error("PayPal credentials not found in environment variables")
        return None
    
    # Use sandbox or live API endpoint
    base_url = 'https://api-m.sandbox.paypal.com' if mode == 'sandbox' else 'https://api-m.paypal.com'
    token_url = f'{base_url}/v1/oauth2/token'
    
    # Encode credentials in base64
    credentials = f'{client_id}:{client_secret}'
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {'grant_type': 'client_credentials'}
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        logger.info(f"PayPal token request status: {response.status_code}")
        
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            logger.info("Successfully obtained PayPal access token")
            return access_token
        else:
            logger.error(f"Failed to get access token: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.exception(f"Exception while getting PayPal access token: {e}")
        return None


def send_payout_to_cupid(cupid, amount, gig_id):
    """
    Send a payout to a Cupid via PayPal.
    
    Args:
        cupid (Cupid): The Cupid object to send payment to
        amount (Decimal): The amount to send
        gig_id (int): The ID of the gig (used as sender_item_id for tracking)
    
    Returns:
        dict: Result dictionary with 'success' boolean and additional info
    """
    access_token = get_paypal_access_token()
    
    if not access_token:
        return {
            'success': False,
            'error': 'Failed to authenticate with PayPal'
        }
    
    mode = os.getenv('PAYPAL_MODE', 'sandbox')
    base_url = 'https://api-m.sandbox.paypal.com' if mode == 'sandbox' else 'https://api-m.paypal.com'
    payout_url = f'{base_url}/v1/payments/payouts'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Convert amount to string with 2 decimal places
    amount_str = f'{float(amount):.2f}'
    
    payout_data = {
        'sender_batch_header': {
            'sender_batch_id': f'cupid_gig_{gig_id}_{cupid.user_id}_{int(datetime.datetime.utcnow().timestamp())}',
            'email_subject': 'You have received a payment from Cupid!',
            'email_message': f'Congratulations! You have received ${amount_str} for completing a gig.'
        },
        'items': [
            {
                'recipient_type': 'EMAIL',
                'amount': {
                    'value': amount_str,
                    'currency': 'USD'
                },
                'receiver': cupid.paypal_email,
                'note': f'Payment for Gig #{gig_id}',
                'sender_item_id': f'gig_{gig_id}'
            }
        ]
    }
    
    try:
        logger.info(f"Sending payout: ${amount_str} to {cupid.paypal_email}")
        response = requests.post(payout_url, json=payout_data, headers=headers)
        
        logger.info(f"PayPal payout response status: {response.status_code}")
        
        if response.status_code == 201:
            response_data = response.json()
            payout_batch_id = response_data.get('batch_header', {}).get('payout_batch_id')
            
            logger.info(f"Payout successful! Batch ID: {payout_batch_id}")
            
            return {
                'success': True,
                'payout_batch_id': payout_batch_id,
                'message': 'Payout sent successfully'
            }
        else:
            error_message = f"Failed. Response status: {response.status_code}. Response message: {response.reason}. Error message: {response.text}"
            logger.error(f"Payout failed: {error_message}")
            
            return {
                'success': False,
                'error': error_message
            }
            
    except Exception as e:
        logger.exception(f"Exception during payout: {e}")
        return {
            'success': False,
            'error': str(e)
        }