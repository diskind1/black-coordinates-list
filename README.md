# Black Coordinates List

## תיאור הפרויקט
פרויקט **Black Coordinates List** הוא מערכת מבוססת Microservices שמטרתה לקבל כתובת IP, להמיר אותה לקואורדינטות גיאוגרפיות (Latitude, Longitude),
ולשמור את המידע בצורה מרכזית לצורך ניתוח, מעקב או שימוש עתידי.

המערכת בנויה כך שכל רכיב אחראי על תפקיד ברור, ומתקשרת באמצעות HTTP ו־Redis.

---

## ארכיטקטורה כללית

הפרויקט כולל שלושה רכיבים עיקריים:

### 🔹 Service A
- מקבל בקשת API עם כתובת IP
- פונה לשירות חיצוני (GeoIP)
- מחזיר קואורדינטות ללקוח
- שולח את הנתונים ל־Service B

### 🔹 Service B
- מקבל קואורדינטות מ־Service A
- שומר את הנתונים ב־Redis
- מאפשר שליפה עתידית של המידע

### 🔹 Redis
- בסיס נתונים In‑Memory
- שומר רשימת קואורדינטות
- משותף לשני השירותים

---

## זרימת המידע (Flow)

1. הלקוח שולח בקשת POST ל־Service A עם IP
2. Service A פונה לשירות GeoIP חיצוני
3. מתקבלות קואורדינטות
4. הנתונים נשלחים ל־Service B
5. Service B שומר את הנתונים ב־Redis
6. Service A מחזיר תשובה ללקוח

---

## טכנולוגיות
- Python 3.11
- FastAPI
- Docker & Docker Compose
- Redis
- OpenShift
- Git & GitHub

---

## הרצה
הפרויקט ניתן להרצה:
- לוקאלית באמצעות Docker Compose
- בסביבת Cloud באמצעות OpenShift

קבצי YAML נמצאים בתיקיית `k8s/`  
קבצי Docker נמצאים בכל Service בנפרד.

---

## מטרות הפרויקט
- תרגול עבודה עם Microservices
- שימוש ב־Redis
- עבודה עם Docker ו־OpenShift
- הפרדת אחריות בין שירותים
- תיעוד והרצה מסודרת של מערכת מבוזרת
