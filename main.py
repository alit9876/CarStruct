from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QVBoxLayout
from PyQt5 import QtWidgets,QtCore
from UI.loginUi4.loginUi4 import Ui_Form as LoginUi
from UI.loginUi4.SignupUi4 import Ui_Form as SignupUi
import Components.Data_Structures.Hashing as Hashing
import Components.Login as Login
from UI.main import Ui_MainWindow  # Replace 'your_ui_module' with the actual module name
import csv
import Components.Data_Structures.graphs as Graphs
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
import Components.Data_Structures.queues as queue
import Components.Our_Showroom as Our_Showroom

class MyMainWindow_1(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #initail Variables
        self.file_path = './Files/car_showroom_data.csv'
        self.path_testdrive = './Files/car_testdrive_data.csv'
        self.showroom = Our_Showroom.Showroom()
        self.showroom.RetrieveTestDriveQueueFromFile(self.path_testdrive)
        # Calling Function
        self.loadShowroom()

        # These 2 lines are used to put functions on close and minimize buttons.
        # self.MinimizeButton.clicked.connect(lambda: self.showMinimized())
        # self.CrossButton.clicked.connect(lambda: self.close())

        # integration of map
        self.graph_display_layout = QVBoxLayout(self.Graph_display)
        self.source = "Receptionist"
        self.source_display.setText(self.source)
        self.car_show = self.getgraph()
        self.plot()
        self.display_testdrive()

        # Connect navigation buttons to slots
        self.prev_button.clicked.connect(self.show_previous_page)
        self.next_button.clicked.connect(self.show_next_page)

        # Connect buttons to their respective pages
        self.Home.clicked.connect(self.show_page_home)
        self.Crud_PushButton.clicked.connect(self.show_page_crud)
        self.pushButton_3.clicked.connect(self.show_page_map)
        self.TestDrive_PushButton.clicked.connect(self.show_page_test_drive)
        self.ViewCar_PushButton.clicked.connect(self.show_page_view_car)
        # button for test drive
        self.Enqueue_btn.clicked.connect(self.enqueue_button)
        self.Dequeue_btn.clicked.connect(self.dequeue_button)
        # button for Crud
        self.pushButton_8.clicked.connect(self.insert_cardata)
        self.pushButton_7.clicked.connect(self.delete_cardata)

        # button for view_car
        self.pushButton_9.clicked.connect(self.search_in_viewcar)
        # button for map layout
        self.find.clicked.connect(self.find_location)
        self.reset.clicked.connect(self.plot)
        self.mst.clicked.connect(self.display_mist)

        # Initialize the page stack with the index of the initial page
        self.page_stack = [0]
        self.stackedWidget.setCurrentIndex(0)

        # Connect the store_data_on_exit method to the aboutToQuit signal
        app.aboutToQuit.connect(self.store_data_on_exit)

    def store_data_on_exit(self):
        # Store data from showroom and User_hash_table
        self.showroom.WriteDataToFile(self.file_path)  # Assuming you have a WriteDataToFile method in your showroom class
        window.User_hash_table.WriteToFile() 
        
    def show_previous_page(self):
        if len(self.page_stack) > 1:
            self.page_stack.pop()  # Remove the current page
            prev_page_index = self.page_stack[-1]
            self.stackedWidget.setCurrentIndex(prev_page_index)

    def show_next_page(self):
        current_page_index = self.stackedWidget.currentIndex()
        next_page_index = (current_page_index + 1) % self.stackedWidget.count()
        self.page_stack.append(next_page_index)
        self.stackedWidget.setCurrentIndex(next_page_index)

    def show_page_home(self):
        self.stackedWidget.setCurrentIndex(0)

    # ##################################################################################################
    # Crud page
    # ##################################################################################################

    # toggle page
    def show_page_crud(self):
        self.stackedWidget.setCurrentIndex(1)
        self.load_data_crud()

    # To load hashtable and treesDict
    def loadShowroom(self):
        self.showroom.ReadDataFromFile(self.file_path)

    def insert_cardata(self):
        try:
            # Get data from textboxes
            serialNumber = self.textEdit_4.toPlainText().strip().upper()
            name = self.textEdit.toPlainText().strip()
            model = self.textEdit_3.toPlainText().strip()
            color = self.textEdit_2.toPlainText().strip()
            manufacturer = self.comboBox.currentText().strip()
            Features = self.textEdit_10.toPlainText().strip()
            mileage = self.textEdit_6.toPlainText().strip()
            engineCC = self.textEdit_7.toPlainText().strip()
            price = self.textEdit_8.toPlainText().strip()
            Reviews = self.textEdit_9.toPlainText().strip()

            # Validation checks
            if not serialNumber or not name or not model or not price:
                QMessageBox.information(None, 'Error', 'Serial Number, Name, Model, and Price cannot be empty.')
                return

            # Check if model, price, and Reviews can be converted to numbers
            if not model.isdigit():
                QMessageBox.information(None, 'Error', 'Model must be a valid integer.')
                return

            if not (price.replace(".", "", 1).isdigit() or price.isdigit()):
                QMessageBox.information(None, 'Error', 'Price must be a valid float or integer.')
                return

            if Reviews and not Reviews.replace(".", "", 1).isdigit():
                QMessageBox.information(None, 'Error', 'Reviews must be a valid float or integer.')
                return

            # Call function insertcar in showroom.py
            flag = self.showroom.InsertCar(serialNumber, name, model, color, manufacturer, Features, mileage, engineCC, price, Reviews)
            if flag:
                QMessageBox.information(None, 'Success', f"Car with serial number {serialNumber} Added")
            else:
                QMessageBox.information(None, 'Error', f"Car with serial number {serialNumber} is not added. There is an error in the details.")

            self.load_data_crud()

        except Exception as e:
            print("Exception: ", e)



    def load_data_crud(self):
        #Change the table widget name
        with open(self.file_path, "r", encoding="utf-8") as fileInput:
            roww = 0
            data = list(csv.reader(fileInput))
            self.tableWidget.setHorizontalHeaderLabels(['Serial No.','Name', 'Model', 'Color', 'Company', 'Features',
                                                       'Milage', 'Engine CC', 'Price', 'Review'])
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]))
            for row in data:
                for col, item in enumerate(row):
                    self.tableWidget.setItem(roww, col, QtWidgets.QTableWidgetItem(item))
                roww += 1

    def delete_cardata(self):
        serialNumber = self.textEdit_4.toPlainText()
        flag = self.showroom.DeleteCar(serialNumber)
        if flag:
            QMessageBox.information(None, 'success', f"Car {serialNumber} deleted")
            self.load_data_crud()
        if not flag:
            QMessageBox.information(None, 'success', f"Car with serial number {serialNumber} not found")
    
    # ##################################################################################################
    # Maps page
    # ##################################################################################################
    def show_page_map(self):
        self.stackedWidget.setCurrentIndex(3)

    # code for maps

    def getgraph(self):
        car_show = Graphs.WeightedGraph()

        graph_data = {
            'Receptionist': {'Chevrolet': 15, 'Suzuki': 25, 'Mitsubishi': 3, 'BMW': 3, 'Audi': 2, 'Rolls-Royce': 15},
            'Chevrolet': {'Receptionist': 15, 'Suzuki': 2, 'Mitsubishi': 5, 'BMW': 7, 'Audi': 13, 'Rolls-Royce': 12},
            'Suzuki': {'Receptionist': 25, 'Chevrolet': 2, 'Mitsubishi': 3, 'BMW': 7, 'Audi': 5, 'Rolls-Royce': 9},
            'Mitsubishi': {'Receptionist': 3, 'Chevrolet': 5, 'Suzuki': 3, 'BMW': 1, 'Audi': 2, 'Rolls-Royce': 3},
            'BMW': {'Receptionist': 3, 'Chevrolet': 7, 'Suzuki': 7, 'Mitsubishi': 1, 'Audi': 1, 'Rolls-Royce': 1},
            'Audi': {'Receptionist': 2, 'Chevrolet': 13, 'Suzuki': 5, 'Mitsubishi': 2, 'BMW': 1, 'Rolls-Royce': 2},
            'Rolls-Royce': {'Receptionist': 15, 'Chevrolet': 12, 'Suzuki': 9, 'Mitsubishi': 3, 'BMW': 1, 'Audi': 2}
        }

        for node, connections in graph_data.items():
            for neighbor, weight in connections.items():
                if node != neighbor:  # Avoiding self-loop edges
                    car_show.add_edge(node, neighbor, weight)

        car_show.mst = car_show.kruskal_mst()
        return car_show

    def update_graph(self, fig):
        for i in reversed(range(self.graph_display_layout.count())):
            widget = self.graph_display_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        canvas = FigureCanvas(fig)
        self.graph_display_layout.addWidget(canvas)


    def find_location(self):
        try:
            destination = self.inputText.text()
            if self.car_show.node_exists(destination):
                shortest_path = self.car_show.dijkstra_shortest_path(self.source, destination)
                fig = self.car_show.draw_graph(shortest_path)
                self.update_graph(fig)
                self.source = destination
                self.source_display.setText(self.source)
            else:
                QMessageBox.information(None, "Invalid Name", 'Car brand with such name does not exist')
                self.inputText.setText('')
        except Exception as e:
            print(e)

    def display_mist(self):
        try:
            self.inputText.setText('')
            fig = self.car_show.mst.draw_graph()
            self.update_graph(fig)
        except Exception as e:
            print(e)

    def plot(self):
        try:
            self.inputText.setText('')
            self.source = 'Receptionist'

            fig = self.car_show.draw_graph(None)
            self.source_display.setText(self.source)
            self.update_graph(fig)
        except Exception as e:
            print(e)

    # ##################################################################################################
    # Test Drive page
    # ##################################################################################################

    def show_page_test_drive(self):
        self.stackedWidget.setCurrentIndex(4)

    def enqueue_button(self):
        name = self.customer_txtbox.toPlainText()
        car_name = self.Car_txtbox.toPlainText()
        if name != '' and car_name != "":
            if self.showroom.CarTable.CheckValuekey(car_name):
                self.showroom.EnqueueForTestDrive(car_name, name)
                self.display_testdrive()
                self.showroom.SaveTestDriveQueueToFile(self.path_testdrive)
            else:
                QMessageBox.information(None, 'Error', 'Invalid key for car name')

        else:
            QMessageBox.information(None, "Error Message", 'Please fill all the columns')

    def dequeue_button(self):
        data = self.showroom.DequeueForTestDrive()
        name = data.customer_name
        car = data.car
        QMessageBox.information(None,'Successfully', f'The user {car} has successfully completed his test drive trial'
                                                     f' on car: {name}')
        self.display_testdrive()
        self.showroom.SaveTestDriveQueueToFile(self.path_testdrive)

    def display_testdrive(self):
        if not self.showroom.test_drive_queue.is_empty():
            data = self.showroom.test_drive_queue.get_queue_data()
            table = self.testdrive_table
            table.setRowCount(len(data))
            table.setColumnCount(len(data[0]))
            for i, (name, car) in enumerate(data):
                name_item = QTableWidgetItem(name)
                car_item = QTableWidgetItem(car)

                table.setItem(i, 0, name_item)
                table.setItem(i, 1, car_item)

            table.setHorizontalHeaderLabels(['Car', 'Name'])
        else:
            self.clearTable()

    def clearTable(self):
        table = self.testdrive_table
        table.clearContents()
        table.setRowCount(0)

    # ##################################################################################################
    # View cars page
    # ##################################################################################################

    # page toggle

    def show_page_view_car(self):
        self.stackedWidget.setCurrentIndex(2)
        self.load_data_csv()

    # code

    def load_data_csv(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                self.tableWidget_2.setColumnCount(10)
                self.tableWidget_2.setHorizontalHeaderLabels(
                    ['Serial No.', 'Name', 'Model', 'Color', 'Company', 'Features',
                     'Milage', 'Engine CC', 'Price', 'Review'])
                for row in reader:
                    # Combine additional features into a single column
                    additional_features = "; ".join(row[5].split(';'))
                    row[5] = additional_features

                    # Add the row to the table
                    self.add_row_to_table(row)
        except Exception as e:
            print(f"Error loading data from CSV: {e}")

    def add_row_to_table(self, row_data):
        row_position = self.tableWidget_2.rowCount()
        self.tableWidget_2.insertRow(row_position)
        for col, item in enumerate(row_data):
            self.tableWidget_2.setItem(row_position, col, QTableWidgetItem(item))



    # def load_table_viewcars(self,data_array):
    # #   after loading data from csv load that data in tableWidget_2
    #     self.tableWidget_2.setRowCount(len(data_array))
    #     for row_idx, row in enumerate(data_array):
    #         for col_idx, item in enumerate(row):
    #             self.tableWidget_2.setItem(row_idx, col_idx, QTableWidgetItem(item))


    def search_in_viewcar(self):
        if self.comboBox_2.currentText() != '' and self.textEdit_12.toPlainText() == '':
            self.search_by_company()
        elif self.comboBox_2.currentText() != '' and self.textEdit_12.toPlainText() != '':
            # Validate textEdit_13 and textEdit_12
            try:
                min_price = float(self.textEdit_12.toPlainText())
                max_price = float(self.textEdit_13.toPlainText())
                # Check if min_price and max_price are floats
                if isinstance(min_price, float) and isinstance(max_price, float):
                    self.search_by_pricerange()
                else:
                    QMessageBox.information(None, "Error", "Please enter valid numeric values for price range.")
            except ValueError:
                QMessageBox.information(None, "Error", "Please enter valid numeric values for price range.")



    def search_by_company(self):
        try:
            self.clear_table_widget_2()

            # get text from comboBox_2 and you can send it to a function in showroom.py named as getcarbyserialnumber
            # OR
            # search in the array you loaded from csv in load_data_csv and then call load_table_viewcars again
            manufacturerName = self.comboBox_2.currentText()
            mTree = self.showroom.GetTreeOfManufacturer(manufacturerName)
            if mTree is None:
                QMessageBox.information(None, 'Error', "Manufacturer not found")
                return
            
            price_12 = self.textEdit_12.toPlainText()
            price_13 = self.textEdit_13.toPlainText()

            if not price_12.isdigit() or not price_13.isdigit():
                QMessageBox.information(None, 'Error', 'Price must be valid integers.')
                return
            
            arr = self.showroom.inorderTraversal(mTree.root, [])

            for i in arr:
                arr2 = [i.serialNumber, i.name, i.model, i.color, i.manufacturer, i.Features, i.mileage, i.engineCC, i.price,
                        i.Reviews]
                self.add_row_to_table(arr2)
        except Exception as e:
            print('Exception ', e)


    # Add this method to clear the headers and reset the row count
    def clear_table_widget_2(self):
        self.tableWidget_2.clear()
        self.tableWidget_2.setRowCount(0)


    def search_by_pricerange(self):
        try:
            self.clear_table_widget_2()
            # get text from comboBox_2 and you can send it to a function in showroom.py named as getcarinspecificrange
            # OR
            # search in the array you loaded from csv in load_data_csv and then call load_table_viewcars again
            manufacturerName = self.comboBox_2.currentText()
            minPrice = float(self.textEdit_12.toPlainText()) 
            maxPrice = float(self.textEdit_13.toPlainText()) 

            mTree = self.showroom.GetTreeOfManufacturer(manufacturerName)
            arr = self.showroom.GetCarsInSpecificRange(mTree.root, minPrice, maxPrice, [])
            for i in arr:
                arr2 = [i.serialNumber, i.name, i.model, i.color, i.manufacturer, i.Features, i.mileage, i.engineCC, i.price,
                        i.Reviews]
                self.add_row_to_table(arr2)
        except Exception as e:
            print('Exception ' ,e)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.login_ui = LoginUi()
        self.signup_ui = SignupUi()
        
        self.login_widget = QtWidgets.QWidget()
        self.login_ui.setupUi(self.login_widget)

        self.signup_widget = QtWidgets.QWidget()
        self.signup_ui.setupUi(self.signup_widget)

        # application ui
        self.application = MyMainWindow_1()
        self.application.hide()
        self.application.pushButton_5.clicked.connect(self.return_to_login)
        # HashTables
        self.User_hash_table = Hashing.MyHashTable()

        #calls for data retrival
        self.RetriveAdminData()


        #button cals
        self.login_ui.pushButton_8.clicked.connect(self.switch_to_signup)
        self.signup_ui.pushButton.clicked.connect(self.switch_to_login)
        self.signup_ui.pushButton_6.clicked.connect(self.pop_stack)
        self.login_ui.pushButton.clicked.connect(self.sign_in)
        self.signup_ui.pushButton.clicked.connect(self.sign_up)

        # These 2 lines are used to put functions on close and minimize buttons.
        # self.MinimizeButton.clicked.connect(lambda: self.showMinimized())
        # self.CrossButton.clicked.connect(lambda: self.close())


        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.login_widget)  # Initial page is loginUi4

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.stack)  # Show the QStackedWidget

    def switch_to_application_ui(self):
        self.hide()
        self.application.show()

    def switch_to_signup(self):
        self.stack.addWidget(self.signup_widget)  # Add SignupUi4 to the stack
        self.stack.setCurrentWidget(self.signup_widget)  # Switch to SignupUi4

    def return_to_login(self):
        self.application.close()
        self.show()

    def switch_to_login(self):
        self.stack.setCurrentWidget(self.login_widget)  # Switch to loginUi4

    def pop_stack(self):
        # Pop the top widget from the stack
        if self.stack.count() > 1:
            self.stack.removeWidget(self.stack.currentWidget())
            self.stack.setCurrentIndex(self.stack.count() - 1)  # Show the new top widget

    def WriteAdminData(self):
        path = './Files/AdminCredentials.csv'
        self.User_hash_table.WriteToFile(path)

    def RetriveAdminData(self):
        path = './Files/AdminCredentials.csv'
        self.User_hash_table.retriveDataFromFile(path)
        print('Printing table ',self.User_hash_table)

    def sign_in(self):
        try:
            username = self.login_ui.lineEdit.text()
            userpassword = self.login_ui.lineEdit_2.text()
            if username != '' and userpassword != '':
                user1 = Hashing.KeyNode(userpassword, username)
                flag = Login.signIn(self.User_hash_table, user1)
                if not flag:
                    QMessageBox.information(None, 'Error', "User do not exist")
                else:
                    QMessageBox.information(None, 'Success', 'User has been login in successfully')
                    self.switch_to_application_ui()
            else:
                QMessageBox.information(None, "Error", ' Please fill all the columns')
        except Exception as e:
            print('Exception: ',e)

    def sign_up(self):
        try:
            name = self.signup_ui.lineEdit.text()
            password = self.signup_ui.lineEdit_2.text()
            confirm_password = self.signup_ui.lineEdit_3.text()
            if name != '' and password != '' and confirm_password != '':
                if password == confirm_password:
                    user1 = Hashing.KeyNode(password, name)
                    flag = Login.signUp(self.User_hash_table, user1)
                    if flag:
                        QMessageBox.information(None, 'Success', "Sign_up successfull")
                        self.signup_ui.lineEdit.clear()
                        self.signup_ui.lineEdit_2.clear()
                        self.login_ui.lineEdit.clear()
                        self.login_ui.lineEdit_2.clear()
                        self.signup_ui.lineEdit_3.clear()
                        self.WriteAdminData()
                        self.toggleframe1()
                    else:
                        QMessageBox.information(None, 'Error', "User already exists, Or Password is not strong (should contain At least 1Capital letter and 1 special character and minimum length should be 8))")
                else:
                    QMessageBox.information(None, 'Error', "Passwords Do not match.")
            else:
                QMessageBox.information(None, 'Error', "Please fill all Input")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.resize(800, 950)
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    window.show()
    app.exec_()
