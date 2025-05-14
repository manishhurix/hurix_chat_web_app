import streamlit as st
import streamlit.components.v1 as components

def render_privacy_policy():
    # Redirect to the official Hurix privacy policy
    st.markdown('''
        <meta http-equiv="refresh" content="0; url=https://www.hurix.com/privacy-policy/" />
        <div style="margin-top: 2em; text-align: center;">
            <h2>Redirecting to Hurix Privacy Policy...</h2>
            <p>If you are not redirected, <a href="https://www.hurix.com/privacy-policy/">click here</a>.</p>
        </div>
    ''', unsafe_allow_html=True)

    st.title("Privacy Policy")
    st.markdown('''
    <style>
    .privacy-section h2, .privacy-section h3, .privacy-section h4 {
        color: #1a73e8;
        margin-top: 2em;
    }
    .privacy-section p, .privacy-section li {
        font-size: 1.1em;
        line-height: 1.7;
    }
    .privacy-section ul {
        margin-left: 2em;
    }
    </style>
    <div class="privacy-section">
    <h2>Introduction</h2>
    <p>Hurix Systems Pvt. Ltd. (“Hurix”, “us”, “we”) helps organizations from across the world achieve their business goals through its learning content, digital marketing, and technology services. ...</p>
    <h2>Services</h2>
    <p>It is Hurix's policy to respect your privacy regarding any information we may collect while you use or access our software applications and websites...</p>
    <h2>Acceptance</h2>
    <p>This document is an electronic record in terms of the Information Technology Act, 2000 and the rules framed thereunder, as applicable and amended from time to time, pertaining to electronic records in various statutes as amended by the Information Technology Act, 2000. ...</p>
    <h2>Data Controller and Data Processor</h2>
    <p>We process two main types of personal data...</p>
    <h2>Domains and Websites for this Policy</h2>
    <p>For the purposes of this Policy, the term, "Websites", shall refer collectively to www.hurix.com, www.kitaboo.com as well as the other websites that the Hurix Group operates and that link to this Policy.</p>
    <h2>Information We Collect</h2>
    <ul>
        <li>Customer Data that you provide</li>
        <li>Other Data that we collect</li>
        <li>Website Visitor Data</li>
        <li>Data from Others</li>
        <li>Google Analytics</li>
    </ul>
    <h2>Security Measures to Protect your Data</h2>
    <p>We implement security controls to prevent breaches and unauthorised access to your data. ...</p>
    <h2>Contact Information</h2>
    <p>You can contact us about this privacy policy or use of our services.<br>
    If you have questions or complaints regarding this Policy, you may contact us through email at <a href="mailto:gdpr.compliance@hurix.com">gdpr.compliance@hurix.com</a>.<br>
    Hurix System Private Limited<br>
    Unit #102, 1st Floor,<br>
    Seepz-SEZ, Andheri (East)<br>
    Mumbai 400096</p>
    <h2>Privacy policy change</h2>
    <p>Hurix may change this Privacy Policy from time to time, at our sole discretion. ...</p>
    </div>
    ''', unsafe_allow_html=True) 