import streamlit as st
import re
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Inuit | Intelligent Concierge", page_icon="⚜️", layout="centered")

st.markdown("""
<style>
    /* 1. Force Light Background for the Main App */
    .stApp { 
        background-color: #F9FAFB; 
        font-family: 'Helvetica Neue', sans-serif; 
    }
    
    /* 2. Header Gradient */
    .inuit-header {
        background: linear-gradient(90deg, #D9480F, #F76707);
        padding: 2rem;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-text h1 { margin: 0; font-size: 2rem; font-weight: 600; color: white !important; }
    
    /* 3. CHAT BUBBLES (The Fix) */
    div[data-testid="stChatMessageContent"] {
        background-color: #ffffff !important;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 1.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* FORCE TEXT COLOR TO BE DARK (Fixes the "Invisible Text" issue) */
    div[data-testid="stChatMessageContent"] p, 
    div[data-testid="stChatMessageContent"] div,
    div[data-testid="stChatMessageContent"] span {
        color: #1F2937 !important; /* Dark Grey */
    }

    /* 4. User Bubble (Slightly different color) */
    div[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stChatMessageContent"] {
        background-color: #FFF7ED !important; /* Light Orange Tint */
        border-color: #FFEDD5;
    }

    /* 5. Trust Badges */
    .trust-badge {
        font-size: 0.75rem;
        color: #059669 !important; /* Green */
        background: #D1FAE5 !important;
        padding: 4px 8px;
        border-radius: 12px;
        margin-right: 5px;
        display: inline-block;
        margin-bottom: 5px;
        font-weight: 600;
    }

    /* 6. Buttons */
    div.stButton > button {
        border-radius: 20px;
        border: 1px solid #F76707;
        color: #C05621 !important;
        background: white !important;
        width: 100%;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background: #F76707 !important;
        color: white !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. DATA (CATALOG) ---
CATALOG = {
    "formal": {
        "keywords": ["formal", "office", "work", "meeting", "suit", "wedding", "business"],
        "vibe": "impeccable elegance",
        "options": [
            {
                "name": "The Noir Oxford", "price": "$450", 
                "image": "https://images.unsplash.com/photo-1481729379561-24626b813364?w=500&q=80", 
                "desc": "Classic black leather. Definition of authority.",
                "fit": "True to size", "policy": "Lifetime Polish"
            },
            {
                "name": "The Sienna Derby", "price": "$420", 
                "image": "https://images.unsplash.com/photo-1549650179-8d8376246473?w=500&q=80", 
                "desc": "Rich cognac leather. Versatile sophistication.",
                "fit": "True to size", "policy": "Lifetime Polish"
            }
        ]
    },
    "sports": {
        "keywords": ["sport", "run", "gym", "training", "workout", "active"],
        "vibe": "peak performance",
        "options": [
            {
                "name": "The Velocity Runner", "price": "$180", 
                "image": "https://images.unsplash.com/photo-1516478177764-9fe5bd7e9717?w=500&q=80", 
                "desc": "Engineered mesh for breathable speed.",
                "fit": "Fits narrow", "policy": "30-Day Trial"
            },
            {
                "name": "The Endurance Trainer", "price": "$195", 
                "image": "https://images.unsplash.com/photo-1597893669661-d7253457a3ae?w=500&q=80", 
                "desc": "High-impact support for intense sessions.",
                "fit": "True to size", "policy": "30-Day Trial"
            }
        ]
    },
    "sneakers": {
        "keywords": ["sneaker", "casual", "street", "style", "jordan", "air", "weekend"],
        "vibe": "street luxury",
        "options": [
            {
                "name": "The High-Top Legend", "price": "$350", 
                "image": "https://images.unsplash.com/photo-1556906781-9a412961c28c?w=500&q=80", 
                "desc": "Iconic silhouette. Red, Black & White.",
                "fit": "Runs large", "policy": "Verified Authentic"
            },
            {
                "name": "The Air Max Pulse", "price": "$220", 
                "image": "https://images.unsplash.com/photo-1514989940723-e8875ea6ab7d?w=500&q=80", 
                "desc": "Cloud-like cushioning for all-day wear.",
                "fit": "True to size", "policy": "Verified Authentic"
            }
        ]
    }
}

# --- 3. STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "type": "text", "content": "Welcome to **Inuit**. ⚜️\n\nI am Maya, your styling concierge. I'm here to ensure you find the perfect fit."},
        {"role": "assistant", "type": "text", "content": "To start, what is the **Occasion**? (e.g., *'I have a big interview'* or *'Hitting the gym'*)"}
    ]
if "step" not in st.session_state: st.session_state.step = "consultation"
if "selected_shoe" not in st.session_state: st.session_state.selected_shoe = None

# --- 4. LOGIC ENGINE ---
def think(text):
    with st.spinner("Thinking..."):
        time.sleep(0.5)
    st.session_state.messages.append({"role": "assistant", "type": "text", "content": text})

def get_estimated_date():
    return (datetime.now() + timedelta(days=4)).strftime("%A, %b %d")

def handle_input(user_text):
    # 1. Log User Message
    st.session_state.messages.append({"role": "user", "type": "text", "content": user_text})
    
    # [cite_start]STEP 1: CONSULTATION [cite: 7]
    if st.session_state.step == "consultation":
        text = user_text.lower()
        greetings = ["hi", "hello", "hey"]
        if any(w in text for w in greetings) and len(text.split()) < 3:
            think("Hello! Are you looking for **Formal**, **Sports**, or **Sneakers**?")
            return

        found = False
        for key, data in CATALOG.items():
            if any(k in text for k in data["keywords"]):
                found = True
                # [cite_start]A. Response Text [cite: 8]
                think(f"For that, you need **{data['vibe']}**.\n\nI've curated two excellent options below. Both come with our **Quality Guarantee**.")
                # [cite_start]B. Save Cards to History [cite: 13]
                st.session_state.messages.append({
                    "role": "assistant", 
                    "type": "gallery", 
                    "content": "", 
                    "data": data["options"]
                })
                st.session_state.step = "selection_wait" # Wait for button click
                break
        
        if not found:
            # [cite_start]Fallback for misunderstanding [cite: 16]
            think("I can style you for **Formal**, **Sports**, or **Sneakers**. Which do you prefer?")
            st.session_state.step = "fallback"

    # STEP 1.5: FALLBACK
    elif st.session_state.step == "fallback":
        text = user_text.lower()
        target_cat = CATALOG["sneakers"] # default
        if "formal" in text: target_cat = CATALOG["formal"]
        elif "sport" in text or "gym" in text: target_cat = CATALOG["sports"]
        
        think("Understood. Here are the finest pairs from that collection:")
        st.session_state.messages.append({
            "role": "assistant", 
            "type": "gallery", 
            "content": "", 
            "data": target_cat["options"]
        })
        st.session_state.step = "selection_wait"

    # STEP 3: SHOWCASE (Contextual Questions)
    elif st.session_state.step == "showcase":
        if any(w in user_text.lower() for w in ["buy", "order", "get", "yes"]):
            shoe_name = st.session_state.selected_shoe['name']
            think(f"Wonderful choice. To get these to you, I just need your **Shoe Size** and the **City**.")
            st.session_state.step = "fulfillment"
        elif any(w in user_text.lower() for w in ["size", "fit"]):
             think(f"The {st.session_state.selected_shoe['name']} fits **{st.session_state.selected_shoe['fit']}**.")
        else:
             think("Take your time. Say **'Place Order'** when ready.")

    # [cite_start]STEP 4: FULFILLMENT [cite: 10]
    elif st.session_state.step == "fulfillment":
        size = re.findall(r'\d+', user_text)
        ignore = ["in", "at", "to", "size", "and", "my", "is", "for"]
        city_words = [w for w in user_text.split() if w.lower() not in ignore and not any(c.isdigit() for c in w)]
        
        if size and city_words:
            city = " ".join(city_words).title()
            shoe = st.session_state.selected_shoe
            arrival = get_estimated_date()
            # [cite_start]Final Confirmation Card [cite: 15]
            think("🎉 **Order Confirmed.**")
            st.session_state.messages.append({
                "role": "assistant",
                "type": "receipt",
                "content": "",
                "data": {"shoe": shoe, "size": size[0], "city": city, "date": arrival}
            })
            st.session_state.step = "finished"
        else:
            think("I missed a detail. Please confirm your **Size** (e.g. 10) and **City**.")

    elif st.session_state.step == "finished":
        if "start" in user_text.lower():
            st.session_state.messages = []
            st.session_state.step = "consultation"
            st.rerun()
        else:
            think("Type **'Start'** to browse again.")

def select_shoe_callback(shoe):
    st.session_state.selected_shoe = shoe
    # Log Selection
    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": f"I selected **{shoe['name']}**"
    })
    msg = f"Excellent taste. The **{shoe['name']}** is known for its {shoe['fit']} fit.\n\nBefore you commit, take 30 seconds to see the craftsmanship:"
    st.session_state.messages.append({"role": "assistant", "type": "text", "content": msg})
    st.session_state.step = "showcase"

# --- 5. RENDER UI (HISTORY LOOP) ---
st.markdown("""
<div class="inuit-header">
    <div class="header-icon">⚜️</div>
    <div class="header-text">
        <h1>INUIT</h1>
        <p>Handcrafted Italian Excellence</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Chat Loop
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="🕴️" if msg["role"] == "assistant" else "👤"):
        
        # TYPE 1: STANDARD TEXT
        if msg["type"] == "text":
            st.write(msg["content"])
        
        # [cite_start]TYPE 2: SHOE GALLERY (Suggested Shoes) [cite: 13]
        elif msg["type"] == "gallery":
            cols = st.columns(2)
            for i, shoe in enumerate(msg["data"]):
                col = cols[i % 2]
                with col:
                    st.image(shoe["image"], use_container_width=True)
                    st.markdown(f"**{shoe['name']}**")
                    st.markdown(f"""<span class="trust-badge">📏 {shoe['fit']}</span><span class="trust-badge">🛡️ {shoe['policy']}</span>""", unsafe_allow_html=True)
                    st.caption(f"{shoe['price']}")
                    if st.button("Select Pair", key=f"btn_{idx}_{i}"):
                        select_shoe_callback(shoe)
                        st.rerun()

        # TYPE 3: RECEIPT (Final Order)
        elif msg["type"] == "receipt":
            data = msg["data"]
            st.success(f"Reserved: {data['shoe']['name']}")
            st.markdown(f"**Size:** {data['size']} • **City:** {data['city']}")
            st.caption(f"Estimated Arrival: {data['date']}")

# [cite_start]--- 6. DYNAMIC FOOTER (Showcase Videos) [cite: 9] ---
if st.session_state.step == "showcase":
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1: st.video("https://www.youtube.com/shorts/_HkoDWPjgYs"); st.caption("1. Hides")
        with c2: st.video("https://www.youtube.com/watch?v=RxQENDONmlQ"); st.caption("2. Stitching")
        with c3: st.video("https://www.youtube.com/shorts/Q-OHsxEX-a0"); st.caption("3. Polish")
        
        if st.button("🛍️ Place Order", type="primary"):
            handle_input("I want to buy")
            st.rerun()

if prompt := st.chat_input("Type your response..."):
    handle_input(prompt)
    st.rerun()
