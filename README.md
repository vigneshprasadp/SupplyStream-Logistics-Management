# 🚚 SupplyStream | Logistics Management System

**SupplyStream** is a high-performance logistics management platform designed to bridge the gap between complex database operations and intuitive user experiences. Developed as a DBMS core project, it simulates a real-world supply chain environment—managing everything from supplier procurement to final shipment tracking.

---

## 💡 The Inspiration
Most academic database projects focus on simple CRUD (Create, Read, Update, Delete) operations. I wanted to push further. **SupplyStream** was built to solve a logical puzzle: *How do you synchronize inventory, validate stock in real-time, and maintain data integrity across a multi-table ecosystem?*

The result is a platform that doesn't just store data—it enforces business logic, preventing "impossible" orders and tracking the lifecycle of a shipment from warehouse to doorstep.

---

## ✨ Key Features
* **📦 Intelligent Product Lifecycle:** Comprehensive management of SKUs, categories, and pricing.
* **🧾 Dynamic Order Processing:** A robust system that handles transactions while performing real-time inventory validation.
* **🚚 Decoupled Shipment Logic:** Mirroring real logistics, shipments are managed as distinct entities with independent tracking and delivery scheduling.
* **🏬 Supplier Ecosystem:** Centralized database for vendor relationships and procurement history.
* **📉 Smart Inventory:** Automated stock level checks that prevent order fulfillment if supplies are insufficient.
* **🌑 Modern Interface:** A data-rich, dark-themed dashboard designed for high readability and professional aesthetics.

---

## 🏗️ Technical Architecture
I chose a modern, decoupled stack to ensure the application is scalable and maintainable:

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) – Selected for its high performance and automatic documentation.
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) – Used to manage complex relational mappings and database migrations.
* **Database:** [MySQL](https://www.mysql.com/) – The backbone for reliable, structured data storage.
* **Frontend:** [Streamlit](https://streamlit.io/) – Leveraged to build a responsive, data-centric UI with Python.

---

## 🔄 The Logic Flow
1.  **Onboarding:** Register Suppliers and link them to specific Product lines.
2.  **Procurement:** Place Orders; the system automatically validates against current Inventory levels.
3.  **Logistics:** Generate Shipments for pending orders, assigning carriers and estimated delivery windows.
4.  **Monitoring:** Audit status updates through the centralized administrative dashboard.

---

## 🚀 Getting Started

### 1. Backend Setup
```bash

# Install dependencies
pip install -r requirements.txt
# Launch the API
uvicorn app.main:app --reload
```
### 2. Frontend Setup
```bash
    #change directory
    cd frontend

    # to run 
    streamlit run app.py