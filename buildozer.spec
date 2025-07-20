[app]

# (str) Title of your application
title = EchoCoreCB

# (str) Package name
package.name = echocorecb

# (str) Package domain (needed for android/ios packaging)
package.domain = org.loganlorentz.echocorecb

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,txt,md,yml,yaml

# (str) Application versioning (method 1)
version = 2.0

# (list) Application requirements
# comma separated e.g. requirements = python3,kivy,requests,pyyaml
requirements = python3,kivy,requests,pyyaml

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#presplash.color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
# android.service_main_class = org.kivy.android.PythonService

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# android.archs = arm64-v8a, armeabi-v7a
android.archs = armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules =

# (str) If you need to insert variables into your AndroidManifest.xml file,
# you can do so with the manifestPlaceholders property.
# This property takes a map of key-value pairs.
# android.manifest_placeholders = [:]

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The format used to package the app for release mode (aab or apk)
# android.release_artifact = aab

[buildozer:build_dir]
# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

[buildozer:bin_dir]
# (str) Path to final binaries, absolute or relative to spec file
# bin_dir = ./bin
# Build triggered: 2025-07-19T21:15:43.577947

# Deployment timestamp: 2025-07-19T21:21:50.593340
# Mobile deployment: 2025-07-19T21:22:51.736035
# Automated compatibility check: 2025-07-19T21:27:45.890123

# Automated compatibility check: 2025-07-19T21:33:23.146582

# Automated compatibility check: 2025-07-19T21:33:37.276990

# Automated compatibility check: 2025-07-19T21:38:37.377985

# Automated compatibility check: 2025-07-19T21:43:37.496323

# Automated compatibility check: 2025-07-19T22:21:21.717296

# EchoNexus auto-fix applied: 2025-07-19T22:24:29.819659

# Automated compatibility check: 2025-07-19T22:26:21.805781

# Automated compatibility check: 2025-07-19T22:31:21.898054

# Automated compatibility check: 2025-07-19T22:36:21.998667

# Automated compatibility check: 2025-07-19T22:41:22.115660

# Automated compatibility check: 2025-07-19T22:46:22.200432

# Automated compatibility check: 2025-07-19T22:51:22.281537

# Automated compatibility check: 2025-07-19T22:56:22.408622

# Automated compatibility check: 2025-07-19T23:49:58.445555

# Automated compatibility check: 2025-07-19T23:51:07.933602

# Automated compatibility check: 2025-07-19T23:54:04.660717

# Automated compatibility check: 2025-07-19T23:55:23.633975

# Automated compatibility check: 2025-07-19T23:58:36.252575

# Automated compatibility check: 2025-07-20T00:03:36.344723

# Automated compatibility check: 2025-07-20T00:04:52.694083

# Automated compatibility check: 2025-07-20T00:05:40.577231
