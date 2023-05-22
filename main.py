import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QHBoxLayout, QFileDialog, QMainWindow, QDesktopWidget, QListWidget, QGridLayout, QMessageBox, QMenuBar, QMenu, \
    QAction

IMAGE_EXT = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.prog_info = None
        self.workdir = ''

        # Инициализируем параметры главного окна
        self.setWindowTitle('Трансформация изображений')
        screen = QDesktopWidget().screenGeometry()
        self.resize(int(0.75 * screen.width()), int(0.75 * screen.height()))

        # Создаем макет левой части окна - для выбора графических файлов
        btn_dir = QPushButton('Выбор директории')
        btn_dir.clicked.connect(self.open_dir)
        self.lst_files = QListWidget()
        lo_left = QVBoxLayout()
        lo_left.addWidget(btn_dir)
        lo_left.addWidget(self.lst_files)

        # Создаем макет правой части - для выбора отображения выбранного файла и кнопок преобразования

        # Создаем кнопки для преобразования изображения и добавляем их в макет для них
        btn_left = QPushButton('Left')
        btn_right = QPushButton('Right')
        btn_sharp = QPushButton('Sharp')
        btn_blur = QPushButton('Blur')
        btn_edge_enhance = QPushButton('Edge enhance')
        btn_edge_enhance_more = QPushButton('Edge enhance more')
        btn_smooth = QPushButton('Smooth')
        btn_smooth_more = QPushButton('Smooth more')
        btn_b_w = QPushButton('B/W')
        btn_contour = QPushButton('Contour')
        btn_flip = QPushButton('Flip')
        btn_emboss = QPushButton('Emboss')
        btn_gaussian_blur = QPushButton('Gaussian Blur')
        btn_unsharp_mask = QPushButton('Unsharp Mask')
        btn_detail = QPushButton('Detail')
        btn_find_edges = QPushButton('Find edges')
        lo_transform = QGridLayout()
        lo_transform.addWidget(btn_left, 0, 0)
        lo_transform.addWidget(btn_right, 1, 0)
        lo_transform.addWidget(btn_sharp, 0, 1)
        lo_transform.addWidget(btn_blur, 1, 1)
        lo_transform.addWidget(btn_edge_enhance, 0, 2)
        lo_transform.addWidget(btn_edge_enhance_more, 1, 2)
        lo_transform.addWidget(btn_smooth, 0, 3)
        lo_transform.addWidget(btn_smooth_more, 1, 3)
        lo_transform.addWidget(btn_b_w, 0, 4)
        lo_transform.addWidget(btn_contour, 1, 4)
        lo_transform.addWidget(btn_flip, 0, 5)
        lo_transform.addWidget(btn_emboss, 1, 5)
        lo_transform.addWidget(btn_gaussian_blur, 0, 6)
        lo_transform.addWidget(btn_unsharp_mask, 1, 6)
        lo_transform.addWidget(btn_detail, 0, 7)
        lo_transform.addWidget(btn_find_edges, 1, 7)

        # Добавляем в макет правой части метку для изображения и кнопки для преобразования
        lbl_image = QLabel('Загрузите изображение')
        lo_right = QVBoxLayout()
        lo_right.addWidget(lbl_image)
        lo_right.setAlignment(lbl_image, Qt.AlignCenter)
        lo_right.addLayout(lo_transform)

        # Создаем макет главного окна и добавляем в него макеты левой и правой части
        lo_main = QHBoxLayout()
        lo_main.addLayout(lo_left, 20)
        lo_main.addLayout(lo_right, 80)

        widget = QWidget()
        widget.setLayout(lo_main)
        self.setCentralWidget(widget)

        # Добавляем главное меню
        menu_main = QMenuBar(self)
        menu_file = QMenu('Файл', self)
        act_open = QAction('Выбор директории', self)
        act_open.triggered.connect(self.open_dir)
        act_save = QAction('Сохранить', self)
        act_exit = QAction('Выйти', self)
        act_exit.triggered.connect(self.exit_prog)
        menu_file.addAction(act_open)
        menu_file.addAction(act_save)
        menu_file.addAction(act_exit)
        menu_edit = QMenu('Преобразовать', self)
        menu_main.addMenu(menu_file)
        menu_main.addMenu(menu_edit)
        act_about = QAction('О программе', self)
        act_about.triggered.connect(self.show_info)
        menu_main.addAction(act_about)
        self.setMenuBar(menu_main)

    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Выбрать рабочую директорию')
        if dir_name:
            # IMAGE_EXT
            self.lst_files.clear()
            self.lst_files.addItems(os.listdir(dir_name))

    def exit_prog(self):
        self.close()

    def show_info(self):
        self.prog_info = QMessageBox()
        self.prog_info.setWindowTitle('О программе')
        self.prog_info.setText('Эта программа предназначена\nдля трансформации изображений')
        self.prog_info.setWindowModality(Qt.ApplicationModal)
        self.prog_info.exec_()


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    os.environ['QT_PLUGIN_PATH'] = r'Lib\site-packages\PyQt5\Qt5\plugins'
    main()
