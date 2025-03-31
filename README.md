# 📏 PixiTape

**PixiTape** is a full-stack application that allows users to upload an image, set a pixel-to-mm ratio, and view labeled length/width measurements on the object within the image.

Built with:

* Backend: **Django + Django REST Framework + OpenCV**
* Frontend: **React + Axios**

---

## 🚀 Features

* Upload any image with an object (e.g., pencil, marker, bill)
* Specify pixel-to-mm ratio
* Automatically detect and label dimensions
* View original + measured images side-by-side

---

## 🛠 Folder Structure

```
pixiTape/
├── measureit/             # Django backend
│   └── ...
├── measureit-frontend/   # React frontend
│   └── ...
```

---

## 🐍 Backend Setup (Django)

### 1. Create Virtual Environment

```
cd measureit
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Required Packages

```
pip install -r requirements.txt
```

> If `<span>requirements.txt</span>` is missing, manually run:

```
pip install django djangorestframework pillow opencv-python django-cors-headers
```

### 3. Run Migrations

```
python manage.py migrate
```

### 4. Start Server

```
python manage.py runserver
```

> ✅ Backend will run at: `<span>http://localhost:8000</span>`

---

## ⚛️ Frontend Setup (React)

### 1. Install Node Modules

```
cd measureit-frontend
npm install
```

### 2. Start React Dev Server

```
npm start
```

> ✅ Frontend will run at: `<span>http://localhost:3000</span>`

Make sure your Django backend is running in parallel.

---

## 🧪 How to Use

1. Open `<span>http://localhost:3000</span>`
2. Enter pixel-to-mm ratio (e.g., 0.1193)
3. Upload an image
4. Click **"Measure Length"**
5. View original and labeled images side-by-side

> ℹ️ To calculate pixel-to-mm ratio: place a ruler or object with known size in the image. Divide real size (in mm) by its pixel length from the image. Example 100 mm object / 985 pixel = 0.1015

---

## 📦 Optional: Sample Requirements File (Backend)

### `<span>measureit/requirements.txt</span>`

```
django
djangorestframework
pillow
opencv-python
django-cors-headers
```

---

## 📸 Credits

Built with ❤️ for easy, accurate, and user-friendly object measurement.

---

## 📬 Questions / Issues

Open an issue or ping the dev team!
