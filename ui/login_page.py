import tkinter as tk
from config.message import Message
import customtkinter
from tkinter import messagebox

class LoginPage:
    def __init__(self, context):
        self.context = context
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.alert_message = None

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()
        title = tk.Label(self.context, text="Log in with your personal credentials or create an account", font=(
            "arial", 15, "bold"), bg=self.context.bg_color,fg="#FF3399")
        title.pack(pady=5)
        
        authF = tk.Frame(self.context, bg=self.context.bg_color)
        authF.pack(pady=0)
        authF.rowconfigure(0, weight=1)
        usernameL = tk.Label(
            authF, text="Username", bg=self.context.bg_color,fg="#FFFFFF", font=("Arial", 16))
        usernameL.grid(row=0, column=0, padx=20, pady=10,
                       sticky=tk.N + tk.S + tk.E + tk.W)
        usernameInput = tk.Entry(authF, textvariable=self.username)
        usernameInput.grid(row=0, column=1, padx=20, pady=10,
                           sticky=tk.N + tk.S + tk.E + tk.W)
        passwordL = tk.Label(authF, text="Password",
                             bg=self.context.bg_color,fg="#FFFFFF", font=("Arial", 16))
        passwordL.grid(row=2, column=0, padx=20, pady=10,
                       sticky=tk.N + tk.S + tk.E + tk.W)
        passwordInput = tk.Entry(authF, textvariable=self.password, show="*")
        passwordInput.grid(row=2, column=1, padx=20, pady=10,
                           sticky=tk.N + tk.S + tk.E + tk.W)
        # alert msg : error or success
        self.alert_message = tk.Label(self.context, text="", font=(
            "arial", 15), bg=self.context.bg_color)
        self.alert_message.pack()
        loginButton = tk.Button(authF, text="Login", command=self.login, font=("arial", 14),
                                bg='#FF3399',
                                fg='white')
        loginButton.grid(row=11, column=0, padx=10, pady=10,
                         sticky=tk.N + tk.S + tk.E + tk.W)
        
        registerButton = tk.Button(authF, text="Register", command=self.context.show_register_page,
                                   font=("arial", 14),
                                   bg='#FF3399',
                                   fg='white')
        registerButton.grid(row=11, column=1, padx=10,
                            pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        usernameL.grid(row=1, column=0)
        usernameInput.grid(row=1, column=1, pady=20)
        passwordL.grid(row=2, column=0)
        passwordInput.grid(row=2, column=1, pady=20)

    def login(self):
        login_object = {
            'username': self.username.get(),
            'password': self.password.get()
        }
        message = Message('LOGIN', login_object)
        Message.send_encrypted_message(
            self.context.client.server_socket,
            self.context.client.server_public_key,
            message.to_json()
        )
        server_message = Message.receive_and_decrypt(
            self.context.client.server_socket,
            self.context.client.private_key
        )
        if server_message and server_message == 'OK':
            self.context.client.username = self.username.get()
            self.context.show_home_page()
        else:
            messagebox.showinfo(title="Login Error", message="Invalid credentials.Please try again.")
