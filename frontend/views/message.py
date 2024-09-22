#!/usr/bin/python3
""" Module for in app messages and notification"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user
from frontend.app import socketio
from flask_socketio import emit, send, join_room, leave_room, disconnect

# Create blueprint for the view
message_bp = Blueprint("message", __name__, url_prefix='/message')

@message_bp.route('/chat')
def chat():
    """ Chat link"""
    return render_template('message/chat.html')

@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        emit('message', {'message': 'Connection rejected by server'})
        disconnect()
    else:
        print(f"User {current_user.id} connected with session id {request.sid}")

@socketio.on('message')
def handle_message(message):
    print(message)
    username = 'Akin'  # You can replace this with the actual username
    emit('message', {'alert': 'message received', 'username': username, 'message': message}, broadcast=True)