# Electronic Attendance Management System

## 📌 Project Description
The Electronic Attendance Management System is a web-based application designed for private educational centers to manage student attendance efficiently.  
Teachers can record attendance through a simple interface, and once attendance is saved, an automatic notification is sent to the parent via SMS or WhatsApp to confirm the student’s presence in real time.

The system improves discipline, transparency, and communication between educational centers and parents.

---

## 🎯 Features
- Secure teacher login system
- Student attendance management (Present / Absent)
- Automatic parent notification via SMS or WhatsApp
- Organized student and attendance records
- Role-based access control
- Activity logging for auditing purposes

---

## 🛠 Technologies Used
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Database:** SQLite / MySQL  
- **Messaging API:** Twilio SMS / WhatsApp Business API  

---

## 🧱 System Architecture
The system consists of three main components:
1. **Frontend:** User interface for teachers to record attendance.
2. **Backend:** Handles business logic, database operations, and messaging.
3. **Database:** Stores students, teachers, and attendance records.

---

## 🔄 System Workflow
1. Teacher logs into the system.
2. Selects the class or group.
3. Marks student attendance.
4. Clicks the "Save Attendance" button.
5. The system saves attendance data and sends a notification to the parent automatically.

---

## 📂 Database Structure
### Students Table
- id
- name
- parent_phone
- class
- created_at

### Attendance Table
- id
- student_id
- date
- status

### Teachers Table
- id
- username
- password (encrypted)

---

## 🔐 Security Features
- Encrypted passwords
- Restricted access for authorized teachers only
- Prevention of duplicate attendance entries
- System activity logs

---

## 🚀 Future Enhancements
- QR code-based attendance
- Monthly attendance reports (PDF)
- Mobile application support
- Automatic absence alerts
- Integration with payment systems

---

## ▶️ How to Run the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/marwan-yasser644/attendance-system.git
