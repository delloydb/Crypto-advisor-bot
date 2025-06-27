# Crypto Investment Advisor

## Overview

This is a Streamlit-based cryptocurrency investment advisor application that provides educational cryptocurrency analysis and investment insights. The application leverages real-time cryptocurrency data from CoinGecko API to offer market analysis, portfolio recommendations, and sustainability scoring for various cryptocurrencies.

## System Architecture

The application follows a modular architecture pattern with clear separation of concerns:

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid development and deployment
- **Visualization**: Plotly for interactive charts and graphs
- **Layout**: Wide layout with expandable sidebar for settings and quick stats
- **State Management**: Streamlit session state for maintaining chat history and component instances

### Backend Architecture
- **Modular Design**: Separate modules for different functionalities
- **API Integration**: RESTful API calls to CoinGecko for real-time cryptocurrency data
- **Caching Strategy**: Built-in caching mechanism to reduce API calls and improve performance
- **Rate Limiting**: Implemented rate limiting to comply with API usage restrictions

## Key Components

### 1. Main Application (`app.py`)
- Entry point and user interface controller
- Handles user interactions and routing
- Manages session state and component initialization
- Implements risk disclaimer and user settings

### 2. Crypto Analyzer (`crypto_analyzer.py`)
- Core analysis engine for cryptocurrency data
- Fetches and processes market data from CoinGecko API
- Implements caching mechanism for API optimization
- Provides market overview and cryptocurrency-specific analysis

### 3. Data Fetcher (`data_fetcher.py`)
- Dedicated module for external API interactions
- Implements robust error handling and retry mechanisms
- Manages rate limiting and request optimization
- Provides caching layer for improved performance

### 4. Rules Engine (`rules_engine.py`)
- Business logic processor for investment recommendations
- Implements risk profiling (Conservative, Moderate, Aggressive)
- Processes natural language queries and routes to appropriate handlers
- Integrates sustainability and profitability scoring

### 5. Sustainability Scorer (`sustainability_scorer.py`)
- Environmental and governance assessment module
- Evaluates cryptocurrencies based on energy efficiency, governance, innovation, and transparency
- Maintains sustainability profiles for major cryptocurrencies
- Supports ESG (Environmental, Social, Governance) investment strategies

## Data Flow

1. **User Input**: User enters queries, portfolio size, risk tolerance, and time horizon
2. **Query Processing**: Rules engine processes natural language queries and determines response type
3. **Data Fetching**: Data fetcher retrieves real-time cryptocurrency data from CoinGecko API
4. **Analysis**: Crypto analyzer processes raw data and applies technical analysis
5. **Scoring**: Sustainability scorer evaluates environmental and governance factors
6. **Recommendation Generation**: Rules engine combines analysis results to generate investment recommendations
7. **Visualization**: Streamlit renders interactive charts and displays recommendations to user

## External Dependencies

### APIs
- **CoinGecko API**: Primary data source for cryptocurrency market data, prices, and statistics
- **Rate Limiting**: 1-second minimum interval between requests to comply with free tier limitations

### Python Libraries
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing operations
- **Plotly**: Interactive data visualization
- **Requests**: HTTP library for API communications

## Deployment Strategy

### Platform
- **Replit**: Cloud-based development and hosting platform
- **Auto-scaling**: Configured for automatic scaling based on demand

### Configuration
- **Python 3.11**: Runtime environment
- **Port 5000**: Default application port
- **Streamlit Server**: Headless mode for production deployment

### Workflow
- Parallel workflow execution for improved performance
- Automated deployment triggers on code changes

## Changelog

- June 27, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.