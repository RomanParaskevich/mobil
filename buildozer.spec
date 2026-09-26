[app]

# (string) Title of your application
title = Рыболовный Дневник

# (string) Package name
package.name = fishingtracker

# (string) Package domain (needed for android package name)
package.domain = org.fishingapp

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json

# (string) Application version
version = 1.0

# (list) Application requirements
# Здесь обязательно указываем kivy и python3. 
# Модуль json является встроенным, поэтому дополнительных библиотек не требуется.
requirements = python3,kivy

# (str) Supported orientations (valid options are: landscape, portrait or all)
orientation = portrait

# -----------------------------------------------------------------------------
# Android specific configurations
# -----------------------------------------------------------------------------

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions. Для работы локального JsonStore особых разрешений не требуется,
# но если в будущем вы захотите сохранять файлы во внутреннюю память телефона, 
# можно раскомментировать эту строку:
# android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
# API 34 или 33 является стандартом для современных версий Android (13/14)
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use (Buildozer обычно скачивает нужную сам, если оставить пустой)
# android.ndk = 25b

# (bool) Use --private data storage for binary pickle
android.private_storage = 1

# (str) Theme for the Android application
android.theme = @android:style/Theme.NoTitleBar

# -----------------------------------------------------------------------------
# Buildozer configurations
# -----------------------------------------------------------------------------

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
