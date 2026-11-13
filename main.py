from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_website_title("Password Manager")
set_site_information(
    author="Nurfat Noheri",
    description="Creates and keeps track of your passwords.",
    sources="Thanks to the Drafter docs and LLM.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Password:
    group: str
    application: str
    password: str
    username: str

@dataclass
class State:
    passwords:list[Password]
    selected_password: str
    password_length: int
    special_character: bool
    numbers: bool
    uppercase: bool

@route
def home (state: State)-> Page:
    return Page (state, [
        "Welcome! What would you like to do?",
        Button("Create Password", create_password),
        Button("View Passwords", view_passwords),
        Button ("Modify Password", modify_password)
    ])


@route
def create_password (state: State)->Page:
    return Page (state, [
        "Create a Password",
        TextBox("Password Length", "password_length"),
        CheckBox("need numbers", "numbers"),
        CheckBox("need special characters", "special_character"), 
        Button("Generate passowrd", generate_password)
    ])

""" @route
def generate_password

@route
def save_password

@route
def modify_password

@route
def view_groups

@route
def view_passwords

@route
def delete_password """

start_server()
    
    
