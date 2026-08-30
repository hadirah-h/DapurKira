# DapurKira

DapurKira is a Malay-language food costing and pricing web application designed for Malaysian homepreneurs.

It helps home-based food sellers calculate their actual product costs, choose more informed selling prices, save product records, and estimate how many units they need to sell to cover monthly business costs.

## About This Project

DapurKira was developed as my Python bootcamp project.

Coming from a non-computer-science background, I built this application step by step while learning Python fundamentals, business logic, database modelling, API development, data validation, CRUD operations, and frontend integration.

The project began as a command-line calculator. It later evolved into a full-stack FastAPI web application with:

- Three calculation modes
- Product, ingredient, and packaging CRUD
- SQLite data storage
- Automatic unit conversion
- Responsive web pages
- A conversational Malay interface

The original terminal version is preserved in `learning/cli_prototype.py` to document this learning journey.

## Development Approach and AI Assistance

I learned the foundations of Python through a Python bootcamp, including
variables, conditionals, loops, functions, input validation, and basic
problem-solving.

DapurKira was then developed through a combination of hands-on coding
and AI-assisted development, usually described as vibe coding.

I used AI as a learning and development partner to:

- Explain unfamiliar concepts and code
- Brainstorm the application architecture
- Troubleshoot errors
- Review calculations and validation
- Develop and refine the frontend
- Improve the Malay interface wording
- Test and review the application

I implemented, tested, and revised the application throughout the
process. I also made the main product, calculation, language, and
user-experience decisions based on the needs of Malaysian food
homepreneurs.

This project reflects both the Python fundamentals I learned during the
bootcamp and my experience learning how to work responsibly with AI
tools while building a larger full-stack application.

## Problem Statement

Home-based food sellers may calculate their selling prices using only the most obvious ingredient expenses.

Costs such as packaging, labour, small quantities of ingredients, utilities, equipment, and other overhead may be overlooked. This can result in a selling price that does not provide enough profit to sustain the business.

DapurKira provides a structured workflow to help users understand where their costs come from before deciding on a selling price.

## Intended Users

DapurKira is designed for Malaysian food homepreneurs, including:

- Home bakers
- Traditional kuih sellers
- Frozen-food sellers
- Home-based caterers
- Sambal, sauce, and paste producers
- Small food vendors
- Other micro food businesses

## Main Features

### Mode 1: Kira Pantas

A quick calculator for users who already know their total batch cost.

Users can:

- Enter the total cost of one batch
- Enter the number of selling units produced
- Choose a target markup
- Enter a custom selling price
- Calculate cost per unit
- Calculate profit per unit
- View the actual markup
- View the resulting profit margin

### Mode 2: Kos Produk

A detailed product-costing mode with saved records.

Users can:

- Create, view, update, and delete products
- Organise products by category
- Add, edit, and delete ingredients
- Add, edit, and delete packaging items
- Include labour and other batch costs
- Calculate the actual cost of each ingredient used
- Calculate the actual cost of each packaging item used
- View the total batch cost
- View the cost per selling unit
- Receive a suggested selling price
- Enter a custom selling price
- View markup, gross profit, and profit margin

Supported product categories include:

- Kuih Tradisional
- Kek & Dessert
- Roti & Pastri
- Makanan Frozen
- Hidangan Utama
- Snek & Kudapan
- Minuman
- Sambal, Sos & Pes
- Lain-lain

### Mode 3: Target Jual

A break-even and monthly sales-target calculator.

Users can:

- Select a saved product from Mode 2
- Automatically reuse its cost per unit and selling price
- Enter values manually when required
- Estimate the business portion of household utilities
- Spread equipment costs across a selected recovery period
- Include other monthly fixed costs
- Set an optional monthly income target
- View monthly, weekly, and daily sales targets

## CRUD Implementation

Mode 2 contains the main CRUD functionality.

CRUD represents:

- **Create** — Add products, ingredients, and packaging
- **Read** — View saved products and their costing details
- **Update** — Edit existing records
- **Delete** — Remove records that are no longer required

DapurKira provides CRUD operations for:

- Recipes or products
- Ingredients
- Packaging items

When a product is deleted, its related ingredient and packaging records are also deleted through SQLAlchemy cascade relationships.

## Unit Conversion

DapurKira uses a custom unit-conversion system.

Supported units include:

| Category | Units |
|---|---|
| Weight | g, kg |
| Volume | ml, L, tsp, tbsp |
| Length | cm, m |
| Quantity | pcs |

Measurements are converted into a shared base unit before their costs are calculated.

Example:

```text
Rice purchase price: RM30
Purchase size: 10 kg
Quantity used: 100 g

10 kg = 10,000 g
Cost per gram = RM30 / 10,000 g
Cost of 100 g = RM0.30
```

DapurKira prevents incompatible conversions, such as kilograms to millilitres, because weight and volume are different measurement categories.

## Pricing Model

DapurKira uses markup-first pricing.

### Selling price from markup

```text
Selling price = Cost per item * (1 + Markup / 100)
```

### Profit per item

```text
Profit per item = Selling price - Cost per item
```

### Resulting margin

```text
Margin = Profit per item / Selling price * 100
```

### Reverse markup from a custom selling price

```text
Markup = (Selling price - Cost per item) / Cost per item * 100
```

Markup is used as the primary input because it is easier to apply directly to cost. The resulting margin is displayed as additional information.

## Break-Even Model

The minimum monthly sales target is calculated using:

```text
Break-even units =
Total monthly overhead / Gross profit per unit
```

The result is rounded upward because a seller cannot normally sell a fraction of a unit.

DapurKira also converts the result into estimated weekly and daily targets.

## Language and User Experience

DapurKira uses friendly, conversational Malay instead of highly formal terminology.

Familiar English business terms such as `markup` and `packaging` are retained where they may be easier for local users to understand.

The interface also includes Cik Kira, a friendly user-experience persona created to make costing and pricing feel less intimidating.

Cik Kira is not an AI assistant in the current version. She acts as a visual and conversational guide throughout the application.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language and calculation logic |
| FastAPI | Web application, routes, and API endpoints |
| Pydantic | Request, response, and input validation |
| SQLAlchemy | ORM and database operations |
| SQLite | Local database storage |
| Jinja2 | Dynamic server-rendered HTML templates |
| HTML | Page structure and content |
| CSS | Visual design and responsive layout |
| JavaScript | Browser interaction and API communication |
| Uvicorn | ASGI development server |

## Application Architecture

```text
User enters information in the browser
                |
                v
HTML forms and JavaScript
                |
                v
FastAPI routes in main.py
                |
                v
Pydantic validation in schemas.py
                |
                v
CRUD operations and SQLAlchemy models
                |
                v
SQLite database
                |
                v
Calculation helpers
                |
                v
Jinja or JavaScript displays the result
```

## Python File Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Creates the FastAPI application and defines routes |
| `database_dapurkira.py` | Configures the SQLite connection and sessions |
| `models.py` | Defines SQLAlchemy database tables and relationships |
| `schemas.py` | Defines Pydantic validation and API schemas |
| `crud.py` | Performs Create, Read, Update, and Delete operations |
| `calculations.py` | Contains reusable costing and pricing formulas |
| `recipe_calculator.py` | Combines saved product data into a complete calculation |
| `learning/cli_prototype.py` | Preserves the original terminal application |

## Project Structure

```text
DapurKira/
|-- main.py
|-- database_dapurkira.py
|-- models.py
|-- schemas.py
|-- crud.py
|-- calculations.py
|-- recipe_calculator.py
|-- requirements.txt
|-- README.md
|
|-- learning/
|   |-- __init__.py
|   `-- cli_prototype.py
|
|-- static/
|   |-- css/
|   |   `-- style.css
|   |
|   `-- js/
|       |-- dashboard.js
|       |-- quick_calculate.js
|       |-- break_even.js
|       |-- recipe_form.js
|       |-- recipe_edit.js
|       `-- recipe_detail.js
|
`-- templates/
    |-- base.html
    |-- dashboard.html
    |
    |-- calculators/
    |   |-- quick_calculate.html
    |   `-- break_even.html
    |
    `-- recipes/
        |-- form.html
        |-- edit.html
        `-- detail.html
```

## Running the Web Application

### Prerequisites

- Python 3.10 or newer
- Git

### 1. Clone the repository

```powershell
git clone https://github.com/hadirah-h/DapurKira.git
cd DapurKira
```

### 2. Create a virtual environment

```powershell
py -m venv pb.venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\pb.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source pb.venv/bin/activate
```

### 4. Install the dependencies

```powershell
py -m pip install -r requirements.txt
```

### 5. Start the FastAPI server

```powershell
py -m uvicorn main:app --reload
```

### 6. Open DapurKira

Dashboard:

```text
http://127.0.0.1:8000/
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

The local `.dapurkira.db` SQLite database is created automatically when the application starts.

## Running the Original CLI Prototype

The original command-line version can be run from the project root:

```powershell
py -m learning.cli_prototype
```

This version is preserved for learning documentation and is not required to run the FastAPI web application.

## Current Scope

DapurKira is currently a single-user MVP using a local SQLite database.

The current version does not include:

- User accounts or authentication
- Multi-user data separation
- Cloud database storage
- AI assistance
- Receipt scanning
- Formal accounting or tax calculations

The results are intended as costing and pricing guidance rather than professional financial advice.

## Future Enhancements

Possible future improvements include:

- Additional units such as cups and ounces
- Ingredient-specific cup-to-weight conversions
- Ingredient wastage or `kadar susut bahan`
- Practical selling-price rounding
- Price and cost history
- Exportable PDF reports
- Malay and English language options
- User accounts and authentication
- PostgreSQL database support
- Cloud deployment
- Automated tests
- Optional AI guidance
- Receipt scanning

For financial accuracy, the core calculations should remain based on transparent and deterministic formulas even if AI assistance is introduced later.

## Learning Journey

DapurKira developed through several stages:

1. Built individual costing formulas using Python.
2. Created an interactive command-line calculator.
3. Added compatible unit conversions.
4. Separated the formulas into reusable helper functions.
5. Modelled products, ingredients, and packaging with SQLAlchemy.
6. Added Pydantic validation.
7. Built FastAPI CRUD endpoints.
8. Connected the backend to Jinja templates.
9. Added JavaScript interactions.
10. Designed a responsive Malay-language interface.
11. Added detailed costing and break-even planning.
12. Refined the application through testing and user-experience review.

This project taught me that developing a web application involves more than writing formulas. The database, validation, API, calculations, frontend, and user experience must work together consistently.

## Project Status

The core single-user MVP is complete.

Current functionality includes:

- Three calculation modes
- Product, ingredient, and packaging CRUD
- Unit conversion
- Markup-first pricing
- Custom selling prices
- Profit and margin calculations
- Break-even and income targets
- Responsive Jinja templates
- Friendly validation and error messages
- Local SQLite storage

## Author

Developed as a Python bootcamp project by [hadirah-h](https://github.com/hadirah-h), a learner from a non-computer-science background.