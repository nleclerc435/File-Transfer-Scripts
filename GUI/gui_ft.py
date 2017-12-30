import sys
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QPushButton, QFileDialog, QMainWindow, QAction, qApp, QListWidget, QLabel, QTextEdit, QDialog, QLineEdit
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import pyqtSignal
import os
import json



class FileSender(QMainWindow):

    ip = ''
    port = ''

    def __init__(self):
        super().__init__()
        self.list_box = ListBox()
        self.setCentralWidget(self.list_box)
        self.connect_dialog = ConnectDialog()
        self.connect_dialog.tar_info.connect(self.get_info)
        if os.path.exists('target_info.json'):
            with open('target_info.json') as j_data:
                data = json.load(j_data)
            self.ip = data['ip']
            self.port = data['port']
            self.list_box.status_lbl.setText(f'IP: {self.ip} \nPort: {self.port}')
            print(f'IP: {self.ip} \nPort: {self.port}')
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

    def get_info(self, data):
        print('get_info called')
        split_data = data.split('|')
        self.ip = split_data[0]
        self.port = split_data[1]
        self.list_box.status_lbl.setText(f'IP: {self.ip} \nPort: {self.port}')
        print(self.list_box.status_lbl.text())


class ListBox(QWidget):

    filenames = []

    def __init__(self):
        super(ListBox, self).__init__()
        self.layout = QHBoxLayout()
        self.v_layout1 = QVBoxLayout()
        self.v_layout2 = QVBoxLayout()

        self.status_lbl = QLabel('No Target.\nUse File->Connect to enter a target.')

        add_btn = QPushButton('Add files')
        add_btn.clicked.connect(self.open_dialog)
        lbl = QLabel('Files to send')
        self.fts_box = QListWidget()

        send_btn = QPushButton('Send')
        send_btn.clicked.connect(self.send_files)
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
        self.filenames = QFileDialog.getOpenFileNames(self, 'Open File', os.getenv('HOME'))
        if len(self.filenames) > 0:
            for filename in self.filenames[0]:
                print(filename)
                self.fts_box.addItem(os.path.basename(filename))

    def send_files(self):
        print(self.filenames[0])

        

class ConnectDialog(QDialog):
    
    tar_info = pyqtSignal(str)

    def __init__(self):
        super(ConnectDialog, self).__init__()
        self.ip_box = QLineEdit()
        self.port_box = QLineEdit()

        self.ip_lbl = QLabel('IP: ')
        self.port_lbl = QLabel('Port: ')

        self.conn_btn = QPushButton('Connect')
        self.conn_btn.clicked.connect(self.register_target)

        self.save_check = QCheckBox('Save info for later')

        self.box_layout1 = QHBoxLayout()
        self.box_layout1.addWidget(self.ip_lbl)
        self.box_layout1.addWidget(self.ip_box)

        self.box_layout2 = QHBoxLayout()
        self.box_layout2.addWidget(self.port_lbl)
        self.box_layout2.addWidget(self.port_box)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.box_layout1)
        self.layout.addLayout(self.box_layout2)
        self.layout.addWidget(self.save_check)
        self.layout.addWidget(self.conn_btn)
        self.setLayout(self.layout)

        self.setWindowTitle('Connect')

    def register_target(self):
        if self.ip_box.text() and self.port_box.text():
            target_info = {'ip':str(self.ip_box.text()), 'port':str(self.port_box.text())}
            self.tar_info.emit(target_info['ip'] + '|' + target_info['port'])
            if self.save_check.isChecked():
                with open('target_info.json', 'w') as j:
                    json.dump(target_info, j)
            print(target_info)
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_sender = FileSender()
    sys.exit(app.exec_())