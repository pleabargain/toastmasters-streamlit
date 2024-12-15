import streamlit as st
import pdfkit
import tempfile
from datetime import datetime
import json

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Membership Form", "Print Format", "JSON Data", "README"])

with tab1:
    # Title and introductory text
    st.title("Toastmasters Membership Form")
    st.write("Fill out the form below to join Toastmasters Club.")

    # Input fields
    first_name = st.text_input("First name")
    last_name = st.text_input("Last name")
    email = st.text_input("Email")
    phone = st.text_input("Phone # (Whatsapp)")
    birthday = st.date_input("Birthday")
    linkedin = st.text_input("LinkedIn name (Optional)")
    instagram = st.text_input("Instagram handle (Optional)")
    mailing_address = st.text_area("Mailing Address")

    # Membership history
    previous_member = st.radio("Have you ever been a member of Toastmasters?", ["No", "Yes"])
    if previous_member == "Yes":
        member_number = st.text_input("Member number (if known)")

    # How they heard about the club
    referral = st.selectbox(
        "How did you hear about DIC2 Toastmasters Club?",
        ["Meetup", "Instagram", "Toastmasters website", "Word of mouth", "Other"]
    )
    if referral == "Word of mouth":
        word_of_mouth_details = st.text_input("Please specify")
    elif referral == "Other":
        other_details = st.text_input("Please specify")

    # Guest visits
    guest_visits = st.radio("How many times have you been a guest at DIC2?", ["0-1", "2-4", "5+"])
    visited_other_clubs = st.radio("Have you visited other clubs before joining DIC2?", ["No", "Yes"])
    if visited_other_clubs == "Yes":
        other_club_names = st.text_area("Club names")

    # Reasons for joining
    reasons = st.multiselect(
        "I’ve joined Toastmasters to:",
        [
            "Improve communication skills",
            "Improve leadership skills",
            "General personal growth and self-confidence",
            "Networking and relationship-building",
            "Prepare for a particular event or project",
            "New challenge",
            "Other"
        ]
    )
    if "Other" in reasons:
        other_reason = st.text_input("Please specify")

    # Goals
    specific_goal = st.radio("Do you have a specific goal you would like to achieve during your Toastmasters journey?", ["No", "Yes"])
    if specific_goal == "Yes":
        goal_details = st.text_area("Please specify your goal")

    # Membership promise
    st.subheader("Membership Promise")
    st.text("""As a member of Toastmasters International and my club, I promise to:
    - Attend club meetings regularly
    - Prepare all of my projects to the best of my ability, based on the Toastmasters education program
    - Prepare for and fulfill meeting assignments
    - Provide fellow members with helpful, constructive evaluations
    - Help the club maintain the positive, friendly environment necessary for all members to learn and grow
    - Serve my club as an officer when called upon to do so
    - Treat my fellow club members and our guests with respect and courtesy
    - Bring guests to club meetings so they can see the benefits Toastmasters membership offers
    - Adhere to the guidelines and rules for all Toastmasters educational and recognition programs
    - Act within Toastmasters’ core values of Integrity, Respect, Service, and Excellence during the conduct of all Toastmasters activities.""")

    # Payment details
    st.subheader("Membership Payment Schedule")
    st.write("Refer to the payment schedule and transfer details in the original form.")

    # Submit button and PDF generation
    if st.button("Submit"):
        # Store all form data in a dictionary
        form_data = {
            "Name": f"{first_name} {last_name}",
            "Email": email,
            "Phone": phone,
            "Birthday": str(birthday),
            "LinkedIn": linkedin,
            "Instagram": instagram,
            "Mailing Address": mailing_address,
            "Previous Member": previous_member,
            "Referral": referral,
            "Guest Visits": guest_visits,
            "Visited Other Clubs": visited_other_clubs,
            "Reasons for Joining": ', '.join(reasons),
            "Specific Goal": specific_goal
        }

        # Add conditional fields
        if previous_member == "Yes":
            form_data["Member Number"] = member_number
        if referral == "Word of mouth":
            form_data["Word of Mouth Details"] = word_of_mouth_details
        elif referral == "Other":
            form_data["Other Details"] = other_details
        if visited_other_clubs == "Yes":
            form_data["Other Club Names"] = other_club_names
        if "Other" in reasons:
            form_data["Other Reason"] = other_reason
        if specific_goal == "Yes":
            form_data["Goal Details"] = goal_details

        # Display success message and form data
        st.success("Thank you for filling out the membership form!")
        st.subheader("Submitted Details")
        for key, value in form_data.items():
            st.write(f"**{key}:** {value}")

        # Generate HTML content for PDF
        html_content = f"""
        <h1>DIC2 Toastmasters Membership Form</h1>
        <h2>Submitted on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>
        """
        for key, value in form_data.items():
            html_content += f"<p><strong>{key}:</strong> {value}</p>"
        
        # Add membership promise to PDF
        html_content += """
        <h2>Membership Promise</h2>
        <p>As a member of Toastmasters International and my club, I promise to:</p>
        <ul>
            <li>Attend club meetings regularly</li>
            <li>Prepare all of my projects to the best of my ability</li>
            <li>Prepare for and fulfill meeting assignments</li>
            <li>Provide fellow members with helpful, constructive evaluations</li>
            <li>Help maintain a positive, friendly environment</li>
            <li>Serve as a club officer when called upon</li>
            <li>Treat fellow members and guests with respect and courtesy</li>
            <li>Bring guests to club meetings</li>
            <li>Adhere to Toastmasters guidelines and rules</li>
            <li>Act within Toastmasters' core values</li>
        </ul>
        """

        # Create PDF download button
        if st.button("Download as PDF"):
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    # Convert HTML to PDF
                    pdfkit.from_string(html_content, tmp_file.name)
                    # Read PDF file
                    with open(tmp_file.name, 'rb') as pdf_file:
                        pdf_data = pdf_file.read()
                        st.download_button(
                            label="Click here to download PDF",
                            data=pdf_data,
                            file_name=f"membership_form_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

with tab2:
    st.header("Formatted for Printing")
    st.info("""
    To print this form:
    1. Fill out the form in the 'Membership Form' tab first
    2. Click the three dots (⋮) menu in the top right corner
    3. Select 'Print'
    4. Choose your printer settings and print
    """)
    
    if 'form_data' in locals():  # Only show if form is filled
        st.subheader("DIC2 Toastmasters Membership Form")
        st.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Display form data in a clean format
        for key, value in form_data.items():
            st.write(f"**{key}:** {value}")
        
        st.subheader("Membership Promise")
        st.write("""
        As a member of Toastmasters International and my club, I promise to:
        * Attend club meetings regularly
        * Prepare all of my projects to the best of my ability
        * Prepare for and fulfill meeting assignments
        * Provide fellow members with helpful, constructive evaluations
        * Help maintain a positive, friendly environment
        * Serve as a club officer when called upon
        * Treat fellow members and guests with respect and courtesy
        * Bring guests to club meetings
        * Adhere to Toastmasters guidelines and rules
        * Act within Toastmasters' core values
        """)
    else:
        st.warning("Please fill out the form in the 'Membership Form' tab first.")

with tab3:
    st.header("JSON Data")
    if 'form_data' in locals():  # Only show if form is filled
        st.json(form_data)
    else:
        st.warning("Please fill out the form in the 'Membership Form' tab first.")

with tab4:
    st.header("README")
    st.markdown("""
    # DIC2 Toastmasters Membership Form Application

    This Streamlit application provides a digital membership form for DIC2 Toastmasters Club.

    ## Features

    - Digital form submission
    - PDF download of completed form
    - Print-friendly format
    - JSON data export
    - Membership promise inclusion

    ## How to Use

    1. **Fill Out the Form**
       - Navigate to the 'Membership Form' tab
       - Fill in all required fields
       - Submit the form

    2. **Get Your Form**
       - Download as PDF using the download button
       - Print directly using the 'Print Format' tab
       - View data in JSON format in the 'JSON Data' tab

    3. **Printing Instructions**
       - Go to the 'Print Format' tab
       - Click the three dots (⋮) in the top right corner
       - Select 'Print'
       - Choose your printer settings
       - Print the form

    ## Running the Application

    ### Windows
    ```bash
    streamlit run main.py
    ```

    ### Linux/Mac
    ```bash
    python -m streamlit run main.py
    ```

    ## Requirements
    - Python 3.7+
    - Streamlit
    - FPDF2
    - Python-dateutil

    ## Support
    For any issues or questions, please contact the DIC2 Toastmasters Club administration.
    """)
