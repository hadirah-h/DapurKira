# DapurKira

DapurKira is a Malay-language food costing and pricing web application designed for Malaysian homepreneurs.

It helps users calculate product costs, choose suitable selling prices, record product details, and estimate the number of units required to cover monthly business costs.

## Main Features

### 1. Kira Pantas

A quick calculator for users who already know their total batch cost.

- Calculate cost per unit
- Apply a target markup
- Enter a custom selling price
- Display profit, markup, and resulting margin

### 2. Kos Produk

A detailed costing mode for saved products.

- Create, view, update, and delete products
- Organise products by category
- Add, edit, and delete ingredients
- Add, edit, and delete packaging
- Include labour and other costs
- Support units such as g, kg, ml, L, tsp, tbsp, pcs, cm, and m
- Automatically calculate batch cost, cost per unit, selling price, and profit

### 3. Target Jual

A break-even planner for monthly sales targets.

- Use the calculated cost from a saved product
- Enter values manually when needed
- Estimate the business portion of household utilities
- Spread equipment costs across a chosen number of months
- Include other monthly fixed costs
- Set an optional monthly income target
- Display monthly, weekly, and daily sales targets

## Pricing Model

DapurKira uses markup-first pricing:

```text
Selling price = Cost per item × (1 + Markup ÷ 100)
```

The resulting profit margin is shown for reference:

```text
Margin = Profit per item ÷ Selling price × 100
```

## Technology Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Jinja2
- HTML
- CSS
- JavaScript

## Project Structure

```text
PROJECT_BAKERS/
├── main.py
├── database_dapurkira.py
├── models.py
├── schemas.py
├── crud.py
├── calculations.py
├── recipe_calculator.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── dashboard.js
│       ├── quick_calculate.js
│       ├── break_even.js
│       ├── recipe_form.js
│       ├── recipe_edit.js
│       └── recipe_detail.js
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── calculators/
    │   ├── quick_calculate.html
    │   └── break_even.html
    └── recipes/
        ├── form.html
        ├── edit.html
        └── detail.html
```

## Running the Project

### 1. Create a virtual environment

```powershell
py -m venv pb.venv
```

### 2. Activate it

```powershell
.\pb.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```powershell
py -m pip install -r requirements.txt
```

### 4. Start the FastAPI server

```powershell
py -m uvicorn main:app --reload
```

### 5. Open the application

Dashboard:

```text
http://127.0.0.1:8000/
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Current Scope

DapurKira is currently a single-user MVP using a local SQLite database.

The current version does not include:

- User accounts or login
- Multi-user data separation
- AI assistance
- Receipt scanning
- Cloud file storage

These may be considered as future enhancements after the core costing workflow is complete.

## Language and Audience

The interface uses friendly, conversational Malay with familiar English business terms where they are easier for local users to understand.

The intended audience includes home-based food sellers, single mothers, micro-vendors, and other Malaysian homepreneurs.

## Project Status

The core MVP includes all three calculation modes, product CRUD, responsive templates, input validation, and automatic costing calculations.