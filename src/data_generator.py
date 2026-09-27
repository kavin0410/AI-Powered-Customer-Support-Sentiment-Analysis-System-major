"""
Dataset Generator for Customer Feedback & Sentiment Analysis.

This module generates a rich, realistic, reproducible synthetic dataset
of customer feedback entries covering 6 distinct issue categories and 3 sentiment classes.
Realistic raw data anomalies (duplicates, missing fields, dirty formatting) are intentionally
introduced to test and demonstrate the cleaning and preprocessing pipeline.
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


CATEGORIES = [
    "Product Issue",
    "Delivery Issue",
    "Payment Issue",
    "Technical Issue",
    "Service Issue",
    "General Feedback",
]

SENTIMENTS = ["Positive", "Negative", "Neutral"]

# Seeded templates and phrase pools for each category and sentiment
FEEDBACK_CORPUS = {
    ("Product Issue", "Negative"): [
        "The item arrived broken and feels extremely cheap. The plastic cracked within two hours of use.",
        "Completely dissatisfied with the build quality. The zipper got stuck immediately and broke off.",
        "The screen on this monitor has terrible backlight bleeding and dead pixels right in the center.",
        "Defective unit received. It refuses to power on even after charging overnight with the original cable.",
        "The stitching on the jacket came undone after the very first gentle wash. Very poor quality control.",
        "Battery life is terrible, barely lasts 45 minutes on a full charge instead of the advertised 8 hours.",
        "Ordered a size Large but it fits like an Extra Small. The sizing chart is completely inaccurate.",
        "The headphones produce constant static noise in the left ear cup. Unusable for work calls.",
        "Missing essential accessories from the retail box. Missing screws and power adapter.",
        "Product smells strongly of harsh chemicals and the material feels flimsy and brittle.",
        "The device overheats within ten minutes of normal usage. Severe fire hazard in my opinion.",
        "Not as advertised at all. The color shown online was vibrant navy blue, but what arrived is faded grey.",
        "The blender blades became dull after blending soft fruits twice. Terrible motor vibration.",
        "Hardware failure after only two weeks. The buttons no longer register any clicks.",
        "The sole of the running shoe detached during my second jog. Shockingly substandard durability.",
        "Item feels like a counterfeit knockoff. Materials are noticeably different from authentic retail stores.",
        "The hinge feels loose and wobbles whenever opened. Not worth half of what I paid.",
        "Water leaks right through the supposed waterproof seam. Ruined my electronics during light rain.",
        "The motor makes an alarming grinding noise when turned on. Immediate return initiated.",
        "The replacement unit had the exact same defect as the first one. Terrible manufacturing batches."
    ],
    ("Product Issue", "Positive"): [
        "Outstanding build quality! Feels hefty, solid, and premium in hand. Highly recommend this brand.",
        "Exceeded all my expectations. The battery lasts well over two full days of heavy use.",
        "The fabric is luxurious, soft, and fits true to size. The stitching is impeccable.",
        "Superb audio fidelity with deep bass and crystal clear treble. Truly noise cancelling!",
        "The screen is vibrant and crisp with zero glare. Best display I have ever purchased.",
        "Top tier craftsmanship. Everything feels durable, well-finished, and built to last years.",
        "The knife set is razor sharp right out of the box and balances comfortably in hand.",
        "High quality product that matches the photos and descriptions perfectly. Very pleased.",
        "Remarkable ergonomics and silent keys. Typing all day has become significantly more comfortable.",
        "Works straight out of the box with zero fuss. Intuitive design and rock solid performance."
    ],
    ("Product Issue", "Neutral"): [
        "The product matches the specifications listed. It performs standard functions as described.",
        "Standard quality for the price point. Neither exceptionally good nor noticeably bad.",
        "The item is functional. Dimensions match the specification sheet provided on the website.",
        "It performs the required tasks. The design is utilitarian and does what it is supposed to.",
        "Average build quality. It is acceptable for occasional household use.",
        "The material feels standard. Let us see how durable it proves to be over the next few months.",
        "Basic entry-level unit. It comes with standard plastic casing and standard power cords.",
        "Product functions as stated in the user manual. No unexpected features or defects detected."
    ],
    ("Delivery Issue", "Negative"): [
        "Package arrived two weeks past the guaranteed delivery date. Tracking was completely frozen.",
        "The delivery courier literally threw the box over my gate and crushed the contents inside.",
        "The shipping driver marked the package as delivered, but nothing was at my door or porch.",
        "Tracking status says delivered to resident, but security camera footage proves no driver showed up.",
        "The outer shipping carton was completely soaked, torn open, and taped haphazardly by the courier.",
        "Delivery was delayed four separate times with zero explanation or notification from the carrier.",
        "Driver delivered my order to the wrong street address entirely. Neighbor had to bring it over.",
        "Package was left out in heavy pouring rain without any protective plastic wrap.",
        "Express next-day shipping fee paid, yet took seven business days to arrive. Terrible courier service.",
        "The delivery guy was extremely rude, refused to bring the heavy parcel up the elevator.",
        "Order has been stuck at the local sorting hub for over ten days with no scheduled delivery date.",
        "Carrier mishandled the parcel. The fragile sticker was completely ignored and items were shattered."
    ],
    ("Delivery Issue", "Positive"): [
        "Delivered in less than 24 hours in pristine condition. Super fast and careful logistics!",
        "The package arrived two days earlier than expected. Safe packaging with plenty of bubble wrap.",
        "Delivery driver followed all delivery instructions perfectly and hid the parcel behind the pillar.",
        "Excellent delivery tracking updates via SMS every step of the transit. Very impressed.",
        "Courier was polite, arrived within the designated delivery window, and handed the package directly.",
        "Seamless delivery experience. Box arrived in mint condition with zero dents or creases."
    ],
    ("Delivery Issue", "Neutral"): [
        "The package arrived on the scheduled date within the afternoon delivery window.",
        "Delivery took four business days as estimated during checkout. Standard transit time.",
        "Tracking updates were logged at each regional distribution center as expected.",
        "The courier left the parcel in the designated parcel locker box.",
        "Shipping timeframe was within the standard five to seven day window indicated on the invoice.",
        "Package arrived in standard cardboard packaging with carrier shipping labels attached."
    ],
    ("Payment Issue", "Negative"): [
        "I was double billed for a single order! Two identical charges appeared on my credit card statement.",
        "The refund was promised within 3 to 5 business days, but four weeks have passed with no money returned.",
        "The checkout page applied an unauthorized recurring subscription charge without my explicit consent.",
        "My payment went through and funds were deducted from my bank, but the website shows order failed.",
        "The promotional discount coupon code was accepted at checkout but the full price was charged anyway.",
        "Hidden processing fees and unexpected convenience surcharges were added without disclosure at checkout.",
        "The payment gateway crashed during verification, resulting in pending holds on my debit card.",
        "Unable to remove my expired credit card from the saved billing wallet. Security concern!",
        "Refused to honor price match policy despite valid proof submitted before the purchase.",
        "Direct debit was processed twice in one billing cycle. Bank overdraft fees incurred as a result."
    ],
    ("Payment Issue", "Positive"): [
        "The billing department resolved my refund request within a few hours. Money back in my account!",
        "Payment process was swift, seamless, and securely authenticated with Apple Pay.",
        "Promotional discount coupon and reward points were applied smoothly at checkout with clear breakdown.",
        "Accidental overcharge was proactively spotted and refunded by billing team before I even asked.",
        "Invoice receipt was sent instantly to my email with clear itemized taxes and discounts.",
        "Refund was processed back to my bank account instantly. Great service and hassle free transaction!",
        "Payment issue was resolved promptly and the full refund was credited back to my card without delay.",
        "Quick and easy payment processing, very secure and transparent billing statements."
    ],
    ("Payment Issue", "Neutral"): [
        "The charge reflects the exact amount stated on the order summary page.",
        "Billing statement displays the company merchant name and invoice reference number.",
        "Payment processed through the standard 3D secure verification window without errors.",
        "The invoice shows standard itemized sales tax and shipping calculation.",
        "A pre-authorization hold was placed on the card and settled upon shipment dispatch."
    ],
    ("Technical Issue", "Negative"): [
        "The mobile app crashes every single time I tap the checkout or view cart button.",
        "Website throws a 500 internal server error whenever I attempt to update my profile information.",
        "Password reset emails are never received, even after checking spam folders multiple times.",
        "The desktop application constantly freezes during data sync, losing all unsaved customer entries.",
        "Latest app update completely broke the biometric face ID login functionality on iOS.",
        "Infinite loading spinner when trying to download the digital purchase files or license keys.",
        "The browser extension consumes 100% CPU and causes Google Chrome to become unresponsive.",
        "Session timeout occurs every two minutes while filling out the order details. Infuriating bug.",
        "Bluetooth pairing disconnects constantly after three minutes of connection on modern Android.",
        "Search filter on the store website is completely broken; returning zero results for standard items."
    ],
    ("Technical Issue", "Positive"): [
        "The latest software update fixed all previous bugs. The app is lightning fast and responsive now!",
        "Single sign-on worked effortlessly and synchronized all my cross-platform cloud data in seconds.",
        "Smooth, glitch-free UI with intuitive navigation. Great performance even on older phone models.",
        "API documentation is clear and the integration was completely error-free and stable under load.",
        "Crash reporting tool automatically recovered my unsaved workspace data after my computer rebooted."
    ],
    ("Technical Issue", "Neutral"): [
        "The application requires iOS 16 or Android 12 minimum version to install.",
        "Password requirements require at least eight characters, one uppercase letter, and a number.",
        "Software update prompt appeared upon launching the application as scheduled.",
        "The web portal uses standard HTTPS authentication and session cookie validation.",
        "Data synchronization executes automatically at 15-minute intervals when connected to Wi-Fi."
    ],
    ("Service Issue", "Negative"): [
        "Customer support representative was extremely rude, dismissive, and hung up on me mid-sentence.",
        "Waited on hold for over 85 minutes only to be transferred to an automated voicemail system.",
        "Support agent closed my ticket without providing any resolution or response to my question.",
        "Received generic copy-paste canned responses that did not even address the issue I described.",
        "The live chat bot is an endless loop that refuses to transfer me to a human representative.",
        "Agent promised a follow-up call back by 3 PM yesterday, but nobody ever bothered to call.",
        "Representative gave contradictory information compared to what is written in your official refund policy.",
        "Horrible customer service. Nobody takes accountability and every department blames the other.",
        "Support rep claimed they could not locate my account despite providing the exact account ID and email.",
        "Escalated to a supervisor three days ago and still waiting in total silence for an update.",
        "Customer agent took over two hours to answer and then hung up the phone without helping.",
        "The phone agent hung up on me after keeping me on hold for an hour. Unacceptable behavior.",
        "Support agent was useless and refused to answer simple questions on the phone.",
        "Waited on the phone for two hours and customer agent gave zero assistance."
    ],
    ("Service Issue", "Positive"): [
        "Customer representative Sarah was phenomenal! Patient, attentive, and solved my problem in 5 minutes.",
        "Best support experience I have ever had. The agent went above and beyond to make things right.",
        "Immediate response on live chat within 30 seconds. Handled my inquiry with total professionalism.",
        "Support team followed up with a courtesy call the next day to confirm everything was working smoothly.",
        "Agent was knowledgeable, empathetic, and replaced my lost item without any hassle or friction.",
        "Customer support agent took quick action and resolved my issue immediately. Great service!",
        "Superb customer service experience, polite and helpful agents."
    ],
    ("Service Issue", "Neutral"): [
        "Contacted customer support regarding policy clarification. Representative provided the standard policy text.",
        "Support ticket was logged under reference ID 49201 with an estimated reply time of 24 hours.",
        "Automated chat system provided links to the relevant knowledge base articles for my query.",
        "Representative confirmed receipt of documents and forwarded them to the review department.",
        "Operating hours for live phone support are Monday through Friday from 9 AM to 6 PM EST."
    ],
    ("General Feedback", "Negative"): [
        "The new website redesign is messy, cluttered, and much harder to navigate than the previous layout.",
        "Disappointed to see prices increased across the board while portion and package sizes were reduced.",
        "The loyalty rewards program has been devalued so heavily that accumulated points are virtually worthless.",
        "Physical retail store was messy, disorganized, and understaffed during peak shopping hours.",
        "Excessive marketing emails and push notifications sent three times a day despite opting out.",
        "Product packaging uses far too much non-recyclable plastic and styrofoam. Very eco-unfriendly."
    ],
    ("General Feedback", "Positive"): [
        "Love shopping with this company! Always a delight, high standards, and wonderful overall experience.",
        "The commitment to eco-friendly biodegradable packaging is commendable and deeply appreciated.",
        "The new user interface layout is modern, clean, visually appealing, and very easy on the eyes.",
        "Great brand loyalty rewards program. Truly values recurring customers with meaningful perks.",
        "Consistently wonderful service and quality across all my orders over the past three years. Keep it up!"
    ],
    ("General Feedback", "Neutral"): [
        "I would suggest adding more color options and sizes to your seasonal catalog in future releases.",
        "It would be helpful to have a physical store location opened in the downtown metropolitan area.",
        "Feedback regarding the store hours: extending Sunday opening hours to 8 PM would be beneficial.",
        "Survey response regarding brand awareness: learned about your products through an online podcast ad.",
        "Product catalog arrived in the mail today. Browsing through the new winter collection options."
    ],
}

# Modifiers, sentence starters, and realistic contextual additions to create realistic variations
PREFIXES = [
    "",
    "Honestly, ",
    "To be completely frank, ",
    "Writing this review after recent experience: ",
    "My honest feedback: ",
    "Warning to potential buyers: ",
    "Just wanted to share my feedback: ",
    "Customer review: ",
    "Quick update on my order: ",
    "Here is my experience: ",
    "In my opinion, ",
    "Reviewing this after one month: ",
    "Overall impression: ",
]

SUFFIXES = [
    "",
    " Will not be buying again.",
    " Highly recommend!",
    " Hope management addresses this promptly.",
    " Will see how it holds up.",
    " 10/10 would recommend to anyone.",
    " Extremely disappointing experience.",
    " Decent enough for the price.",
    " Very satisfied with this purchase.",
    " Please fix this issue as soon as possible.",
    " Average overall.",
    " Truly five star quality.",
    " One star is too generous for this.",
    " Standard service, nothing extraordinary."
]


def generate_feedback_record(record_id: int, category: str, sentiment: str, base_date: datetime) -> dict:
    """Generate a single customer feedback record."""
    templates = FEEDBACK_CORPUS[(category, sentiment)]
    base_text = random.choice(templates)
    
    # 35% chance to combine two templates for natural longer feedback
    if random.random() < 0.35 and len(templates) > 1:
        second_text = random.choice([t for t in templates if t != base_text] or templates)
        base_text = f"{base_text} {second_text}"
        
    prefix = random.choice(PREFIXES)
    suffix = random.choice(SUFFIXES)
    
    # Context-appropriate suffix pairing
    if sentiment == "Positive" and "disappointing" in suffix:
        suffix = " Truly five star quality."
    elif sentiment == "Negative" and "recommend" in suffix:
        suffix = " Will not be buying again."
    elif sentiment == "Neutral" and ("disappointing" in suffix or "recommend" in suffix):
        suffix = " Decent enough for the price."

    full_text = f"{prefix}{base_text}{suffix}".strip()
    
    # Random date within last 14 months
    days_offset = random.randint(0, 425)
    record_date = (base_date - timedelta(days=days_offset)).strftime("%Y-%m-%d")
    
    return {
        "feedback_id": f"FB-{record_id:05d}",
        "feedback_text": full_text,
        "sentiment": sentiment,
        "issue_category": category,
        "date": record_date,
    }


def generate_raw_dataset(n_samples: int = 3200, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic dataset with realistic distribution and deliberate anomalies
    (missing values, duplicates, whitespace, irregular casing) for data cleaning validation.
    """
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    base_date = datetime(2026, 3, 20)
    records = []
    
    # Realistic sentiment distribution: Negative ~45%, Positive ~35%, Neutral ~20%
    # (Customer support datasets naturally skew toward negative feedback)
    sentiment_weights = [0.35, 0.45, 0.20]  # Positive, Negative, Neutral
    
    # Issue category distribution across typical customer support domain
    category_weights = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]
    
    for i in range(1, n_samples + 1):
        cat = random.choices(CATEGORIES, weights=category_weights, k=1)[0]
        sent = random.choices(SENTIMENTS, weights=sentiment_weights, k=1)[0]
        rec = generate_feedback_record(i, cat, sent, base_date)
        records.append(rec)
        
    df = pd.DataFrame(records)
    
    # Intentionally introduce realistic raw-data anomalies:
    # 1. Duplicates (25 duplicated rows)
    duplicates = df.sample(n=25, random_state=random_seed).copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # 2. Missing/Empty feedback texts (20 records)
    empty_indices = np.random.choice(df.index, size=20, replace=False)
    for idx in empty_indices[:10]:
        df.loc[idx, "feedback_text"] = np.nan
    for idx in empty_indices[10:]:
        df.loc[idx, "feedback_text"] = "   \t\n  "
        
    # 3. Dirty casing and whitespace in sentiment / category for 30 rows
    dirty_indices = np.random.choice(df.index, size=30, replace=False)
    for idx in dirty_indices[:15]:
        df.loc[idx, "sentiment"] = f"  {df.loc[idx, 'sentiment'].lower()}  "
    for idx in dirty_indices[15:]:
        df.loc[idx, "issue_category"] = f"  {df.loc[idx, 'issue_category'].upper()}  "
        
    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    return df


if __name__ == "__main__":
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    raw_path = os.path.join(raw_dir, "raw_feedback.csv")
    
    print("Generating raw feedback dataset...")
    df_raw = generate_raw_dataset(n_samples=3200)
    df_raw.to_csv(raw_path, index=False)
    print(f"Raw dataset successfully created at: {raw_path}")
    print(f"Total raw rows: {len(df_raw)}")
    print(f"Columns: {list(df_raw.columns)}")
