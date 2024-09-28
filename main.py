import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = "abubakkarsiddique584@gmail.com"
receiver_email = "ik8944046@gmail.com"
password = "Your Gmail App Password"  # Use an app-specific password if 2-Step Verification is enabled

# Amazon product URL
product_url = "https://www.amazon.com/Amazfit-Android-Fitness-Tracking-Waterproof/dp/B09H5TWSB3"

# Headers to mimic a browser visit (to avoid being blocked)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive"
}

# Send a request to the live Amazon URL
response = requests.get(product_url, headers=headers)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Debugging: Print out the HTML content (or a snippet) to verify if the content is loaded
print(soup.prettify()[:1000])  # Print the first 1000 characters to check if the expected content is there

# Extract price using the correct class
try:
    price_element = soup.find("span", class_="aok-offscreen")
    if price_element:
        price_text = price_element.text.strip()
        price_without_currency = price_text.replace("$", "").replace(",", "").strip()
        combined_price = float(price_without_currency)
        print("Price:", combined_price)
    else:
        combined_price = None
        print("Price not found.")
except AttributeError:
    combined_price = None
    print("Price not found.")
except ValueError:
    print(f"Error converting price to float: {price_text}")
    combined_price = None

# Extract the product title
try:
    product_title = soup.find(id="productTitle").text.strip()
    print("Product Title:", product_title)
except AttributeError:
    product_title = "Product Title Not Found"
    print(product_title)

# Check if the price is less than $121 and send an email if it is
if combined_price is not None and combined_price < 121:  # Adjusted condition for testing
    # Compose the email
    subject = "Price Alert: Price Dropped Below $121!"
    body = f"Good news! The price of {product_title} has dropped to ${combined_price}.\n\n" \
           f"Check it out here: {product_url}"

    # Create a MIMEText object for the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
else:
    print(f"Price is ${combined_price}, which is not less than $121.")
