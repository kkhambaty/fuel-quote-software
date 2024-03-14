from flask import Blueprint, render_template, request, redirect, url_for, session

login_bp = Blueprint('login', __name__, url_prefix='/login')

#for now, mock user data
users = {
    'user1': {'username': 'user1', 'password': 'password1'},
    'user2': {'username': 'user2', 'password': 'password2'}
}