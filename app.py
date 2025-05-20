import streamlit as st
from main import extract_data_from_image, parse_extracted_data, chatbot_query
from PIL import Image
import os
from benchmark import run_benchmark




st.set_page_config(page_title="Receipt Chatbot", layout="centered")
st.title("🧾 Receipt Chatbot")

st.markdown("Upload a receipt image and ask questions like:")
st.markdown("- What is the total?")
st.markdown("- What items were ordered?")
st.markdown("- What is the payment method?")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "receipt_data" not in st.session_state:
    st.session_state.receipt_data = None

# File uploader
uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png", "jfif"])

if uploaded_file is not None and st.session_state.receipt_data is None:
    with open("temp_uploaded_receipt.jfif", "wb") as f:
        f.write(uploaded_file.read())
    st.image("temp_uploaded_receipt.jfif", caption="Uploaded Receipt", use_container_width=True)

    try:
        extracted_text = extract_data_from_image("temp_uploaded_receipt.jfif")
        st.session_state.receipt_data = parse_extracted_data(extracted_text)
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")
        st.stop()

# Show chat messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if st.session_state.receipt_data:
    user_input = st.chat_input("Ask a question about the receipt")
    if user_input:
        # Add user's message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get bot's response
        response = chatbot_query(user_input, st.session_state.receipt_data)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

            st.markdown("---")
st.header("📊 Run Accuracy Benchmark")

if st.button("Run Benchmark"):
    with st.spinner("Evaluating test receipts..."):
        avg_accuracy, overall_stats, results = run_benchmark()

    st.success(f"✅ Average Accuracy: {avg_accuracy:.2f}%")

    st.subheader("📌 Field-wise Accuracy:")
    for field, stat in overall_stats.items():
        field_accuracy = (stat["correct"] / stat["total"]) * 100
        st.write(f"- **{field}**: {field_accuracy:.2f}% correct")

    st.subheader("🧾 Per-Receipt Accuracy:")
    for result in results:
        st.write(f"- {result['image']}: **{result['accuracy']:.2f}%**")

