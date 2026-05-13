import streamlit as st
import pickle
import requests
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="MoodFlix", page_icon="🎭", layout="wide")

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Raleway:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Serif+Display:ital@0;1&display=swap');

.stApp { background:#050510; }

[data-testid="stHeader"] { display:none !important; }
[data-testid="stToolbar"] { display:none !important; }
[data-testid="stDecoration"] { display:none !important; }

.block-container {
    padding-top:0rem !important;
    padding-left:1rem !important;
    padding-right:1rem !important;
    max-width:100% !important;
}

div[data-testid="stVerticalBlock"] > div {
    border: none !important;
    box-shadow: none !important;
}

.hero-container{
    position:relative;
    width:100%;
    height:600px;
    border-radius:0px;
    overflow:hidden;
    border:none !important;
    outline:none !important;
    box-shadow:none !important;
    margin-bottom:35px;
}

.poster-grid{
    position:absolute;
    inset:0;
    display:grid;
    grid-template-columns:repeat(8, 1fr);
    grid-template-rows:repeat(3, 1fr);
    gap:4px;
    z-index:0;
    transform:skewY(-3deg) scale(1.15);
    transform-origin:center center;
}

.poster-cell{
    background-size:cover;
    background-position:center;
    width:100%;
    height:100%;
    border-radius:4px;
}

.hero-overlay{
    position:absolute;
    inset:0;
    background:
        linear-gradient(to right, rgba(5,5,16,0.6) 0%, rgba(5,5,16,0.2) 50%, rgba(5,5,16,0.6) 100%),
        linear-gradient(to bottom, rgba(5,5,16,0.3) 0%, rgba(5,5,16,0.5) 60%, rgba(5,5,16,0.95) 100%);
    z-index:1;
}

.hero-content{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    text-align:center;
    width:100%;
    z-index:2;
}

.main-title{
    font-family:'Cinzel', serif;
    font-size:8rem;
    font-weight:700;
    letter-spacing:14px;
    background:linear-gradient(90deg,#c084fc,#f472b6,#c084fc);
    background-size:200% auto;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation:shine 4s linear infinite;
    margin-bottom:30px;
}

.hero-tagline-box{
    display:inline-block;
    padding:28px 70px;
    border-radius:30px;
    background:transparent !important;
    border:none !important;
    outline:none !important;
    box-shadow:none !important;
    backdrop-filter:none !important;
}

.hero-tagline{
    font-family:'Raleway', sans-serif;
    font-size:2.8rem;
    font-weight:800;
    letter-spacing:4px;
    color:white;
    margin:0;
    line-height:1.4;
    text-shadow:
        0 0 20px rgba(236,72,153,0.6),
        0 0 40px rgba(167,139,250,0.4),
        0 2px 20px rgba(0,0,0,0.9);
}

.hero-highlight{
    font-family:'Playfair Display', serif;
    font-style:italic;
    font-size:3.2rem;
    background:linear-gradient(90deg, #f472b6, #a855f7, #f97316, #f472b6);
    background-size:300% auto;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation:shine 3s linear infinite;
    text-shadow:none;
    padding:0 4px;
}

.hero-small-wrapper{
    margin-top:30px;
    display:flex;
    justify-content:center;
    align-items:center;
}

.hero-small{
    display:inline-flex;
    align-items:center;
    gap:18px;
    padding:14px 44px;
    border-radius:50px;
    background:linear-gradient(135deg, rgba(167,139,250,0.15), rgba(236,72,153,0.15));
    border:1.5px solid rgba(236,72,153,0.5);
    box-shadow:
        0 0 20px rgba(236,72,153,0.3),
        0 0 40px rgba(167,139,250,0.2),
        inset 0 0 20px rgba(167,139,250,0.05);
    backdrop-filter:blur(10px);
    animation:pulse-border 3s ease-in-out infinite;
}

.hero-small span{
    font-family:'Raleway', sans-serif;
    font-size:1.15rem;
    font-weight:800;
    letter-spacing:10px;
    text-transform:uppercase;
    background:linear-gradient(90deg, #c4b5fd, #f9a8d4, #c4b5fd);
    background-size:200% auto;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation:shine 4s linear infinite;
}

.hero-small .dot{
    width:5px;
    height:5px;
    border-radius:50%;
    background:linear-gradient(135deg,#a855f7,#ec4899);
    box-shadow:0 0 8px rgba(236,72,153,0.8);
    flex-shrink:0;
    animation:dot-pulse 2s ease-in-out infinite;
}

.section-heading {
    font-family: 'Cinzel', serif !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    letter-spacing: 5px !important;
    text-transform: uppercase !important;
    background: linear-gradient(90deg, #c084fc, #f472b6, #c084fc);
    background-size: 200% auto;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: shine 5s linear infinite;
    margin: 28px 0 20px 0 !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid rgba(167,139,250,0.2) !important;
    display: block !important;
}

/* ── HIDE native stButton completely when we use custom HTML buttons ── */
.stButton > button {
    display: none !important;
}

/* =============================================
   CUSTOM ERA & MOOD BUTTONS
   ============================================= */

.custom-btn-grid {
    display: grid;
    gap: 14px;
    margin-bottom: 10px;
}

.era-grid   { grid-template-columns: repeat(4, 1fr); }
.mood-grid  { grid-template-columns: repeat(3, 1fr); }

.custom-btn {
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 130px;
    background: rgba(10, 8, 28, 0.75);
    border: 1px solid rgba(167,139,250,0.22);
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    backdrop-filter: blur(12px);
    box-shadow: 0 2px 20px rgba(5,5,16,0.6), inset 0 1px 0 rgba(167,139,250,0.08);
    text-decoration: none !important;
    padding: 0 18px;
}

.custom-btn::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), transparent);
}

.custom-btn:hover {
    background: linear-gradient(145deg, rgba(88,28,135,0.35), rgba(157,23,77,0.25));
    border-color: rgba(196,132,252,0.6);
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 35px rgba(88,28,135,0.35), 0 0 25px rgba(236,72,153,0.18), inset 0 1px 0 rgba(255,255,255,0.08);
}

.custom-btn.active {
    background: linear-gradient(145deg, rgba(109,40,217,0.45), rgba(157,23,77,0.38)) !important;
    border: 1px solid rgba(196,132,252,0.75) !important;
    box-shadow: 0 0 0 1px rgba(167,139,250,0.3), 0 8px 32px rgba(109,40,217,0.45), 0 0 50px rgba(196,132,252,0.15), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

.btn-emoji {
    font-size: 1.9rem;
    line-height: 1;
}

.btn-label {
    font-family: 'DM Serif Display', serif;
    font-size: 1.55rem;
    font-weight: 400;
    font-style: italic;
    letter-spacing: 1.5px;
    color: #f0e6ff;
    line-height: 1.1;
    text-align: center;
}

.btn-sub {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-weight: 400;
    letter-spacing: 2px;
    color: rgba(196,181,253,0.7);
    text-align: center;
    line-height: 1.2;
}

/* =============================================
   MOVIE RESULT CARDS
   ============================================= */

.movie-card {
    background: linear-gradient(160deg, rgba(15,10,35,0.95), rgba(25,10,40,0.9));
    border: 1px solid rgba(167,139,250,0.15);
    border-radius: 16px;
    padding: 14px 12px 18px 12px;
    margin-top: 10px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}

.movie-card::before {
    content: '';
    position: absolute;
    top: 0; left: 15%; right: 15%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.35), transparent);
}

.movie-card:hover {
    border-color: rgba(196,132,252,0.4);
    transform: translateY(-3px);
    box-shadow: 0 10px 35px rgba(109,40,217,0.25), 0 0 20px rgba(236,72,153,0.1);
}

.movie-title {
    font-family: 'Cinzel', serif;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #f0e6ff;
    margin: 0 0 10px 0;
    line-height: 1.4;
    text-shadow: 0 0 15px rgba(167,139,250,0.3);
}

.movie-meta {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-weight: 400;
    letter-spacing: 1px;
    color: rgba(196,181,253,0.85);
    margin: 4px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

.movie-match {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-style: italic;
    letter-spacing: 1px;
    background: linear-gradient(90deg, #f9a8d4, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 6px 0 0 0;
}

.movie-rank {
    position: absolute;
    top: 8px;
    right: 10px;
    font-family: 'Cinzel', serif;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: rgba(167,139,250,0.4);
}

/* Back button — keep native for results page */
.back-btn > button {
    display: flex !important;
    background: rgba(10,8,28,0.7) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    color: #d4c5f9 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 2px !important;
    border-radius: 10px !important;
    padding: 8px 22px !important;
}

@keyframes pulse-border{
    0%,100%{ box-shadow: 0 0 20px rgba(236,72,153,0.3), 0 0 40px rgba(167,139,250,0.2), inset 0 0 20px rgba(167,139,250,0.05); }
    50%{ box-shadow: 0 0 30px rgba(236,72,153,0.55), 0 0 60px rgba(167,139,250,0.35), inset 0 0 30px rgba(167,139,250,0.1); }
}

@keyframes dot-pulse{
    0%,100%{ transform:scale(1); opacity:1; }
    50%{ transform:scale(1.6); opacity:0.7; }
}

@keyframes shine { to { background-position:200% center; } }

hr { border:none !important; border-top:1px solid rgba(167,139,250,0.12) !important; margin: 30px 0 !important; }
img { border-radius:12px; border:1px solid rgba(167,139,250,0.25); }
p,h2,h3 { color:white !important; }

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================

movies = pickle.load(open('model/movie_list.pkl', 'rb'))
cv = pickle.load(open('model/cv.pkl', 'rb'))
vectors = cv.transform(movies['tags']).toarray()

API_KEY = "56c2d898d35f479689951fd7e0242a98"

# =========================
# FETCH POSTER
# =========================

def fetch_poster(movie_id):
    try:
        movie_id = int(movie_id)
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# =========================
# MOOD TAGS
# =========================

mood_tags = {
    '🤯 Mind Bending': "scifi thriller mystery dream twist mind psychology illusion reality",
    '🚀 Adventure':    "action adventure fantasy epic hero journey quest warrior",
    '❤️ Romance':      "love romance drama relationship emotion heart passion wedding",
    '😂 Comedy':       "comedy funny humor laugh lighthearted fun entertaining silly",
    '😨 Edge of Seat': "horror suspense dark crime thriller violence scary tension",
    '😢 Emotional':    "sad drama grief loss family emotional deep touching heart"
}

# =========================
# RECOMMEND FUNCTION
# =========================

def recommend(mood, era=None):
    mood_vector = cv.transform([mood_tags[mood]]).toarray()
    mood_similarity = cosine_similarity(mood_vector, vectors)[0]
    movies_list = sorted(list(enumerate(mood_similarity)), reverse=True, key=lambda x: x[1])
    recommended = []
    for i in movies_list[1:]:
        movie = movies.iloc[i[0]]
        if era and era != 'All':
            year = int(str(movie['release_date'])[:4])
            if era == 'New'     and year < 2010:              continue
            if era == 'Mid'     and not (1990 <= year < 2010): continue
            if era == 'Classic' and year >= 1990:             continue
        recommended.append({
            'title':    movie['title'],
            'movie_id': movie['movie_id'],
            'rating':   movie['vote_average'],
            'score':    round(i[1] * 100, 1),
            'year':     str(movie['release_date'])[:4]
        })
        if len(recommended) == 10:
            break
    return recommended

# =========================
# SESSION STATE
# =========================

if 'page'          not in st.session_state: st.session_state.page          = 'home'
if 'selected_mood' not in st.session_state: st.session_state.selected_mood = None
if 'selected_era'  not in st.session_state: st.session_state.selected_era  = 'All'

# =========================
# URL-PARAM TRIGGERS
# (custom HTML buttons post to ?era=X or ?mood=X)
# =========================

params = st.query_params

if 'era' in params:
    st.session_state.selected_era = params['era']
    st.query_params.clear()
    st.rerun()

if 'mood' in params:
    raw = params['mood']
    # map URL-safe key back to full mood key
    mood_map = {
        'mind':      '🤯 Mind Bending',
        'adventure': '🚀 Adventure',
        'romance':   '❤️ Romance',
        'comedy':    '😂 Comedy',
        'edge':      '😨 Edge of Seat',
        'emotional': '😢 Emotional',
    }
    if raw in mood_map:
        st.session_state.selected_mood = mood_map[raw]
        st.session_state.page = 'results'
        st.query_params.clear()
        st.rerun()

# =========================
# HOME PAGE
# =========================

if st.session_state.page == 'home':

    posters = [
        "https://image.tmdb.org/t/p/w300/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "https://image.tmdb.org/t/p/w300/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "https://image.tmdb.org/t/p/w300/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
        "https://image.tmdb.org/t/p/w300/6CoRTJTmijhBLJTUNoVSUNxZMEI.jpg",
        "https://image.tmdb.org/t/p/w300/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "https://image.tmdb.org/t/p/w300/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "https://image.tmdb.org/t/p/w300/3bhkrj58Vtu7enYsLe1rjPU5Abe.jpg",
        "https://image.tmdb.org/t/p/w300/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
        "https://image.tmdb.org/t/p/w300/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "https://image.tmdb.org/t/p/w300/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
        "https://image.tmdb.org/t/p/w300/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg",
        "https://image.tmdb.org/t/p/w300/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg",
        "https://image.tmdb.org/t/p/w300/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg",
        "https://image.tmdb.org/t/p/w300/qNBAXBIQlnOThrVvA6mA2B5ggV6.jpg",
        "https://image.tmdb.org/t/p/w300/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "https://image.tmdb.org/t/p/w300/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
        "https://image.tmdb.org/t/p/w300/svIDTNUoajS8dLEo7EosxvyAsgJ.jpg",
        "https://image.tmdb.org/t/p/w300/5YZbUmjbMa3ClvSW1Wj3D6XGkVA.jpg",
        "https://image.tmdb.org/t/p/w300/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
        "https://image.tmdb.org/t/p/w300/xvk18d3iqwdcPccRtOyTCqAaAaY.jpg",
        "https://image.tmdb.org/t/p/w300/nBNZadXqJSdt05SHLqgT0HuC5Gm.jpg",
        "https://image.tmdb.org/t/p/w300/lmZFxXgJE3vgrciwuDib0N8CfQo.jpg",
        "https://image.tmdb.org/t/p/w300/6MKr3KgOLmzOP6MSuZERO41Lpbb.jpg",
        "https://image.tmdb.org/t/p/w300/mSD1JPS4GjNSMITv9HLWPsrBGMp.jpg",
    ]

    poster_cells = "".join([
        f'<div class="poster-cell" style="background-image:url(\'{p}\')"></div>'
        for p in posters
    ])

    st.markdown(f"""
    <div class="hero-container">
        <div class="poster-grid">{poster_cells}</div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="main-title">🎬 MOODFLIX</div>
            <div class="hero-tagline-box">
                <p class="hero-tagline">
                    Find your <span class="hero-highlight">perfect</span> watch mood 🍿
                </p>
            </div>
            <div class="hero-small-wrapper">
                <div class="hero-small">
                    <div class="dot"></div>
                    <span>LIGHTS &nbsp;&nbsp;•&nbsp;&nbsp; CAMERA &nbsp;&nbsp;•&nbsp;&nbsp; ACTION</span>
                    <div class="dot"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ERA SELECTOR ───────────────────────────────────────────────────
    st.markdown('<span class="section-heading">🕐 &nbsp; Choose Your Movie Era</span>', unsafe_allow_html=True)

    sel_era = st.session_state.selected_era

    era_options = [
        ('All',     '🌐', 'All Eras',   'Every decade'),
        ('New',     '✨', 'New Age',    '2010 & beyond'),
        ('Mid',     '🎬', 'Golden Mid', '1990 – 2009'),
        ('Classic', '🎞️', 'Classics',   'Before 1990'),
    ]

    era_html = '<div class="custom-btn-grid era-grid">'
    for val, emoji, label, sub in era_options:
        active_cls = 'active' if sel_era == val else ''
        era_html += f"""
        <a class="custom-btn {active_cls}" href="?era={val}">
            <div class="btn-emoji">{emoji}</div>
            <div class="btn-label">{label}</div>
            <div class="btn-sub">{sub}</div>
        </a>"""
    era_html += '</div>'
    st.markdown(era_html, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── MOOD SELECTOR ──────────────────────────────────────────────────
    st.markdown('<span class="section-heading">🎭 &nbsp; Select Your Mood</span>', unsafe_allow_html=True)

    mood_options = [
        ('mind',      '🤯', 'Mind Bending',  'Sci-fi · Thriller · Mystery'),
        ('adventure', '🚀', 'Adventure',      'Action · Fantasy · Epic'),
        ('romance',   '❤️', 'Romance',        'Love · Drama · Emotion'),
        ('comedy',    '😂', 'Comedy',         'Funny · Lighthearted · Fun'),
        ('edge',      '😨', 'Edge of Seat',   'Horror · Suspense · Dark'),
        ('emotional', '😢', 'Emotional',      'Sad · Family · Deep'),
    ]

    mood_html = '<div class="custom-btn-grid mood-grid">'
    for key, emoji, label, sub in mood_options:
        mood_html += f"""
        <a class="custom-btn" href="?mood={key}">
            <div class="btn-emoji">{emoji}</div>
            <div class="btn-label">{label}</div>
            <div class="btn-sub">{sub}</div>
        </a>"""
    mood_html += '</div>'
    st.markdown(mood_html, unsafe_allow_html=True)

# =========================
# RESULTS PAGE
# =========================

if st.session_state.page == 'results':

    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown(
        f"<h2 style='text-align:center; font-family:Cinzel,serif; letter-spacing:4px; text-shadow:0 0 20px rgba(167,139,250,0.8);'>Top 10 Movies for {st.session_state.selected_mood}</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='text-align:center; font-family:Cormorant Garamond,serif; font-size:1.2rem; letter-spacing:4px; color:rgba(196,181,253,0.7);'>— Era: {st.session_state.selected_era} —</p>",
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    results = recommend(st.session_state.selected_mood, st.session_state.selected_era)

    for i in range(0, len(results), 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if i + j < len(results):
                movie = results[i + j]
                rank = i + j + 1
                with col:
                    poster = fetch_poster(movie['movie_id'])
                    st.image(poster, use_container_width=True)
                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="movie-rank">#{rank}</div>
                        <div class="movie-title">{movie['title']}</div>
                        <div class="movie-meta">⭐ {movie['rating']} &nbsp;·&nbsp; 📅 {movie['year']}</div>
                        <div class="movie-match">🎯 {movie['score']}% match</div>
                    </div>
                    """, unsafe_allow_html=True)