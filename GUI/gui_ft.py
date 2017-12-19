import sys
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QApplication, QWidget, QPushButton, QFileDialog, QMainWindow, QAction, qApp, QListView, QLabel, QTextEdit
from PyQt5.QtGui import QStandardItemModel


class FileSender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.list_box = ListBox()
        self.list_box2 = ListBox()
        self.setCentralWidget(self.list_box)

        
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('File Transfer Tool')
        self.setGeometry(10, 10, 600, 400)
        menu = self.menuBar()
        file = menu.addMenu('File')
        connect_act = QAction('Connect', self)
        file.addAction(connect_act)

        self.show()


class ListBox(QWidget):
    def __init__(self):
        super(ListBox, self).__init__()
        self.layout = QHBoxLayout()
        self.v_layout1 = QVBoxLayout()
        self.v_layout2 = QVBoxLayout()

        lbl = QLabel('Files to send')
        fts_box = QListView()

        lbl2 = QLabel('Files sent')
        sent_box = QListView()

        self.v_layout1.addWidget(lbl)
        self.v_layout1.addWidget(fts_box)

        self.v_layout2.addWidget(lbl2)
        self.v_layout2.addWidget(sent_box)

        self.layout.addLayout(self.v_layout1)
        self.layout.addLayout(self.v_layout2)
        self.setLayout(self.layout)


app = QApplication(sys.argv)
file_sender = FileSender()
sys.exit(app.exec_())