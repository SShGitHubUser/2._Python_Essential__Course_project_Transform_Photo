""" Модуль реализует функционал простого графического редактора, который позволяет производить трансформацию
выбранного графического файла по командам и сохранить результат """

import os
from PIL import Image
from PIL.ImageFilter import BLUR, SHARPEN, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, \
    FIND_EDGES, SMOOTH, SMOOTH_MORE, GaussianBlur, UnsharpMask
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, \
    QFileDialog, QMainWindow, QDesktopWidget, QListWidget, QGridLayout, QMessageBox, QMenuBar, QMenu, \
    QAction

IMAGE_EXT = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
SAVE_DIR = 'Modified/'
TEMP_FILE_NAME = 'image_tmp'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.prog_info = None
        self.workdir = ''
        self.file_name = ''
        self.temp_file_path = ''
        self.image = None
        self.lbl_image = QLabel('Загрузите изображение')
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.context_menu = QMenu(self.lbl_image)

        # Инициализируем параметры главного окна
        self.setWindowTitle('Трансформация изображений')
        screen = QDesktopWidget().screenGeometry()
        self.resize(int(0.75 * screen.width()), int(0.75 * screen.height()))

        # Создаём QAction сразу для всей программы
        act_open = self.create_action('Выбор директории', self.open_dir, 'Ctrl+O')
        act_save = self.create_action('Сохранить', self.save_image, 'Ctrl+S')
        act_exit = self.create_action('Выйти', self.exit_prog, '')

        act_left = self.create_action('Left', lambda: self.transform_image('Left'), '')
        act_right = self.create_action('Right', lambda: self.transform_image('Right'), '')
        act_flip = self.create_action('Flip', lambda: self.transform_image('Flip'), '')
        act_sharp = self.create_action('Sharp', lambda: self.transform_image('Sharp'), '')
        act_blur = self.create_action('Blur', lambda: self.transform_image('Blur'), '')
        act_edge_enhance = self.create_action('Edge enhance', lambda: self.transform_image('Edge enhance'), '')
        act_edge_enhance_more = self.create_action('Edge enhance more',
                                                   lambda: self.transform_image('Edge enhance more'), '')
        act_smooth = self.create_action('Smooth', lambda: self.transform_image('Smooth'), '')
        act_smooth_more = self.create_action('Smooth more', lambda: self.transform_image('Smooth more'), '')
        act_contour = self.create_action('Contour', lambda: self.transform_image('Contour'), '')
        act_emboss = self.create_action('Emboss', lambda: self.transform_image('Emboss'), '')
        act_gaussian_blur = self.create_action('Gaussian blur', lambda: self.transform_image('Gaussian blur'), '')
        act_unsharp_mask = self.create_action('Unsharp mask', lambda: self.transform_image('Unsharp mask'), '')
        act_detail = self.create_action('Detail', lambda: self.transform_image('Detail'), '')
        act_find_edges = self.create_action('Find edges', lambda: self.transform_image('Find edges'), '')
        act_b_w = self.create_action('B/W', lambda: self.transform_image('B/W'), '')

        act_about = self.create_action('О программе', self.show_info, '')

        # Добавляем главное меню
        menu_main = QMenuBar(self)
        self.setMenuBar(menu_main)
        # создаем меню Файл
        menu_file = QMenu('Файл', self)
        menu_file.addActions([act_open, act_save, act_exit])
        # создаем меню Преобразовать
        menu_edit = QMenu('Преобразовать', self)
        menu_edit.addActions(
            [act_left, act_right, act_sharp, act_blur, act_edge_enhance, act_edge_enhance_more, act_smooth,
             act_smooth_more, act_b_w, act_contour, act_flip, act_emboss, act_gaussian_blur, act_unsharp_mask,
             act_detail, act_find_edges])
        # добавляем все подменю в главное меню
        menu_main.addMenu(menu_file)
        menu_main.addMenu(menu_edit)
        menu_main.addAction(act_about)

        # Добавляем контекстное меню
        self.context_menu.addActions(
            [act_left, act_right, act_sharp, act_blur, act_edge_enhance, act_edge_enhance_more, act_smooth,
             act_smooth_more, act_b_w, act_contour, act_flip, act_emboss, act_gaussian_blur, act_unsharp_mask,
             act_detail, act_find_edges])
        # активируем контекстное меню
        self.lbl_image.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lbl_image.customContextMenuRequested.connect(self.show_context_menu)

        # Создаем макет левой части окна - для выбора графических файлов
        btn_dir = QPushButton('Выбор директории')
        btn_dir.clicked.connect(self.open_dir)
        self.lst_files = QListWidget()
        self.lst_files.currentRowChanged.connect(self.show_chosen_image)
        lo_left = QVBoxLayout()
        lo_left.addWidget(btn_dir)
        lo_left.addWidget(self.lst_files)

        # Создаем макет правой части - для выбора отображения выбранного файла и кнопок преобразования

        # Создаем кнопки для преобразования изображения и добавляем их в соответствующий макет
        btn_left = self.create_button(act_left)
        btn_right = self.create_button(act_right)
        btn_sharp = self.create_button(act_sharp)
        btn_blur = self.create_button(act_blur)
        btn_edge_enhance = self.create_button(act_edge_enhance)
        btn_edge_enhance_more = self.create_button(act_edge_enhance_more)
        btn_smooth = self.create_button(act_smooth)
        btn_smooth_more = self.create_button(act_smooth_more)
        btn_b_w = self.create_button(act_b_w)
        btn_contour = self.create_button(act_contour)
        btn_flip = self.create_button(act_flip)
        btn_emboss = self.create_button(act_emboss)
        btn_gaussian_blur = self.create_button(act_gaussian_blur)
        btn_unsharp_mask = self.create_button(act_unsharp_mask)
        btn_detail = self.create_button(act_detail)
        btn_find_edges = self.create_button(act_find_edges)

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
        lo_right = QVBoxLayout()
        lo_right.addWidget(self.lbl_image, stretch=95)
        lo_right.addLayout(lo_transform)

        # Создаем макет главного окна и добавляем в него макеты левой и правой части
        lo_main = QHBoxLayout()
        lo_main.addLayout(lo_left, stretch=20)
        lo_main.addLayout(lo_right, stretch=80)

        widget = QWidget()
        widget.setLayout(lo_main)
        self.setCentralWidget(widget)

    def create_action(self, text: str, function, shortcut: str) -> QAction:
        action = QAction(text, self)
        action.triggered.connect(function)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    @staticmethod
    def create_button(action: QAction) -> QPushButton:
        button = QPushButton(action.text())
        button.addAction(action)
        button.clicked.connect(action.trigger)
        return button

    def show_context_menu(self, position):
        global_position = self.lbl_image.mapToGlobal(position)
        self.context_menu.exec_(global_position)

    @staticmethod
    def filter_image(files: list) -> list:
        return [file_name for file_name in files if str(os.path.splitext(file_name)[1]).lower() in IMAGE_EXT]

    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Выбрать рабочую директорию')
        if dir_name:
            self.workdir = dir_name.replace('/', '\\')
            self.lst_files.clear()
            self.lst_files.addItems(self.filter_image(os.listdir(self.workdir)))

    def load_image(self, image_path):
        self.lbl_image.hide()
        self.image = Image.open(image_path)
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.lbl_image.width(), self.lbl_image.height(), Qt.KeepAspectRatio)
        self.lbl_image.setPixmap(pixmap)
        self.lbl_image.show()

    def show_chosen_image(self):
        if self.lst_files.currentRow() >= 0:
            self.delete_temp_file()
            self.file_name = self.lst_files.currentItem().text()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.temp_file_path = os.path.join(script_dir, TEMP_FILE_NAME + os.path.splitext(self.file_name)[1])
            self.load_image(os.path.join(self.workdir, self.file_name))

    def save_image(self):
        full_path = os.path.join(self.workdir, SAVE_DIR)
        if not (os.path.exists(full_path) or os.path.isdir(full_path)):
            os.mkdir(full_path)
        self.image.save(os.path.join(full_path, self.file_name))

    def reload_image(self):
        self.image.save(self.temp_file_path)
        self.load_image(self.temp_file_path)

    def delete_temp_file(self):
        if self.temp_file_path:
            self.image.close()
            os.remove(self.temp_file_path)

    def exit_prog(self):
        self.delete_temp_file()
        self.close()

    def transform_image(self, command):
        commands = {'Left': self.image.transpose(Image.ROTATE_90),
                    'Right': self.image.transpose(Image.ROTATE_270),
                    'Sharp': self.image.filter(SHARPEN),
                    'Blur': self.image.filter(BLUR),
                    'Edge enhance': self.image.filter(EDGE_ENHANCE),
                    'Edge enhance more': self.image.filter(EDGE_ENHANCE_MORE),
                    'Smooth': self.image.filter(SMOOTH),
                    'Smooth more': self.image.filter(SMOOTH_MORE),
                    'B/W': self.image.convert("L"),
                    'Contour': self.image.filter(CONTOUR),
                    'Flip': self.image.transpose(Image.FLIP_LEFT_RIGHT),
                    'Emboss': self.image.filter(EMBOSS),
                    'Gaussian blur': self.image.filter(GaussianBlur),
                    'Unsharp mask': self.image.filter(UnsharpMask),
                    'Detail': self.image.filter(DETAIL),
                    'Find edges': self.image.filter(FIND_EDGES)
                    }
        self.image = commands.get(command)
        self.reload_image()

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
