from faker import Faker
from uuid import uuid4
from datetime import datetime
import random
import json

faker = Faker("fr_FR")

def generate_receipt_data(
    overrides: dict = None,
    tax_rate: float = 0.1,
    num_items: int = 3
) -> dict:
    overrides = overrides or {}

    forced_items = overrides.get("items")
    forced_merchant = overrides.get("merchant_name")
    forced_total_ttc = overrides.get("total_ttc")
    forced_tax_rate = overrides.get("tax_rate", tax_rate)

    # If items are provided by the user, use them directly
    if forced_items:
        items = []
        for item in forced_items:
            quantity = item["quantity"]
            unit_price = item["unit_price"]
            line_total = round(quantity * unit_price, 2)
            tax = round(line_total * forced_tax_rate, 2)
            items.append({
                "description": item["description"],
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
                "tax": tax
            })
        ht_total = sum(i["line_total"] for i in items)
        tax_amount = round(ht_total * forced_tax_rate, 2)
        ttc = round(ht_total + tax_amount, 2)

    # Otherwise, generate items to match a specific total if provided
    elif forced_total_ttc:
        ht_total = forced_total_ttc / (1 + forced_tax_rate)
        items = []
        remaining = ht_total
        for i in range(num_items):
            if i == num_items - 1:
                line_total = round(remaining, 2)
            else:
                line_total = round(random.uniform(0.1, remaining / 2), 2)
                remaining -= line_total
            quantity = random.randint(1, 2)
            unit_price = round(line_total / quantity, 2)
            items.append({
                "description": faker.word().capitalize(),
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": round(unit_price * quantity, 2),
                "tax": round(unit_price * quantity * forced_tax_rate, 2)
            })
        ht_total = sum(item["line_total"] for item in items)
        tax_amount = round(ht_total * forced_tax_rate, 2)
        ttc = round(ht_total + tax_amount, 2)

    # Otherwise, fully random generation
    else:
        items = []
        for _ in range(num_items):
            quantity = random.randint(1, 2)
            unit_price = round(random.uniform(1, 10), 2)
            line_total = round(unit_price * quantity, 2)
            items.append({
                "description": faker.word().capitalize(),
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
                "tax": round(line_total * tax_rate, 2)
            })
        ht_total = sum(item["line_total"] for item in items)
        tax_amount = round(ht_total * tax_rate, 2)
        ttc = round(ht_total + tax_amount, 2)

    return {
        "transaction_id": str(uuid4())[:12],
        "authorization_code": str(random.randint(100000, 999999)),
        "transaction_date_time": overrides.get(
            "transaction_date_time",
            datetime.utcnow().isoformat() + "Z"
        ),
        "status": "APPROVED",
        "transaction_amount": {
            "amount": f"{ht_total:.2f}",
            "currency": "EUR",
            "tax_rate": f"{tax_rate * 100:.0f}%",
            "tax_amount": f"{tax_amount:.2f}",
            "amount_tendered": f"{ttc:.2f}",
        },
        "receipt_number": f"RCPT-{random.randint(100000,999999)}",
        "operator_id": "CASHIER01",
        "merchant": {
            "name": forced_merchant or faker.company(),
            "merchant_id": f"M{random.randint(100000000,999999999)}",
            "vat_id": "VAT FR" + str(random.randint(100000000,999999999)),
            "registration_id": "CRN " + str(random.randint(10000000,99999999)),
            "address": {
                "line1": faker.street_address(),
                "city": faker.city(),
                "state": faker.department(),
                "postal_code": faker.postcode(),
                "country": "FR"
            },
            "phone": faker.phone_number(),
            "website": faker.url(),
            "logo_url": "https://dummyimage.com/400x100",
            "logo_alt_text": "Logo",
            "custom_footer_lines": ["Thank you for your visit!"]
        },
        "terminal": {
            "terminal_id": "T" + str(random.randint(100000000,999999999)),
            "entry_mode": "CHIP"
        },
        "card": {
            "card_number_masked": "************1234",
            "cardholder_name": faker.name(),
            "payment_network": "VISA",
            "card_type": "DEBIT"
        },
        "items": items,
        "barcode": {
            "barcode_data": "TXN:" + str(random.randint(1000000000, 9999999999)),
            "barcode_type": "QR"
        }
    }

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    receipt = generate_receipt_data()
    save_json(receipt, "examples/generated_receipt.json")
    print("✅ Receipt JSON generated in /examples/")
