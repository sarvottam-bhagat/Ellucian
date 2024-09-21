from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()  

# Set page configuration
st.set_page_config(page_title="I can Retrieve Any SQL query")

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Promotion questions and answers
promotions_questions = [
    "Are there any current discounts on Ellucian services?",
    "Do you offer any special packages for new clients?",
    "What are today's special offers?",
    "Is there a sale on your software products?",
    "What are the current promotions available?",
    "Do you provide discounts for bulk licensing?",
    "Can educational institutions get a special offer?",
    "Is there a discount for subscribing to Ellucian's newsletter?",
    "Are there student discounts for Ellucian products?",
    "Do you offer first-time customer discounts?",
    "Are there any loyalty rewards or points?"
]

promotions_answers = {
    "Are there any current discounts on Ellucian services?": "We offer custom discounts based on the institution's needs. Contact our sales team for more details.",
    "Do you offer any special packages for new clients?": "Yes, we have a special onboarding package for new clients, including discounted rates.",
    "What are today's special offers?": "Today's offer includes a free demo of our cloud solutions with a subscription discount.",
    "Is there a sale on your software products?": "Yes, we have a seasonal sale on select products, including our SIS solutions.",
    "What are the current promotions available?": "We offer various promotions, including discounts on our student success packages and cloud services.",
    "Do you provide discounts for bulk licensing?": "Yes, bulk licensing discounts are available. Please contact our sales team for details.",
    "Can educational institutions get a special offer?": "Educational institutions can access tailored offers and discounts. Contact us for a consultation.",
    "Is there a discount for subscribing to Ellucian's newsletter?": "Newsletter subscribers receive updates on exclusive offers and discounts.",
    "Are there student discounts for Ellucian products?": "We offer institutional discounts that can be passed on to students. Contact us for more information.",
    "Do you offer first-time customer discounts?": "Yes, first-time customers can enjoy a special introductory discount on our services.",
    "Are there any loyalty rewards or points?": "We have a loyalty program where institutions can earn points for future discounts."
}

# Support questions and answers
support_questions = [
    "How do I get support for Ellucian products?",
    "What is your software deployment process?",
    "What payment methods do you accept?",
    "How can I track my order for Ellucian services?",
    "Do you offer international support?",
    "How do I cancel a subscription?",
    "What should I do if I encounter a software issue?",
    "How long does it take to process a refund?",
    "Can I change my subscription plan?",
    "Do you offer customized training services?",
    "How do I contact Ellucian customer support?"
]

support_answers = {
    "How do I get support for Ellucian products?": "You can reach our support team via the customer portal or by contacting support@ellucian.com.",
    "What is your software deployment process?": "Our deployment process includes planning, implementation, and ongoing support tailored to your institution's needs.",
    "What payment methods do you accept?": "We accept various payment methods including bank transfers, credit cards, and purchase orders.",
    "How can I track my order for Ellucian services?": "Order tracking details are provided via email after purchase. Contact us if you need assistance.",
    "Do you offer international support?": "Yes, we provide support to institutions globally. Contact us for specific regional details.",
    "How do I cancel a subscription?": "Please contact your account manager or customer support to initiate a subscription cancellation.",
    "What should I do if I encounter a software issue?": "Report the issue through our support portal, and our team will assist you promptly.",
    "How long does it take to process a refund?": "Refunds are processed within 5-10 business days after approval.",
    "Can I change my subscription plan?": "Yes, you can upgrade or downgrade your plan by contacting our sales team.",
    "Do you offer customized training services?": "We provide customized training tailored to your institution's specific needs. Contact us for details.",
    "How do I contact Ellucian customer support?": "You can contact our support team via email at support@ellucian.com or by calling 1-800-123-4567."
}

product_questions = [
    "What is Ellucian Banner?",
    "How does Ellucian Colleague differ from Banner?",
    "What is Ellucian PowerCampus used for?",
    "How does Ellucian CRM Advance support fundraising?",
    "What is unique about Ellucian Quercus?",
    "Can Ellucian products integrate with third-party systems?",
    "Does Ellucian offer cloud-based solutions?",
    "What analytics tools does Ellucian provide?",
    "What is Ellucian’s Ethos platform?",
    "How does Ellucian support student success?"
]

product_answers = {
    "What is Ellucian Banner?": "Ellucian Banner is a comprehensive ERP system for managing student information, finance, human resources, and financial aid in higher education institutions.",
    "How does Ellucian Colleague differ from Banner?": "Ellucian Colleague is an ERP system often used by smaller institutions, offering flexibility and ease of integration with third-party tools.",
    "What is Ellucian PowerCampus used for?": "Ellucian PowerCampus is a student information system designed for smaller institutions, managing student lifecycle processes with a focus on personalized service.",
    "How does Ellucian CRM Advance support fundraising?": "Ellucian CRM Advance is a tool for fundraising and alumni relations, helping institutions track donations, manage campaigns, and engage with donors effectively.",
    "What is unique about Ellucian Quercus?": "Ellucian Quercus is a cloud-based student information system designed to be highly flexible and customizable, catering primarily to international and non-traditional educational institutions.",
    "Can Ellucian products integrate with third-party systems?": "Yes, Ellucian products are designed to integrate with various third-party tools and platforms to create a seamless technology ecosystem.",
    "Does Ellucian offer cloud-based solutions?": "Yes, many of Ellucian’s products, such as Banner and Colleague, are available as cloud-based solutions, providing scalability, security, and ease of management.",
    "What analytics tools does Ellucian provide?": "Ellucian Analytics is a powerful data analytics platform that allows institutions to gain insights into student success, operational efficiency, and institutional performance.",
    "What is Ellucian’s Ethos platform?": "Ellucian Ethos is a data integration platform that connects various applications across the institution, enabling data sharing and a unified approach to managing information.",
    "How does Ellucian support student success?": "Ellucian supports student success through tools like CRM Advise and Degree Works, which help institutions track student progress, provide personalized advising, and support student retention and completion."
}



def get_gemini_response(question, prompt):
    # Check if the question is a promotion or support question
    if question in promotions_questions:
        return promotions_answers[question]
    elif question in support_questions:
        return support_answers[question]
    elif question in product_questions:
        return product_answers[question]
    # Otherwise, generate SQL query
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database contains a table named ELLUCIAN_PRODUCTS with the following columns - PRODUCT_NAME, SALES_COUNT, PRICE, and CATEGORY.

    For example,
    Example 1 - Which Ellucian product is selling the most?,
    the SQL command will be something like this: SELECT PRODUCT_NAME FROM ELLUCIAN_PRODUCTS ORDER BY SALES_COUNT DESC LIMIT 1;

    Example 2 - Show me all Ellucian products that are under $1000,
    the SQL command will be something like this: SELECT * FROM ELLUCIAN_PRODUCTS WHERE PRICE < 1000;

    The SQL code should not include extra characters at the beginning or end, and should avoid the word SQL in the output.
    """
]


# Streamlit App
st.header("Ellucian's AI Assistant")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")
if submit:
    response = get_gemini_response(question, prompt)
    
    # Check if the response is a promotion/support answer or SQL query
    if response in promotions_answers.values() or response in support_answers.values() or response in product_answers.values():
        st.subheader("Answer:")
        st.write(response)
    else:
        rows = read_sql_query(response, "student.db")
        st.subheader("The Response is:")
        for row in rows:
            st.write(row)
