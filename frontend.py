import streamlit as st

from main import analyze_ticket


st.set_page_config(
    page_title="Support Desk",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root { --ink: #f3f7fc; --muted: #b9c8d9; --mint: #c5e7df; --lime: #c5e878; --paper: #0b1f3a; --line: #294565; }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stSidebar"] { background: #061426; }
    [data-testid="stSidebar"] * { color: #edf4fc; }
    h1, h2, h3 { color: var(--ink); font-family: Georgia, serif; letter-spacing: 0; }
    .eyebrow { color: var(--lime); font-size: 0.76rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }
    .hero { padding: 1.3rem 0 1rem; border-bottom: 1px solid var(--line); margin-bottom: 1.4rem; }
    .hero h1 { font-size: clamp(2.3rem, 5vw, 4.6rem); line-height: 0.98; margin: 0.35rem 0 0.7rem; }
    .hero p { color: var(--muted); font-size: 1.05rem; max-width: 680px; }
    .result-label { color: var(--lime); font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
    .result-summary { background: #f7fafc; color: #14243a; border-left: 5px solid var(--lime); padding: 1rem 1.1rem; margin: 0.4rem 0 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state.history = []


def render_analysis(analysis):
    st.markdown('<div class="result-label">AI triage result</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-summary"><strong>{analysis.summary}</strong></div>',
        unsafe_allow_html=True,
    )
    first, second, third = st.columns(3)
    first.metric("Category", analysis.category.value.replace("_", " ").title())
    second.metric("Urgency", analysis.urgency.value.title())
    third.metric("Sentiment", analysis.sentiment.value.title())

    st.subheader("Recommended next step")
    st.write(analysis.suggested_action)
    if analysis.affected_product_or_feature:
        st.caption(f"Affected product or feature: {analysis.affected_product_or_feature}")
    st.progress(analysis.confidence_score, text=f"Confidence: {analysis.confidence_score:.0%}")


def analyze_and_show(ticket, customer_name="", customer_email=""):
    if not ticket.strip():
        st.warning("Please enter a query before submitting.")
        return
    with st.spinner("Analyzing your request..."):
        try:
            analysis = analyze_ticket(ticket.strip())
        except Exception as error:
            st.error(f"The request could not be analyzed: {error}")
            return

    st.session_state.history.insert(
        0,
        {
            "query": ticket.strip(),
            "name": customer_name.strip(),
            "email": customer_email.strip(),
            "analysis": analysis,
        },
    )
    render_analysis(analysis)


st.markdown(
    '<div class="hero"><div class="eyebrow">Support desk / intake</div>'
    '<h1>Turn a messy question into a clear next step.</h1>'
    '<p>Choose the intake style that fits the moment. Every request is classified by topic, urgency, sentiment, and suggested action.</p></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Intake options")
    mode = st.radio(
        "Choose a request type",
        [
            "Direct query",
            "Guided issue form",
            "Email to ticket",
            "Urgent issue",
            "Knowledge request",
        ],
    )
    st.divider()
    st.caption("Your request is sent to the configured Gemini model for triage.")

if mode == "Direct query":
    st.subheader("Ask directly")
    st.write("Describe the problem in your own words. No special format is needed.")
    query = st.text_area(
        "Your query",
        height=190,
        placeholder="Example: I was charged twice for my subscription and cannot find the refund option.",
    )
    if st.button("Analyze query", type="primary", use_container_width=True):
        analyze_and_show(query)

elif mode == "Guided issue form":
    st.subheader("Tell us about the issue")
    with st.form("guided_issue_form"):
        name = st.text_input("Full name")
        email = st.text_input("Email address")
        product = st.text_input("Product or feature", placeholder="Example: Mobile app, billing page")
        issue_type = st.selectbox(
            "What best describes the issue?",
            ["Billing", "Technical problem", "Account access", "Feature request", "General question"],
        )
        impact = st.select_slider("How much is this affecting you?", options=["Low", "Medium", "High", "Critical"])
        details = st.text_area("Describe what happened", height=150)
        submitted = st.form_submit_button("Create analysis", type="primary", use_container_width=True)
    if submitted:
        ticket = f"Customer: {name}\nEmail: {email}\nIssue type: {issue_type}\nImpact: {impact}\nProduct: {product}\nDetails: {details}"
        analyze_and_show(ticket, name, email)

elif mode == "Email to ticket":
    st.subheader("Convert an email into a ticket")
    st.write("Paste the message and add the sender details so the team can follow up.")
    with st.form("email_form"):
        sender_name = st.text_input("Sender name")
        sender_email = st.text_input("Sender email")
        subject = st.text_input("Email subject")
        email_body = st.text_area("Paste email body", height=220)
        submitted = st.form_submit_button("Analyze email", type="primary", use_container_width=True)
    if submitted:
        ticket = f"From: {sender_name} <{sender_email}>\nSubject: {subject}\n\n{email_body}"
        analyze_and_show(ticket, sender_name, sender_email)

elif mode == "Urgent issue":
    st.subheader("Report an urgent issue")
    st.warning("Use this for outages, security concerns, lost access, or issues blocking essential work.")
    with st.form("urgent_form"):
        urgent_name = st.text_input("Your name")
        urgent_email = st.text_input("Best contact email")
        affected_users = st.number_input("How many people are affected?", min_value=1, value=1, step=1)
        urgent_details = st.text_area("What is blocked or at risk?", height=180)
        submitted = st.form_submit_button("Prioritize urgent issue", type="primary", use_container_width=True)
    if submitted:
        ticket = f"URGENT ISSUE\nReporter: {urgent_name}\nEmail: {urgent_email}\nAffected users: {affected_users}\nDetails: {urgent_details}"
        analyze_and_show(ticket, urgent_name, urgent_email)

else:
    st.subheader("Ask for an explanation")
    st.write("Use this when you need guidance, documentation, or help understanding a feature.")
    with st.form("knowledge_form"):
        knowledge_name = st.text_input("Your name")
        topic = st.text_input("Topic or feature")
        goal = st.text_area("What are you trying to accomplish?", height=150)
        submitted = st.form_submit_button("Analyze knowledge request", type="primary", use_container_width=True)
    if submitted:
        ticket = f"Knowledge request\nRequester: {knowledge_name}\nTopic: {topic}\nGoal: {goal}"
        analyze_and_show(ticket, knowledge_name)

if st.session_state.history:
    st.divider()
    with st.expander(f"Recent analyses ({len(st.session_state.history)})"):
        for item in st.session_state.history[:5]:
            label = item["query"].replace("\n", " ")[:90]
            st.markdown(f"**{label}**")
            st.caption(
                f"{item['analysis'].category.value.replace('_', ' ').title()} · "
                f"{item['analysis'].urgency.value.title()} · "
                f"{item['analysis'].summary}"
            )
            st.divider()
