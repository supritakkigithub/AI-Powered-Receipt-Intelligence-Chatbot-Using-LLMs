import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import re

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("Google API key not found. Please check your .env file.")
genai.configure(api_key=google_api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

def clean_text(text):
    # Remove unwanted formatting characters and normalize spaces
    return " ".join(text.replace("**", "").strip().split())

def extract_data_from_image(image_path):
    image = Image.open(image_path)
    response = model.generate_content(
        [
            "Extract the following details from the receipt: "
            "Restaurant Name, Address, Order Date and Time, Payment Method, "
            "Items Ordered (including quantities and prices), Subtotal, Tax, and Total Amount Paid.",
            image  
        ]
    )
    extracted_text = response.text

    cleaned_lines = []
    seen_lines = set()
    for line in extracted_text.splitlines():
        stripped_line = line.strip()
        if stripped_line and stripped_line not in seen_lines:
            cleaned_lines.append(clean_text(stripped_line))
            seen_lines.add(stripped_line)
    cleaned_text = "\n".join(cleaned_lines)

    print("\nCleaned Extracted Text:")
    print(cleaned_text)

    return cleaned_text

def parse_extracted_data(extracted_text):
    receipt_data = {}

    # Restaurant Name
    restaurant_name_match = re.search(r"Restaurant\s*Name:\s*([^\n]+)", extracted_text, re.IGNORECASE)
    receipt_data["restaurant_name"] = (
        clean_text(restaurant_name_match.group(1)) if restaurant_name_match else "Unknown"
    )

    # Restaurant Address
    address_match = re.search(r"Address:\s*([^\n]+)", extracted_text, re.IGNORECASE)
    receipt_data["restaurant_address"] = (
        clean_text(address_match.group(1)) if address_match else "Unknown"
    )

    # Order Date and Time (Updated Regex Pattern)
    date_time_match = re.search(r"Order\s*Date\s*and\s*Time:\s*([\d,/]+\s*,?\s*\d+:\d+\s*[AaPp][Mm])", extracted_text, re.IGNORECASE)
    receipt_data["order_date_time"] = (
        clean_text(date_time_match.group(1)) if date_time_match else "Unknown"
    )

    # Payment Method
    payment_method_match = re.search(r"Payment\s*Method:\s*([^\n]+)", extracted_text, re.IGNORECASE)
    receipt_data["payment_method"] = (
        clean_text(payment_method_match.group(1)) if payment_method_match else "Unknown"
    )

    # Items Ordered
    items_ordered = []
    item_matches = re.findall(r"\*\s*(\d+)\s+([\w\s]+)\s+-\s+\$(\d+\.\d+)", extracted_text, re.IGNORECASE)
    for quantity, item, price in item_matches:
        items_ordered.append({
            "item": clean_text(item),
            "quantity": int(quantity),
            "price": float(price)
        })
    receipt_data["items_ordered"] = items_ordered

    # Subtotal
    subtotal_match = re.search(r"Subtotal:\s*\$?([\d.]+)", extracted_text, re.IGNORECASE)
    receipt_data["subtotal"] = float(subtotal_match.group(1)) if subtotal_match else 0.0

    # Tax
    tax_match = re.search(r"Tax:\s*\$?([\d.]+)", extracted_text, re.IGNORECASE)
    receipt_data["tax"] = float(tax_match.group(1)) if tax_match else 0.0

    # Total Amount Paid
    total_match = re.search(r"Total\s*Amount\s*Paid:\s*\$?([\d.]+)", extracted_text, re.IGNORECASE)
    receipt_data["total"] = float(total_match.group(1)) if total_match else 0.0

    print("\nParsed Receipt Data:")
    print(receipt_data)

    return receipt_data

def chatbot_query(query, receipt_data):
    normalized_query = re.sub(r"[^\w\s]", "", query.lower()).strip()

    if "restaurant name" in normalized_query:
        return f"The restaurant name is {receipt_data['restaurant_name']}."
    elif "address" in normalized_query:
        return f"The restaurant address is {receipt_data['restaurant_address']}."
    elif "date" in normalized_query or "time" in normalized_query or "placed" in normalized_query:
        if receipt_data["order_date_time"] == "Unknown":
            return "The order date and time are not available in the receipt."
        return f"The order was placed on {receipt_data['order_date_time']}."
    elif "payment" in normalized_query or "method" in normalized_query:
        return f"The payment method used was {receipt_data['payment_method']}."
    elif "items" in normalized_query or "ordered" in normalized_query:
        items = "\n".join([
            f"- {item['item']} (Quantity: {item['quantity']}, Price: ${item['price']:.2f})"
            for item in receipt_data["items_ordered"]
        ])
        return f"The items ordered are:\n{items}"
    elif "subtotal" in normalized_query:
        return f"The subtotal is ${receipt_data['subtotal']:.2f}."
    elif "tax" in normalized_query:
        return f"The tax amount is ${receipt_data['tax']:.2f}."
    elif "total" in normalized_query:
        return (
            f"The breakdown of the total amount paid is as follows:\n"
            f"- Subtotal: ${receipt_data['subtotal']:.2f}\n"
            f"- Tax: ${receipt_data['tax']:.2f}\n"
            f"- Total Amount Paid: ${receipt_data['total']:.2f}"
        )
    else:
        return (
            "I'm sorry, I couldn't understand your query. "
            "You can ask about the restaurant name, address, order date and time, payment method, items ordered, subtotal, tax, or total."
        )

def main():
    print("Welcome to the Receipt Chatbot!")
    print("You can ask questions about the receipt details.")
    print("Type 'exit' to quit.")

    image_path = "data/receipt_image.jfif"

    try:
        extracted_text = extract_data_from_image(image_path)
        receipt_data = parse_extracted_data(extracted_text)
    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return

    while True:
        user_input = input("\nEnter your query: ")
        if user_input.lower() == "exit":
            print("Thank you for using the Receipt Chatbot!")
            break
        response = chatbot_query(user_input, receipt_data)
        print(response)

if __name__ == "__main__":
    main()
