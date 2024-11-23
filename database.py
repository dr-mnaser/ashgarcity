# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 16:23:28 2023

@author: MANaser
"""
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import json
import streamlit as st

# # Ucomment this if used locally#################################
# # Load the environment variables
# load_dotenv(".env")
# # Path to your Firebase service account key JSON file
# FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
# # Check if the default app has already been initialized
# if not firebase_admin._apps:
#     # Initialize Firebase app
#     #cred = credentials.Certificate(firebase_credentials_json)
#     cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
#     firebase_admin.initialize_app(cred)
################################################################

# Use the following when deploy to streamlit####################
# Load Firebase credentials from Streamlit secrets
firebase_credentials_json = st.secrets["firebase"]["FIREBASE_CREDENTIALS"]

# Parse the credentials
firebase_credentials = json.loads(firebase_credentials_json)

# Initialize Firebase
cred = credentials.Certificate(firebase_credentials)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
##############################################################


# Initialize Firestore client
db = firestore.client()

# Function to add a document to the "ashgarcity-tracker" collection
def insert_period(name, date, transaction, value, comment):
    doc_ref = db.collection("ashgarcity-tracker").document(name)  # Using 'name' as the document ID
    doc_ref.set({
        "key": name,
        "date": date,
        "transaction": transaction,
        "value": value,
        "comment": comment
    })

# Function to fetch all documents in the "ashgarcity-tracker" collection
def fetch_all_periods():
    """Fetches all documents in the ashgarcity-tracker collection"""
    docs = db.collection("ashgarcity-tracker").stream()
    return [doc.to_dict() for doc in docs]

# Function to get a single document from the "ashgarcity-tracker" collection by name
def get_period(name):
    """Fetches a single document from ashgarcity-tracker by name"""
    doc = db.collection("ashgarcity-tracker").document(name).get()
    return doc.to_dict() if doc.exists else None

# Function to delete a document from the "ashgarcity-tracker" collection by name
def delete_period(name):
    """Deletes a document from ashgarcity-tracker by name"""
    db.collection("ashgarcity-tracker").document(name).delete()

# Function to get all period names from the "ashgarcity-tracker" collection
def get_all_periods():
    items = fetch_all_periods()
    return [item["name"] for item in items] if items else []

# User database functions using the "users-ashgarcity" collection
def insert_user(username, name, password):
    """Inserts a user document into the users-ashgarcity collection"""
    doc_ref = db.collection("users-ashgarcity").document(username)
    doc_ref.set({
        "key": username,
        "name": name,
        "password": password
    })
    return doc_ref.get().to_dict()

def fetch_all_users():
    """Fetches all user documents from users-ashgarcity collection"""
    docs = db.collection("users-ashgarcity").stream()
    return [doc.to_dict() for doc in docs]

def get_user(username):
    """Fetches a user document from users-ashgarcity by username"""
    doc = db.collection("users-ashgarcity").document(username).get()
    return doc.to_dict() if doc.exists else None

def update_user(username, updates):
    """Updates a user document in the users-ashgarcity collection"""
    db.collection("users-ashgarcity").document(username).update(updates)

def delete_user(username):
    """Deletes a user document from the users-ashgarcity collection"""
    db.collection("users-ashgarcity").document(username).delete()

###########################################################
# Example usage:
#insert_period(
#    name="JohnDoe",
#    date="2024-10-10",
#    transaction="income",
#    value=500,
#    comment="October salary"
#)

#insert_user(username, name, hash_password)
##############################################


