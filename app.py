from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

# FAQ database
faq_database = [
    {
        "question": "What are your business hours?",
        "answer": "Our business hours are Monday to Friday, 9:00 AM to 6:00 PM EST. We're closed on weekends and major holidays.",
        "keywords": ["business", "hours", "time", "open", "closed", "schedule", "when"]
    },
    {
        "question": "How do I return a product?",
        "answer": "To return a product, please visit our Returns page and fill out the return form. You have 30 days from purchase to return items. Make sure the product is in original condition with all packaging.",
        "keywords": ["return", "refund", "exchange", "send back", "money back", "defective"]
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, Apple Pay, Google Pay, and bank transfers.",
        "keywords": ["payment", "pay", "credit card", "paypal", "visa", "mastercard", "money", "purchase"]
    },
    {
        "question": "How long does shipping take?",
        "answer": "Standard shipping takes 3-5 business days, expedited shipping takes 1-2 business days, and overnight shipping is available for next-day delivery. International shipping takes 7-14 business days.",
        "keywords": ["shipping", "delivery", "how long", "fast", "time", "days", "arrive", "receive"]
    },
    {
        "question": "Do you offer customer support?",
        "answer": "Yes! We offer 24/7 customer support via live chat, email at support@company.com, and phone at 1-800-SUPPORT. Our support team is always ready to help.",
        "keywords": ["support", "help", "customer service", "contact", "phone", "email", "chat", "assistance"]
    },
    {
        "question": "What is your privacy policy?",
        "answer": "We take your privacy seriously. We never sell your personal data to third parties. You can view our complete privacy policy on our website under the Privacy Policy section.",
        "keywords": ["privacy", "data", "personal information", "policy", "security", "protection", "safe"]
    },
    {
        "question": "How do I create an account?",
        "answer": "To create an account, click the 'Sign Up' button on our homepage, enter your email address and create a password. You'll receive a verification email to activate your account.",
        "keywords": ["account", "sign up", "register", "create", "email", "password", "profile"]
    },
    {
        "question": "Can I track my order?",
        "answer": "Yes! Once your order ships, you'll receive a tracking number via email. You can also log into your account and view order status in the 'My Orders' section.",
        "keywords": ["track", "tracking", "order", "status", "shipment", "where", "location", "delivery"]
    },
    {
        "question": "Do you offer discounts for bulk orders?",
        "answer": "Yes, we offer volume discounts for bulk orders. Orders over $500 get 5% off, orders over $1000 get 10% off, and orders over $2000 get 15% off. Contact our sales team for custom quotes.",
        "keywords": ["bulk", "discount", "volume", "wholesale", "large order", "savings", "cheap", "deal"]
    },
    {
        "question": "What if I forgot my password?",
        "answer": "If you forgot your password, click the 'Forgot Password' link on the login page. Enter your email address and we'll send you a password reset link within a few minutes.",
        "keywords": ["password", "forgot", "reset", "login", "account", "access", "email", "recover"]
    },
    {
        "question": "Where can I find my invoice or receipt?",
        "answer": "You can find your invoice by logging into your account, going to 'My Orders', and selecting the order for which you'd like the receipt.",
        "keywords": ["invoice", "receipt", "bill", "proof", "order", "payment", "download"]
    },
    {
        "question": "Can I cancel my order after placing it?",
        "answer": "Yes, you can cancel your order within 1 hour of placing it by going to 'My Orders' and clicking on 'Cancel'. After that, cancellation depends on the order status.",
        "keywords": ["cancel", "order", "remove", "stop", "change", "undo"]
    },
    {
        "question": "Do you ship internationally?",
        "answer": "Yes, we ship to most countries worldwide. Shipping costs and times vary based on location and shipping method selected at checkout.",
        "keywords": ["international", "worldwide", "outside", "country", "global", "shipping"]
    },
    {
        "question": "Can I update my shipping address after ordering?",
        "answer": "If your order hasn't shipped yet, you can update your shipping address by contacting our support team. Once shipped, address changes are not possible.",
        "keywords": ["address", "shipping", "change", "update", "location", "delivery"]
    },
    {
        "question": "Do you have a loyalty or rewards program?",
        "answer": "Yes! Join our rewards program to earn points for every purchase. Points can be redeemed for discounts on future orders.",
        "keywords": ["loyalty", "rewards", "points", "program", "benefits", "membership", "earn"]
    },
    {
        "question": "What browsers or devices are supported?",
        "answer": "Our site works on all modern browsers like Chrome, Firefox, Safari, and Edge, and is optimized for both desktop and mobile devices.",
        "keywords": ["browser", "device", "mobile", "desktop", "support", "compatibility"]
    },
    {
        "question": "How do I subscribe or unsubscribe from your newsletter?",
        "answer": "You can subscribe to our newsletter at the bottom of our homepage. To unsubscribe, click the 'Unsubscribe' link at the bottom of any of our emails.",
        "keywords": ["newsletter", "subscribe", "unsubscribe", "email", "stop", "mailing"]
    },
    {
        "question": "Are gift cards available for purchase?",
        "answer": "Yes, we offer digital gift cards in various denominations. They can be purchased through our Gift Cards page and used during checkout.",
        "keywords": ["gift", "card", "voucher", "present", "code", "purchase", "buy"]
    }
]

# Preprocessing function
def preprocess(text):
    stop_words = {'the', 'is', 'a', 'in', 'on', 'to', 'with', 'and', 'your', 'you'}
    return [word for word in text.lower().split() if word not in stop_words and len(word) > 2]

# Cosine similarity
def cosine_similarity(a, b):
    words = list(set(a + b))
    vec_a = [a.count(w) for w in words]
    vec_b = [b.count(w) for w in words]
    dot = sum(i * j for i, j in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(i ** 2 for i in vec_a))
    norm_b = math.sqrt(sum(j ** 2 for j in vec_b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("question", "")
    print(f"Received: {user_input}")

    if not user_input.strip():
        return jsonify({"answer": "Please ask a valid question.", "confidence": 0})

    processed_input = preprocess(user_input)
    best_score = 0
    best_answer = "Sorry, I don't understand that yet."

    for faq in faq_database:
        faq_words = preprocess(faq["question"])
        similarity = cosine_similarity(processed_input, faq_words)
        keyword_match = len(set(processed_input) & set(faq["keywords"]))
        keyword_score = keyword_match / len(faq["keywords"])
        score = (similarity * 0.6) + (keyword_score * 0.4)

        if score > best_score:
            best_score = score
            best_answer = faq["answer"]

    return jsonify({
        "answer": best_answer if best_score > 0.3 else "I'm not sure about that. Try asking something else.",
        "confidence": round(best_score * 100)
    })

if __name__ == '__main__':
    app.run(debug=True)