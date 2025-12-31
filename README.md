# Inuit Luxury Concierge Chatbot ⚜️

### Analyst Intern Assignment - Task 1

**Live Demo:** [Insert Streamlit Share Link Here]  

---

## 📖 Project Overview
Inuit is a luxury online footwear shop facing a challenge: high bounce rates due to a lack of product exploration. 

This project solves that problem by replacing the static browsing experience with **"Maya," an Intelligent Styling Concierge**. Unlike standard chatbots, Maya curates choices based on the user's lifestyle (e.g., "Interview" vs. "Gym"), builds trust through transparent policies, and guides the user through a structured sales funnel: **Consultation → Selection → Showcase → Fulfillment**.

## 📸 Application Screenshots

| **1. Intelligent Consultation** | **2. Order Fulfillment & Receipt** |
|:---:|:---:|
| <img src="output 1.png"> | <img src="img2.png" width="300"> |
| *Maya detects intent ("Interview") and suggests the "Sneakers" category based on user preference, displaying persistent product cards.* | *The bot confirms the selection ("High-Top Legend"), captures sizing details, and generates a final digital receipt.* |

## ✨ Key Features (UX & Logic)
* **🧠 Intelligent Intent Recognition:** The bot understands context. It maps inputs like *"I have a meeting"* to **Formal** shoes and *"Hitting the gym"* to **Sports** shoes.
* **🖼️ Persistent Visual History:** Product cards and galleries remain visible in the chat history, allowing users to scroll back and review options without losing context.
* **🛡️ Trust & Assurance UI:** Integrated "Trust Badges" (e.g., *True to Size*, *Lifetime Warranty*) and a permanent sidebar policy reduce purchase anxiety.
* **📽️ Storytelling via Video:** Seamlessly integrates specific YouTube Shorts/Videos for "Hides," "Stitching," and "Polish" to showcase brand value.
* **🎨 Custom Luxury Design:** Uses custom CSS to override Streamlit defaults, featuring a premium Orange/Charcoal color palette and rounded chat bubbles.
* **⚡ Robust Error Handling:** Gracefully handles missing information (e.g., if a user orders without providing a size) by prompting specifically for the missing detail.

## 🛠️ Tech Stack
* **Python 3.x**
* **Streamlit** (Frontend & State Management)
* **CSS3** (Custom Styling & High Contrast Accessibility)

## 🚀 How to Run Locally

1.  **Clone or Download this repository.**
2.  **Install Dependencies:**
    Open your terminal in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```
4.  **View:** The app will open automatically in your default browser at `http://localhost:8501`.

## 📂 Project Structure
```text
Inuit_Chatbot/
│
├── app.py                # Main application logic
├── requirements.txt      # List of dependencies (streamlit, gTTS)
├── README.md             # Project documentation
└── screenshots/          # Images for documentation
    ├── consultation.png
    └── receipt.png
