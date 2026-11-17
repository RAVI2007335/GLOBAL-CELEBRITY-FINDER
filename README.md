# 🌍 Global Celebrity Finder

A desktop application built with **Python, Tkinter, SQLite, Requests,
and Pillow**. Search for celebrities from around the world, view their
Wikipedia profile and biography, load their profile photo, and save
profiles to a local Favorites list.

## ✨ Features

-   **Global celebrity search** using the Wikipedia Search API.
-   **Search results** displayed as cards with names and short
    descriptions.
-   **Celebrity profiles** with biography text and an available profile
    image.
-   **Favorites** saved locally in an SQLite database.
-   **Open Wikipedia** to view the original profile page.
-   **Modern desktop interface** with a dark theme, sidebar navigation,
    and status bar.
-   **Background network requests** so searches and image downloads do
    not normally freeze the interface.

## 🧰 Technologies Used

  Technology           Purpose
  -------------------- ----------------------------------------------------
  Python               Main programming language
  Tkinter / ttk        Desktop graphical user interface
  SQLite (`sqlite3`)   Local storage for favorite profiles
  Requests             Calls Wikipedia's online APIs and downloads images
  Pillow (`PIL`)       Opens, resizes, and displays profile photos
  Threading            Runs network tasks in background threads

## 📋 Requirements

-   Python 3.10 or newer recommended.
-   An internet connection for searching Wikipedia and loading profile
    photos.
-   `requests` and `Pillow` Python packages.

Tkinter and SQLite are included with most standard Python installations.
On some Linux distributions, Tkinter may need to be installed
separately.

## 🚀 Installation and Setup

### 1. Download or clone the project

Place the Python source file in a project folder. For example:

``` text
Global-Celebrity-Finder/
└── main.py
```

If your Python file has a different name, use that filename in the run
command below.

### 2. Open the project folder in a terminal

In VS Code, choose **File → Open Folder**, open the project folder, and
then choose **Terminal → New Terminal**.

### 3. Install the required packages

``` bash
python -m pip install requests Pillow
```

If the `python` command is not recognized on Windows, try:

``` bash
py -m pip install requests Pillow
```

### 4. Run the application

If the source file is named `main.py`:

``` bash
python main.py
```

On Windows, this may also work:

``` bash
py main.py
```

## 🖥️ How to Use

1.  Start the application.
2.  On the Home page, enter a celebrity's name in the search box.
3.  Click **SEARCH** or press **Enter**.
4.  Choose a result by clicking **VIEW PROFILE**.
5.  Read the biography and view the available profile photo.
6.  Click **SAVE FAVORITE** to save the profile.
7.  Open **Favorites** from the sidebar to view saved profiles.
8.  Use **OPEN WIKIPEDIA** to visit the source page.
9.  Select **REMOVE** on a Favorites card to delete it from the saved
    list.

## 🗄️ Database

The application automatically creates a local SQLite database named:

``` text
global_celebrity.db
```

It creates a `favorites` table containing:

-   `id` --- unique record ID.
-   `title` --- celebrity/profile title.
-   `description` --- biography text.
-   `image_url` --- profile image address.
-   `page_url` --- Wikipedia profile page address.

The database is created in the application's current working directory
the first time the program runs. Keep this file if you want to retain
your saved Favorites.

## 🌐 Data Source and Internet Use

The app retrieves search results from the **Wikipedia Search API** and
profile summaries/photos from the **Wikimedia REST API**. Search,
profile details, and photos require an internet connection.

Wikipedia content and image availability can vary. Some profiles may not
have an image, and search results may include pages that are not
celebrity profiles. Check the linked Wikipedia page when you need to
verify information.

## 📁 Suggested Project Structure

``` text
Global-Celebrity-Finder/
├── main.py                 # Python application source
├── global_celebrity.db     # Created automatically when the app runs
└── README.md               # Project documentation
```

The database file may not exist until the application has been launched.

## 🛠️ Troubleshooting

### `ModuleNotFoundError: No module named 'requests'`

Install Requests:

``` bash
python -m pip install requests
```

### `ModuleNotFoundError: No module named 'PIL'`

Install Pillow:

``` bash
python -m pip install Pillow
```

### Search or profile loading fails

-   Check that the computer is connected to the internet.
-   Try again later if Wikipedia's service is temporarily unavailable.
-   Check whether a firewall or network setting is blocking the request.

### Profile photo is not displayed

Some Wikipedia pages do not provide a suitable image, and some image
requests may fail. The app displays a **PHOTO NOT AVAILABLE** message
when it cannot load the image.

### Tkinter is unavailable

On some Linux systems, install the system package for Python Tkinter
using your distribution's package manager.

## 🔒 Privacy

Favorite profiles are stored locally in `global_celebrity.db`. The
application sends search and profile requests to Wikipedia/Wikimedia
services. Do not store private or sensitive information in the Favorites
database.

## 📄 License and Attribution

This project is provided for learning and educational use. Wikipedia and
Wikimedia content is subject to the terms and licenses applicable to
that content. The application is not affiliated with or endorsed by the
Wikimedia Foundation.

------------------------------------------------------------------------

**Project:** Global Celebrity Finder\
**Application type:** Python desktop application\
**Main source:** Wikipedia / Wikimedia APIs
