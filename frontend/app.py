
import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

BACKEND_URL = "http://localhost:8000"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Helpdesk",
    page_icon="🎫",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "selected_ticket_id" not in st.session_state:
    st.session_state.selected_ticket_id = None

if "ticket_details" not in st.session_state:
    st.session_state.ticket_details = None

if "processing_result" not in st.session_state:
    st.session_state.processing_result = None

if "review_required" not in st.session_state:
    st.session_state.review_required = False

if "proposed_resolution" not in st.session_state:
    st.session_state.proposed_resolution = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def api_get(endpoint):
    try:
        response = requests.get(
            f"{BACKEND_URL}{endpoint}",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "Unable to connect to the FastAPI backend. "
            "Make sure the backend is running on http://localhost:8000."
        )

        return None

    except requests.exceptions.Timeout:
        st.error("The request timed out.")

        return None

    except requests.exceptions.HTTPError:
        try:
            error = response.json()
            st.error(error.get("detail", "Backend request failed."))
        except Exception:
            st.error("Backend request failed.")

        return None

    except Exception as exc:
        st.error(f"Unexpected error: {exc}")

        return None


def api_post(endpoint, payload):
    try:
        response = requests.post(
            f"{BACKEND_URL}{endpoint}",
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "Unable to connect to the FastAPI backend."
        )

        return None

    except requests.exceptions.Timeout:
        st.error(
            "The request timed out. "
            "The AI workflow may still be processing."
        )

        return None

    except requests.exceptions.HTTPError:
        try:
            error = response.json()
            st.error(error.get("detail", "Backend request failed."))
        except Exception:
            st.error("Backend request failed.")

        return None

    except Exception as exc:
        st.error(f"Unexpected error: {exc}")

        return None


def api_put(endpoint, payload=None):
    try:
        response = requests.put(
            f"{BACKEND_URL}{endpoint}",
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "Unable to connect to the FastAPI backend."
        )

        return None

    except requests.exceptions.Timeout:
        st.error(
            "The request timed out. "
            "The AI workflow may still be processing."
        )

        return None

    except requests.exceptions.HTTPError:
        try:
            error = response.json()
            st.error(error.get("detail", "Backend request failed."))
        except Exception:
            st.error("Backend request failed.")

        return None

    except Exception as exc:
        st.error(f"Unexpected error: {exc}")

        return None


def api_delete(endpoint):
    try:
        response = requests.delete(
            f"{BACKEND_URL}{endpoint}",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "Unable to connect to the FastAPI backend."
        )

        return None

    except requests.exceptions.HTTPError:
        try:
            error = response.json()
            st.error(error.get("detail", "Backend request failed."))
        except Exception:
            st.error("Backend request failed.")

        return None

    except Exception as exc:
        st.error(f"Unexpected error: {exc}")

        return None


def load_ticket(ticket_id):
    ticket = api_get(f"/tickets/{ticket_id}")

    if ticket:
        st.session_state.selected_ticket_id = ticket_id
        st.session_state.ticket_details = ticket

        return ticket

    return None


def clear_ticket_state():
    st.session_state.selected_ticket_id = None
    st.session_state.ticket_details = None
    st.session_state.processing_result = None
    st.session_state.review_required = False
    st.session_state.proposed_resolution = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎫 AI Helpdesk")

    st.caption(
        "AI-powered IT Helpdesk Ticket Resolution System"
    )

    st.divider()

    if st.button(
        "🏠 Dashboard",
        use_container_width=True,
    ):
        st.session_state.page = "Dashboard"

    if st.button(
        "➕ Create Ticket",
        use_container_width=True,
    ):
        st.session_state.page = "Create Ticket"

    if st.button(
        "📋 Tickets",
        use_container_width=True,
    ):
        st.session_state.page = "Tickets"

    if st.button(
        "🔍 View Ticket",
        use_container_width=True,
    ):
        st.session_state.page = "View Ticket"

    st.divider()

    health = api_get("/health")

    if health and health.get("status") == "ok":
        st.success("Backend Online")
    else:
        st.error("Backend Offline")


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.title("AI Helpdesk Dashboard")

    st.write(
        "Create, process, review and resolve IT support tickets "
        "using an AI-powered agentic workflow."
    )

    st.divider()

    tickets = api_get("/tickets")

    if tickets is None:
        st.stop()

    total_tickets = len(tickets)

    pending_tickets = sum(
        1
        for ticket in tickets
        if ticket.get("status") == "PENDING"
    )

    resolved_tickets = sum(
        1
        for ticket in tickets
        if ticket.get("status") == "RESOLVED"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Tickets",
            total_tickets,
        )

    with col2:
        st.metric(
            "Pending",
            pending_tickets,
        )

    with col3:
        st.metric(
            "Resolved",
            resolved_tickets,
        )

    st.divider()

    st.subheader("Recent Tickets")

    if not tickets:
        st.info("No tickets have been created yet.")

    else:

        for ticket in tickets[-10:][::-1]:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2, 3, 2, 1]
                )

                with col1:
                    st.write(
                        f"**{ticket.get('ticket_id', '-') }**"
                    )

                with col2:
                    st.write(
                        ticket.get("subject", "-")
                    )

                with col3:

                    status = ticket.get(
                        "status",
                        "-"
                    )

                    if status == "RESOLVED":
                        st.success(status)

                    else:
                        st.warning(status)

                with col4:

                    if st.button(
                        "View",
                        key=f"dashboard_view_{ticket.get('ticket_id')}",
                    ):
                        load_ticket(
                            ticket.get("ticket_id")
                        )

                        st.session_state.page = "View Ticket"

                        st.rerun()


# ============================================================
# CREATE TICKET
# ============================================================

elif st.session_state.page == "Create Ticket":

    st.title("Create New Ticket")

    st.write(
        "Enter the user's issue. "
        "The ticket ID will be generated automatically."
    )

    st.divider()

    with st.form("create_ticket_form"):

        title = st.text_input(
            "Title",
            placeholder="Example: Unable to connect to VPN",
        )

        subject = st.text_input(
            "Subject",
            placeholder="Example: VPN connection failure",
        )

        description = st.text_area(
            "Description",
            placeholder=(
                "Describe the issue in detail...\n\n"
                "Example:\n"
                "I am unable to connect to the company VPN. "
                "The VPN client shows 'Authentication failed'. "
                "This started this morning."
            ),
            height=200,
        )

        submitted = st.form_submit_button(
            "Create Ticket",
            use_container_width=True,
        )

    if submitted:

        if not title.strip():
            st.error("Title is required.")

        elif not subject.strip():
            st.error("Subject is required.")

        elif not description.strip():
            st.error("Description is required.")

        else:

            payload = {
                "title": title.strip(),
                "subject": subject.strip(),
                "description": description.strip(),
            }

            result = api_post(
                "/ticket",
                payload,
            )

            if result:

                st.success(
                    f"Ticket {result.get('ticket_id')} created successfully."
                )

                st.session_state.selected_ticket_id = (
                    result.get("ticket_id")
                )

                st.session_state.ticket_details = result

                st.session_state.page = "View Ticket"

                st.rerun()


# ============================================================
# TICKETS
# ============================================================

elif st.session_state.page == "Tickets":

    st.title("All Tickets")

    tickets = api_get("/tickets")

    if tickets is None:
        st.stop()

    if not tickets:

        st.info(
            "No tickets are available."
        )

    else:

        for ticket in tickets:

            ticket_id = ticket.get(
                "ticket_id",
                "-"
            )

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2, 4, 2, 1]
                )

                with col1:
                    st.write(
                        f"**{ticket_id}**"
                    )

                with col2:
                    st.write(
                        ticket.get(
                            "subject",
                            "-"
                        )
                    )

                with col3:

                    status = ticket.get(
                        "status",
                        "-"
                    )

                    if status == "RESOLVED":
                        st.success(status)

                    else:
                        st.warning(status)

                with col4:

                    if st.button(
                        "Open",
                        key=f"open_{ticket_id}",
                    ):

                        load_ticket(ticket_id)

                        st.session_state.page = "View Ticket"

                        st.rerun()


# ============================================================
# VIEW TICKET
# ============================================================

elif st.session_state.page == "View Ticket":

    st.title("Ticket Details")

    ticket_id = st.session_state.selected_ticket_id

    if not ticket_id:

        st.info(
            "Select a ticket from the Tickets page."
        )

        st.stop()

    ticket = api_get(
        f"/tickets/{ticket_id}"
    )

    if not ticket:
        st.stop()

    st.session_state.ticket_details = ticket

    status = ticket.get(
        "status",
        "PENDING"
    )

    st.subheader(
        ticket.get(
            "subject",
            "Ticket"
        )
    )

    st.caption(
        f"Ticket ID: {ticket_id}"
    )

    st.divider()

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    st.subheader("Ticket Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Title:** {ticket.get('title', '-')}"
        )

        st.write(
            f"**Category:** {ticket.get('category') or 'Not classified'}"
        )

    with col2:

        st.write(
            f"**Status:** {status}"
        )

        st.write(
            f"**Priority:** {ticket.get('priority') or 'Not assigned'}"
        )

    st.write("**Description:**")

    st.info(
        ticket.get(
            "description",
            "-"
        )
    )

    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    if (
        ticket.get("category")
        or ticket.get("priority")
        or ticket.get("confidence_score") is not None
    ):

        st.divider()

        st.subheader("AI Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Category",
                ticket.get(
                    "category",
                    "N/A"
                ),
            )

        with col2:

            st.metric(
                "Priority",
                ticket.get(
                    "priority",
                    "N/A"
                ),
            )

        with col3:

            confidence = ticket.get(
                "confidence_score"
            )

            if confidence is not None:

                st.metric(
                    "Confidence",
                    f"{float(confidence):.2%}",
                )

            else:

                st.metric(
                    "Confidence",
                    "N/A",
                )

    # --------------------------------------------------------
    # RESOLUTION
    # --------------------------------------------------------

    resolution = ticket.get(
        "resolution"
    )

    if resolution:

        st.divider()

        st.subheader("Resolution")

        st.success(
            resolution
        )

    # --------------------------------------------------------
    # PROCESS TICKET
    # --------------------------------------------------------

    st.divider()

    if status == "PENDING":

        st.subheader("AI Processing")

        st.write(
            "Run the LangGraph workflow to analyze this ticket, "
            "retrieve relevant knowledge, generate a resolution "
            "and calculate confidence."
        )

        if st.button(
            "🤖 Process Ticket",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner(
                "Running AI workflow..."
            ):

                result = api_put(
                    f"/ticket/{ticket_id}/process"
                )

            if result:

                st.session_state.processing_result = result

                if result.get(
                    "requires_human_review",
                    False
                ):

                    st.session_state.review_required = True

                    st.session_state.proposed_resolution = (
                        result.get(
                            "proposed_resolution",
                            ""
                        )
                    )

                    st.warning(
                        "Human review is required."
                    )

                    st.rerun()

                else:

                    st.session_state.review_required = False

                    st.success(
                        "Ticket resolved automatically."
                    )

                    st.rerun()

    # --------------------------------------------------------
    # HUMAN REVIEW
    # --------------------------------------------------------

    if (
        st.session_state.review_required
        and status == "PENDING"
    ):

        st.divider()

        st.subheader(
            "👤 Human Review Required"
        )

        st.warning(
            "The AI confidence score is below the configured "
            "threshold. Please review the proposed resolution."
        )

        confidence = ticket.get(
            "confidence_score"
        )

        if confidence is not None:

            st.metric(
                "AI Confidence",
                f"{float(confidence):.2%}"
            )

        st.write(
            "**AI Proposed Resolution**"
        )

        proposed_resolution = st.session_state.proposed_resolution

        st.info(
            proposed_resolution
        )

        review_action = st.radio(
            "Review Decision",
            options=[
                "Approve",
                "Modify",
            ],
            horizontal=True,
        )

        modified_resolution = ""

        if review_action == "Modify":

            modified_resolution = st.text_area(
                "Modified Resolution",
                value=proposed_resolution,
                height=220,
                placeholder=(
                    "Enter the corrected resolution..."
                ),
            )

        reviewer_comment = st.text_area(
            "Reviewer Comment (optional)",
            height=100,
            placeholder=(
                "Explain why the resolution was approved "
                "or modified..."
            ),
        )

        if st.button(
            "Submit Human Review",
            type="primary",
            use_container_width=True,
        ):

            if review_action == "Modify":

                if not modified_resolution.strip():

                    st.error(
                        "Modified resolution cannot be empty."
                    )

                    st.stop()

                resolution_to_submit = (
                    modified_resolution.strip()
                )

                action = "modify"

            else:

                resolution_to_submit = None

                action = "approve"

            payload = {
                "action": action,
                "resolution": resolution_to_submit,
                "comment": (
                    reviewer_comment.strip()
                    if reviewer_comment
                    else None
                ),
            }

            with st.spinner(
                "Submitting human review and "
                "continuing workflow..."
            ):

                result = api_put(
                    f"/ticket/{ticket_id}/review",
                    payload,
                )

            if result:

                st.session_state.review_required = False

                st.session_state.proposed_resolution = ""

                st.session_state.processing_result = result

                st.success(
                    "Human review completed. "
                    "The ticket has been resolved."
                )

                st.rerun()

    # --------------------------------------------------------
    # DELETE TICKET
    # --------------------------------------------------------

    st.divider()

    st.subheader("Ticket Actions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 Refresh Ticket",
            use_container_width=True,
        ):

            st.rerun()

    with col2:

        if st.button(
            "🗑️ Delete Ticket",
            use_container_width=True,
        ):

            result = api_delete(
                f"/ticket/{ticket_id}"
            )

            if result:

                st.success(
                    "Ticket deleted successfully."
                )

                clear_ticket_state()

                st.session_state.page = "Tickets"

                st.rerun()

