import sys
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QApplication, QWidget, QPushButton, QFileDialog, QMainWindow, QAction, qApp, QListWidget, QLabel, QTextEdit, QDialog, QLineEdit
from PyQt5.QtGui import QStandardItemModel
import os



class FileSender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.list_box = ListBox()
        self.list_box2 = ListBox()
        self.setCentralWidget(self.list_box)
        self.connect_dialog = ConnectDialog()
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('File Transfer Tool')
        self.setGeometry(10, 10, 600, 400)
        menu = self.menuBar()
        file = menu.addMenu('File')
        connect_act = QAction('Connect', self)
        file.addAction(connect_act)
        file.triggered.connect(self.connect)

        self.show()

    def connect(self):
        self.connect_dialog.exec_()


class ListBox(QWidget):
    def __init__(self):
        super(ListBox, self).__init__()
        self.layout = QHBoxLayout()
        self.v_layout1 = QVBoxLayout()
        self.v_layout2 = QVBoxLayout()

        self.status_lbl = QLabel('Status: Not connected')

        add_btn = QPushButton('Add files')
        add_btn.clicked.connect(self.open_dialog)
        lbl = QLabel('Files to send')
        self.fts_box = QListWidget()

        send_btn = QPushButton('Send')
        lbl2 = QLabel('Files sent')
        sent_box = QListWidget()


        self.v_layout1.addWidget(lbl)
        self.v_layout1.addWidget(add_btn)
        self.v_layout1.addWidget(self.fts_box)

        self.v_layout2.addWidget(lbl2)
        self.v_layout2.addWidget(send_btn)
        self.v_layout2.addWidget(sent_box)

        self.layout.addWidget(self.status_lbl)
        self.layout.addLayout(self.v_layout1)
        self.layout.addLayout(self.v_layout2)
        self.setLayout(self.layout)

    def open_dialog(self):
        filenames = QFileDialog.getOpenFileNames(self, 'Open File', os.getenv('HOME'))
        if len(filenames) > 0:
            for filename in filenames[0]:
                print(filename)
                self.fts_box.addItem(os.path.basename(filename))
        

class ConnectDialog(QDialog):
    def __init__(self):
        super(ConnectDialog, self).__init__()
        self.ip_box = QLineEdit()
        self.port_box = QLineEdit()

        self.ip_lbl = QLabel('IP: ')
        self.port_lbl = QLabel('Port: ')

        self.conn_btn = QPushButton('Connect')

        self.box_layout1 = QHBoxLayout()
        self.box_layout1.addWidget(self.ip_lbl)
        self.box_layout1.addWidget(self.ip_box)

        self.box_layout2 = QHBoxLayout()
        self.box_layout2.addWidget(self.port_lbl)
        self.box_layout2.addWidget(self.port_box)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.box_layout1)
        self.layout.addLayout(self.box_layout2)
        self.layout.addWidget(self.conn_btn)
        self.setLayout(self.layout)

        self.setWindowTitle('Connect')


app = QApplication(sys.argv)
file_sender = FileSender()
sys.exit(app.exec_())