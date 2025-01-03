from django.shortcuts import render
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now

from .models import ChatHistory
from .ollama_testing import initialise_model, generate_response
from .chroma_query_handler import retrieve_documents, setup_chroma_client

import json
import uuid

initialise_model()
setup_chroma_client()   


def manage_active_session(user):
    """
    Ensures the user has only one active session. Deactivates existing ones and starts a new session if required.
    """
    active_sessions = ChatHistory.objects.filter(user=user, is_active=True)
    if active_sessions.exists():
        for session in active_sessions:
            session.deactivate_session()
            # Delete records without user input during session cleanup
            ChatHistory.objects.filter(chat_session_id=session.chat_session_id, user_input="").delete()

    # Create a new active session
    new_session = ChatHistory(user=user)
    new_session.chat_session_id = uuid.uuid4()
    new_session.chat_session_title = f"{user.username}_{new_session.chat_session_id}"
    new_session.start_new_session()
    return new_session


@login_required(login_url='login')
def chatbot(request):
    """
    Handles chat interactions, managing sessions, and responding to user inputs.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', "").strip()

        if not user_message:
            return JsonResponse({'response': 'Please type a message.'})

        user_message_received_time = now()
        active_session = ChatHistory.objects.filter(user=request.user, is_active=True).first()

        if not active_session:
            active_session = manage_active_session(request.user)

        # Set a title if none exists
        if not active_session.chat_session_title:
            active_session.chat_session_title = f"{request.user.username}_{active_session.chat_session_id}"
            active_session.save()

        try:
            # Generate and store response for a new record
            retrieved_documents = retrieve_documents(user_message, top_k=3)
            generated_response = generate_response(user_message, retrieved_documents)

            # Create a new ChatHistory record linked to the session
            new_record = ChatHistory(
                user=request.user,
                chat_session_id=active_session.chat_session_id,
                chat_session_title=active_session.chat_session_title,
                user_input=user_message,
                generated_response=generated_response,
                response_time=now() - user_message_received_time,
                is_active=True,
                has_interaction=True
            )
            new_record.save()

            return JsonResponse({'response': generated_response})
        except IndexError:
            return JsonResponse({'response': "I couldn't find any relevant documents."})

    # For GET requests, reload or initiate a chat session
    if not ChatHistory.objects.filter(user=request.user, is_active=True).exists():
        manage_active_session(request.user)

    return render(request, 'chatbot2.html', {
        'message': f"Welcome back {request.session['username']}!"
    })


@login_required(login_url='login')
def new_chat_isPressed(request):
    """
    Handles the action of starting a new chat session.
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User is not authenticated.'}, status=403)

        # End all active sessions for the user
        manage_active_session(request.user)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required(login_url='login')
def fetch_sidebar_data(request):
    dummy_data = ["data7", "data6", "data5", "data4"]
    return JsonResponse({'dummyData': dummy_data})
