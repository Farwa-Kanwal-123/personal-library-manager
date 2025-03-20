import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
from io import BytesIO
import json
import time
from datetime import datetime
from PIL import Image
import re
import os
import hashlib
import base64

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    .main {
        background-color: #1e1e2e;
        color: #cdd6f4;
    }
    .stButton button {
        background-color: #89b4fa;
        color: #1e1e2e;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #b4befe;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    .card {
        background-color: #313244;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        color: #cdd6f4;  /* Light text color for dark background */
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card h3 {
        color: #89b4fa;  /* Light blue for titles */
        margin-bottom: 0.5rem;
    }
    .card p {
        color: #cdd6f4;  /* Light text color */
        margin-bottom: 0.3rem;
    }
    .title {
        color: #89b4fa;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .subtitle {
        color: #a6e3a1;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #313244;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: #cdd6f4;
    }
    .stTabs [aria-selected="true"] {
        background-color: #89b4fa;
        color: #1e1e2e;
    }
    .book-cover {
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        overflow: hidden;
        position: relative;
        aspect-ratio: 2/3;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 10px;
        color: white;
        font-weight: bold;
    }
    .book-title {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        line-height: 1.2;
        overflow-wrap: break-word;
        word-break: break-word;
    }
    .book-author {
        font-size: 0.9rem;
        font-style: italic;
        opacity: 0.9;
    }
    .book-icon {
        position: absolute;
        bottom: 10px;
        right: 10px;
        opacity: 0.3;
        font-size: 1.5rem;
    }
    .dashboard-card {
        background-color: #313244;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 100%;
        transition: all 0.3s ease;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .dashboard-card-title {
        color: #89b4fa;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    .dashboard-card-title svg {
        margin-right: 0.5rem;
    }
    .feature-card {
        background-color: #313244;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        text-align: center;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        color: #89b4fa;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .feature-description {
        color: #cdd6f4;
        font-size: 0.9rem;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #1e1e2e;
        color: #cdd6f4;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        border: 1px solid #89b4fa;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .welcome-banner {
        background: linear-gradient(135deg, #313244, #1e1e2e);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #89b4fa;
    }
    .welcome-title {
        color: #89b4fa;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .welcome-text {
        color: #cdd6f4;
        margin-bottom: 1rem;
    }
    .quick-action {
        background-color: #89b4fa;
        color: #1e1e2e;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
        transition: all 0.3s ease;
        display: inline-block;
        text-align: center;
        text-decoration: none;
    }
    .quick-action:hover {
        background-color: #b4befe;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    .help-text {
        background-color: rgba(166, 227, 161, 0.1);
        border-left: 3px solid #a6e3a1;
        padding: 0.8rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-reading {
        background-color: rgba(137, 180, 250, 0.2);
        color: #89b4fa;
    }
    .status-completed {
        background-color: rgba(166, 227, 161, 0.2);
        color: #a6e3a1;
    }
    .status-to-read {
        background-color: rgba(249, 226, 175, 0.2);
        color: #f9e2af;
    }
    .status-dnf {
        background-color: rgba(243, 139, 168, 0.2);
        color: #f38ba8;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        isbn TEXT,
        publication_year INTEGER,
        pages INTEGER,
        rating REAL,
        status TEXT,
        date_added TEXT,
        notes TEXT
    )
    ''')
    
    # Check if this is a new user (no books in database)
    book_count = c.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    is_new_user = book_count == 0
    
    conn.commit()
    return conn, is_new_user

# Load animations
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Generate a dynamic book cover based on book title and author
def generate_book_cover_html(title, author, genre=None):
    # Generate a deterministic color based on the title
    hash_object = hashlib.md5(title.encode())
    hash_hex = hash_object.hexdigest()
    
    # Use the hash to generate a gradient color
    r1, g1, b1 = int(hash_hex[0:2], 16), int(hash_hex[2:4], 16), int(hash_hex[4:6], 16)
    r2, g2, b2 = int(hash_hex[6:8], 16), int(hash_hex[8:10], 16), int(hash_hex[10:12], 16)
    
    # Ensure colors are vibrant enough
    r1 = max(r1, 50)
    g1 = max(g1, 50)
    b1 = max(b1, 50)
    
    # Choose an icon based on genre
    icon = "📚"  # Default
    if genre:
        genre_icons = {
            "Fiction": "📖",
            "Non-Fiction": "📋",
            "Science Fiction": "🚀",
            "Fantasy": "🧙",
            "Mystery": "🔍",
            "Thriller": "🔪",
            "Romance": "❤️",
            "Biography": "👤",
            "History": "⏳",
            "Self-Help": "🧠",
            "Business": "💼",
            "Science": "🔬",
            "Other": "📚"
        }
        icon = genre_icons.get(genre, "📚")
    
    # Create HTML for the book cover
    html = f"""
    <div class="book-cover" style="background: linear-gradient(135deg, rgb({r1},{g1},{b1}), rgb({r2},{g2},{b2}));">
        <div class="book-title">{title}</div>
        <div class="book-author">by {author}</div>
        <div class="book-icon">{icon}</div>
    </div>
    """
    return html

# Get status badge HTML
def get_status_badge(status):
    status_class = {
        "Reading": "status-reading",
        "Completed": "status-completed",
        "To Read": "status-to-read",
        "DNF": "status-dnf"
    }.get(status, "")
    
    return f'<span class="status-badge {status_class}">{status}</span>'

# Main function
def main():
    load_css()
    conn, is_new_user = init_db()
    
    # Initialize session state for first-time visitors
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="title">📚 Library Manager</div>', unsafe_allow_html=True)
        
        # Lottie animation
        lottie_book = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_1cazwtnc.json")
        if lottie_book:
            st_lottie(lottie_book, speed=1, height=200, key="book_animation")
        
        st.markdown("---")
        menu = st.radio(
            "📋 Navigation",
            ["Dashboard", "My Books", "Add Book", "Search", "Statistics", "Help & Tips"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        # Get quick stats
        c = conn.cursor()
        total_books = c.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        reading = c.execute("SELECT COUNT(*) FROM books WHERE status='Reading'").fetchone()[0]
        completed = c.execute("SELECT COUNT(*) FROM books WHERE status='Completed'").fetchone()[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", total_books)
        col2.metric("Reading", reading)
        col3.metric("Completed", completed)
    
    # Main content
    if menu == "Dashboard":
        display_dashboard(conn, is_new_user)
    elif menu == "My Books":
        display_books(conn)
    elif menu == "Add Book":
        add_book(conn)
    elif menu == "Search":
        search_books(conn)
    elif menu == "Statistics":
        display_statistics(conn)
    elif menu == "Help & Tips":
        display_help()

# Dashboard page
def display_dashboard(conn, is_new_user):
    st.markdown('<div class="title">📊 Dashboard</div>', unsafe_allow_html=True)
    
    # Welcome banner for new users or first visit
    if is_new_user or st.session_state.first_visit:
        st.markdown("""
        <div class="welcome-banner">
            <div class="welcome-title">👋 Welcome to Your Personal Library Manager!</div>
            <div class="welcome-text">
                This app helps you track your reading journey, organize your books, and discover insights about your reading habits.
                Get started by adding your first book or exploring the features below.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.first_visit = False
    
    # Main dashboard layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Recently added books
        st.markdown("""
        <div class="dashboard-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8v4l3 3"></path>
                <circle cx="12" cy="12" r="10"></circle>
            </svg>
            Recently Added Books
        </div>
        """, unsafe_allow_html=True)
        
        c = conn.cursor()
        recent_books = c.execute(
            "SELECT id, title, author, genre, status FROM books ORDER BY date_added DESC LIMIT 5"
        ).fetchall()
        
        if recent_books:
            for book in recent_books:
                col_img, col_info = st.columns([1, 3])
                with col_img:
                    # Dynamic book cover
                    st.markdown(generate_book_cover_html(book[1], book[2], book[3]), unsafe_allow_html=True)
                with col_info:
                    st.markdown(f"**{book[1]}**")
                    st.markdown(f"By {book[2]}")
                    st.markdown(f"Genre: {book[3]}")
                    st.markdown(get_status_badge(book[4]), unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("📚 No books added yet. Start building your library by adding your first book!")
            st.button("➕ Add Your First Book", on_click=lambda: st.session_state.update({"menu": "Add Book"}))
    
    with col2:
        # Reading progress
        st.markdown("""
        <div class="dashboard-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
            </svg>
            Currently Reading
        </div>
        """, unsafe_allow_html=True)
        
        reading_books = c.execute(
            "SELECT id, title, author, genre FROM books WHERE status='Reading' LIMIT 3"
        ).fetchall()
        
        if reading_books:
            for book in reading_books:
                st.markdown(generate_book_cover_html(book[1], book[2], book[3]), unsafe_allow_html=True)
                st.markdown(f"**{book[1]}**")
                st.markdown(f"By {book[2]}")
                progress = st.slider(f"Progress for {book[1]}", 0, 100, 25, key=f"progress_{book[0]}")
                st.progress(progress / 100)
                st.markdown("---")
        else:
            st.info("📖 You're not currently reading any books. Start a new book today!")
    
    # Feature highlights
    st.markdown("""
    <div class="dashboard-card-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        App Features
    </div>
    """, unsafe_allow_html=True)
    
    feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)
    
    with feature_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Track Your Books</div>
            <div class="feature-description">Keep a record of all your books in one place with details like genre, rating, and reading status.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Reading Insights</div>
            <div class="feature-description">Discover patterns in your reading habits with visual statistics and charts.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Search & Filter</div>
            <div class="feature-description">Quickly find books by title, author, or genre with powerful search capabilities.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Reading Notes</div>
            <div class="feature-description">Add personal notes and thoughts about each book you read.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Genre distribution
    st.markdown("""
    <div class="dashboard-card-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
            <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
        </svg>
        Genre Distribution
    </div>
    """, unsafe_allow_html=True)
    
    genres = c.execute(
        "SELECT genre, COUNT(*) as count FROM books GROUP BY genre ORDER BY count DESC"
    ).fetchall()
    
    if genres:
        genre_df = pd.DataFrame(genres, columns=["Genre", "Count"])
        fig = px.pie(genre_df, values="Count", names="Genre", hole=0.4)
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cdd6f4")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add some books to see your genre distribution!")

# Books page
def display_books(conn):
    st.markdown('<div class="title">📚 My Books</div>', unsafe_allow_html=True)
    
    # Help text
    st.markdown("""
    <div class="help-text">
        <strong>📖 My Books</strong>: View all your books, filter by status or genre, and manage your collection.
        Use the filters below to find specific books.
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("📊 Filter by Status", ["All", "Reading", "Completed", "To Read", "DNF"], 
                                    help="Select a reading status to filter your books")
    with col2:
        c = conn.cursor()
        genres = [row[0] for row in c.execute("SELECT DISTINCT genre FROM books").fetchall()]
        genres = ["All"] + genres
        genre_filter = st.selectbox("🏷️ Filter by Genre", genres,
                                   help="Select a genre to filter your books")
    with col3:
        sort_by = st.selectbox("🔄 Sort by", ["Title", "Author", "Rating", "Recently Added"],
                              help="Choose how to sort your book list")
    
    # Build query
    query = "SELECT * FROM books"
    params = []
    
    if status_filter != "All":
        query += " WHERE status = ?"
        params.append(status_filter)
    
    if genre_filter != "All":
        if "WHERE" in query:
            query += " AND genre = ?"
        else:
            query += " WHERE genre = ?"
        params.append(genre_filter)
    
    if sort_by == "Title":
        query += " ORDER BY title"
    elif sort_by == "Author":
        query += " ORDER BY author"
    elif sort_by == "Rating":
        query += " ORDER BY rating DESC"
    elif sort_by == "Recently Added":
        query += " ORDER BY date_added DESC"
    
    # Execute query
    c = conn.cursor()
    books = c.execute(query, params).fetchall()
    
    if not books:
        st.info("No books found with the selected filters.")
        return
    
    # Display books in a grid
    cols = st.columns(3)
    for i, book in enumerate(books):
        with cols[i % 3]:
            with st.container():
                # Add dynamic book cover at the top of the card
                st.markdown(generate_book_cover_html(book[1], book[2], book[3]), unsafe_allow_html=True)
                
                # Updated card HTML with explicit text colors
                st.markdown(f"""
                <div class="card">
                    <h3 style="color: #89b4fa;">{book[1]}</h3>
                    <p style="color: #cdd6f4;">By {book[2]}</p>
                    <p style="color: #cdd6f4;">Genre: {book[3]}</p>
                    <p style="color: #cdd6f4;">Status: {get_status_badge(book[8])}</p>
                    <p style="color: #f9e2af;">Rating: {"⭐" * int(book[7]) if book[7] else "Not rated"}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Edit", key=f"edit_{book[0]}", help="Edit book details"):
                        st.session_state.edit_book_id = book[0]
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{book[0]}", help="Remove this book from your library"):
                        delete_book(conn, book[0])
                        st.rerun()
    
    # Edit book modal
    if hasattr(st.session_state, 'edit_book_id'):
        edit_book_modal(conn, st.session_state.edit_book_id)

# Add book page
def add_book(conn):
    st.markdown('<div class="title">📝 Add New Book</div>', unsafe_allow_html=True)
    
    # Help text
    st.markdown("""
    <div class="help-text">
        <strong>📝 Add New Book</strong>: Fill in the details below to add a new book to your library.
        Required fields are marked with an asterisk (*).
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    # Book details for preview
    title_preview = "Book Title"
    author_preview = "Author Name"
    genre_preview = "Fiction"
    
    with col1:
        st.markdown("<h3>📖 Book Cover Preview</h3>", unsafe_allow_html=True)
        
        # Dynamic preview that updates as user types
        if 'preview_title' in st.session_state:
            title_preview = st.session_state.preview_title
        if 'preview_author' in st.session_state:
            author_preview = st.session_state.preview_author
        if 'preview_genre' in st.session_state:
            genre_preview = st.session_state.preview_genre
            
        st.markdown(generate_book_cover_html(title_preview, author_preview, genre_preview), unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.9rem; margin-top: 10px;'>Cover preview updates as you type</p>", unsafe_allow_html=True)
    
    with col2:
        # Update preview as user types
        title = st.text_input("📕 Title*", key="preview_title", value=title_preview if title_preview != "Book Title" else "", 
                             help="Enter the full title of the book")
        author = st.text_input("✍️ Author*", key="preview_author", value=author_preview if author_preview != "Author Name" else "",
                              help="Enter the author's full name")
        genre = st.selectbox("🏷️ Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                      "Mystery", "Thriller", "Romance", "Biography", "History", 
                                      "Self-Help", "Business", "Science", "Other"], key="preview_genre",
                            help="Select the book's primary genre")
        
        col1, col2 = st.columns(2)
        with col1:
            isbn = st.text_input("📘 ISBN", help="International Standard Book Number (optional)")
            publication_year = st.number_input("📅 Publication Year", min_value=1000, max_value=datetime.now().year, step=1,
                                             help="Year when the book was published")
        with col2:
            pages = st.number_input("📄 Pages", min_value=1, step=1, help="Total number of pages in the book")
            rating = st.slider("⭐ Rating", 0.0, 5.0, 0.0, 0.5, help="Your rating from 0 to 5 stars")
        
        status = st.selectbox("📊 Status", ["To Read", "Reading", "Completed", "DNF"], 
                             help="Current reading status (DNF = Did Not Finish)")
        notes = st.text_area("📝 Notes", help="Your personal notes about this book")
        
        if st.button("➕ Add Book", use_container_width=True):
            if not title or not author:
                st.error("Title and author are required fields.")
            else:
                c = conn.cursor()
                c.execute("""
                INSERT INTO books (title, author, genre, isbn, publication_year, pages, rating, status, date_added, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (title, author, genre, isbn, publication_year, pages, rating, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), notes))
                conn.commit()
                
                # Success animation
                success_lottie = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json")
                if success_lottie:
                    st_lottie(success_lottie, speed=1, height=200, key="success")
                
                st.success(f"'{title}' has been added to your library!")
                time.sleep(2)
                st.rerun()

# Search books page
def search_books(conn):
    st.markdown('<div class="title">🔍 Search Books</div>', unsafe_allow_html=True)
    
    # Help text
    st.markdown("""
    <div class="help-text">
        <strong>🔍 Search Books</strong>: Find books in your library by title, author, or genre.
        Enter your search term below to get started.
    </div>
    """, unsafe_allow_html=True)
    
    search_term = st.text_input("🔍 Search by title, author, or genre", help="Enter any part of the title, author name, or genre")
    
    if search_term:
        c = conn.cursor()
        search_results = c.execute("""
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")).fetchall()
        
        if search_results:
            st.markdown(f"Found {len(search_results)} results for '{search_term}'")
            
            for book in search_results:
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    # Dynamic book cover
                    st.markdown(generate_book_cover_html(book[1], book[2], book[3]), unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{book[1]}**")
                    st.markdown(f"By {book[2]}")
                    st.markdown(f"Genre: {book[3]}")
                    if book[7]:  # rating
                        st.markdown(f"Rating: {'⭐' * int(book[7])}")
                with col3:
                    st.markdown(get_status_badge(book[8]), unsafe_allow_html=True)
                    if st.button("👁️ View Details", key=f"view_{book[0]}", help="See complete book details"):
                        st.session_state.view_book_id = book[0]
                st.markdown("---")
                
                # Show book details if requested
                if hasattr(st.session_state, 'view_book_id') and st.session_state.view_book_id == book[0]:
                    with st.expander("Book Details", expanded=True):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            # Dynamic book cover
                            st.markdown(generate_book_cover_html(book[1], book[2], book[3]), unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"**Title:** {book[1]}")
                            st.markdown(f"**Author:** {book[2]}")
                            st.markdown(f"**Genre:** {book[3]}")
                            st.markdown(f"**ISBN:** {book[4] or 'N/A'}")
                            st.markdown(f"**Publication Year:** {book[5] or 'N/A'}")
                            st.markdown(f"**Pages:** {book[6] or 'N/A'}")
                            st.markdown(f"**Rating:** {book[7] or 'Not rated'}")
                            st.markdown(f"**Status:** {book[8]}")
                            st.markdown(f"**Date Added:** {book[9]}")
                            st.markdown(f"**Notes:** {book[10] or 'No notes'}")
        else:
            st.info(f"No books found matching '{search_term}'")
    else:
        # Lottie animation
        search_lottie = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_t9gkkhz4.json")
        if search_lottie:
            st_lottie(search_lottie, speed=1, height=300, key="search_animation")
        st.markdown("<div style='text-align: center;'>Enter a search term to find books in your library</div>", unsafe_allow_html=True)

# Statistics page
def display_statistics(conn):
    st.markdown('<div class="title">📊 Library Statistics</div>', unsafe_allow_html=True)
    
    # Help text
    st.markdown("""
    <div class="help-text">
        <strong>📊 Statistics</strong>: Discover insights about your reading habits and library composition.
        The charts below update automatically as you add more books.
    </div>
    """, unsafe_allow_html=True)
    
    c = conn.cursor()
    
    # Get basic stats
    total_books = c.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    total_pages = c.execute("SELECT SUM(pages) FROM books").fetchone()[0] or 0
    avg_rating = c.execute("SELECT AVG(rating) FROM books WHERE rating > 0").fetchone()[0] or 0
    
    # Create metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 2.5rem; text-align: center; color: #89b4fa; font-weight: bold;">
                📚 {}
            </div>
            <div style="text-align: center; margin-top: 0.5rem; font-size: 1.2rem;">
                Total Books
            </div>
        </div>
        """.format(total_books), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 2.5rem; text-align: center; color: #89b4fa; font-weight: bold;">
                📄 {:,}
            </div>
            <div style="text-align: center; margin-top: 0.5rem; font-size: 1.2rem;">
                Total Pages
            </div>
        </div>
        """.format(total_pages), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 2.5rem; text-align: center; color: #89b4fa; font-weight: bold;">
                ⭐ {:.1f}
            </div>
            <div style="text-align: center; margin-top: 0.5rem; font-size: 1.2rem;">
                Average Rating
            </div>
        </div>
        """.format(avg_rating), unsafe_allow_html=True)
    
    # Reading status distribution
    st.markdown("""
    <div class="dashboard-card-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="3" y1="9" x2="21" y2="9"></line>
            <line x1="9" y1="21" x2="9" y2="9"></line>
        </svg>
        Reading Status Distribution
    </div>
    """, unsafe_allow_html=True)
    
    status_data = c.execute("""
    SELECT status, COUNT(*) as count FROM books GROUP BY status ORDER BY count DESC
    """).fetchall()
    
    if status_data:
        status_df = pd.DataFrame(status_data, columns=["Status", "Count"])
        fig = px.bar(status_df, x="Status", y="Count", color="Status", 
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cdd6f4")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add some books to see reading status distribution!")
    
    # Books added over time
    st.markdown("""
    <div class="dashboard-card-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="20" x2="12" y2="10"></line>
            <line x1="18" y1="20" x2="18" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="16"></line>
        </svg>
        Books Added Over Time
    </div>
    """, unsafe_allow_html=True)
    
    timeline_data = c.execute("""
    SELECT substr(date_added, 1, 7) as month, COUNT(*) as count 
    FROM books 
    GROUP BY month 
    ORDER BY month
    """).fetchall()
    
    if timeline_data:
        timeline_df = pd.DataFrame(timeline_data, columns=["Month", "Books Added"])
        fig = px.line(timeline_df, x="Month", y="Books Added", markers=True)
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cdd6f4")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add some books to see your reading timeline!")
    
    # Top genres and authors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
                <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
            </svg>
            Top Genres
        </div>
        """, unsafe_allow_html=True)
        
        genre_data = c.execute("""
        SELECT genre, COUNT(*) as count FROM books GROUP BY genre ORDER BY count DESC LIMIT 5
        """).fetchall()
        
        if genre_data:
            genre_df = pd.DataFrame(genre_data, columns=["Genre", "Count"])
            fig = px.pie(genre_df, values="Count", names="Genre", hole=0.4)
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cdd6f4")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add some books to see your top genres!")
    
    with col2:
        st.markdown("""
        <div class="dashboard-card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            Top Authors
        </div>
        """, unsafe_allow_html=True)
        
        author_data = c.execute("""
        SELECT author, COUNT(*) as count FROM books GROUP BY author ORDER BY count DESC LIMIT 5
        """).fetchall()
        
        if author_data:
            author_df = pd.DataFrame(author_data, columns=["Author", "Books"])
            fig = px.bar(author_df, x="Author", y="Books", color="Books",
                        color_continuous_scale=px.colors.sequential.Viridis)
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cdd6f4")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add some books to see your favorite authors!")

# Help and tips page
def display_help():
    st.markdown('<div class="title">❓ Help & Tips</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-title">👋 Welcome to the Library Manager Help Center</div>
        <div class="welcome-text">
            This guide will help you get the most out of your Personal Library Manager app.
            Learn about all the features and how to use them effectively.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # App overview
    st.markdown("""
    <div class="dashboard-card-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
        App Overview
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    The Personal Library Manager helps you track and organize your books. Key features include:
    
    - **Dashboard**: Get an overview of your library and recent activity
    - **My Books**: View and manage all books in your collection
    - **Add Book**: Add new books to your library
    - **Search**: Find specific books by title, author, or genre
    - **Statistics**: Visualize your reading habits and preferences
    """)
    
    # How to use
    st.markdown("""
    <div class="dashboard-card-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
        How to Use
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📚 Adding a New Book"):
        st.markdown("""
        1. Click on "Add Book" in the sidebar menu
        2. Fill in the book details (title and author are required)
        3. Select the appropriate genre and reading status
        4. Add any additional information like ISBN, publication year, etc.
        5. Click "Add Book" to save it to your library
        
        The book cover will be automatically generated based on the title and genre.
        """)
    
    with st.expander("🔍 Finding Books"):
        st.markdown("""
        There are two ways to find books in your library:
        
        **Using My Books:**
        1. Go to "My Books" in the sidebar
        2. Use the filters at the top to narrow down by status or genre
        3. Sort the results by title, author, rating, or date added
        
        **Using Search:**
        1. Go to "Search" in the sidebar
        2. Enter any part of the title, author name, or genre
        3. The app will show all matching books
        4. Click "View Details" to see complete information about a book
        """)
    
    with st.expander("✏️ Editing and Deleting Books"):
        st.markdown("""
        **To edit a book:**
        1. Find the book in "My Books" or through "Search"
        2. Click the "Edit" button below the book
        3. Update any information as needed
        4. Click "Update Book" to save changes
        
        **To delete a book:**
        1. Find the book in "My Books" or through "Search"
        2. Click the "Delete" button below the book
        3. The book will be permanently removed from your library
        """)
    
    with st.expander("📊 Understanding Statistics"):
        st.markdown("""
        The Statistics page provides insights about your reading habits:
        
        - **Basic Metrics**: Total books, pages read, and average rating
        - **Reading Status**: Distribution of books by reading status
        - **Timeline**: Books added over time
        - **Top Genres**: Your most common book genres
        - **Top Authors**: Authors with the most books in your library
        
        These charts update automatically as you add, edit, or remove books.
        """)
    
    # Tips and tricks
    st.markdown("""
    <div class="dashboard-card-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        Tips and Tricks
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - **Book Covers**: The app generates unique covers based on book titles and genres
    - **Reading Progress**: Track your reading progress for books with the "Reading" status
    - **Notes**: Use the Notes field to record your thoughts, favorite quotes, or reading dates
    - **Filtering**: Combine status and genre filters to find specific books quickly
    """)
    
    # Contact and feedback
    st.markdown("""
    <div class="dashboard-card-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
        </svg>
        Feedback
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    We're constantly improving the Library Manager app. If you have suggestions or encounter any issues, please let us know!
    
    Enjoy organizing your personal library!
    """)

# Helper functions
def edit_book_modal(conn, book_id):
    c = conn.cursor()
    book = c.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    
    if not book:
        st.error("Book not found!")
        return
    
    st.markdown('<div class="subtitle">✏️ Edit Book</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Dynamic book cover
        st.markdown(generate_book_cover_html(book[1], book[2], book[3]), unsafe_allow_html=True)
    
    with col2:
        # Update preview as user types
        title = st.text_input("📕 Title*", value=book[1], key=f"edit_title_{book[0]}")
        author = st.text_input("✍️ Author*", value=book[2], key=f"edit_author_{book[0]}")
        genre = st.selectbox("🏷️ Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                      "Mystery", "Thriller", "Romance", "Biography", "History", 
                                      "Self-Help", "Business", "Science", "Other"], 
                            index=0 if not book[3] else ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                                                        "Mystery", "Thriller", "Romance", "Biography", "History", 
                                                        "Self-Help", "Business", "Science", "Other"].index(book[3]),
                            key=f"edit_genre_{book[0]}")
        
        col1, col2 = st.columns(2)
        with col1:
            isbn = st.text_input("📘 ISBN", value=book[4] or "")
            publication_year = st.number_input("📅 Publication Year", min_value=1000, max_value=datetime.now().year, step=1, value=book[5] or 2000)
        with col2:
            pages = st.number_input("📄 Pages", min_value=1, step=1, value=book[6] or 1)
            rating = st.slider("⭐ Rating", 0.0, 5.0, float(book[7] or 0.0), 0.5)
        
        status = st.selectbox("📊 Status", ["To Read", "Reading", "Completed", "DNF"], index=["To Read", "Reading", "Completed", "DNF"].index(book[8]))
        notes = st.text_area("📝 Notes", value=book[10] or "")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Update Book", use_container_width=True):
                if not title or not author:
                    st.error("Title and author are required fields.")
                else:
                    c.execute("""
                    UPDATE books SET 
                    title = ?, author = ?, genre = ?, isbn = ?, publication_year = ?, 
                    pages = ?, rating = ?, status = ?, notes = ?
                    WHERE id = ?
                    """, (title, author, genre, isbn, publication_year, pages, rating, status, notes, book_id))
                    conn.commit()
                    st.success(f"'{title}' has been updated!")
                    time.sleep(1)
                    del st.session_state.edit_book_id
                    st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                del st.session_state.edit_book_id
                st.rerun()

def delete_book(conn, book_id):
    c = conn.cursor()
    book = c.execute("SELECT title FROM books WHERE id = ?", (book_id,)).fetchone()
    
    if book:
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        st.success(f"'{book[0]}' has been deleted from your library!")

if __name__ == "__main__":
    main()


