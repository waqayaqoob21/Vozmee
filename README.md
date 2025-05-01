# 🔊 **Vozmee – Short Video Sharing Platform**

**Vozmee** is a short-form video sharing application inspired by platforms like TikTok and Instagram Reels. It allows users to upload, browse, and engage with short videos. Built using Django REST Framework, PostgreSQL, Redis, and AWS S3, Vozmee is designed to be scalable, secure, and deliver a smooth user experience.

---

## 📌 **Features**

- 🎥 Upload and stream short videos
- 🎵 Add audio/music overlays
- ❤️ Like and comment on videos
- 🔍 Explore trending videos and creators
- 👤 Follow user profiles
- ☁️ Media storage with AWS S3
- 🔐 JWT-based secure authentication
- ⚡ High-speed caching using Redis

---

## 🛠 **Tech Stack**

| Component         | Technology                              |
|-------------------|------------------------------------------|
| Backend API       | Django REST Framework (DRF)              |
| Database          | PostgreSQL                               |
| Media Storage     | AWS S3 Bucket                            |
| Caching           | Redis                                    |
| Authentication    | JWT (via `djangorestframework-simplejwt`)|
| API Docs (UI)     | drf_yasg (Swagger UI)                    |
| Background Tasks  | Crontab (Scheduled Jobs)                 |
| Video Management  | moviepy, moviepy.editor                  |
| Deployment        | Docker, Gunicorn, Nginx                  |

---

## 📥 **Setup & Installation**

### 🔧 **1. Clone the Repository**

```bash
git clone https://github.com/waqayaqoob21/Vozmee.git
cd Vozmee
```

---

### 🧪 **2. Create Virtual Environment & Install Packages**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 🗂️ **3. Configure Environment Variables**

Create a `.env` file in the root directory and fill in your configuration:

```env
DEBUG=True
SECRET_KEY=your_secret_key

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_STORAGE_BUCKET_NAME=vozmee-media

REDIS_URL=redis://localhost:6379
```

---

### 🧱 **4. Run Migrations & Create Superuser**

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

### ▶️ **5. Start the Development Server**

```bash
python manage.py runserver
```

Visit the application at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📡 **API Endpoints**

### 🔐 **Authentication**

| Method | Endpoint              | Description              |
|--------|-----------------------|--------------------------|
| POST   | `/api/register/`      | Register new users       |
| POST   | `/api/token/`         | Obtain JWT token         |
| POST   | `/api/token/refresh/` | Refresh JWT token        |

### 📽️ **Video APIs**

| Method | Endpoint                      | Description              |
|--------|-------------------------------|--------------------------|
| GET    | `/api/videos/`                | List public videos       |
| POST   | `/api/videos/upload/`         | Upload a video           |
| GET    | `/api/videos/<id>/`           | View a video             |
| POST   | `/api/videos/<id>/like/`      | Like a video             |
| POST   | `/api/videos/<id>/comment/`   | Comment on a video       |

### 👤 **User Profiles**

| Method | Endpoint                      | Description               |
|--------|-------------------------------|---------------------------|
| GET    | `/api/users/<username>/`      | View user profile         |
| POST   | `/api/follow/<username>/`     | Follow a user             |

---

## 📘 **API Documentation (Swagger UI)**

Interactive API documentation is available via Swagger UI:

👉 [http://127.0.0.1:8000/api_documentation/](http://127.0.0.1:8000/api_documentation/)

### ✅ Swagger Setup (in `urls.py`)

```python
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Vozmee API",
        default_version='v1',
        description="API documentation for Vozmee",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ... your other URL patterns
    path('api_documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
```

---

## 🖼️ **Swagger Screenshots**

![Swagger UI](https://tse3.mm.bing.net/th?id=OIP.QmvJ3wVD-_i1TocU-5dF-gHaDp&pid=Api)
![Swagger Endpoint Example](https://tse3.mm.bing.net/th?id=OIP.1tEbwvxC19RigRVzvsu3KwHaIc&pid=Api)

---

## 🚀 **Deployment Suggestions**

- 🐳 Use Docker for containerization
- 🌐 Use Gunicorn + Nginx for production servers
- ☁️ Host media files on AWS S3 and optionally serve via CloudFront
- 🔐 Store secrets securely in environment variables or secret managers
- ⚡ Use Redis for caching trending videos and user sessions
- 🕒 Automate background jobs using crontab

---

## 👨‍💻 **Author**

**Waqar Yaqoob**

- GitHub: [@waqayaqoob21](https://github.com/waqayaqoob21)  
- Email: waqaryaqoob21@gmail.com  
- LinkedIn: [linkedin.com/in/waqaryaqoob21](https://linkedin.com/in/waqaryaqoob21)

---

## 📄 **License**

This project is licensed under the **MIT License**.  
See the [`LICENSE`](LICENSE) file for details.

---

## 🌟 **Show Your Support**

If you like this project:

- ⭐ Star this repository on GitHub  
- 🧑‍💻 Share it with your network  
- ☕ Optionally support the author with kind words or coffee!
