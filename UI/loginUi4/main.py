from PyQt5 import QtWidgets,QtCore
from loginUi4 import Ui_Form as LoginUi
from SignupUi4 import Ui_Form as SignupUi

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.login_ui = LoginUi()
        self.signup_ui = SignupUi()

        self.login_widget = QtWidgets.QWidget()
        self.login_ui.setupUi(self.login_widget)

        self.signup_widget = QtWidgets.QWidget()
        self.signup_ui.setupUi(self.signup_widget)

        self.login_ui.pushButton_8.clicked.connect(self.switch_to_signup)
        self.signup_ui.pushButton.clicked.connect(self.switch_to_login)
        self.signup_ui.pushButton_6.clicked.connect(self.pop_stack)

        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.login_widget)  # Initial page is loginUi4

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.stack)  # Show the QStackedWidget

    def switch_to_signup(self):
        self.stack.addWidget(self.signup_widget)  # Add SignupUi4 to the stack
        self.stack.setCurrentWidget(self.signup_widget)  # Switch to SignupUi4

    def switch_to_login(self):
        self.stack.setCurrentWidget(self.login_widget)  # Switch to loginUi4

    def pop_stack(self):
        # Pop the top widget from the stack
        if self.stack.count() > 1:
            self.stack.removeWidget(self.stack.currentWidget())
            self.stack.setCurrentIndex(self.stack.count() - 1)  # Show the new top widget


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.resize(450, 550)
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    window.show()
    app.exec_()
