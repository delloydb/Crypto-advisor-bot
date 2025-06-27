import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from crypto_analyzer import CryptoAnalyzer
from rules_engine import RulesEngine
from data_fetcher import DataFetcher
from sustainability_scorer import SustainabilityScorer

# Page configuration
st.set_page_config(
    page_title="Crypto Investment Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = CryptoAnalyzer()
if 'rules_engine' not in st.session_state:
    st.session_state.rules_engine = RulesEngine()

def main():
    st.title("🚀 Cryptocurrency Investment Advisor")
    st.markdown("*Educational cryptocurrency analysis and investment insights*")
    
    # Risk disclaimer
    with st.expander("⚠️ Important Risk Disclaimer - Please Read"):
        st.warning("""
        **IMPORTANT DISCLAIMER:**
        - This tool provides educational information only and is NOT financial advice
        - Cryptocurrency investments are highly volatile and risky
        - You may lose all or part of your investment
        - Always do your own research and consult with qualified financial advisors
        - Past performance does not guarantee future results
        - Never invest more than you can afford to lose
        """)
    
    # Sidebar for settings and quick stats
    with st.sidebar:
        st.header("🔧 Settings")
        
        # Portfolio size input
        portfolio_size = st.number_input(
            "Portfolio Size (USD)", 
            min_value=100, 
            max_value=1000000, 
            value=10000,
            step=500,
            help="Enter your intended investment amount"
        )
        
        # Risk tolerance
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            ["Conservative", "Moderate", "Aggressive"],
            index=1
        )
        
        # Time horizon
        time_horizon = st.selectbox(
            "Investment Time Horizon",
            ["Short-term (< 1 year)", "Medium-term (1-3 years)", "Long-term (> 3 years)"],
            index=1
        )
        
        st.divider()
        
        # Quick market stats
        st.header("📊 Market Overview")
        market_data = st.session_state.analyzer.get_market_overview()
        
        if market_data:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Market Cap", f"${market_data.get('total_market_cap', 0):,.0f}B")
            with col2:
                st.metric("24h Volume", f"${market_data.get('total_volume', 0):,.0f}B")
            
            st.metric("Bitcoin Dominance", f"{market_data.get('market_cap_percentage', {}).get('btc', 0):.1f}%")
    
    # Main chat interface
    st.header("💬 Chat with Crypto Advisor")
    
    # Quick action buttons
    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Analyze Top Cryptos"):
            handle_quick_action("analyze_top")
    
    with col2:
        if st.button("📈 Market Trends"):
            handle_quick_action("market_trends")
    
    with col3:
        if st.button("🌱 Sustainability Report"):
            handle_quick_action("sustainability")
    
    with col4:
        if st.button("💼 Portfolio Suggestions"):
            handle_quick_action("portfolio")
    
    st.divider()
    
    # Chat input
    user_query = st.text_input(
        "Ask me about cryptocurrency investments:",
        placeholder="e.g., 'Should I invest in Bitcoin?' or 'Compare Ethereum vs Cardano'"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Send", type="primary"):
            if user_query:
                handle_user_query(user_query, portfolio_size, risk_tolerance, time_horizon)
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for i, (timestamp, query, response) in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                st.markdown(f"**🕐 {timestamp}**")
                st.markdown(f"**You:** {query}")
                st.markdown(f"**Advisor:** {response}")
                st.divider()

def handle_quick_action(action_type):
    """Handle quick action buttons"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    try:
        if action_type == "analyze_top":
            query = "Analyze top 10 cryptocurrencies"
            response = analyze_top_cryptocurrencies()
        elif action_type == "market_trends":
            query = "Show current market trends"
            response = show_market_trends()
        elif action_type == "sustainability":
            query = "Generate sustainability report"
            response = generate_sustainability_report()
        elif action_type == "portfolio":
            query = "Suggest portfolio allocation"
            response = suggest_portfolio_allocation()
        
        st.session_state.chat_history.append((timestamp, query, response))
        st.rerun()
        
    except Exception as e:
        error_response = f"Sorry, I encountered an error: {str(e)}. Please try again later."
        st.session_state.chat_history.append((timestamp, query, error_response))
        st.rerun()

def handle_user_query(query, portfolio_size, risk_tolerance, time_horizon):
    """Process user query and generate response"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    try:
        # Analyze the query and generate appropriate response
        response = st.session_state.rules_engine.process_query(
            query, portfolio_size, risk_tolerance, time_horizon
        )
        
        st.session_state.chat_history.append((timestamp, query, response))
        st.rerun()
        
    except Exception as e:
        error_response = f"Sorry, I encountered an error processing your query: {str(e)}. Please try again."
        st.session_state.chat_history.append((timestamp, query, error_response))
        st.rerun()

def analyze_top_cryptocurrencies():
    """Analyze top cryptocurrencies"""
    with st.spinner("Analyzing top cryptocurrencies..."):
        try:
            top_cryptos = st.session_state.analyzer.get_top_cryptocurrencies(limit=10)
            
            if not top_cryptos:
                return "Unable to fetch cryptocurrency data at the moment. Please try again later."
            
            # Create analysis
            analysis = "## 📊 Top 10 Cryptocurrency Analysis\n\n"
            
            for crypto in top_cryptos:
                name = crypto.get('name', 'Unknown')
                symbol = crypto.get('symbol', '').upper()
                price = crypto.get('current_price', 0)
                change_24h = crypto.get('price_change_percentage_24h', 0)
                market_cap_rank = crypto.get('market_cap_rank', 0)
                
                # Get recommendation
                recommendation = st.session_state.rules_engine.get_crypto_recommendation(crypto)
                
                analysis += f"**{market_cap_rank}. {name} ({symbol})**\n"
                analysis += f"- Price: ${price:,.2f}\n"
                analysis += f"- 24h Change: {change_24h:+.2f}%\n"
                analysis += f"- Recommendation: {recommendation}\n\n"
            
            # Show visualization
            show_top_cryptos_chart(top_cryptos)
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing cryptocurrencies: {str(e)}"

def show_market_trends():
    """Show current market trends"""
    with st.spinner("Analyzing market trends..."):
        try:
            market_data = st.session_state.analyzer.get_market_trends()
            
            if not market_data:
                return "Unable to fetch market trend data at the moment."
            
            # Create trend analysis
            analysis = "## 📈 Current Market Trends\n\n"
            
            # Market sentiment
            total_market_cap_change = market_data.get('market_cap_change_percentage_24h_usd', 0)
            if total_market_cap_change > 2:
                sentiment = "🟢 **Bullish** - Strong upward momentum"
            elif total_market_cap_change > 0:
                sentiment = "🟡 **Cautiously Optimistic** - Mild positive movement"
            elif total_market_cap_change > -2:
                sentiment = "🟡 **Neutral** - Sideways movement"
            elif total_market_cap_change > -5:
                sentiment = "🟠 **Cautious** - Mild downward pressure"
            else:
                sentiment = "🔴 **Bearish** - Strong downward momentum"
            
            analysis += f"**Market Sentiment:** {sentiment}\n\n"
            analysis += f"**Total Market Cap Change (24h):** {total_market_cap_change:+.2f}%\n\n"
            
            # Show trend visualization
            show_market_trend_chart()
            
            # Get trending coins
            trending = st.session_state.analyzer.get_trending_coins()
            if trending:
                analysis += "**🔥 Trending Cryptocurrencies:**\n\n"
                for i, coin in enumerate(trending[:5], 1):
                    analysis += f"{i}. {coin.get('name', 'Unknown')} ({coin.get('symbol', '').upper()})\n"
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing market trends: {str(e)}"

def generate_sustainability_report():
    """Generate sustainability report"""
    with st.spinner("Generating sustainability report..."):
        try:
            sustainability_data = st.session_state.analyzer.get_sustainability_data()
            
            analysis = "## 🌱 Cryptocurrency Sustainability Report\n\n"
            
            # Sustainability scoring
            scorer = SustainabilityScorer()
            
            # Analyze major cryptocurrencies for sustainability
            major_cryptos = ['bitcoin', 'ethereum', 'cardano', 'polkadot', 'solana']
            sustainability_scores = {}
            
            for crypto_id in major_cryptos:
                score_data = scorer.calculate_sustainability_score(crypto_id)
                sustainability_scores[crypto_id] = score_data
            
            # Sort by sustainability score
            sorted_cryptos = sorted(sustainability_scores.items(), 
                                  key=lambda x: x[1]['total_score'], reverse=True)
            
            analysis += "**🏆 Sustainability Rankings:**\n\n"
            
            for i, (crypto_id, score_data) in enumerate(sorted_cryptos, 1):
                name = score_data['name']
                total_score = score_data['total_score']
                energy_score = score_data['energy_efficiency']
                governance_score = score_data['governance']
                innovation_score = score_data['innovation']
                
                analysis += f"**{i}. {name}**\n"
                analysis += f"- Overall Score: {total_score}/100\n"
                analysis += f"- Energy Efficiency: {energy_score}/100\n"
                analysis += f"- Governance: {governance_score}/100\n"
                analysis += f"- Innovation: {innovation_score}/100\n\n"
            
            # Show sustainability chart
            show_sustainability_chart(sustainability_scores)
            
            return analysis
            
        except Exception as e:
            return f"Error generating sustainability report: {str(e)}"

def suggest_portfolio_allocation():
    """Suggest portfolio allocation"""
    with st.spinner("Generating portfolio suggestions..."):
        try:
            # Get portfolio recommendations based on market analysis
            portfolio = st.session_state.rules_engine.generate_portfolio_recommendation()
            
            analysis = "## 💼 Suggested Portfolio Allocation\n\n"
            
            if not portfolio:
                return "Unable to generate portfolio recommendations at this time."
            
            analysis += "**Recommended Allocation:**\n\n"
            
            total_allocation = 0
            for crypto in portfolio:
                name = crypto['name']
                allocation = crypto['allocation']
                reasoning = crypto['reasoning']
                
                analysis += f"**{name}: {allocation}%**\n"
                analysis += f"- Reasoning: {reasoning}\n\n"
                total_allocation += allocation
            
            # Show portfolio visualization
            show_portfolio_chart(portfolio)
            
            analysis += f"**Total Allocation: {total_allocation}%**\n\n"
            
            if total_allocation < 100:
                cash_allocation = 100 - total_allocation
                analysis += f"**Recommended Cash Reserve: {cash_allocation}%**\n"
                analysis += "Keep remaining funds in cash/stablecoins for opportunities and risk management.\n\n"
            
            analysis += "**⚠️ Remember:** This is educational guidance only. Always diversify and never invest more than you can afford to lose."
            
            return analysis
            
        except Exception as e:
            return f"Error generating portfolio suggestions: {str(e)}"

def show_top_cryptos_chart(cryptos):
    """Display chart for top cryptocurrencies"""
    if not cryptos:
        return
    
    names = [crypto.get('name', '') for crypto in cryptos]
    prices = [crypto.get('current_price', 0) for crypto in cryptos]
    changes = [crypto.get('price_change_percentage_24h', 0) for crypto in cryptos]
    
    fig = go.Figure()
    
    # Price chart
    fig.add_trace(go.Bar(
        x=names,
        y=prices,
        name='Price (USD)',
        marker_color=['green' if change >= 0 else 'red' for change in changes]
    ))
    
    fig.update_layout(
        title='Top 10 Cryptocurrencies by Market Cap',
        xaxis_title='Cryptocurrency',
        yaxis_title='Price (USD)',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_market_trend_chart():
    """Display market trend chart"""
    try:
        # Get historical data for major cryptocurrencies
        historical_data = st.session_state.analyzer.get_historical_data(['bitcoin', 'ethereum'], days=30)
        
        if historical_data:
            fig = go.Figure()
            
            for crypto_id, data in historical_data.items():
                if data and 'prices' in data:
                    dates = [datetime.fromtimestamp(price[0]/1000) for price in data['prices']]
                    prices = [price[1] for price in data['prices']]
                    
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=prices,
                        mode='lines',
                        name=crypto_id.title(),
                        line=dict(width=2)
                    ))
            
            fig.update_layout(
                title='30-Day Price Trends',
                xaxis_title='Date',
                yaxis_title='Price (USD)',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying trend chart: {str(e)}")

def show_sustainability_chart(sustainability_scores):
    """Display sustainability comparison chart"""
    if not sustainability_scores:
        return
    
    names = [data['name'] for data in sustainability_scores.values()]
    scores = [data['total_score'] for data in sustainability_scores.values()]
    
    fig = go.Figure(data=[
        go.Bar(x=names, y=scores, marker_color='green')
    ])
    
    fig.update_layout(
        title='Sustainability Scores Comparison',
        xaxis_title='Cryptocurrency',
        yaxis_title='Sustainability Score (0-100)',
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_portfolio_chart(portfolio):
    """Display portfolio allocation pie chart"""
    if not portfolio:
        return
    
    names = [crypto['name'] for crypto in portfolio]
    allocations = [crypto['allocation'] for crypto in portfolio]
    
    # Add cash if total allocation < 100
    total_allocation = sum(allocations)
    if total_allocation < 100:
        names.append('Cash/Stablecoins')
        allocations.append(100 - total_allocation)
    
    fig = go.Figure(data=[go.Pie(
        labels=names, 
        values=allocations,
        hole=0.3
    )])
    
    fig.update_layout(
        title='Recommended Portfolio Allocation',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
