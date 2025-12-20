import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
import io

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None


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
        ["Dashboard", "Suppliers", "Products", "Orders", "Shipments", "Reports"],
        index=0
    )
    st.markdown("---")
    st.caption("System Status: 🟢 Online")
    st.caption("v2.1.0 | Dark Mode")




# --- PDF GENERATOR ---
def create_pdf(dataframe, title):
    if not FPDF:
        return None
    
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, title, 0, 1, 'C')
            self.ln(10)
            
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Column headers
    cols = dataframe.columns.tolist()
    col_width = 190 / len(cols) if cols else 190
    
    # Header
    pdf.set_font("Arial", 'B', 10)
    for col in cols:
        pdf.cell(col_width, 10, str(col).upper(), 1, 0, 'C')
    pdf.ln()
    
    # Rows
    pdf.set_font("Arial", size=10)
    for _, row in dataframe.iterrows():
        for col in cols:
            # Type handling for clean output
            val = str(row[col])
            # Truncate if too long to avoid break
            if len(val) > 20: val = val[:17] + "..."
            pdf.cell(col_width, 10, val, 1, 0, 'C')
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')

# --- HELPER FUNCTIONS ---
def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def send_data(endpoint, payload):
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=payload)
        return response
    except Exception as e:
        return None

def update_data(endpoint, payload):
    try:
        response = requests.put(f"{API_URL}/{endpoint}", json=payload)
        return response
    except Exception as e:
        return None

def delete_data(endpoint):
    try:
        response = requests.delete(f"{API_URL}/{endpoint}")
        return response
    except Exception as e:
        return None

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
    st.title("📊 SupplyStream")
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
    
    tab1, tab2 = st.tabs(["➕ Add Supplier", "📋 Manage Suppliers"])
    
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
                    res = send_data("suppliers/", payload)
                    if res and res.status_code == 200:
                        show_success("Supplier added successfully!")
                    elif res:
                        show_error(f"Failed: {res.text}")
                    else:
                        show_error("Connection Failed")

    with tab2:
        st.markdown("### 📋 Manage Suppliers")
        suppliers = fetch_data("suppliers/")
        if suppliers:
            # Master List
            supplier_map = {f"{s['name']}" : s for s in suppliers}
            selected_s_name = st.selectbox("Select Supplier to View/Edit", options=list(supplier_map.keys()))
            
            if selected_s_name:
                s_data = supplier_map[selected_s_name]
                s_id = s_data['supplier_id']
                
                # Detail View
                with st.expander("📝 Supplier Details & Actions", expanded=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        new_name = st.text_input("Name", value=s_data['name'])
                        new_contact = st.text_input("Contact", value=s_data['contact_person'])
                    with c2:
                        new_phone = st.text_input("Phone", value=s_data['phone_number'])
                        new_addr = st.text_input("Address", value=s_data['address'])
                    
                    c3, c4 = st.columns(2)
                    with c3:
                        if st.button("💾 Update Supplier"):
                            payload = {
                                "name": new_name,
                                "contact_person": new_contact,
                                "phone_number": new_phone,
                                "address": new_addr
                            }
                            res = update_data(f"suppliers/{s_id}", payload)
                            if res and res.status_code == 200:
                                show_success("Supplier updated!")
                                st.rerun()
                            else:
                                show_error("Update failed")
                    with c4:
                        if st.button("🗑️ Delete Supplier", type="primary"):
                            res = delete_data(f"suppliers/{s_id}")
                            if res and res.status_code == 200:
                                show_success("Supplier deleted!")
                                st.rerun()
                            else:
                                show_error("Delete failed")

                # Related Data
                st.markdown("#### � Supplied Orders")
                s_orders = fetch_data(f"suppliers/{s_id}/orders")
                if s_orders:
                    st.dataframe(pd.DataFrame(s_orders), use_container_width=True)
                else:
                    st.info("No orders from this supplier.")
                
                st.markdown("#### 🚚 Related Shipments")
                s_shipments = fetch_data(f"suppliers/{s_id}/shipments")
                if s_shipments:
                    st.dataframe(pd.DataFrame(s_shipments), use_container_width=True)
                else:
                    st.info("No shipments related to this supplier.")

        else:
            st.info("No suppliers found.")



elif menu == "Products":
    st.title("📦 Product Inventory")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Product", "�️ Inventory Management", "⚠️ Low Stock Alerts"])
    
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
                    res = send_data("products/", payload)
                    if res and res.status_code == 200:
                        show_success("Product added successfully!")
                    elif res:
                        show_error(f"Failed: {res.text}")
                    else:
                        show_error("Connection Failed")

    with tab2:
        st.markdown("### �️ Inventory Management")
        products = fetch_data("products/")
        if products:
            # Table View
            st.dataframe(
                pd.DataFrame(products), 
                use_container_width=True,
                column_config={
                    "unit_price": st.column_config.NumberColumn("Price", format="$%.2f"),
                    "quantity_available": st.column_config.ProgressColumn("Stock", min_value=0, max_value=100, format="%d")
                }
            )
            
            st.markdown("---")
            st.subheader("Manage Product")
            
            prod_options = {f"{p['name']} (ID: {p['product_id']})": p for p in products}
            selected_prod_key = st.selectbox("Select Product to Manage", options=list(prod_options.keys()))
            
            if selected_prod_key:
                selected_prod = prod_options[selected_prod_key]
                p_id = selected_prod['product_id']
                
                action = st.radio("Action", ["Update Details", "Adjust Stock", "Delete Product"], horizontal=True)
                
                if action == "Update Details":
                    with st.form("update_prod"):
                        new_desc = st.text_input("New Description", value=selected_prod.get('description', ''))
                        new_price = st.number_input("New Price", value=float(selected_prod.get('unit_price', 0.0)))
                        
                        if st.form_submit_button("Update Details"):
                            payload = {"description": new_desc, "unit_price": new_price}
                            res = update_data(f"products/{p_id}", payload)
                            if res and res.status_code == 200:
                                show_success("Product updated!")
                                st.rerun()
                            else:
                                show_error("Update failed")

                elif action == "Adjust Stock":
                    with st.form("adjust_stock"):
                        amount = st.number_input("Adjustment Amount (positive to add, negative to reduce)", step=1, value=0)
                        if st.form_submit_button("Adjust Stock"):
                            res = update_data(f"products/{p_id}/adjust-stock?amount={amount}", {})
                            if res and res.status_code == 200:
                                show_success("Stock adjusted!")
                                st.rerun()
                            else:
                                show_error("Adjustment failed")

                elif action == "Delete Product":
                    st.warning("Are you sure you want to delete this product?")
                    if st.button("Confirm Delete"):
                        res = delete_data(f"products/{p_id}")
                        if res and res.status_code == 200:
                            show_success("Product deleted!")
                            st.rerun()
                        else:
                            show_error("Delete failed")
        else:
            st.info("No products found.")

    with tab3:
        st.markdown("### ⚠️ Low Stock Alerts")
        threshold = st.slider("Stock Threshold", 1, 100, 10)
        low_stock = fetch_data(f"products/low-stock?threshold={threshold}")
        if low_stock:
            st.error(f"Found {len(low_stock)} products with low stock!")
            st.dataframe(pd.DataFrame(low_stock), use_container_width=True)
        else:
            st.success("No products below threshold.")



elif menu == "Orders":
    st.title("🛒 Order Management")
    
    tab1, tab2 = st.tabs(["➕ Place Order", "📋 Manage Orders"])
    
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
                    res = send_data("orders/", payload)
                    if res and res.status_code == 200:
                        show_success("Order placed successfully!")
                    elif res:
                        show_error(f"Failed: {res.text}")
                    else:
                        show_error("Connection Failed")

    with tab2:
        st.markdown("### 📋 Manage Orders")
        
        # Filters
        filter_type = st.radio("Filter By", ["All Orders", "Date Range", "Product", "Supplier"], horizontal=True)
        orders_data = []
        
        if filter_type == "All Orders":
            orders_data = fetch_data("orders/")
            
        elif filter_type == "Date Range":
            c1, c2 = st.columns(2)
            start_d = c1.date_input("Start Date", value=datetime.now())
            end_d = c2.date_input("End Date", value=datetime.now())
            if st.button("Apply Date Filter"):
                orders_data = fetch_data(f"orders/date-range?start_date={start_d}&end_date={end_d}")
                
        elif filter_type == "Product":
            products = fetch_data("products/")
            if products:
                p_map = {p['name']: p['product_id'] for p in products}
                sel_p = st.selectbox("Select Product", list(p_map.keys()))
                if sel_p:
                    orders_data = fetch_data(f"orders/product/{p_map[sel_p]}")
                    
        elif filter_type == "Supplier":
            suppliers = fetch_data("suppliers/")
            if suppliers:
                s_map = {s['name']: s['supplier_id'] for s in suppliers}
                sel_s = st.selectbox("Select Supplier", list(s_map.keys()))
                if sel_s:
                    orders_data = fetch_data(f"orders/supplier/{s_map[sel_s]}")
        
        # Display & Actions
        if orders_data:
            st.dataframe(pd.DataFrame(orders_data), use_container_width=True)
            
            st.markdown("---")
            st.subheader("Order Actions")
            
            o_map = {f"Order #{o['order_id']}": o for o in orders_data}
            sel_o_key = st.selectbox("Select Order to Manage", list(o_map.keys()))
            
            if sel_o_key:
                sel_o = o_map[sel_o_key]
                o_id = sel_o['order_id']
                
                # Fetch single order details to be sure
                full_order = fetch_data(f"orders/{o_id}")
                if full_order:
                    st.json(full_order)
                    
                    if st.button("❌ Cancel Order", type="primary"):
                        res = delete_data(f"orders/{o_id}")
                        if res and res.status_code == 200:
                            show_success("Order cancelled!")
                            st.rerun()
                        elif res:
                            # Try to parse detail from error
                            try:
                                detail = res.json().get('detail', res.text)
                            except:
                                detail = res.text
                            show_error(f"Failed to cancel: {detail}")
                        else:
                            show_error("Connection Failed")
                
        else:
            st.info("No orders found matching criteria.")



elif menu == "Shipments":
    st.title("🚚 Shipment Logistics")
    
    tab1, tab2 = st.tabs(["➕ Create Shipment", "📋 Tracking & Management"])
    
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
                    res = send_data("shipments/", payload)
                    if res and res.status_code == 200:
                        show_success("Shipment created successfully!")
                    elif res:
                        show_error(f"Failed: {res.text}")
                    else:
                        show_error("Connection Failed")

    with tab2:
        st.markdown("### 📋 Tracking & Management")
        
        filter_mode = st.radio("List Components", ["All Shipments", "Delayed Shipments", "On-Time Shipments", "Find by Order"], horizontal=True)
        ship_data = []
        
        if filter_mode == "All Shipments":
            ship_data = fetch_data("shipments/")
        elif filter_mode == "Delayed Shipments":
            ship_data = fetch_data("shipments/delayed")
        elif filter_mode == "On-Time Shipments":
            ship_data = fetch_data("shipments/on-time")
        elif filter_mode == "Find by Order":
            orders = fetch_data("orders/")
            if orders:
                o_map = {f"Order #{o['order_id']}": o['order_id'] for o in orders}
                sel_o = st.selectbox("Select Order", list(o_map.keys()))
                if sel_o:
                    ship_data = fetch_data(f"shipments/order/{o_map[sel_o]}")

        if ship_data:
            st.dataframe(pd.DataFrame(ship_data), use_container_width=True)
            
            st.markdown("---")
            st.subheader("Update Shipment")
            
            s_map = {f"Shipment #{s['shipment_id']} ({s['status']})": s for s in ship_data}
            sel_s_key = st.selectbox("Select Shipment to Update", list(s_map.keys()))
            
            if sel_s_key:
                sel_s = s_map[sel_s_key]
                s_id = sel_s['shipment_id']
                
                action = st.radio("Action", ["Update Status/Details", "Record Arrival"], horizontal=True)
                
                if action == "Update Status/Details":
                    with st.form("update_ship"):
                        new_status = st.selectbox("Status", ["Pending", "In Transit", "Delivered", "Delayed"], index=["Pending", "In Transit", "Delivered", "Delayed"].index(sel_s['status']) if sel_s['status'] in ["Pending", "In Transit", "Delivered", "Delayed"] else 0)
                        
                        # Handle dates logic if needed, simplfied here to just status as example or can add dates
                        if st.form_submit_button("Update Status"):
                            # The schema for Shipmentupdate might need other fields, but let's send what we change
                            # Checking schema: Shipmentupdate
                            payload = {"status": new_status}
                            res = update_data(f"shipments/{s_id}", payload)
                            if res and res.status_code == 200:
                                show_success("Shipment Updated!")
                                st.rerun()
                            else:
                                show_error("Update Failed")
                                
                elif action == "Record Arrival":
                    with st.form("arrive_ship"):
                        # If actual_arrival_date is None, use today
                        def_val = datetime.now()
                        if sel_s.get('actual_arrival_date'):
                            try:
                                def_val = datetime.fromisoformat(sel_s['actual_arrival_date'])
                            except:
                                pass
                        
                        arr_date = st.date_input("Actual Arrival Date", value=def_val)
                        
                        if st.form_submit_button("Confirm Arrival"):
                            final_date = datetime.combine(arr_date, datetime.min.time()).isoformat()
                            # URL param for this endpoint
                            res = update_data(f"shipments/{s_id}/arrival?actual_arrival_date={final_date}", {})
                            if res and res.status_code == 200:
                                show_success("Arrival Recorded!")
                                st.rerun()
                            else:
                                show_error("Update Failed")
            else:
                st.info("No shipments found.")


elif menu == "Reports":
    st.title("📑 Reports & Exports")
    st.markdown("Download your data in **CSV** or **PDF** formats.")
    
    if FPDF is None:
        st.warning("⚠️ The 'fpdf' library is not installed. PDF generation is disabled. (Run `pip install fpdf` to enable)")

    report_type = st.selectbox("Select Data Source", ["Products", "Orders", "Shipments", "Suppliers"])
    
    if st.button("Generate Preview"):
        with st.spinner("Fetching data..."):
            endpoint_map = {
                "Products": "products/",
                "Orders": "orders/",
                "Shipments": "shipments/",
                "Suppliers": "suppliers/"
            }
            
            data = fetch_data(endpoint_map[report_type])
            
            if data:
                df = pd.DataFrame(data)
                
                # Preview
                st.markdown(f"### Preview: {report_type}")
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(f"Total Records: {len(df)}")
                
                # Export Area
                st.markdown("---")
                st.subheader("📥 Download")
                
                c1, c2 = st.columns(2)
                
                # CSV
                csv = df.to_csv(index=False).encode('utf-8')
                c1.download_button(
                    label=f"📄 Download {report_type} (CSV)",
                    data=csv,
                    file_name=f"{report_type.lower()}_report.csv",
                    mime="text/csv",
                )
                
                # PDF
                if FPDF:
                    try:
                        pdf_bytes = create_pdf(df, f"{report_type} Report")
                        if pdf_bytes:
                            c2.download_button(
                                label=f"📕 Download {report_type} (PDF)",
                                data=pdf_bytes,
                                file_name=f"{report_type.lower()}_report.pdf",
                                mime="application/pdf",
                            )
                    except Exception as e:
                        c2.error(f"PDF Generation Error: {e}")
            else:
                st.info("No data available to export.")
