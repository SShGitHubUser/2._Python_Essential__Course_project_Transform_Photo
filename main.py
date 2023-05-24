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

        self.image = None
        self.prog_info = None
        self.workdir = ''
        self.file_name = ''
        self.lbl_image = QLabel('Загрузите изображение')
        self.lbl_image.setAlignment(Qt.AlignCenter)
        # self.lbl_image.setScaledContents(True)
        # self.work_image = ImageTransform()

        # Инициализируем параметры главного окна
        self.setWindowTitle('Трансформация изображений')
        screen = QDesktopWidget().screenGeometry()
        self.resize(int(0.75 * screen.width()), int(0.75 * screen.height()))

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
        lo_right = QVBoxLayout()
        lo_right.addWidget(self.lbl_image, 95)
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
            self.image = Image.open(os.path.join(self.workdir, self.file_name))
            pixmap = QPixmap.fromImage(
                QImage(self.image.tobytes(), self.image.size[0], self.image.size[1], QImage.Format_RGB888))
            pixmap = pixmap.scaled(self.lbl_image.width(), self.lbl_image.height(), Qt.KeepAspectRatio)
            self.lbl_image.setPixmap(pixmap)
            self.lbl_image.show()

    def exit_prog(self):
        self.close()

    def show_info(self):
        self.prog_info = QMessageBox()
        self.prog_info.setWindowTitle('О программе')
        self.prog_info.setText('Эта программа предназначена\nдля трансформации изображений')
        self.prog_info.setWindowModality(Qt.ApplicationModal)
        self.prog_info.exec_()


# class ImageTransform:
#     def __init__(self):
#         self.image = None
#         self.dir = None
#         self.filename = None
#
#     def load_image(self, workdir, filename):
#         self.filename = filename
#         fullname = os.path.join(workdir, filename)
#         self.image = Image.open(fullname)
#
#     def save_image(self, workdir):
#         path = os.path.join(workdir, SAVE_DIR)
#         if not (os.path.exists(path) or os.path.isdir(path)):
#             os.mkdir(path)
#         fullname = os.path.join(path, self.filename)
#         self.image.save(fullname)
#
#     def show_image(self, workdir, filename):
#         fullname = os.path.join(workdir, filename)
#         self.lbl_image.hide()
#         pixmap = QPixmap(fullname)
#         w, h = lb_image.width(), lb_image.height()
#         pixmap_image = pixmap_image.scaled(w, h, Qt.KeepAspectRatio)
#         lb_image.setPixmap(pixmap_image)
#         lb_image.show()
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
#     def turn_left(self):
#         self.image = self.image.transpose(Image.ROTATE_90)
#         """self.save_image()
#         image_path = os.path.join(workdir, self.save_dir, self.filename)
#         self.show_image(image_path)"""
#         self.save_image()
#         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
#
#     def turn_right(self):
#         self.image = self.image.transpose(Image.ROTATE_270)
#         """self.save_image()
#         image_path = os.path.join(workdir, self.save_dir, self.filename)
#         self.show_image(image_path)"""
#         self.save_image()
#         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
#
#     def do_flip(self):
#         self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
#         """self.save_image()
#         image_path = os.path.join(workdir, self.save_dir, self.filename)
#         self.show_image(image_path)"""
#         self.save_image()
#         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
#
#     def do_blur(self):
#         self.image = self.image.filter(BLUR)
#         """self.save_image()
#         image_path = os.path.join(workdir, self.save_dir, self.filename)
#         self.show_image(image_path)"""
#         self.save_image()
#         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
#
#     def do_sharpen(self):
#         self.image = self.image.filter(SHARPEN)
#         """self.save_image()
#         image_path = os.path.join(workdir, self.save_dir, self.filename)
#         self.show_image(image_path)"""
#         self.save_image()
#         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
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
#     def do_edge_enhance(self):
#         self.image = self.image.filter(EDGE_ENHANCE)
#         """self.save_image()
#         image_path = os.path.join(workdir, self.save_dir, self.filename)
#         self.show_image(image_path)"""
#         self.save_image()
#         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
#
#     def do_edge_enhance_more(self):
#         self.image = self.image.filter(EDGE_ENHANCE_MORE)
#         """self.save_image()
#         image_path = os.path.join(workdir, self.save_dir, self.filename)
#         self.show_image(image_path)"""
#         self.save_image()
#         self.show_image(os.path.join(workdir, SAVE_DIR, self.filename))
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


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    os.environ['QT_PLUGIN_PATH'] = r'Lib\site-packages\PyQt5\Qt5\plugins'
    main()
