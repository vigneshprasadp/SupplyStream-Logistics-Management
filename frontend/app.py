import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date


st.set_page_config(
    page_title="Logistics Pro Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


API_URL = "http://127.0.0.1:8000"


st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #00f2ff !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
    }
    
    /* Cards/Containers */
    .stDataFrame, .stForm {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(45deg, #00f2ff, #bd00ff);
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(189, 0, 255, 0.4);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.6);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 8px 8px 0 0;
        color: #8b949e;
        border: 1px solid #30363d;
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0e1117 !important;
        color: #00f2ff !important;
        border-top: 2px solid #00f2ff !important;
    }
    
    /* Success/Error Messages */
    .stAlert {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-left: 5px solid #00f2ff;
        border-radius: 8px;
    }
    
    /* Table Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 8px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("🚚 Logistics Pro")
    st.markdown("---")
    menu = st.radio(
        "Navigate",
        ["Dashboard", "Suppliers", "Products", "Orders", "Shipments"],
        index=0
    )
    st.markdown("---")
    st.caption("System Status: 🟢 Online")
    st.caption("v2.1.0 | Dark Mode")

# --- HELPER FUNCTIONS ---
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def show_success(message):
    st.markdown(f"""
        <div style="padding: 1rem; background: rgba(0, 242, 255, 0.1); border: 1px solid #00f2ff; border-radius: 8px; color: #00f2ff; margin-bottom: 1rem;">
            ✨ {message}
        </div>
    """, unsafe_allow_html=True)

def show_error(message):
    st.markdown(f"""
        <div style="padding: 1rem; background: rgba(255, 0, 85, 0.1); border: 1px solid #ff0055; border-radius: 8px; color: #ff0055; margin-bottom: 1rem;">
            ⚠️ {message}
        </div>
    """, unsafe_allow_html=True)


if menu == "Dashboard":
    st.title("📊 System Overview")
    st.markdown("Welcome to the **Logistics Management Command Center**.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with st.spinner("Loading metrics..."):
        products = fetch_data("products/")
        orders = fetch_data("orders/")
        shipments = fetch_data("shipments/")
        suppliers = fetch_data("suppliers/")
    

    def metric_card(title, value, icon, color):
        st.markdown(f"""
            <div style="background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                <h3 style="color: {color} !important; margin: 0; font-size: 2rem;">{value}</h3>
                <p style="color: #8b949e; margin: 5px 0 0 0; font-size: 1rem;">{icon} {title}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col1: metric_card("Products", len(products), "📦", "#00f2ff")
    with col2: metric_card("Orders", len(orders), "🛒", "#bd00ff")
    with col3: metric_card("Shipments", len(shipments), "🚚", "#00f2ff")
    with col4: metric_card("Suppliers", len(suppliers), "🏭", "#bd00ff")
    
    st.markdown("### 📉 Recent Activity")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Latest Orders")
        if orders:
            st.dataframe(pd.DataFrame(orders).tail(5), use_container_width=True)
        else:
            st.info("No recent orders")
            
    with c2:
        st.markdown("#### Pending Shipments")
        if shipments:
            df_ship = pd.DataFrame(shipments)
            if not df_ship.empty and 'status' in df_ship.columns:
                st.dataframe(df_ship[df_ship['status'] != 'Delivered'].tail(5), use_container_width=True)
            else:
                st.dataframe(df_ship.tail(5), use_container_width=True)
        else:
            st.info("No pending shipments")


elif menu == "Suppliers":
    st.title("🏭 Supplier Management")
    
    tab1, tab2 = st.tabs(["➕ Add Supplier", "📋 View Suppliers"])
    
    with tab1:
        st.markdown("### Add New Supplier")
        with st.form("supplier_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Supplier Name", placeholder="e.g. Global Tech Supplies")
                contact = st.text_input("Contact Person", placeholder="e.g. John Doe")
            with c2:
                phone = st.text_input("Phone Number", placeholder="e.g. +1 234 567 890")
                address = st.text_input("Address", placeholder="Full business address")
            
            submitted = st.form_submit_button("🏭 Add Supplier")
            
            if submitted:
                if not name or not address:
                    show_error("Name and Address are required!")
                else:
                    payload = {
                        "name": name,
                        "address": address,
                        "contact_person": contact,
                        "phone_number": phone
                    }
                    try:
                        res = requests.post(f"{API_URL}/suppliers/", json=payload)
                        if res.status_code == 200:
                            show_success("Supplier added successfully!")
                        else:
                            show_error(f"Failed: {res.text}")
                    except Exception as e:
                        show_error(f"Connection Error: {e}")

    with tab2:
        st.markdown("### 📋 Registered Suppliers")
        with st.spinner("Fetching suppliers..."):
            suppliers = fetch_data("suppliers/")
            if suppliers:
                st.dataframe(pd.DataFrame(suppliers), use_container_width=True)
            else:
                st.info("No suppliers found.")


elif menu == "Products":
    st.title("📦 Product Inventory")
    
    tab1, tab2 = st.tabs(["➕ Add Product", "📋 View Inventory"])
    
    with tab1:
        st.markdown("### Add New Product")
        with st.form("product_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Product Name", placeholder="e.g. Wireless Mouse")
                unit_price = st.number_input("Unit Price ($)", min_value=0.0, step=0.01)
            with c2:
                quantity = st.number_input("Quantity Available", min_value=0, step=1)
                description = st.text_input("Description", placeholder="Short product description")
            
            submitted = st.form_submit_button("🚀 Add Product")
            
            if submitted:
                if not name:
                    show_error("Product name is required")
                else:
                    payload = {
                        "name": name,
                        "description": description,
                        "unit_price": unit_price,
                        "quantity_available": quantity
                    }
                    try:
                        res = requests.post(f"{API_URL}/products/", json=payload)
                        if res.status_code == 200:
                            show_success("Product added successfully!")
                        else:
                            show_error(f"Failed: {res.text}")
                    except Exception as e:
                        show_error(f"Connection Error: {e}")

    with tab2:
        st.markdown("### 📋 Current Inventory")
        with st.spinner("Fetching products..."):
            products = fetch_data("products/")
            if products:
                df = pd.DataFrame(products)
                st.dataframe(
                    df, 
                    use_container_width=True,
                    column_config={
                        "unit_price": st.column_config.NumberColumn("Price", format="$%.2f"),
                        "quantity_available": st.column_config.ProgressColumn("Stock", min_value=0, max_value=100, format="%d")
                    }
                )
            else:
                st.info("No products found in the system.")


elif menu == "Orders":
    st.title("🛒 Order Management")
    
    tab1, tab2, tab3 = st.tabs(["➕ Place Order", "📋 Order History", "❌ Cancel Order"])
    
    with tab1:
        st.markdown("### Place New Order")
        
        products = fetch_data("products/")
        suppliers = fetch_data("suppliers/")
        
        if not products or not suppliers:
            st.warning("⚠️ Please add Products and Suppliers first.")
        else:
            with st.form("order_form"):
                c1, c2 = st.columns(2)
                with c1:
                    prod_map = {f"{p['name']} (Stock: {p['quantity_available']})": p['product_id'] for p in products}
                    selected_prod = st.selectbox("Select Product", options=list(prod_map.keys()))
                with c2:
                    sup_map = {s['name']: s['supplier_id'] for s in suppliers}
                    selected_sup = st.selectbox("Select Supplier", options=list(sup_map.keys()))
                
                quantity = st.number_input("Quantity Ordered", min_value=1, step=1)
                
                submitted = st.form_submit_button("🛒 Place Order")
                
                if submitted:
                    payload = {
                        "product_id": prod_map[selected_prod],
                        "supplier_id": sup_map[selected_sup],
                        "quantity_ordered": quantity,
                        "order_date": datetime.now().isoformat()
                    }
                    try:
                        res = requests.post(f"{API_URL}/orders/", json=payload)
                        if res.status_code == 200:
                            show_success("Order placed successfully!")
                        else:
                            show_error(f"Failed: {res.text}")
                    except Exception as e:
                        show_error(f"Connection Error: {e}")

    with tab2:
        st.markdown("### 📋 All Orders")
        with st.spinner("Fetching orders..."):
            orders = fetch_data("orders/")
            if orders:
                st.dataframe(pd.DataFrame(orders), use_container_width=True)
            else:
                st.info("No orders found.")

    with tab3:
        st.markdown("### ❌ Cancel Order")
        st.info("Note: Orders that have been delivered cannot be cancelled. Cancelling an order will restore the product stock.")
        
        orders = fetch_data("orders/")
        if orders:
            order_map = {f"Order #{o['order_id']} (Qty: {o['quantity_ordered']})": o['order_id'] for o in orders}
            selected_cancel_order = st.selectbox("Select Order to Cancel", options=list(order_map.keys()))
            
            if st.button("🚫 Cancel Selected Order"):
                order_id = order_map[selected_cancel_order]
                try:
                    res = requests.delete(f"{API_URL}/orders/{order_id}")
                    if res.status_code == 200:
                        show_success("Order cancelled and stock restored successfully!")
                        st.rerun()
                    else:
                        # Try to parse detail from error
                        try:
                            detail = res.json().get('detail', res.text)
                        except:
                            detail = res.text
                        show_error(f"Failed to cancel: {detail}")
                except Exception as e:
                    show_error(f"Connection Error: {e}")
        else:
            st.info("No active orders to cancel.")


elif menu == "Shipments":
    st.title("🚚 Shipment Logistics")
    
    tab1, tab2 = st.tabs(["➕ Create Shipment", "📋 Shipment Tracking"])
    
    with tab1:
        st.markdown("### Create New Shipment")
        
        orders = fetch_data("orders/")
        if not orders:
            st.warning("⚠️ No orders available to ship.")
        else:
            with st.form("shipment_form"):
                c1, c2 = st.columns(2)
                with c1:
                    order_map = {f"Order #{o['order_id']} (Qty: {o['quantity_ordered']})": o['order_id'] for o in orders}
                    selected_order = st.selectbox("Select Order", options=list(order_map.keys()))
                    status = st.selectbox("Status", ["Pending", "In Transit", "Delivered", "Delayed"])
                with c2:
                    ship_date = st.date_input("Shipment Date", value=datetime.now())
                    est_arrival = st.date_input("Estimated Arrival", value=datetime.now())
                
                submitted = st.form_submit_button("🚚 Dispatch Shipment")
                
                if submitted:
                    payload = {
                        "order_id": order_map[selected_order],
                        "shipment_date": datetime.combine(ship_date, datetime.min.time()).isoformat(),
                        "estimated_arrival_date": datetime.combine(est_arrival, datetime.min.time()).isoformat(),
                        "status": status
                    }
                    try:
                        res = requests.post(f"{API_URL}/shipments/", json=payload)
                        if res.status_code == 200:
                            show_success("Shipment created successfully!")
                        else:
                            show_error(f"Failed: {res.text}")
                    except Exception as e:
                        show_error(f"Connection Error: {e}")

    with tab2:
        st.markdown("### 📋 Shipment Status")
        with st.spinner("Tracking shipments..."):
            shipments = fetch_data("shipments/")
            if shipments:
                df = pd.DataFrame(shipments)
                st.dataframe(
                    df, 
                    use_container_width=True,
                    column_config={
                        "status": st.column_config.SelectboxColumn(
                            "Status",
                            options=["Pending", "In Transit", "Delivered", "Delayed"],
                            required=True
                        )
                    }
                )
            else:
                st.info("No shipments found.")
