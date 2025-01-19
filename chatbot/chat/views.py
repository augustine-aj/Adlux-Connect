from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from .models import ChatSession, Interaction
from .ollama_testing import initialise_model, generate_response
from .chroma_query_handler import retrieve_documents, setup_chroma_client

import json

# Initialize the model and Chroma client
initialise_model()
setup_chroma_client()   

def check_active_session(request):
    active = ChatSession.objects.filter(user=request.user, is_active=True).first()
    return active


def get_chat_interactions(session):

    interactions = Interaction.objects.filter(session=session).order_by('created_at')
    interaction_list = [
        {
            "interaction_id": str(interaction.interaction_id),
            "user_message": interaction.user_message,
            "bot_response": interaction.bot_response,
            "created_at": interaction.created_at.isoformat(),
            "feedback": interaction.feedback if interaction.feedback is not None else ""
        }

        for interaction in interactions
    ]
    return json.dumps(interaction_list)


def manage_active_session(user):
    """
    Ensures the user has only one active session. Deactivates existing ones and starts a new session if required.
    """
    active_sessions = ChatSession.objects.filter(user=user, is_active=True)
    if active_sessions.exists():
        # Deactivate the existing active session
        active_sessions.update(is_active=False, ended_at=now())

    # Create and return a new active session
    new_session = ChatSession.objects.create(user=user)
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
        active_session = check_active_session(request)

        if not active_session:
            print('no active session....')
            active_session = manage_active_session(request.user)

        # Set the session title to the first user input if the title is not already set
        if not active_session.title:
            active_session.title = user_message
            active_session.save()

        try:
            # Retrieve related documents and generate a response
            retrieved_documents = retrieve_documents(user_message, top_k=3)
            generated_response = generate_response(user_message, retrieved_documents)

            # Store interaction details in the Interaction model
            new_interaction = Interaction(
                session=active_session,
                user_message=user_message,
                bot_response=generated_response
            )
            new_interaction.save()

            response_time = now() - user_message_received_time
            return JsonResponse({'response': generated_response, 'response_time': str(response_time)})

        except IndexError:
            return JsonResponse({'response': "I couldn't find any relevant documents."})

    # For GET requests, start a new chat session if none exists
    if not ChatSession.objects.filter(user=request.user, is_active=True).exists():
        manage_active_session(request.user)

    print(request.user)
    active_session = check_active_session(request)
    if active_session:
        interaction_list = get_chat_interactions(active_session)
        print(f'Interactions of {request.user} of the active sessios {interaction_list = }')
        return render(request, 'chatbot2.html', {'user': request.user, 'interactions': interaction_list})
    else:
        print('no active sessions for this user. New user found..')
        return render(request, 'chatbot2.html', {'user': request.user, 'interactions': []})


@login_required(login_url='login')
def new_chat_isPressed(request):
    """
    Starts a new chat session.
    """
    if request.method == 'POST':
        print('new chat is pressed///')
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User is not authenticated.'}, status=403)

        # End all active sessions and start a new one
        manage_active_session(request.user)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required(login_url='login')
def fetch_sidebar_data(request):
    """
    Fetches dummy data for sidebar rendering.
    """
    print("uploading sidebar data")
    chat_sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
    chat_titles = [session.title for session in chat_sessions if session.title]
    return JsonResponse({'dummyData': chat_titles})


@login_required(login_url='login')
def get_chat_history(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            chat_title = body.get('data')
            print(f'requesting chat history for {chat_title}')

            if not chat_title:
                return JsonResponse({'status': 'error', 'message': 'Chat title is required'}, status=400)

            ChatSession.objects.filter(user=request.user, is_active=True).update(is_active=False, ended_at=now())
            
            chat_session = ChatSession.objects.filter(user=request.user, title=chat_title).first()

            if not chat_session:
                return JsonResponse({'status': 'error', 'message': 'No chat session is found'}, status=404)

            chat_session.is_active = True
            chat_session.save()

            interaction_list = get_chat_interactions(chat_session)
            print(interaction_list)  # For debugging purposes

            return JsonResponse(
                {
                    'status': 'success',
                    'chat_title': chat_title,
                    'interactions': interaction_list
                }
            )
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

