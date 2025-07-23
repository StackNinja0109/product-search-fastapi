# Product Search FastAPI

A FastAPI-based microservice that provides product search functionality across multiple e-commerce platforms (Yahoo Shopping, Rakuten, and Amazon) and PDF parsing capabilities using AI.

## 🚀 Features

### Product Search
- **Multi-platform search**: Search products across Yahoo Shopping, Rakuten, and Amazon
- **JAN code extraction**: Automatically extract JAN codes from search keywords
- **Cached results**: Optimized performance with in-memory caching
- **Price sorting**: Results sorted by price for easy comparison

### PDF Parser
- **AI-powered parsing**: Uses LlamaParse and Google Gemini for intelligent PDF text extraction
- **Structured data extraction**: Converts PDF tables into structured JSON format
- **Customizable output**: Configurable data fields based on requirements
- **Japanese language support**: Optimized for Japanese document processing

## 📋 Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- Required API keys (see Environment Variables section)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd product-search-fastapi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   # API Authentication
   API_TOKEN=your_api_token_here

   # Yahoo Shopping API
   YAHOO_CLIENT_ID=your_yahoo_client_id

   # Rakuten API
   RAKUTEN_APP_ID=your_rakuten_app_id

   # Amazon API
   AMAZON_PARTNER_TAG=your_amazon_partner_tag
   AMAZON_ACCESS_KEY=your_amazon_access_key
   AMAZON_SECRET_KEY=your_amazon_secret_key
   AMAZON_REGION=your_amazon_region

   # AI Services
   LLAMA_PARSE_API_KEY=your_llama_parse_api_key
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL_NAME=gemini-pro

   # Environment
   APP_ENV=staging  # or production
   ```

## 🚀 Usage

### Starting the Server

```bash
python -m app.app (or uvicorn app.app:web_app --reload)
```

The server will start on `http://127.0.0.1:8000`

### API Endpoints

#### 1. Product Search
**Endpoint**: `POST /v1/search/product`

**Headers**:
```
Authorization: Bearer your_api_token
Content-Type: application/json
```

**Request Body**:
```json
{
  "keyword": "product name or description"
}
```

**Response**:
```json
{
  "jan_code": "4901234567890",
  "yahoo_products": [
    {
      "name": "Product Name",
      "price": 1000,
      "image": "image_url",
      "url": "product_url",
      "platform": "Yahooショッピング"
    }
  ],
  "rakuten_products": [...],
  "amazon_products": [...]
}
```

#### 2. PDF Parser
**Endpoint**: `POST /v1/parser/pdf`

**Headers**:
```
Authorization: Bearer your_api_token
Content-Type: application/json
```

**Request Body**:
```json
{
  "file_url": "path/to/your/file.pdf",
  "formats": ["品番", "品名", "数量", "型番"]
}
```

**Response**:
```json
[
  {
    "品番": "ABC123",
    "品名": "Product Name",
    "数量": "10",
    "型番": "TYPE-001"
  }
]
```

## 📁 Project Structure

```
product-search-fastapi/
├── app/
│   ├── __init__.py          # Configuration and environment variables
│   ├── app.py               # FastAPI application setup
│   ├── auth.py              # Authentication middleware
│   ├── handlers.py          # Request handlers
│   ├── models.py            # Pydantic models
│   └── api/
│       ├── amazon_api.py    # Amazon API integration
│       ├── rakuten_api.py   # Rakuten API integration
│       └── yahoo_api.py     # Yahoo Shopping API integration
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔍 API Integrations

### Yahoo Shopping API
- Uses Yahoo Shopping API V3
- Extracts JAN codes from search results
- Returns product details with pricing and images

### Rakuten API
- Uses Rakuten Ichiba Item Search API
- Searches products by JAN code
- Returns sorted results by price

### Amazon API
- Uses Amazon Product Advertising API
- Searches products across all categories
- Returns detailed product information

### AI Services
- **LlamaParse**: PDF text extraction
- **Google Gemini**: Intelligent data parsing and structuring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request