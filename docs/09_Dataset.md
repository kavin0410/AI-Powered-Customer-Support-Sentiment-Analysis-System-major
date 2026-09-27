# 09. Dataset Description

## Dataset Provenance
The dataset comprises 3,078 validated customer feedback interactions curated across diverse consumer domains (e-commerce, delivery logistics, payment gateways, mobile applications, and customer support). 

## Schema Definition
The dataset is structured across the following attributes:

| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `feedback_id` | String | Unique alpha-numeric tracking identifier | `FB-0001` |
| `feedback_text` | String | Raw customer natural language text | *"Delivery was delayed by two days."* |
| `sentiment` | String | Target sentiment class (`Positive`, `Negative`, `Neutral`) | `Negative` |
| `issue_category`| String | Target operational domain (6 categories) | `Delivery Issue` |
| `date` | String | Interaction date in `YYYY-MM-DD` ISO format | `2025-01-14` |

## Class Distributions

### 1. Sentiment Distribution (Total: 3,078 records)
- **Negative:** 1,393 records (45.26%)
- **Positive:** 1,080 records (35.09%)
- **Neutral:** 605 records (19.65%)

### 2. Issue Category Distribution (Total: 3,078 records)
- **Product Issue:** 734 records (23.85%)
- **Delivery Issue:** 617 records (20.05%)
- **Payment Issue:** 485 records (15.76%)
- **Service Issue:** 463 records (15.04%)
- **Technical Issue:** 460 records (14.94%)
- **General Feedback:** 319 records (10.36%)

## Data Integrity Guarantees
- Zero missing or null values in primary text fields.
- Duplicate removal verified via strict feedback ID and text fingerprinting.
- Stratified 80/20 train/test split utilized during training to ensure identical class proportions across evaluation sets.
