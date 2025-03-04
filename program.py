import sys
import os
import psutil
import shutil
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QComboBox, QDialog, QMessageBox
from PyQt6.QtGui import QPalette, QColor, QIcon, QPixmap, QPainter, QPainterPath, QBitmap, QDesktopServices
from PyQt6.QtCore import Qt, QSettings, QSize, QUrl




def get_circular_mask(size):
 mask = QPixmap(size)
 mask.fill(Qt.GlobalColor.transparent)
 painter = QPainter(mask)
 painter.setRenderHint(QPainter.RenderHint.Antialiasing)
 path = QPainterPath()
 path.addEllipse(0, 0, size.width(), size.height())
 painter.fillPath(path, QColor(Qt.GlobalColor.white))
 painter.end()
 return mask


class ProfileManager(QtWidgets.QWidget):

  def __init__(self):
   super().__init__()

   
   self.current_language = "English"
   self.language_translations = {
      "English": {
          "app_title": "NikkeProfilesSwitch - Profile Selector",
          "select_profile_title": "Select a profile",
          "info_window_title": "NikkeProfilesSwitch",
          "dev_info": "Developed by <b>Robeth Monsalve</b>",
          "app_info": "This application is completely free. I would appreciate any donation that allows me to develop more applications like this, thank you :).",
          "donate": "Donate",
          "info": "Info",
          "github": "GitHub",
          "version_label": "Version - 1.0.0",
          "version": "Version",
          "info_window_title_bar": "NikkeProfilesSwitch",
          "add_profile_dialog_title": "Add Profile",
          "add_profile_dialog_text": "Profile name..",
          "input_title_dialog_text": "New Profile",
          "existing_profile_warning_title": "Existing Name",
          "existing_profile_warning_text": "A profile with that name already exists.",
          "delete_profile_title": "Delete Profile",
          "delete_profile_text": "Are you sure you want to delete the profile",
          "error_title": "Error deleting",
          "error_text": "Could not delete profile",
          "image_action": "Image",
          "rename_action": "Rename",
          "delete_action": "Delete",
          "launcher_warn_title": "Warning",
          "launcher_warn": "Please close the Nikke launcher before switching profiles."

      },
      "Español": {
          "app_title": "NikkeProfilesSwitch - Selector de Perfiles",
          "select_profile_title": "Selecciona un perfil",
          "info_window_title": "NikkeProfilesSwitch",
          "dev_info": "Desarrollado por <b>Robeth Monsalve</b>",
          "app_info": "Esta aplicación es completamente gratuita. Agradecería cualquier donación que me permita desarrollar más aplicaciones como esta, gracias :).",
          "donate": "Donar",
          "info": "Info",
          "github": "GitHub",
          "version_label": "Versión - 1.0.0",
          "version": "Versión",
          "info_window_title_bar": "NikkeProfilesSwitch",
          "add_profile_dialog_title": "Añadir Perfil",
          "add_profile_dialog_text": "Nombre del perfil...",
          "input_title_dialog_text": "Nuevo Perfil",
          "existing_profile_warning_title": "Nombre Existente",
          "existing_profile_warning_text": "Ya existe un perfil con ese nombre.",
          "delete_profile_title": "Eliminar Perfil",
          "delete_profile_text": "¿Seguro que quieres eliminar el perfil",
          "error_title": "Error al Eliminar",
          "error_text": "No se pudo eliminar el perfil",
          "image_action": "Imagen",
          "rename_action": "Renombrar",
          "delete_action": "Eliminar",
          "launcher_warn_title": "Advertencia",
          "launcher_warn": "Por favor, cierre el launcher de Nikke antes de cambiar de perfil.",
      }
  }

   self.settings = QSettings("NikkeProfilesSwitch", "LanguageSettings") 
   self.nikke_launcher_path = os.path.join(os.getenv("APPDATA"), "nikke_launcher")
   self.load_language_setting()
   self.init_ui()
   self.create_profiles_directory()
   self.load_profiles()


  def init_ui(self):

    self.setWindowTitle(self.language_translations[self.current_language]["app_title"])

    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return relative_path
    
    icon_path = resource_path("resources/icon.png")
    window_icon = QIcon(icon_path)
    self.setWindowIcon(window_icon)

    
    screen = QtWidgets.QApplication.primaryScreen()
    screen_rect = screen.availableGeometry()

    
    window_width = 1024
    window_height = 768
    x = (screen_rect.width() - window_width) // 2
    y = (screen_rect.height() - window_height) // 2
    self.setGeometry(x, y, window_width, window_height)

    self.main_layout = QGridLayout(self)
    self.setLayout(self.main_layout)

    top_left_layout = QHBoxLayout()  

    self.language_icon = QLabel()
    self.language_icon.setFixedSize(50, 50)

    icon_lang = resource_path("resources/lang.png")
    pixmap = QPixmap(icon_lang)  
    self.language_icon.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    self.language_icon.setStyleSheet("border-radius: 25px; background: transparent;") 

    top_left_layout.addWidget(self.language_icon)


    self.language_combo = QComboBox()
    self.language_combo.addItems(["English", "Español"])
    self.language_combo.setCurrentText(self.current_language)  
    self.language_combo.setFixedSize(100, 30)  
    self.language_combo.setStyleSheet("QComboBox { background: transparent; }")  
    self.language_combo.currentIndexChanged.connect(self.change_language)
    top_left_layout.addWidget(self.language_combo)

    top_left_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    
    self.main_layout.addLayout(top_left_layout, 0, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


    self.top_right_button = QPushButton()
    self.top_right_button.setFixedSize(50, 50)
    self.top_right_button.setStyleSheet("""
        QPushButton {
            border-radius: 25px;
            background-color: transparent;
        }
        QPushButton:hover {
            background-color: deepskyblue;
        }
    """)

    self.main_layout.setContentsMargins(30, 30, 30, 30)

    icon_path = resource_path("resources/info.png")
    icon = QIcon(icon_path)
    self.top_right_button.setIcon(icon)
    self.top_right_button.setIconSize(QSize(50, 50))

    self.main_layout.addWidget(self.top_right_button, 0, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
    self.top_right_button.clicked.connect(self.open_info_window)

    self.title_label = QLabel(self.language_translations[self.current_language]["select_profile_title"])
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    self.title_label.setObjectName("titleLabel")
    self.title_label.setStyleSheet("font-size: 36px; color: white; background: transparent;")

    self.profiles_area_layout = QHBoxLayout()
    self.profiles_circle_layout = QGridLayout()
    self.add_button_layout = QVBoxLayout()
    self.profile_buttons = {}
    self.selected_profile = None

    self.add_profile_button = QPushButton()
    self.add_profile_button.setObjectName("addButton")
    self.add_profile_button.setFixedSize(160, 160)

    icon_path = resource_path("resources/add.png")
    icon = QIcon(icon_path)
    self.add_profile_button.setIcon(icon)
    self.add_profile_button.setIconSize(QSize(160, 160))
    self.add_profile_button.clicked.connect(self.add_profile)

    self.add_button_layout.addWidget(self.add_profile_button)
    self.add_button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.profiles_area_layout.addLayout(self.profiles_circle_layout)
    self.profiles_area_layout.addLayout(self.add_button_layout)
    self.profiles_area_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    self.profiles_area_layout.setSpacing(30)
    self.profiles_area_layout.setContentsMargins(0, 100, 0, 100)

    self.content_layout = QVBoxLayout()
    self.content_layout.addWidget(self.title_label)
    self.content_layout.addLayout(self.profiles_area_layout)
    self.content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    self.main_layout.addLayout(self.content_layout, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

    version_text = self.language_translations[self.current_language]["version_label"]
    self.beta_label = QLabel(version_text)
    self.beta_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
    self.beta_label.setStyleSheet("color: rgba(255, 255, 255, 140); font-size: 15px; background: transparent;")

    self.main_layout.addWidget(self.beta_label, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

    nebula_lighter = "#2b004a"
    nebula_bg = "#190033"
    nebula_darker = "#0b0020"
    nebula_more_darker = "#040010"

    self.setStyleSheet(f"""
    QWidget {{
        background: qradialgradient(cx:0.5, cy:0.5, radius:0.9,
        stop:0.0 {nebula_lighter},
        stop:0.3 {nebula_bg},
        stop:0.6 {nebula_darker},
        stop:0.9 {nebula_more_darker},
        stop:1.0 black);
        font-size: 20px;
        color: lightgray;
    }}
    QPushButton#addButton, QPushButton[objectName^="profileButton_"] {{
        background-color: transparent;
        border-radius: 75px;
        border: 2px solid black;
        padding: 15px;
    }}
    QPushButton#addButton:hover, QPushButton[objectName^="profileButton_"]:hover {{
        background-color: deepskyblue;
    }}
    QLabel#addLabel, QLabel[objectName^="profileLabel_"] {{
        background-color: transparent;
        qproperty-alignment: 'AlignCenter';
        font-size: 30px;
        color: white;
    }}
    """)

    


  def change_language(self, index):
        selected_language = self.language_combo.itemText(index)
        if selected_language in self.language_translations:
            self.current_language = selected_language
            self.setWindowTitle(self.language_translations[self.current_language]["app_title"])
            self.title_label.setText(self.language_translations[self.current_language]["select_profile_title"])
            version_text = self.language_translations[self.current_language]["version_label"]
            version_text = version_text.replace("Version", self.language_translations[self.current_language]["version"]) 
            self.beta_label.setText(version_text)
            self.save_language_setting() 

  def load_language_setting(self):
        lang = self.settings.value("language", "English") 
        if lang in self.language_translations:
            self.current_language = lang
        else:
            self.current_language = "English" 

  def save_language_setting(self):
        self.settings.setValue("language", self.current_language)

  def closeEvent(self, event):
        self.save_language_setting() 
        event.accept()

  def open_info_window(self):
    info_window = QDialog(self)
    info_window.setWindowTitle(self.language_translations[self.current_language]["info_window_title_bar"])  
    info_window.setFixedSize(400, 570) 
    info_window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return relative_path

    layout = QVBoxLayout(info_window)

    icon_path = resource_path("resources/icon.png")
    image_label = QLabel()
    pixmap = QPixmap(icon_path)
    if not pixmap.isNull():
        size = 150  
        pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        mask = QBitmap(pixmap.size())
        mask.fill(Qt.GlobalColor.white)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawEllipse(0, 0, size, size)
        painter.end()

        pixmap.setMask(mask)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(image_label)
    else:
        print("Error: No se pudo cargar la imagen.")

    title_label = QLabel(f"<h2>{self.language_translations[self.current_language]['info_window_title']}</h2>")  
    title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(title_label)

    layout.addSpacing(10)  

    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    layout.addWidget(line)
    layout.addSpacing(10)  

    dev_info = QLabel(self.language_translations[self.current_language]["dev_info"])  
    dev_info.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(dev_info)

    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    layout.addWidget(line)
    layout.addSpacing(10) 

    app_info = QLabel(self.language_translations[self.current_language]["app_info"])  
    app_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
    app_info.setWordWrap(True) 
    layout.addWidget(app_info)

    layout.addSpacing(10)  

    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    layout.addWidget(line)
    layout.addSpacing(10) 

    def create_circular_icon(icon_path, size):
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(size.width(), size.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        mask = QBitmap(pixmap.size())
        mask.fill(Qt.GlobalColor.white)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawEllipse(0, 0, size.width(), size.height())
        painter.end()

        pixmap.setMask(mask)
        return pixmap

    button_layout = QHBoxLayout()

    button1 = QPushButton()
    button2 = QPushButton()
    button3 = QPushButton()

    button_size = QSize(80, 80)
    button1.setFixedSize(button_size)
    button2.setFixedSize(button_size)
    button3.setFixedSize(button_size)

    icon_pp = resource_path("resources/paypal.png")
    icon_kf = resource_path("resources/ko-fi.jpg")
    icon_gh = resource_path("resources/github.png")

    button1.setIcon(QIcon(create_circular_icon(icon_kf, QSize(70, 70))))
    button2.setIcon(QIcon(create_circular_icon(icon_pp, QSize(70, 70))))
    button3.setIcon(QIcon(create_circular_icon(icon_gh, QSize(70, 70))))

    button1.setIconSize(QSize(70, 70))
    button2.setIconSize(QSize(70, 70))
    button3.setIconSize(QSize(70, 70))

    button_style = "QPushButton { border-radius: 40px; background-color: #e0e0e0; border: none; }" 
    button1.setStyleSheet(button_style)
    button2.setStyleSheet(button_style)
    button3.setStyleSheet(button_style)


    button1.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://ko-fi.com/roberthmz")))
    button2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://paypal.me/zhionmz?country.x=VE&locale.x=es_XC")))
    button3.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/RoberthMZ/NikkeProfilesSwitch")))

    button_layout.addWidget(button1)
    button_layout.addWidget(button2)
    button_layout.addWidget(button3)

    layout.addLayout(button_layout)
    layout.addSpacing(10)  

    info_window.setStyleSheet("background: none;")
    title_label.setStyleSheet("background: none; color: white;")
    dev_info.setStyleSheet("background: none; color: white;")
    app_info.setStyleSheet("background: none; color: white;")
    image_label.setStyleSheet("background: none;")

    info_window.setLayout(layout)
    info_window.exec() 

  def create_profiles_directory(self):
   profile_dir = os.path.join(os.getcwd(), "profiles")
   os.makedirs(profile_dir, exist_ok=True)

   default_profile_path = os.path.join(profile_dir, "Default")
   os.makedirs(default_profile_path, exist_ok=True)

  def load_profiles(self):
   profile_dir = os.path.join(os.getcwd(), "profiles")
   profiles = os.listdir(profile_dir)

   row = 0
   col = 0
   for profile in profiles:
    if profile == ".DS_Store": 
     continue
    self.create_profile_button(profile, row, col)
    col += 1
    if col == 4:
     col = 0
     row += 1

   last_selected = self.load_last_selected_profile()

   if last_selected:
    if last_selected in profiles:
     self.select_profile(last_selected)
    elif "Default" in profiles:
     self.select_profile("Default")
    elif profiles:
     self.select_profile(profiles[0] if profiles[0] != ".DS_Store" else (profiles[1] if len(profiles) > 1 else "Default"))
    else:
     self.select_profile("Default")
   elif "Default" not in profiles:
    self.select_profile("Default")
   elif profiles:
    self.select_profile(profiles[0] if profiles[0] != ".DS_Store" else (profiles[1] if len(profiles) > 1 else "Default"))
   else:
    self.select_profile("Default")
   self.check_nikke_launcher()
   self.show()
   

  def select_profile(self, profile_name):
    if self.selected_profile is not None:
        self.move_nikke_launcher_to_profiles(self.selected_profile)

        if not os.path.exists(self.nikke_launcher_path):
            self.move_nikke_launcher_if_exists(profile_name)

    self.selected_profile = profile_name
    self.update_profile_highlight()
    self.save_last_selected_profile()

  def check_nikke_launcher(self, profile_name=None):
    if any(proc.name() == "nikke_launcher.exe" for proc in psutil.process_iter()):
        self.show_warning("warning_launcher", self.current_language)
    elif profile_name is not None: 
        self.select_profile(profile_name)

  

  def show_warning(self, warning_type, language):
    msg_box = QMessageBox()

    if language == "English":
        title = self.language_translations["English"]["launcher_warn_title"]
        message = self.language_translations["English"]["launcher_warn"]
    elif language == "Español":
        title = self.language_translations["Español"]["launcher_warn_title"]
        message = self.language_translations["Español"]["launcher_warn"]

    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return relative_path

    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    icon_path = resource_path("resources/icon.png")
    window_icon = QIcon(icon_path)
    msg_box.setWindowIcon(window_icon)

    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: transparent;
        }
        QLabel {
            background-color: transparent;
            font-size: 20px;  
        }
        QPushButton {
            background-color: transparent;
            font-size: 20px;  
            padding: 10px;   
            min-width: 100px; 
        }
    """)

    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.exec()





  def create_profile_button(self, profile_name, row, col):
    profile_layout = QtWidgets.QVBoxLayout()

    button = QtWidgets.QPushButton("")
    button.setObjectName(f"profileButton_{profile_name}") 
    button.setFixedSize(160, 160)  
    button.setStyleSheet("""
        QPushButton {
            background-color: lightgray;
            border-radius: 75px;  
            border: 2px solid white;  
            padding: 0;  
        }
        QPushButton:hover {
            background-color: #c0c0c0;
        }
    """)
    button.clicked.connect(lambda: self.check_nikke_launcher(profile_name))

    button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    button.customContextMenuRequested.connect(lambda point: self.show_profile_context_menu(point, profile_name, button))

    profile_label = QtWidgets.QLabel(profile_name)
    profile_label.setObjectName(f"profileLabel_{profile_name}") 
    profile_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    profile_layout.addWidget(button)
    profile_layout.addWidget(profile_label)
    profile_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    image_path = self.get_profile_image_path(profile_name)
    if os.path.exists(image_path):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

        circular_mask = get_circular_mask(scaled_pixmap.size())  
        scaled_pixmap.setMask(circular_mask.mask())  

        button.setIcon(QIcon(scaled_pixmap))
        button.setIconSize(scaled_pixmap.size())

    self.profile_buttons[profile_name] = {'button': button, 'label': profile_label}
    self.profiles_circle_layout.addLayout(profile_layout, row, col)



  def show_profile_context_menu(self, point, profile_name, button):
    menu = QtWidgets.QMenu(self)

    image_action = menu.addAction(self.language_translations[self.current_language]["image_action"])
    image_action.triggered.connect(lambda: self.set_profile_image(profile_name, button))

    rename_action = menu.addAction(self.language_translations[self.current_language]["rename_action"])
    rename_action.triggered.connect(lambda: self.rename_profile(profile_name))

    delete_action = menu.addAction(self.language_translations[self.current_language]["delete_action"])
    delete_action.triggered.connect(lambda: self.delete_profile(profile_name))

    menu.exec(button.mapToGlobal(point))

  def set_profile_image(self, profile_name, button):
   file_dialog = QtWidgets.QFileDialog()
   file_path, _ = file_dialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imagenes (*.png *.jpg *.jpeg)")
   if file_path:
    profile_image_path = self.get_profile_image_path(profile_name)
    shutil.copy(file_path, profile_image_path) 
    pixmap = QPixmap(profile_image_path)
    scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

    circular_mask = get_circular_mask(scaled_pixmap.size()) 
    scaled_pixmap.setMask(circular_mask.mask()) 

    button.setIcon(QIcon(scaled_pixmap))
    button.setIconSize(scaled_pixmap.size())


  def rename_profile(self, profile_name):
   text, ok = QtWidgets.QInputDialog.getText(self, "Renombrar Perfil", "Nuevo nombre para el perfil:", text=profile_name)
   if ok and text and text != profile_name:
    new_profile_name = text
    old_profile_path = os.path.join(os.getcwd(), "profiles", profile_name)
    new_profile_path = os.path.join(os.getcwd(), "profiles", new_profile_name)

    if not os.path.exists(new_profile_path):
     try:
      os.rename(old_profile_path, new_profile_path)

      profile_data = self.profile_buttons.pop(profile_name) 
      self.profile_buttons[new_profile_name] = profile_data 
      profile_data['label'].setText(new_profile_name)

      if self.selected_profile == profile_name:
       self.selected_profile = new_profile_name
       self.save_last_selected_profile()

      self.reload_profile_buttons()

     except OSError as e:
      QtWidgets.QMessageBox.critical(self, "Error al Renombrar", f"No se pudo renombrar el perfil: {e}")
    else:
     QtWidgets.QMessageBox.warning(self, "Nombre Existente", "Ya existe un perfil con ese nombre.")


  def delete_profile(self, profile_name):
    reply = QtWidgets.QMessageBox.question(self, 
                                           self.language_translations[self.current_language]["delete_profile_title"],
                                           f"{self.language_translations[self.current_language]['delete_profile_text']} '{profile_name}'?",
                                           QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

    if reply == QtWidgets.QMessageBox.StandardButton.Yes:
        profile_path = os.path.join(os.getcwd(), "profiles", profile_name)
        try:
            shutil.rmtree(profile_path)
            profile_layout_item = None
            for i in range(self.profiles_circle_layout.count()):
                layout_item = self.profiles_circle_layout.itemAt(i)
                if layout_item and isinstance(layout_item, QtWidgets.QLayout):
                    label_item = layout_item.itemAt(1)
                    if label_item and isinstance(label_item.widget(), QtWidgets.QLabel) and label_item.widget().text() == profile_name:
                        profile_layout_item = layout_item
                        break
            
            if profile_layout_item:
                self.profiles_circle_layout.removeItem(profile_layout_item)  
                for i in reversed(range(profile_layout_item.count())):
                    item = profile_layout_item.itemAt(i).widget()
                    if item:
                        item.setParent(None)  
                profile_layout_item.deleteLater()  

            del self.profile_buttons[profile_name]  

            if self.selected_profile == profile_name:
                self.selected_profile = None
                self.save_last_selected_profile()  

            self.reload_profile_buttons()

        except OSError as e:
            QtWidgets.QMessageBox.critical(self, 
                                            self.language_translations[self.current_language]["error_title"], 
                                            f"{self.language_translations[self.current_language]['error_text']}: {e}")


  def reload_profile_buttons(self):
   for i in reversed(range(self.profiles_circle_layout.count())):
    layout_item = self.profiles_circle_layout.itemAt(i)
    if layout_item and isinstance(layout_item, QtWidgets.QLayout):
     for j in reversed(range(layout_item.count())):
      item = layout_item.itemAt(j).widget()
      if item:
       item.setParent(None) 
     self.profiles_circle_layout.removeItem(layout_item) 

   self.profile_buttons = {}
   self.load_profiles() 




  def add_profile(self):
    dialog_title = self.language_translations[self.current_language]["add_profile_dialog_title"]
    dialog_text = self.language_translations[self.current_language]["add_profile_dialog_text"]
    dialog_inputtitle = self.language_translations[self.current_language]["input_title_dialog_text"]

    dialog = QtWidgets.QDialog(self)
    dialog.setWindowTitle(dialog_title)
    dialog.setFixedSize(300, 200)  

    layout = QtWidgets.QVBoxLayout()

  
    title_label = QtWidgets.QLabel(dialog_inputtitle)
    title_label.setStyleSheet("font-weight: bold; color: white; font-size: 30px; background: transparent;")  
    layout.addWidget(title_label)

    
    line_edit = QtWidgets.QLineEdit()
    line_edit.setPlaceholderText(dialog_text)
    line_edit.setStyleSheet("font-size: 16px; padding: 8px; border: 1px solid #ccc; border-radius: 5px;")
    layout.addWidget(line_edit)

   
    button_box = QtWidgets.QDialogButtonBox(QtCore.Qt.Orientation.Horizontal)  
    ok_button = button_box.addButton(QtWidgets.QDialogButtonBox.StandardButton.Ok)
    cancel_button = button_box.addButton(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
    

    ok_button.setStyleSheet("background-color: white; color: purple; border-radius: 5px; padding: 10px;")
    cancel_button.setStyleSheet("background-color: white; color: purple; border-radius: 5px; padding: 10px;")

    layout.addWidget(button_box)
    dialog.setLayout(layout)


    ok_button.clicked.connect(lambda: self.handle_ok(dialog, line_edit))
    cancel_button.clicked.connect(dialog.reject)

   
    dialog.exec()



  def handle_ok(self, dialog, line_edit):
      text = line_edit.text()
      if text:
          if text not in self.profile_buttons:  
              self.create_new_profile(text)
              dialog.accept()  
          else:
              warning_title = self.language_translations[self.current_language]["existing_profile_warning_title"]
              warning_text = self.language_translations[self.current_language]["existing_profile_warning_text"]
              QtWidgets.QMessageBox.warning(self, warning_title, warning_text)



  def create_new_profile(self, profile_name):
   profile_dir = os.path.join(os.getcwd(), "profiles", profile_name)
   if not os.path.exists(profile_dir): 
    os.makedirs(profile_dir, exist_ok=True)

    
    items_count = self.profiles_circle_layout.count()
    row = items_count // 4
    col = items_count % 4
    self.create_profile_button(profile_name, row, col)
   else:
    QtWidgets.QMessageBox.warning(self, "Nombre Existente", "Ya existe un perfil con ese nombre.")


  def update_profile_highlight(self):
    for profile_name, profile_data in self.profile_buttons.items():
        button = profile_data['button']
        label = profile_data['label']

        button.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
                border-radius: 75px;
                border: 2px solid black;
                box-shadow: none;  
            }
            QPushButton:hover {
                background-color: deepskyblue;
            }
        """)

        label.setStyleSheet("color: white; font-weight: normal;")  

    if self.selected_profile and self.selected_profile in self.profile_buttons:
        selected_button = self.profile_buttons[self.selected_profile]['button']

        selected_button.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border-radius: 75px;
                border: 2px solid deepskyblue;
                box-shadow: 0px 0px 15px rgba(0, 0, 255, 0.7); 
            }
            QPushButton:hover {
                background-color: #a0c0ff;
            }
        """)

        selected_label = self.profile_buttons[self.selected_profile]['label']
        selected_label.setStyleSheet("color: deepskyblue; font-weight: bold;")  




  def move_nikke_launcher_to_profiles(self, old_profile):
   old_profile_path = os.path.join(os.getcwd(), "profiles", old_profile)
   if os.path.exists(self.nikke_launcher_path):
    destination_path = os.path.join(old_profile_path, "nikke_launcher")
    if not os.path.exists(destination_path):
     shutil.move(self.nikke_launcher_path, destination_path)

  def move_nikke_launcher_if_exists(self, new_profile):
   new_profile_path = os.path.join(os.getcwd(), "profiles", new_profile, "nikke_launcher")
   if os.path.exists(new_profile_path):
    shutil.move(new_profile_path, self.nikke_launcher_path)

  def save_last_selected_profile(self):
   if self.selected_profile:
    with open("last_selected_profile.txt", "w") as f:
     f.write(self.selected_profile)

  def load_last_selected_profile(self):
   try:
    with open("last_selected_profile.txt", "r") as f:
     return f.read().strip()
   except FileNotFoundError:
    return None

  def get_profile_image_path(self, profile_name):
   return os.path.join(os.getcwd(), "profiles", profile_name, "profile_image.png")


if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  profile_manager = ProfileManager()
  profile_manager.save_last_selected_profile()
  sys.exit(app.exec())