from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign In")
        self.setGeometry(100, 100, 300, 200)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Please Sign In")
        layout.addWidget(self.label)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.signin_button = QPushButton("Sign In")
        self.signin_button.clicked.connect(self.handle_signin)
        layout.addWidget(self.signin_button)

        self.setLayout(layout)

    def handle_signin(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "user" and password == "password":  # 임시 로그인 검증
            self.label.setText("Login Successful!")
        else:
            self.label.setText("Invalid credentials. Try again.")
