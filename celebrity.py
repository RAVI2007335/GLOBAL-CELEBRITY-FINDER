import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import requests
import threading
import io
import webbrowser
import re
from PIL import Image, ImageTk


# ============================================================
# GLOBAL CELEBRITY FINDER
# ============================================================

APP_NAME = "GLOBAL CELEBRITY FINDER"
DB_NAME = "global_celebrity.db"

BG = "#080d18"
PANEL = "#101827"
CARD = "#172235"
CARD2 = "#202d44"
WHITE = "#f8fafc"
MUTED = "#94a3b8"
BLUE = "#2563eb"
BLUE2 = "#3b82f6"
PINK = "#ec4899"
GREEN = "#22c55e"
RED = "#ef4444"
GOLD = "#f59e0b"


# ============================================================
# DATABASE
# ============================================================

conn = sqlite3.connect(DB_NAME)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE,
    description TEXT,
    image_url TEXT,
    page_url TEXT
)
""")

conn.commit()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(APP_NAME)

root.geometry("1250x760")

root.minsize(1050, 650)

root.configure(bg=BG)


# ============================================================
# VARIABLES
# ============================================================

search_var = tk.StringVar()

status_var = tk.StringVar(
    value="Ready — Search any celebrity from around the world"
)

current_results = []

image_references = []


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "Treeview",
    background=PANEL,
    foreground=WHITE,
    fieldbackground=PANEL,
    rowheight=32
)

style.configure(
    "Treeview.Heading",
    background=CARD2,
    foreground=WHITE,
    font=("Segoe UI", 10, "bold")
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg="#050912",
    height=78
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title_frame = tk.Frame(
    header,
    bg="#050912"
)

title_frame.pack(
    side="left",
    padx=25
)


tk.Label(
    title_frame,
    text="★",
    bg="#050912",
    fg=GOLD,
    font=("Segoe UI", 28, "bold")
).pack(side="left")


tk.Label(
    title_frame,
    text=" GLOBAL",
    bg="#050912",
    fg=WHITE,
    font=("Segoe UI", 23, "bold")
).pack(side="left")


tk.Label(
    title_frame,
    text=" CELEBRITY",
    bg="#050912",
    fg=BLUE2,
    font=("Segoe UI", 23, "bold")
).pack(side="left")


tk.Label(
    title_frame,
    text=" FINDER",
    bg="#050912",
    fg=PINK,
    font=("Segoe UI", 23, "bold")
).pack(side="left")


tk.Label(
    header,
    text="ONLINE • GLOBAL DATABASE",
    bg="#050912",
    fg=GREEN,
    font=("Segoe UI", 10, "bold")
).pack(
    side="right",
    padx=25
)


# ============================================================
# MAIN AREA
# ============================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    fill="both",
    expand=True
)


# ============================================================
# SIDEBAR
# ============================================================

sidebar = tk.Frame(
    main,
    bg=PANEL,
    width=215
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


tk.Label(
    sidebar,
    text="MAIN MENU",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 9, "bold")
).pack(
    anchor="w",
    padx=20,
    pady=(25, 10)
)


# ============================================================
# CONTENT
# ============================================================

content = tk.Frame(
    main,
    bg=BG
)

content.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# BUTTON FUNCTION
# ============================================================

def make_button(
    parent,
    text,
    command,
    color=BLUE,
    width=15
):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=BLUE2,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        width=width,
        padx=8,
        pady=8
    )


# ============================================================
# CLEAR CONTENT
# ============================================================

def clear_content():

    for widget in content.winfo_children():
        widget.destroy()


# ============================================================
# FAVORITE FUNCTIONS
# ============================================================

def is_favorite(title):

    cur.execute(
        "SELECT id FROM favorites WHERE title=?",
        (title,)
    )

    return cur.fetchone() is not None


def save_favorite(data):

    if is_favorite(data["title"]):

        messagebox.showinfo(
            "Favorites",
            "This celebrity is already saved."
        )

        return

    cur.execute("""
    INSERT INTO favorites
    (title, description, image_url, page_url)
    VALUES (?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        data["image_url"],
        data["page_url"]
    ))

    conn.commit()

    messagebox.showinfo(
        "Saved",
        data["title"] + " added to Favorites ⭐"
    )


def remove_favorite(title):

    cur.execute(
        "DELETE FROM favorites WHERE title=?",
        (title,)
    )

    conn.commit()


# ============================================================
# WIKIPEDIA SEARCH
# ============================================================

def search_wikipedia():

    query = search_var.get().strip()

    if not query:

        messagebox.showwarning(
            "Search",
            "Celebrity ka naam enter karo."
        )

        return

    status_var.set(
        "🔎 Searching global database..."
    )

    search_btn.config(
        state="disabled"
    )

    threading.Thread(
        target=perform_search,
        args=(query,),
        daemon=True
    ).start()


def perform_search(query):

    try:

        url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": 20,
            "format": "json",
            "utf8": 1
        }

        response = requests.get(
            url,
            params=params,
            timeout=20,
            headers={
                "User-Agent":
                "GlobalCelebrityFinder/1.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "query",
            {}
        ).get(
            "search",
            []
        )

        root.after(
            0,
            lambda:
            search_finished(results)
        )

    except Exception as e:

        root.after(
            0,
            lambda:
            search_failed(str(e))
        )


def search_failed(error):

    search_btn.config(
        state="normal"
    )

    status_var.set(
        "❌ Connection failed"
    )

    messagebox.showerror(
        "Internet Error",
        "Internet connection check karo.\n\n"
        + str(error)
    )


def search_finished(results):

    global current_results

    current_results = results

    search_btn.config(
        state="normal"
    )

    if not results:

        clear_content()

        status_var.set(
            "No results found"
        )

        tk.Label(
            content,
            text="No celebrity found",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=100
        )

        return

    status_var.set(
        str(len(results)) +
        " results found"
    )

    show_search_results(results)


# ============================================================
# SEARCH RESULT PAGE
# ============================================================

def show_search_results(results):

    clear_content()

    top = tk.Frame(
        content,
        bg=BG
    )

    top.pack(
        fill="x",
        padx=25,
        pady=20
    )


    tk.Label(
        top,
        text="🌍 Global Search Results",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 24, "bold")
    ).pack(
        side="left"
    )


    tk.Label(
        top,
        text=str(len(results)) + " results",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(
        side="right",
        pady=10
    )


    outer = tk.Frame(
        content,
        bg=BG
    )

    outer.pack(
        fill="both",
        expand=True,
        padx=25
    )


    canvas = tk.Canvas(
        outer,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview
    )


    cards = tk.Frame(
        canvas,
        bg=BG
    )


    cards.bind(
        "<Configure>",
        lambda e:
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )


    canvas.create_window(
        (0, 0),
        window=cards,
        anchor="nw"
    )


    canvas.configure(
        yscrollcommand=scrollbar.set
    )


    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar.pack(
        side="right",
        fill="y"
    )


    for index, item in enumerate(results):

        title = item.get(
            "title",
            ""
        )

        snippet = item.get(
            "snippet",
            ""
        )

        create_result_card(
            cards,
            title,
            snippet,
            index
        )


# ============================================================
# RESULT CARD
# ============================================================

def create_result_card(
    parent,
    title,
    snippet,
    index
):

    card = tk.Frame(
        parent,
        bg=CARD,
        width=350,
        height=190
    )

    card.grid(
        row=index // 2,
        column=index % 2,
        padx=10,
        pady=10,
        sticky="n"
    )

    card.grid_propagate(False)


    # Avatar
    avatar = tk.Canvas(
        card,
        width=70,
        height=70,
        bg=CARD2,
        highlightthickness=0
    )

    avatar.pack(
        pady=(15, 5)
    )


    parts = title.split()

    if len(parts) >= 2:

        initials = (
            parts[0][0] +
            parts[-1][0]
        ).upper()

    else:

        initials = title[:2].upper()


    avatar.create_text(
        35,
        35,
        text=initials,
        fill=WHITE,
        font=("Segoe UI", 20, "bold")
    )


    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=WHITE,
        font=("Segoe UI", 14, "bold")
    ).pack()


    clean_snippet = re.sub(
        "<.*?>",
        "",
        snippet
    )


    if len(clean_snippet) > 90:

        clean_snippet = (
            clean_snippet[:90]
            + "..."
        )


    tk.Label(
        card,
        text=clean_snippet,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 8),
        wraplength=310
    ).pack(
        pady=3
    )


    make_button(
        card,
        "VIEW PROFILE",
        lambda t=title:
        load_profile(t),
        BLUE,
        14
    ).pack(
        pady=7
    )


# ============================================================
# PROFILE LOADING
# ============================================================

def load_profile(title):

    status_var.set(
        "⏳ Loading celebrity profile..."
    )

    threading.Thread(
        target=fetch_profile,
        args=(title,),
        daemon=True
    ).start()


def fetch_profile(title):

    try:

        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + requests.utils.quote(
                title.replace(" ", "_"),
                safe=""
            )
        )


        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent":
                "GlobalCelebrityFinder/1.0"
            }
        )


        response.raise_for_status()

        data = response.json()


        image_url = ""

        if "originalimage" in data:

            image_url = data[
                "originalimage"
            ].get(
                "source",
                ""
            )

        elif "thumbnail" in data:

            image_url = data[
                "thumbnail"
            ].get(
                "source",
                ""
            )


        page_url = ""

        content_urls = data.get(
            "content_urls",
            {}
        )

        desktop = content_urls.get(
            "desktop",
            {}
        )

        page_url = desktop.get(
            "page",
            "https://en.wikipedia.org/"
        )


        description = data.get(
            "extract",
            "Biography not available."
        )


        profile = {

            "title":
            data.get(
                "title",
                title
            ),

            "description":
            description,

            "image_url":
            image_url,

            "page_url":
            page_url,

            "type":
            data.get(
                "type",
                ""
            )
        }


        root.after(
            0,
            lambda:
            display_profile(profile)
        )


    except Exception as e:

        root.after(
            0,
            lambda:
            profile_error(str(e))
        )


def profile_error(error):

    status_var.set(
        "❌ Could not load profile"
    )

    messagebox.showerror(
        "Profile Error",
        "Celebrity profile load nahi ho paya.\n\n"
        + str(error)
    )


# ============================================================
# PROFILE PAGE
# ============================================================

def display_profile(data):

    clear_content()

    status_var.set(
        "✅ Profile loaded successfully"
    )


    profile = tk.Frame(
        content,
        bg=CARD
    )

    profile.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=30
    )


    # ========================================================
    # LEFT IMAGE PANEL
    # ========================================================

    left = tk.Frame(
        profile,
        bg=CARD,
        width=330
    )

    left.pack(
        side="left",
        fill="y",
        padx=25,
        pady=25
    )

    left.pack_propagate(False)


    image_box = tk.Frame(
        left,
        bg=CARD2,
        width=270,
        height=270
    )

    image_box.pack(
        pady=15
    )

    image_box.pack_propagate(False)


    image_label = tk.Label(
        image_box,
        text="Loading photo...",
        bg=CARD2,
        fg=MUTED,
        font=("Segoe UI", 12)
    )

    image_label.pack(
        fill="both",
        expand=True
    )


    image_url = data.get(
        "image_url",
        ""
    )


    if image_url:

        threading.Thread(
            target=download_profile_image,
            args=(
                image_url,
                image_label
            ),
            daemon=True
        ).start()

    else:

        image_label.config(
            text="PHOTO\nNOT AVAILABLE"
        )


    make_button(
        left,
        "⭐ SAVE FAVORITE",
        lambda:
        save_favorite(data),
        PINK,
        20
    ).pack(
        pady=12
    )


    make_button(
        left,
        "🌐 OPEN WIKIPEDIA",
        lambda:
        webbrowser.open(
            data["page_url"]
        ),
        BLUE,
        20
    ).pack(
        pady=5
    )


    # ========================================================
    # RIGHT DETAILS
    # ========================================================

    right = tk.Frame(
        profile,
        bg=CARD
    )

    right.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 30),
        pady=30
    )


    make_button(
        right,
        "← BACK TO RESULTS",
        lambda:
        show_search_results(
            current_results
        ),
        CARD2,
        18
    ).pack(
        anchor="w"
    )


    tk.Label(
        right,
        text=data["title"],
        bg=CARD,
        fg=WHITE,
        font=("Segoe UI", 30, "bold")
    ).pack(
        anchor="w",
        pady=(25, 5)
    )


    tk.Label(
        right,
        text="GLOBAL CELEBRITY PROFILE",
        bg=CARD,
        fg=BLUE2,
        font=("Segoe UI", 10, "bold")
    ).pack(
        anchor="w"
    )


    tk.Label(
        right,
        text="BIOGRAPHY",
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 9, "bold")
    ).pack(
        anchor="w",
        pady=(30, 5)
    )


    bio_frame = tk.Frame(
        right,
        bg=CARD2
    )

    bio_frame.pack(
        fill="both",
        expand=True
    )


    bio_scroll = ttk.Scrollbar(
        bio_frame
    )

    bio_scroll.pack(
        side="right",
        fill="y"
    )


    bio = tk.Text(
        bio_frame,
        bg=CARD2,
        fg=WHITE,
        relief="flat",
        wrap="word",
        font=("Segoe UI", 11),
        yscrollcommand=bio_scroll.set
    )

    bio.pack(
        side="left",
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )


    bio_scroll.config(
        command=bio.yview
    )


    bio.insert(
        "1.0",
        data["description"]
    )


    bio.config(
        state="disabled"
    )


# ============================================================
# FIXED IMAGE DOWNLOADER
# ============================================================

def download_profile_image(
    image_url,
    label
):

    try:

        print("IMAGE URL:")
        print(image_url)


        response = requests.get(
            image_url,
            timeout=25,
            headers={
                "User-Agent":
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/154.0 Safari/537.36",
                "Accept":
                "image/avif,image/webp,image/apng,"
                "image/svg+xml,image/*,*/*;q=0.8"
            }
        )


        response.raise_for_status()


        image_bytes = response.content


        if not image_bytes:

            raise Exception(
                "Empty image response"
            )


        image = Image.open(
            io.BytesIO(
                image_bytes
            )
        )


        image.load()


        # Transparent images ko RGB/RGBA me convert
        if image.mode not in (
            "RGB",
            "RGBA"
        ):

            image = image.convert(
                "RGBA"
            )


        # Photo ko box ke according resize
        image.thumbnail(
            (270, 270),
            Image.Resampling.LANCZOS
        )


        photo = ImageTk.PhotoImage(
            image
        )


        def update_image():

            image_references.append(
                photo
            )

            label.config(
                image=photo,
                text=""
            )

            label.image = photo


        root.after(
            0,
            update_image
        )


    except Exception as e:

        print(
            "IMAGE ERROR:",
            repr(e)
        )


        def image_error():

            label.config(
                text="PHOTO\nNOT AVAILABLE",
                fg=MUTED,
                bg=CARD2,
                font=(
                    "Segoe UI",
                    13,
                    "bold"
                )
            )


        root.after(
            0,
            image_error
        )


# ============================================================
# FAVORITES PAGE
# ============================================================

def favorites_page():

    clear_content()

    tk.Label(
        content,
        text="⭐ My Favorites",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 25, "bold")
    ).pack(
        anchor="w",
        padx=25,
        pady=25
    )


    cur.execute("""
    SELECT title,
           description,
           image_url,
           page_url
    FROM favorites
    ORDER BY title
    """)


    rows = cur.fetchall()


    if not rows:

        tk.Label(
            content,
            text="No favorites saved yet.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 15)
        ).pack(
            pady=100
        )

        return


    frame = tk.Frame(
        content,
        bg=BG
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=25
    )


    for index, row in enumerate(rows):

        title = row[0]

        description = row[1]

        image_url = row[2]

        page_url = row[3]


        card = tk.Frame(
            frame,
            bg=CARD,
            width=320,
            height=220
        )

        card.grid(
            row=index // 3,
            column=index % 3,
            padx=10,
            pady=10,
            sticky="n"
        )

        card.grid_propagate(False)


        tk.Label(
            card,
            text="★",
            bg=CARD,
            fg=GOLD,
            font=("Segoe UI", 25)
        ).pack(
            pady=(15, 3)
        )


        tk.Label(
            card,
            text=title,
            bg=CARD,
            fg=WHITE,
            font=("Segoe UI", 14, "bold")
        ).pack()


        make_button(
            card,
            "OPEN PROFILE",
            lambda t=title:
            load_profile(t),
            BLUE,
            14
        ).pack(
            pady=8
        )


        make_button(
            card,
            "REMOVE",
            lambda t=title:
            remove_and_refresh(t),
            RED,
            10
        ).pack()


def remove_and_refresh(title):

    remove_favorite(title)

    favorites_page()


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    clear_content()

    center = tk.Frame(
        content,
        bg=BG
    )

    center.pack(
        fill="both",
        expand=True
    )


    tk.Label(
        center,
        text="🌍",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 55)
    ).pack(
        pady=(65, 5)
    )


    tk.Label(
        center,
        text="GLOBAL CELEBRITY FINDER",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 30, "bold")
    ).pack()


    tk.Label(
        center,
        text="Search celebrities from around the world",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 13)
    ).pack(
        pady=8
    )


    search_box = tk.Frame(
        center,
        bg=PANEL
    )

    search_box.pack(
        padx=100,
        pady=25,
        fill="x"
    )


    global search_btn


    search_entry = tk.Entry(
        search_box,
        textvariable=search_var,
        bg=CARD2,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Segoe UI", 13)
    )

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=15,
        pady=15
    )


    search_btn = make_button(
        search_box,
        "🔎 SEARCH",
        search_wikipedia,
        BLUE,
        14
    )

    search_btn.pack(
        side="left",
        padx=10
    )


    search_entry.bind(
        "<Return>",
        lambda event:
        search_wikipedia()
    )


    tk.Label(
        center,
        text=(
            "Try: Virat Kohli • Cristiano Ronaldo • "
            "Taylor Swift • Shah Rukh Khan"
        ),
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack()


    features = tk.Frame(
        center,
        bg=BG
    )

    features.pack(
        pady=45
    )


    feature_data = [
        ("🌍", "GLOBAL SEARCH"),
        ("🖼", "LIVE PHOTOS"),
        ("📖", "BIOGRAPHY"),
        ("⭐", "FAVORITES")
    ]


    for icon, text in feature_data:

        box = tk.Frame(
            features,
            bg=CARD,
            width=180,
            height=100
        )

        box.pack(
            side="left",
            padx=8
        )

        box.pack_propagate(False)


        tk.Label(
            box,
            text=icon,
            bg=CARD,
            fg=WHITE,
            font=("Segoe UI", 22)
        ).pack(
            pady=(12, 2)
        )


        tk.Label(
            box,
            text=text,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack()


# ============================================================
# SIDEBAR
# ============================================================

def sidebar_button(
    text,
    command
):

    btn = tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=PANEL,
        fg=WHITE,
        activebackground=CARD2,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        anchor="w",
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=12
    )

    btn.pack(
        fill="x",
        padx=8,
        pady=2
    )


sidebar_button(
    "⌂  Home",
    home_page
)

sidebar_button(
    "🔎  Global Search",
    home_page
)

sidebar_button(
    "⭐  Favorites",
    favorites_page
)


tk.Frame(
    sidebar,
    bg=CARD2,
    height=1
).pack(
    fill="x",
    padx=18,
    pady=20
)


tk.Label(
    sidebar,
    text="DATA SOURCE",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 8, "bold")
).pack(
    anchor="w",
    padx=20,
    pady=(5, 3)
)


tk.Label(
    sidebar,
    text="Wikipedia / Wikimedia",
    bg=PANEL,
    fg=WHITE,
    font=("Segoe UI", 9)
).pack(
    anchor="w",
    padx=20
)


tk.Label(
    sidebar,
    text="● ONLINE SEARCH",
    bg=PANEL,
    fg=GREEN,
    font=("Segoe UI", 9, "bold")
).pack(
    side="bottom",
    pady=20
)


# ============================================================
# STATUS BAR
# ============================================================

status = tk.Label(
    root,
    textvariable=status_var,
    bg="#050912",
    fg=MUTED,
    anchor="w",
    padx=15,
    pady=6,
    font=("Segoe UI", 9)
)

status.pack(
    fill="x",
    side="bottom"
)


# ============================================================
# CLOSE
# ============================================================

def close_app():

    try:
        conn.close()
    except:
        pass

    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    close_app
)


# ============================================================
# START APP
# ============================================================

home_page()

root.mainloop()
