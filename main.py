
from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
import random


set_website_title("Password Manager")
set_site_information(
    author="Nurfat Noheri",
    description="Creates and keeps track of your passwords.",
    sources="Thanks to the Drafter docs and LLM.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://noherin.github.io/password_manager_project/"]
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
    passwords: list[Password]
    generated_password: str
    selected_password: str
    password_length: int
    special_character: bool
    numbers: bool
    uppercase: bool


@route
def index(state: State) -> Page:
    return home(state)

@route
def home(state: State) -> Page:
    return Page(state, [
        "Welcome! What would you like to do?\n",
        Button("create password", create_password),
        Button("view passwords", view_passwords),
        Button("modify password", modify_password),
        Button("delete password", delete_password),
        Button("view groups", view_groups)
    ])


@route
def create_password(state: State) -> Page:
    return Page(state, [
        "Choose your password requirements:\n",

        "\n Password length:",
        TextBox("password_length", "8"),

        "\n Include special characters:",
        CheckBox("special_character", False),

        "\n Include numbers:",
        CheckBox("numbers", False),

        "\n Include uppercase letters:",
        CheckBox("uppercase", False),

        Button("generate password", generate_password),
        Button("home", home)
    ])


@route
def generate_password(state: State, password_length: int,
                      numbers: bool, special_character: bool,
                      uppercase: bool) -> Page:

    characters = "abcdefghijklmnopqrstuvwxyz"

    if numbers:
        characters = characters + "0123456789"

    if special_character:
        characters = characters + "!@#$%&*"

    if uppercase:
        characters = characters + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    password = ""

    while password_length > 0:
        password_length = password_length - 1
        password = password + random.choice(characters)

    state.generated_password = password

    return Page(state, [
        "Your generated password:",
        state.generated_password,
        "\n Enter the information for the account you want to save:",
        TextBox("application", "application"),
        TextBox("username", "username"),
        TextBox("group", "group"),
        Button("save password", save_password),
        Button("home", home)
    ])


@route
def save_password(state: State, application: str, username: str,
                  group: str) -> Page:

    new_password = Password(
        group,
        application,
        state.generated_password,
        username
    )

    state.passwords.append(new_password)

    return Page(state, [
        "Your password was saved!",
        Button("view passwords", view_passwords),
        Button("home", home)
    ])


@route
def view_passwords(state: State) -> Page:

    contents = ["Your saved passwords: \n"]

    for password in state.passwords:
        contents.append("\n application: " + password.application)
        contents.append("\n username: " + password.username)
        contents.append("\n Password: " + password.password)
        contents.append("\n group: " + password.group)
        contents.append("\n --------------------")

    contents.append(Button("home", home))
    contents.append(Button("view_groups", view_groups))

    return Page(state, contents)


@route
def view_groups(state: State) -> Page:

    groups = []

    for password in state.passwords:
        if password.group not in groups:
            groups.append(password.group)

    contents = ["Your password groups: \n"]

    for group in groups:
        contents.append(group + "\n")

    if not groups:
        contents.append("You have no saved groups yet.")

    contents.append(Button("view passwords", view_passwords))
    contents.append(Button("home", home))

    return Page(state, contents)


@route
def modify_password(state: State) -> Page:

    return Page(state, [
        "Enter the application and username of the password you want to modify:",
        TextBox("application", "application"),
        TextBox("username", "username"),
        TextBox("new_password", "new_password"),
        Button("update password", update_password),
        Button("home", home)
    ])


@route
def update_password(state: State, application: str, username: str,
                    new_password: str, new_group: str) -> Page:

    found = False

    for password in state.passwords:
        if password.application == application and password.username == username:
            password.password = new_password
            password.group = new_group
            found = True

    if found:
        message = "Your password was updated!"
    else:
        message = "No matching application and username were found."

    return Page(state, [
        message,
        Button("view passwords", view_passwords),
        Button("home", home)
    ])


@route
def delete_password(state: State) -> Page:

    return Page(state, [
        "Delete a Password",
        "Enter the application and username of the password you want to delete:",
        TextBox("application", "application"),
        TextBox("username", "username"),
        Button("delete", confirm_delete),
        Button("home", home)
    ])


@route
def confirm_delete(state: State, application: str,
                   username: str) -> Page:

    found = False
    remaining_passwords = []

    for password in state.passwords:
        if password.application == application and password.username == username:
            found = True
        else:
            remaining_passwords.append(password)

    state.passwords = remaining_passwords

    if found:
        message = "Your password was deleted!"
    else:
        message = "No matching application and username were found."

    return Page(state, [
        message,
        Button("view passwords", view_passwords),
        Button("home", home)
    ])


start_server(State(
    passwords=[],
    generated_password="",
    selected_password="",
    password_length=8,
    special_character=False,
    numbers=False,
    uppercase=False
))

