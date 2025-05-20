# 🧾 Receipt Chatbot – GenAI Programming

## 📌 Overview

This project demonstrates a **chatbot powered by Google's Generative AI (Gemini)** that extracts structured information from **restaurant receipt images** and allows users to **ask questions** about the order. The chatbot is deployed via a **Streamlit web interface**.

---

## ✨ Features

- 🔍 **Data Extraction from Receipts**
  - Uses Google's Gemini Vision Model to extract:
    - Restaurant Name & Address
    - Order Date and Time
    - Items Ordered (with quantities and prices)
    - Subtotal, Tax, and Total
    - Payment Method

- 💬 **Chatbot**
  - Answer questions like:
    - *"What items were ordered?"*
    - *"What was the total amount paid?"*
    - *"Which payment method was used?"*
  - Handles missing/unavailable data gracefully.

- 🌐 **Streamlit Web App**
  - Upload a receipt image
  - Ask natural language questions
  - View extracted data interactively

---

## 📁 Project Structure
AI-Powered Receipt Intelligence Chatbot Using LLMs/
├── app.py                              # Streamlit UI for the chatbot
├── main.py                             # Core logic for extraction and QA
├── benchmark.py                        # Benchmarking functionality
├── test_suite.py                       # Unit tests
├── ground_truths.json                  # Ground truth data for benchmarking
├── .env                                # API keys and environment variables
├── README.md                           # 
├── Approach_Document.pdf               # Design approach and methodology
├── data/                               # Sample receipt images
└── temp_uploaded_receipt.jfif          # Temp image saved by Streamlit

---

##  🔐 Environment Variables

- Create a .env file in the root folder with the following:
  -  GOOGLE_API_KEY=your_google_api_key_here                                       # Add your GOOGLE_API_KEY
  -  Make sure you have access to the Google Generative AI API (Gemini Vision).

---

##  🚀 Running the Application
    
    - 1. Clone or unzip the project:
        - cd AI-Powered Receipt Intelligence Chatbot Using LLMs

    - 2. Start the Streamlit App:
        - streamlit run app.py
            -- This will launch a browser window (usually at http://localhost:8501).

    - 3. Upload & Chat
        - Upload a receipt image (JPG, PNG, JFIF)
        - Ask questions about the receipt in plain English.

---

## 🧪 Running Tests
    - To run the test suite:
        - python test_suite.py

    - Start the Streamlit App:
      - streamlit run app.py

---

## **Usage**
Once the script is running, you can interact with the chatbot via the command line:
1. Enter queries about the receipt details, such as:
   - "What is the restaurant name?"
   - "What is the restaurant address?"
   - "What items were ordered?"
   - "When was the order placed?"
   - "What is the payment method?"
   - "What is the total amount paid?"
2. Type `exit` to quit the chatbot.

---

## **Expected Output**
The chatbot provides clear and concise responses based on the structured data extracted from the receipt image. Below are examples of how the output will look:

### **1. Query: Restaurant Name**
- **Input**: "What is the restaurant name?"
- **Output**:  
  ```
  The restaurant name is [Restaurant Name].
  ```

### **2. Query: Items Ordered**
- **Input**: "What items were ordered?"
- **Output**:  
  ```
  The items ordered are:
  - Item 1 (Quantity: X, Price: $XX.XX)
  - Item 2 (Quantity: Y, Price: $YY.YY)
  ```

### **3. Query: Total Amount Paid**
- **Input**: ""What is the total amount paid?""
- **Output**:  
  ```
  The breakdown of the total amount paid is as follows:
  - Subtotal: $XX.XX
  - Tax: $YY.YY
  - Total Amount Paid: $ZZ.ZZ
  ```

### **4. Edge Case: Missing Information**
- **Input**: "How much was the tip?"
- **Output**:  
  ```
I'm sorry, I couldn't understand your query. You can ask about the restaurant name, address, order date and time, payment method, items ordered, subtotal, tax, or total.
  ```

---

## **Future Enhancements**
- Support additional LLMs like ChatGPT or Claude for comparison.
- Improve error handling for ambiguous or incomplete data.
- Develop a graphical user interface (GUI) or web-based interface for better user interaction.

---







