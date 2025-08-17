# Task: Web Frontend Integration

## Status
**Pending**

## Description
Connect the MySQL database with the existing web frontend ([bluemutualfund.in/app1/](https://bluemutualfund.in/app1/)) to dynamically display analysis per company and in list view. The frontend should auto-refresh (optional) and offer links such as **“View All Companies”** and **“Company Analysis Page.”**

---

## Subtasks

- **Modify `company.php`** to pull latest ML insights.
- **Add styling** for pros and cons (badges/icons).
- **Ensure compatibility** with your HTML/PHP template.
- **Test responsiveness and visibility** across devices.

---

## Notes
- Prioritize dynamic data fetching and clear UI presentation.
- Optional: Implement auto-refresh for real-time updates.
- Ensure all new features are tested before deployment.

---

## How to Run

1. **Start the PHP built-in server** from the `Task_6` directory:
   ```powershell
   php -S localhost:8000