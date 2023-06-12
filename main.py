import os

from PIL import Image
from PIL.ImageFilter import BLUR, SHARPEN, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, \
    FIND_EDGES, SMOOTH, SMOOTH_MORE, GaussianBlur, UnsharpMask
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, \
    QFileDialog, QMainWindow, QDesktopWidget, QListWidget, QGridLayout, QMessageBox, QMenuBar, QMenu, \
    QAction

IMAGE_EXT = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
SAVE_DIR = 'Modified/'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.prog_info = None
        self.workdir = ''
        self.file_name = ''
        self.image = None
        self.lbl_image = QLabel('Загрузите изображение')
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.context_menu = QMenu(self.lbl_image)
        # self.work_image = ImageTransform()

        # Инициализируем параметры главного окна
        self.setWindowTitle('Трансформация изображений')
        screen = QDesktopWidget().screenGeometry()
        self.resize(int(0.75 * screen.width()), int(0.75 * screen.height()))

        # Создаём QAction сразу для всей программы
        # todo: добавить в меню короткие клавиши, enabled и комментарии где чего
        act_open = self.create_action('Выбор директории', self.open_dir, 'Ctrl+O')
        act_save = self.create_action('Сохранить', self.save_image, 'Ctrl+S')
        # act_save.setEnabled()
        act_exit = self.create_action('Выйти', self.exit_prog, '')

        act_left = self.create_action('Left', lambda: self.transform_image('Left'), '')
        act_right = self.create_action('Right', lambda: self.transform_image('Right'), '')
        act_sharp = self.create_action('Sharp', lambda: self.transform_image('Sharp'), '')
        act_blur = self.create_action('Blur', lambda: self.transform_image('Blur'), '')
        act_edge_enhance = self.create_action('Edge enhance', lambda: self.transform_image('Edge enhance'), '')
        act_edge_enhance_more = self.create_action('Edge enhance more',
                                                   lambda: self.transform_image('Edge enhance more'), '')
        act_smooth = self.create_action('Smooth', lambda: self.transform_image('Smooth'), '')
        act_smooth_more = self.create_action('Smooth more', lambda: self.transform_image('Smooth more'), '')
        act_b_w = self.create_action('B/W', lambda: self.transform_image('B_W'), '')
        act_contour = self.create_action('Contour', lambda: self.transform_image('Contour'), '')
        act_flip = self.create_action('Flip', lambda: self.transform_image('Flip'), '')
        act_emboss = self.create_action('Emboss', lambda: self.transform_image('Emboss'), '')
        act_gaussian_blur = self.create_action('Gaussian blur', lambda: self.transform_image('Gaussian blur'), '')
        act_unsharp_mask = self.create_action('Unsharp mask', lambda: self.transform_image('Unsharp mask'), '')
        act_detail = self.create_action('Detail', lambda: self.transform_image('Detail'), '')
        act_find_edges = self.create_action('Find edges', lambda: self.transform_image('Find edges'), '')

        act_about = self.create_action('О программе', self.show_info, '')

        # Добавляем главное меню
        menu_main = QMenuBar(self)
        self.setMenuBar(menu_main)
        # создаем меню Файл
        menu_file = QMenu('Файл', self)
        menu_file.addAction(act_open)
        menu_file.addAction(act_save)
        menu_file.addAction(act_exit)
        # создаем меню Преобразовать
        menu_edit = QMenu('Преобразовать', self)
        menu_edit.addAction(act_left)
        menu_edit.addAction(act_right)
        menu_edit.addAction(act_sharp)
        menu_edit.addAction(act_blur)
        menu_edit.addAction(act_edge_enhance)
        menu_edit.addAction(act_edge_enhance_more)
        menu_edit.addAction(act_smooth)
        menu_edit.addAction(act_smooth_more)
        menu_edit.addAction(act_b_w)
        menu_edit.addAction(act_contour)
        menu_edit.addAction(act_flip)
        menu_edit.addAction(act_emboss)
        menu_edit.addAction(act_gaussian_blur)
        menu_edit.addAction(act_unsharp_mask)
        menu_edit.addAction(act_detail)
        menu_edit.addAction(act_find_edges)
        # добавляем все подменю в главное меню
        menu_main.addMenu(menu_file)
        menu_main.addMenu(menu_edit)
        menu_main.addAction(act_about)

        # Добавляем контекстное меню
        self.context_menu.addAction(act_left)
        self.context_menu.addAction(act_left)
        self.context_menu.addAction(act_right)
        self.context_menu.addAction(act_sharp)
        self.context_menu.addAction(act_blur)
        self.context_menu.addAction(act_edge_enhance)
        self.context_menu.addAction(act_edge_enhance_more)
        self.context_menu.addAction(act_smooth)
        self.context_menu.addAction(act_smooth_more)
        self.context_menu.addAction(act_b_w)
        self.context_menu.addAction(act_contour)
        self.context_menu.addAction(act_flip)
        self.context_menu.addAction(act_emboss)
        self.context_menu.addAction(act_gaussian_blur)
        self.context_menu.addAction(act_unsharp_mask)
        self.context_menu.addAction(act_detail)
        self.context_menu.addAction(act_find_edges)
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

        # Создаем кнопки для преобразования изображения и добавляем их в макет для них
        btn_left = QPushButton(act_left.text())
        btn_left.addAction(act_left)

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

    def show_chosen_image(self):
        if self.lst_files.currentRow() >= 0:
            self.lbl_image.hide()
            self.file_name = self.lst_files.currentItem().text()
            full_path = os.path.join(self.workdir, self.file_name)
            self.image = Image.open(full_path)
            pixmap = QPixmap(full_path)
            pixmap = pixmap.scaled(self.lbl_image.width(), self.lbl_image.height(), Qt.KeepAspectRatio)
            self.lbl_image.setPixmap(pixmap)
            self.lbl_image.show()

    def save_image(self):
        full_path = os.path.join(self.workdir, SAVE_DIR)
        if not (os.path.exists(full_path) or os.path.isdir(full_path)):
            os.mkdir(full_path)
        self.image.save(os.path.join(full_path, self.file_name))

    def exit_prog(self):
        self.close()

    def transform_image(self, command):
        if command == 'Left':
            self.image = self.image.transpose(Image.ROTATE_90)
        if command == 'Right':
            self.image = self.image.transpose(Image.ROTATE_270)
        if command == 'Sharp':
            self.image = self.image.filter(Image.SHARPEN)
        if command == 'Blur':
            self.image = self.image.filter(Image.BLUR)
        if command == 'Edge enhance':
            self.image = self.image.filter(Image.EDGE_ENHANCE)
        if command == 'Edge enhance more':
            self.image = self.image.filter(Image.EDGE_ENHANCE_MORE)
        elif command == 'contour':
            self.image = self.image.filter(ImageFilter.CONTOUR)
        elif command == 'detail':
            self.image = self.image.filter(ImageFilter.DETAIL)
        elif command == 'edge_enhance':
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        elif command == 'edge_enhance_more':
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        elif command == 'emboss':
            self.image = self.image.filter(ImageFilter.EMBOSS)
        elif command == 'find_edges':
            self.image = self.image.filter(ImageFilter.FIND_EDGES)
        elif command == 'gaussian_blur':
            self.image = self.image.filter(ImageFilter.GaussianBlur)
        self.save_image()
        pass

    act_smooth = self.create_action('Smooth', lambda: self.transform_image('Smooth'), '')
    act_smooth_more = self.create_action('Smooth more', lambda: self.transform_image('Smooth more'), '')
    act_b_w = self.create_action('B/W', lambda: self.transform_image('B_W'), '')
    act_contour = self.create_action('Contour', lambda: self.transform_image('Contour'), '')
    act_flip = self.create_action('Flip', lambda: self.transform_image('Flip'), '')
    act_emboss = self.create_action('Emboss', lambda: self.transform_image('Emboss'), '')
    act_gaussian_blur = self.create_action('Gaussian blur', lambda: self.transform_image('Gaussian blur'), '')
    act_unsharp_mask = self.create_action('Unsharp mask', lambda: self.transform_image('Unsharp mask'), '')
    act_detail = self.create_action('Detail', lambda: self.transform_image('Detail'), '')
    act_find_edges = self.create_action('Find edges', lambda: self.transform_image('Find edges'), '')

    #
    #
    #     def do_b_w(self):
    #         self.image = self.image.convert("L")
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #
    #
    #     def do_flip(self):
    #         self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #
    #     def do_contour(self):
    #         self.image = self.image.filter(CONTOUR)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #     def do_detail(self):
    #         self.image = self.image.filter(DETAIL)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #
    #     def do_emboss(self):
    #         self.image = self.image.filter(EMBOSS)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #     def do_find_edges(self):
    #         self.image = self.image.filter(FIND_EDGES)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #     def do_smooth(self):
    #         self.image = self.image.filter(SMOOTH)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #     def do_smooth_more(self):
    #         self.image = self.image.filter(SMOOTH_MORE)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #     def do_gaussian_blur(self):
    #         self.image = self.image.filter(GaussianBlur)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
    #
    #     def do_unsharp_mask(self):
    #         self.image = self.image.filter(UnsharpMask)
    #         """self.save_image()
    #         image_path = os.path.join(workdir, self.save_dir, self.filename)
    #         self.show_image(image_path)"""
    #         self.save_image()
    #         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))

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
