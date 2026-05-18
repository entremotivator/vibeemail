import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Credit Repair Dashboard",
    page_icon="💳",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("💳 AI Credit Repair")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Clients",
        "Disputes",
        "Credit Accounts",
        "Tasks",
        "Analytics",
        "Education Center"
    ]
)

# -----------------------------
# DEMO DATA
# -----------------------------
clients = pd.DataFrame({
    "Client": [
        "John Carter",
        "Sarah Lee",
        "Mike Johnson",
        "Angela Davis",
        "Chris Brown"
    ],
    "Score Before": [540, 580, 510, 620, 490],
    "Score Current": [650, 690, 640, 710, 620],
    "Status": [
        "Active",
        "Active",
        "Pending",
        "Completed",
        "Active"
    ]
})

accounts = pd.DataFrame({
    "Account": [
        "Capital One",
        "Discover",
        "Navy Federal",
        "Chase",
        "American Express"
    ],
    "Balance": [1200, 3500, 4200, 1500, 2100],
    "Utilization": [45, 78, 62, 25, 31],
    "Status": [
        "Negative",
        "Positive",
        "Negative",
        "Positive",
        "Positive"
    ]
})

tasks = pd.DataFrame({
    "Task": [
        "Send Dispute Letters",
        "Call Credit Bureau",
        "Upload Identity Docs",
        "Verify Tradelines",
        "Review Inquiry Removal"
    ],
    "Priority": [
        "High",
        "High",
        "Medium",
        "Low",
        "Medium"
    ],
    "Due Date": [
        "2026-05-20",
        "2026-05-22",
        "2026-05-25",
        "2026-05-27",
        "2026-05-29"
    ]
})

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":

    st.title("💳 AI Credit Repair Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Clients", len(clients))

    with col2:
        avg_before = clients["Score Before"].mean()
        st.metric("Avg Starting Score", int(avg_before))

    with col3:
        avg_current = clients["Score Current"].mean()
        st.metric("Avg Current Score", int(avg_current))

    with col4:
        improvement = int(avg_current - avg_before)
        st.metric("Avg Increase", f"+{improvement}")

    st.divider()

    st.subheader("Client Progress")

    fig = px.bar(
        clients,
        x="Client",
        y=["Score Before", "Score Current"],
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Client Overview")
    st.dataframe(clients, use_container_width=True)

# -----------------------------
# CLIENTS
# -----------------------------
elif page == "Clients":

    st.title("👥 Client Management")

    with st.form("client_form"):
        st.subheader("Add New Client")

        name = st.text_input("Client Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        score = st.number_input(
            "Current Credit Score",
            min_value=300,
            max_value=850,
            value=600
        )

        submitted = st.form_submit_button("Save Client")

        if submitted:
            st.success(f"{name} added successfully!")

    st.divider()

    st.subheader("Existing Clients")
    st.dataframe(clients, use_container_width=True)

# -----------------------------
# DISPUTES
# -----------------------------
elif page == "Disputes":

    st.title("📄 Credit Dispute Center")

    dispute_type = st.selectbox(
        "Select Dispute Type",
        [
            "Late Payment",
            "Charge Off",
            "Collection",
            "Hard Inquiry",
            "Identity Theft",
            "Repossession"
        ]
    )

    bureau = st.multiselect(
        "Credit Bureau",
        [
            "Experian",
            "Equifax",
            "TransUnion"
        ]
    )

    reason = st.text_area("Dispute Reason")

    if st.button("Generate Dispute Letter"):
        st.success("Dispute Letter Generated!")

        letter = f"""
        Date: {datetime.now().strftime('%Y-%m-%d')}

        Dear Credit Bureau,

        I am requesting an investigation into the following item
        on my credit report due to inaccurate reporting.

        Dispute Type: {dispute_type}

        Reason:
        {reason}

        Please remove or correct this information immediately.

        Sincerely,
        Client
        """

        st.text_area("Generated Letter", letter, height=300)

# -----------------------------
# CREDIT ACCOUNTS
# -----------------------------
elif page == "Credit Accounts":

    st.title("🏦 Credit Accounts")

    st.dataframe(accounts, use_container_width=True)

    st.subheader("Utilization Overview")

    fig2 = px.pie(
        accounts,
        names="Account",
        values="Balance"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# TASKS
# -----------------------------
elif page == "Tasks":

    st.title("✅ Credit Repair Tasks")

    st.dataframe(tasks, use_container_width=True)

    st.subheader("Add Task")

    with st.form("task_form"):

        task_name = st.text_input("Task")
        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )

        due = st.date_input("Due Date")

        task_submit = st.form_submit_button("Add Task")

        if task_submit:
            st.success(f"Task '{task_name}' added!")

# -----------------------------
# ANALYTICS
# -----------------------------
elif page == "Analytics":

    st.title("📈 Credit Analytics")

    chart_data = pd.DataFrame({
        "Month": [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"
        ],
        "Credit Score": [
            520,
            540,
            575,
            610,
            645,
            690
        ]
    })

    fig3 = px.line(
        chart_data,
        x="Month",
        y="Credit Score",
        markers=True
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Score Growth Data")
    st.dataframe(chart_data, use_container_width=True)

# -----------------------------
# EDUCATION CENTER
# -----------------------------
elif page == "Education Center":

    st.title("📚 Credit Education Center")

    st.subheader("Credit Repair Tips")

    tips = [
        "Pay all bills on time.",
        "Keep credit utilization below 30%.",
        "Avoid excessive hard inquiries.",
        "Dispute inaccurate information.",
        "Build positive payment history.",
        "Monitor your credit regularly.",
        "Use secured cards responsibly."
    ]

    for tip in tips:
        st.info(tip)

    st.subheader("Recommended Actions")

    st.write("""
    - Review your credit report monthly.
    - Remove inaccurate collections.
    - Reduce high balances.
    - Maintain older accounts.
    - Avoid unnecessary debt.
    """)

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("AI Credit Repair System • Streamlit Dashboard")
