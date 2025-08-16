# 🌍 Eco-Friendly Route Finder

An interactive **Flask-based web application** that helps users find eco-friendly routes with distance, duration, and estimated CO₂ emissions.
It integrates **OpenRouteService API**, **Folium maps**, and provides **user authentication** for a personalized experience.

---

## ✨ Features

* 🔑 User login & registration system (with password hashing)
* 📍 Enter origin & destination to find routes
* 🚴 Choose transport mode: Driving, Cycling, Walking
* 🛣️ Displays **distance** and **duration** of the route
* 🌱 Calculates **estimated CO₂ emissions**
* 🗺️ Interactive route map generated with **Folium**
* 🎨 Styled with HTML + CSS for a clean UI
* 📊 Dashboard view with recent searches and saved routes
* 📂 Stores generated maps in `static/maps/` for easy access

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS
* **Database:** SQLite
* **Maps & Routing:** OpenRouteService API + Folium
* **Authentication:** Werkzeug security (hashed passwords)

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/eco-route-finder.git
cd eco-route-finder
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows use venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file and add your **OpenRouteService API key**:

```env
ORS_API_KEY=your_api_key_here
FLASK_APP=app.py
FLASK_ENV=development
```

### 5. Run the application

```bash
flask run
```

The app will be available at **[http://127.0.0.1:5000](http://127.0.0.1:5000)** 🚀

---

## 📸 Screenshots

*📝 Register Page
<img width="1432" height="585" alt="Screenshot 2025-05-25 095400" src="https://github.com/user-attachments/assets/205a7727-8b04-4d44-8106-a990e5c9cf5d" />

*👤 Login Page
<img width="1397" height="648" alt="Screenshot 2025-05-25 095342" src="https://github.com/user-attachments/assets/d45757ad-0400-4ef6-8944-c244e0f96ec3" />

* 🌍 Route search page
 <img width="1835" height="905" alt="Screenshot 2025-05-25 104347" src="https://github.com/user-attachments/assets/cedbc0eb-5bed-47da-9aa5-c48b8a08d5b5" />
  
* 🗺️ Map view with route
  <img width="1919" height="1079" alt="Screenshot 2025-05-29 211721" src="https://github.com/user-attachments/assets/e465665b-aeb7-4a3a-b2f6-7a4eb70d0bd5" />

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to use and modify! ✨

