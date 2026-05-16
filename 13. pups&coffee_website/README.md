# Pups & Coffee Website

A Flask learning project for puppy adoption with cart, login, and Stripe checkout flow.

## Features
- User registration/login/logout
- Puppy listing and detail pages
- Session-based cart with editable quantity
- Stripe checkout integration
- Promotional coffee offer banner

## Tech Stack
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Stripe API
- Bootstrap + custom CSS

## Setup
```bash
pip install -r requirements.txt
```

Create environment variables (copy from `.env.example`):
- `SECRET_KEY`
- `STRIPE_SECRET_KEY`

## Run
```bash
python main.py
```

Then open `http://127.0.0.1:5000`.

## Seed Data
```bash
http://127.0.0.1:5000/seed
```

## Security Note
- No real keys are stored in source code.
- Keep `.env` private and never commit it.
