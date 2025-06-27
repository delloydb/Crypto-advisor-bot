import re
from datetime import datetime
from crypto_analyzer import CryptoAnalyzer
from sustainability_scorer import SustainabilityScorer

class RulesEngine:
    def __init__(self):
        self.analyzer = CryptoAnalyzer()
        self.sustainability_scorer = SustainabilityScorer()
        
        # Define risk profiles
        self.risk_profiles = {
            'Conservative': {
                'max_volatility': 15,
                'preferred_market_cap_rank': 10,
                'sustainability_weight': 0.4,
                'profitability_weight': 0.6
            },
            'Moderate': {
                'max_volatility': 25,
                'preferred_market_cap_rank': 25,
                'sustainability_weight': 0.3,
                'profitability_weight': 0.7
            },
            'Aggressive': {
                'max_volatility': 50,
                'preferred_market_cap_rank': 100,
                'sustainability_weight': 0.2,
                'profitability_weight': 0.8
            }
        }
    
    def process_query(self, query, portfolio_size, risk_tolerance, time_horizon):
        """Process user query and return appropriate response"""
        query_lower = query.lower()
        
        # Identify query type and route to appropriate handler
        if any(word in query_lower for word in ['compare', 'vs', 'versus', 'between']):
            return self._handle_comparison_query(query, risk_tolerance)
        elif any(word in query_lower for word in ['should i invest', 'buy', 'recommend']):
            return self._handle_investment_query(query, portfolio_size, risk_tolerance, time_horizon)
        elif any(word in query_lower for word in ['portfolio', 'allocation', 'diversify']):
            return self._handle_portfolio_query(portfolio_size, risk_tolerance, time_horizon)
        elif any(word in query_lower for word in ['sustainability', 'environment', 'green', 'energy']):
            return self._handle_sustainability_query(query)
        elif any(word in query_lower for word in ['price', 'trend', 'analysis', 'technical']):
            return self._handle_price_analysis_query(query)
        else:
            return self._handle_general_query(query, risk_tolerance)
    
    def _handle_comparison_query(self, query, risk_tolerance):
        """Handle cryptocurrency comparison queries"""
        # Extract crypto names from query
        crypto_names = self._extract_crypto_names(query)
        
        if len(crypto_names) < 2:
            return "Please specify at least two cryptocurrencies to compare. For example: 'Compare Bitcoin vs Ethereum'"
        
        comparison_result = "## 🔍 Cryptocurrency Comparison\n\n"
        
        for crypto_name in crypto_names[:3]:  # Limit to 3 cryptos for readability
            crypto_id = self._get_crypto_id(crypto_name)
            if crypto_id:
                analysis = self._analyze_single_crypto(crypto_id, risk_tolerance)
                comparison_result += f"### {crypto_name.title()}\n{analysis}\n\n"
        
        # Add comparison summary
        comparison_result += self._generate_comparison_summary(crypto_names, risk_tolerance)
        
        return comparison_result
    
    def _handle_investment_query(self, query, portfolio_size, risk_tolerance, time_horizon):
        """Handle investment recommendation queries"""
        crypto_names = self._extract_crypto_names(query)
        
        if not crypto_names:
            return "Please specify which cryptocurrency you're asking about. For example: 'Should I invest in Bitcoin?'"
        
        crypto_name = crypto_names[0]
        crypto_id = self._get_crypto_id(crypto_name)
        
        if not crypto_id:
            return f"I couldn't find information about {crypto_name}. Please check the spelling or try a different cryptocurrency."
        
        # Get comprehensive analysis
        analysis = self._get_investment_recommendation(crypto_id, portfolio_size, risk_tolerance, time_horizon)
        
        return f"## 💰 Investment Analysis for {crypto_name.title()}\n\n{analysis}"
    
    def _handle_portfolio_query(self, portfolio_size, risk_tolerance, time_horizon):
        """Handle portfolio allocation queries"""
        portfolio_recommendation = self.generate_portfolio_recommendation(portfolio_size, risk_tolerance, time_horizon)
        
        response = "## 💼 Portfolio Allocation Recommendation\n\n"
        
        if not portfolio_recommendation:
            return response + "Unable to generate portfolio recommendations at this time. Please try again later."
        
        response += f"**Based on your {risk_tolerance.lower()} risk profile and ${portfolio_size:,} portfolio:**\n\n"
        
        for allocation in portfolio_recommendation:
            response += f"**{allocation['name']}: {allocation['allocation']}%**\n"
            response += f"- Reasoning: {allocation['reasoning']}\n"
            response += f"- Estimated Amount: ${(portfolio_size * allocation['allocation'] / 100):,.2f}\n\n"
        
        total_crypto_allocation = sum(alloc['allocation'] for alloc in portfolio_recommendation)
        if total_crypto_allocation < 100:
            cash_allocation = 100 - total_crypto_allocation
            response += f"**Cash/Stablecoins: {cash_allocation}%**\n"
            response += f"- Keep ${(portfolio_size * cash_allocation / 100):,.2f} in cash for opportunities and risk management\n\n"
        
        response += "**⚠️ Important Reminders:**\n"
        response += "- This is educational guidance, not financial advice\n"
        response += "- Consider dollar-cost averaging for entry positions\n"
        response += "- Set stop-losses and take-profit levels\n"
        response += "- Review and rebalance regularly\n"
        
        return response
    
    def _handle_sustainability_query(self, query):
        """Handle sustainability-related queries"""
        crypto_names = self._extract_crypto_names(query)
        
        response = "## 🌱 Sustainability Analysis\n\n"
        
        if crypto_names:
            # Analyze specific cryptocurrencies
            for crypto_name in crypto_names:
                crypto_id = self._get_crypto_id(crypto_name)
                if crypto_id:
                    sustainability_data = self.sustainability_scorer.calculate_sustainability_score(crypto_id)
                    response += f"### {crypto_name.title()}\n"
                    response += f"- **Overall Sustainability Score: {sustainability_data['total_score']}/100**\n"
                    response += f"- Energy Efficiency: {sustainability_data['energy_efficiency']}/100\n"
                    response += f"- Governance: {sustainability_data['governance']}/100\n"
                    response += f"- Innovation: {sustainability_data['innovation']}/100\n"
                    response += f"- Key Features: {sustainability_data['key_features']}\n\n"
        else:
            # General sustainability information
            response += self._get_general_sustainability_info()
        
        return response
    
    def _handle_price_analysis_query(self, query):
        """Handle price and technical analysis queries"""
        crypto_names = self._extract_crypto_names(query)
        
        if not crypto_names:
            return "Please specify which cryptocurrency you'd like me to analyze. For example: 'Analyze Bitcoin price trends'"
        
        crypto_name = crypto_names[0]
        crypto_id = self._get_crypto_id(crypto_name)
        
        if not crypto_id:
            return f"I couldn't find price data for {crypto_name}. Please check the spelling."
        
        # Get price analysis
        analysis = self._get_technical_analysis(crypto_id)
        
        return f"## 📈 Technical Analysis for {crypto_name.title()}\n\n{analysis}"
    
    def _handle_general_query(self, query, risk_tolerance):
        """Handle general cryptocurrency queries"""
        response = "## 💡 General Cryptocurrency Guidance\n\n"
        
        if 'beginner' in query.lower() or 'start' in query.lower():
            response += self._get_beginner_guidance(risk_tolerance)
        elif 'market' in query.lower():
            response += self._get_market_overview_analysis()
        elif 'risk' in query.lower():
            response += self._get_risk_management_advice()
        else:
            response += "I'd be happy to help! Here are some things I can assist you with:\n\n"
            response += "- **Investment Analysis**: Ask about specific cryptocurrencies\n"
            response += "- **Portfolio Recommendations**: Get allocation suggestions\n"
            response += "- **Sustainability Reports**: Learn about eco-friendly cryptos\n"
            response += "- **Market Trends**: Current market analysis\n"
            response += "- **Comparisons**: Compare different cryptocurrencies\n\n"
            response += "Try asking: 'Should I invest in Bitcoin?' or 'Compare Ethereum vs Cardano'"
        
        return response
    
    def _extract_crypto_names(self, query):
        """Extract cryptocurrency names from query"""
        # Common cryptocurrency mappings
        crypto_mappings = {
            'bitcoin': 'bitcoin', 'btc': 'bitcoin',
            'ethereum': 'ethereum', 'eth': 'ethereum',
            'cardano': 'cardano', 'ada': 'cardano',
            'polkadot': 'polkadot', 'dot': 'polkadot',
            'solana': 'solana', 'sol': 'solana',
            'chainlink': 'chainlink', 'link': 'chainlink',
            'litecoin': 'litecoin', 'ltc': 'litecoin',
            'dogecoin': 'dogecoin', 'doge': 'dogecoin',
            'polygon': 'matic-network', 'matic': 'matic-network',
            'avalanche': 'avalanche-2', 'avax': 'avalanche-2'
        }
        
        found_cryptos = []
        query_lower = query.lower()
        
        for name, crypto_id in crypto_mappings.items():
            if name in query_lower:
                found_cryptos.append(name)
        
        return list(set(found_cryptos))  # Remove duplicates
    
    def _get_crypto_id(self, crypto_name):
        """Get CoinGecko crypto ID from name"""
        crypto_mappings = {
            'bitcoin': 'bitcoin', 'btc': 'bitcoin',
            'ethereum': 'ethereum', 'eth': 'ethereum',
            'cardano': 'cardano', 'ada': 'cardano',
            'polkadot': 'polkadot', 'dot': 'polkadot',
            'solana': 'solana', 'sol': 'solana',
            'chainlink': 'chainlink', 'link': 'chainlink',
            'litecoin': 'litecoin', 'ltc': 'litecoin',
            'dogecoin': 'dogecoin', 'doge': 'dogecoin',
            'polygon': 'matic-network', 'matic': 'matic-network',
            'avalanche': 'avalanche-2', 'avax': 'avalanche-2'
        }
        
        return crypto_mappings.get(crypto_name.lower())
    
    def _analyze_single_crypto(self, crypto_id, risk_tolerance):
        """Analyze a single cryptocurrency"""
        try:
            # Get crypto data
            crypto_data = self.analyzer.get_cryptocurrency_data(crypto_id)
            if not crypto_data:
                return "Unable to fetch data for this cryptocurrency."
            
            market_data = crypto_data.get('market_data', {})
            current_price = market_data.get('current_price', {}).get('usd', 0)
            price_change_24h = market_data.get('price_change_percentage_24h', 0)
            market_cap_rank = market_data.get('market_cap_rank', 0)
            
            # Get additional analysis
            historical_data = self.analyzer.get_historical_data([crypto_id], 30)
            volatility = 0
            rsi = 50
            
            if historical_data and crypto_id in historical_data and historical_data[crypto_id]:
                prices = historical_data[crypto_id].get('prices', [])
                volatility = self.analyzer.calculate_volatility(prices)
                rsi = self.analyzer.calculate_rsi(prices)
            
            # Generate analysis
            analysis = f"**Current Price:** ${current_price:,.2f}\n"
            analysis += f"**24h Change:** {price_change_24h:+.2f}%\n"
            analysis += f"**Market Cap Rank:** #{market_cap_rank}\n"
            analysis += f"**30-day Volatility:** {volatility:.1f}%\n"
            analysis += f"**RSI (14):** {rsi:.1f}\n"
            
            # Get recommendation
            recommendation = self.get_crypto_recommendation(market_data, risk_tolerance)
            analysis += f"**Recommendation:** {recommendation}\n"
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing cryptocurrency: {str(e)}"
    
    def _get_investment_recommendation(self, crypto_id, portfolio_size, risk_tolerance, time_horizon):
        """Get detailed investment recommendation"""
        try:
            crypto_data = self.analyzer.get_cryptocurrency_data(crypto_id)
            if not crypto_data:
                return "Unable to fetch cryptocurrency data for analysis."
            
            market_data = crypto_data.get('market_data', {})
            name = crypto_data.get('name', 'Unknown')
            
            # Basic metrics
            current_price = market_data.get('current_price', {}).get('usd', 0)
            price_change_24h = market_data.get('price_change_percentage_24h', 0)
            price_change_7d = market_data.get('price_change_percentage_7d', 0)
            price_change_30d = market_data.get('price_change_percentage_30d', 0)
            market_cap_rank = market_data.get('market_cap_rank', 0)
            
            # Technical analysis
            historical_data = self.analyzer.get_historical_data([crypto_id], 30)
            volatility = 0
            rsi = 50
            momentum_7d = 0
            
            if historical_data and crypto_id in historical_data and historical_data[crypto_id]:
                prices = historical_data[crypto_id].get('prices', [])
                volatility = self.analyzer.calculate_volatility(prices)
                rsi = self.analyzer.calculate_rsi(prices)
                momentum_7d = self.analyzer.get_price_momentum(crypto_id, 7)
            
            # Sustainability score
            sustainability_data = self.sustainability_scorer.calculate_sustainability_score(crypto_id)
            sustainability_score = sustainability_data['total_score']
            
            # Risk assessment
            risk_profile = self.risk_profiles[risk_tolerance]
            
            # Generate recommendation
            recommendation = ""
            
            # Price analysis
            recommendation += f"**Current Metrics:**\n"
            recommendation += f"- Price: ${current_price:,.2f}\n"
            recommendation += f"- 24h: {price_change_24h:+.2f}%, 7d: {price_change_7d:+.2f}%, 30d: {price_change_30d:+.2f}%\n"
            recommendation += f"- Market Cap Rank: #{market_cap_rank}\n"
            recommendation += f"- Volatility: {volatility:.1f}%\n"
            recommendation += f"- RSI: {rsi:.1f}\n"
            recommendation += f"- Sustainability Score: {sustainability_score}/100\n\n"
            
            # Risk assessment
            risk_level = "Low"
            if volatility > 30:
                risk_level = "High"
            elif volatility > 20:
                risk_level = "Medium"
            
            recommendation += f"**Risk Assessment:** {risk_level}\n\n"
            
            # Investment recommendation
            recommendation += "**Investment Recommendation:**\n"
            
            # Check if suitable for risk profile
            if volatility > risk_profile['max_volatility']:
                recommendation += f"⚠️ **CAUTION**: This crypto's volatility ({volatility:.1f}%) exceeds your {risk_tolerance.lower()} risk tolerance.\n\n"
            
            if market_cap_rank <= risk_profile['preferred_market_cap_rank']:
                recommendation += "✅ **POSITIVE**: Well-established cryptocurrency with good market position.\n"
            else:
                recommendation += "⚠️ **CAUTION**: Lower market cap cryptocurrency with higher risk.\n"
            
            # Technical signals
            if rsi < 30:
                recommendation += "📈 **TECHNICAL**: Potentially oversold (RSI < 30) - possible buying opportunity.\n"
            elif rsi > 70:
                recommendation += "📉 **TECHNICAL**: Potentially overbought (RSI > 70) - consider waiting.\n"
            else:
                recommendation += "📊 **TECHNICAL**: Neutral technical indicators.\n"
            
            # Sustainability consideration
            if sustainability_score >= 70:
                recommendation += "🌱 **SUSTAINABILITY**: High sustainability score - good for ESG-conscious investors.\n"
            elif sustainability_score >= 50:
                recommendation += "🌱 **SUSTAINABILITY**: Moderate sustainability score.\n"
            else:
                recommendation += "⚠️ **SUSTAINABILITY**: Low sustainability score - consider environmental impact.\n"
            
            # Position size recommendation
            recommended_allocation = self._calculate_position_size(
                volatility, market_cap_rank, sustainability_score, risk_tolerance
            )
            
            recommended_amount = portfolio_size * recommended_allocation / 100
            
            recommendation += f"\n**Suggested Position Size:** {recommended_allocation}% of portfolio (${recommended_amount:,.2f})\n\n"
            
            # Time horizon considerations
            recommendation += f"**{time_horizon} Considerations:**\n"
            if "Short-term" in time_horizon:
                recommendation += "- Focus on technical indicators and market sentiment\n"
                recommendation += "- Consider taking profits at resistance levels\n"
                recommendation += "- Monitor closely for volatility\n"
            elif "Medium-term" in time_horizon:
                recommendation += "- Balance technical and fundamental analysis\n"
                recommendation += "- Consider dollar-cost averaging for entry\n"
                recommendation += "- Monitor project development and adoption\n"
            else:  # Long-term
                recommendation += "- Focus on fundamental strength and adoption potential\n"
                recommendation += "- Consider sustainability and regulatory outlook\n"
                recommendation += "- Regular rebalancing recommended\n"
            
            recommendation += "\n**⚠️ Risk Disclaimer:** This is educational analysis only. Cryptocurrency investments are highly risky and volatile. Never invest more than you can afford to lose."
            
            return recommendation
            
        except Exception as e:
            return f"Error generating investment recommendation: {str(e)}"
    
    def _calculate_position_size(self, volatility, market_cap_rank, sustainability_score, risk_tolerance):
        """Calculate recommended position size based on risk factors"""
        base_allocation = {
            'Conservative': 5,
            'Moderate': 10,
            'Aggressive': 20
        }
        
        allocation = base_allocation[risk_tolerance]
        
        # Adjust for volatility
        if volatility > 40:
            allocation *= 0.5
        elif volatility > 25:
            allocation *= 0.7
        elif volatility < 15:
            allocation *= 1.2
        
        # Adjust for market cap rank
        if market_cap_rank <= 5:
            allocation *= 1.3
        elif market_cap_rank <= 20:
            allocation *= 1.1
        elif market_cap_rank > 50:
            allocation *= 0.7
        
        # Adjust for sustainability (if investor cares about it)
        if sustainability_score >= 80:
            allocation *= 1.1
        elif sustainability_score < 40:
            allocation *= 0.9
        
        # Cap the allocation
        max_allocation = {
            'Conservative': 10,
            'Moderate': 20,
            'Aggressive': 30
        }
        
        return min(allocation, max_allocation[risk_tolerance])
    
    def get_crypto_recommendation(self, crypto_data, risk_tolerance="Moderate"):
        """Get simple recommendation for a cryptocurrency"""
        try:
            if isinstance(crypto_data, dict) and 'current_price' in crypto_data:
                # This is market data from API
                price_change_24h = crypto_data.get('price_change_percentage_24h', 0)
                market_cap_rank = crypto_data.get('market_cap_rank', 100)
            else:
                # This is individual crypto data
                price_change_24h = crypto_data.get('price_change_percentage_24h', 0)
                market_cap_rank = crypto_data.get('market_cap_rank', 100)
            
            # Simple rule-based recommendation
            if market_cap_rank <= 10:
                if price_change_24h > 5:
                    return "🟢 STRONG BUY - Top crypto with positive momentum"
                elif price_change_24h > 0:
                    return "🟢 BUY - Stable top crypto showing growth"
                elif price_change_24h > -5:
                    return "🟡 HOLD - Top crypto with minor decline"
                else:
                    return "🟠 CAUTION - Top crypto showing weakness"
            elif market_cap_rank <= 25:
                if price_change_24h > 10:
                    return "🟢 BUY - Strong momentum in established crypto"
                elif price_change_24h > 0:
                    return "🟡 CONSIDER - Positive movement in mid-cap crypto"
                else:
                    return "🟠 HOLD - Established crypto under pressure"
            else:
                if price_change_24h > 15:
                    return "🟡 SPECULATIVE BUY - High risk, high reward potential"
                else:
                    return "🔴 AVOID - High risk with limited upside"
                    
        except Exception:
            return "🟡 NEUTRAL - Unable to determine recommendation"
    
    def generate_portfolio_recommendation(self, portfolio_size=10000, risk_tolerance="Moderate", time_horizon="Medium-term (1-3 years)"):
        """Generate portfolio allocation recommendations"""
        try:
            portfolio = []
            
            # Get top cryptocurrencies
            top_cryptos = self.analyzer.get_top_cryptocurrencies(20)
            if not top_cryptos:
                return []
            
            risk_profile = self.risk_profiles[risk_tolerance]
            
            # Core holdings (lower risk)
            if risk_tolerance in ['Conservative', 'Moderate']:
                # Bitcoin allocation
                btc_data = next((crypto for crypto in top_cryptos if crypto.get('symbol', '').lower() == 'btc'), None)
                if btc_data:
                    btc_allocation = 40 if risk_tolerance == 'Conservative' else 30
                    portfolio.append({
                        'name': 'Bitcoin (BTC)',
                        'allocation': btc_allocation,
                        'reasoning': 'Digital gold, most established cryptocurrency with institutional adoption'
                    })
                
                # Ethereum allocation
                eth_data = next((crypto for crypto in top_cryptos if crypto.get('symbol', '').lower() == 'eth'), None)
                if eth_data:
                    eth_allocation = 30 if risk_tolerance == 'Conservative' else 25
                    portfolio.append({
                        'name': 'Ethereum (ETH)',
                        'allocation': eth_allocation,
                        'reasoning': 'Leading smart contract platform with strong developer ecosystem'
                    })
            
            # Growth holdings (medium risk)
            if risk_tolerance != 'Conservative':
                growth_cryptos = [
                    {'symbol': 'ada', 'name': 'Cardano (ADA)', 'allocation': 10, 'reasoning': 'Sustainable PoS blockchain with academic approach'},
                    {'symbol': 'dot', 'name': 'Polkadot (DOT)', 'allocation': 8, 'reasoning': 'Interoperability-focused with parachain technology'},
                    {'symbol': 'sol', 'name': 'Solana (SOL)', 'allocation': 7, 'reasoning': 'High-performance blockchain for DeFi and NFTs'}
                ]
                
                for growth_crypto in growth_cryptos:
                    if risk_tolerance == 'Aggressive' or growth_crypto['allocation'] <= 10:
                        portfolio.append(growth_crypto)
            
            # Speculative holdings (higher risk)
            if risk_tolerance == 'Aggressive':
                speculative_cryptos = [
                    {'symbol': 'link', 'name': 'Chainlink (LINK)', 'allocation': 5, 'reasoning': 'Leading oracle network for smart contracts'},
                    {'symbol': 'matic', 'name': 'Polygon (MATIC)', 'allocation': 5, 'reasoning': 'Ethereum scaling solution with growing adoption'}
                ]
                
                for spec_crypto in speculative_cryptos:
                    portfolio.append(spec_crypto)
            
            # Ensure total allocation doesn't exceed reasonable limits
            total_allocation = sum(crypto['allocation'] for crypto in portfolio)
            max_crypto_allocation = {
                'Conservative': 70,
                'Moderate': 80,
                'Aggressive': 90
            }
            
            if total_allocation > max_crypto_allocation[risk_tolerance]:
                # Scale down allocations proportionally
                scale_factor = max_crypto_allocation[risk_tolerance] / total_allocation
                for crypto in portfolio:
                    crypto['allocation'] = round(crypto['allocation'] * scale_factor)
            
            return portfolio
            
        except Exception as e:
            print(f"Error generating portfolio: {str(e)}")
            return []
    
    def _generate_comparison_summary(self, crypto_names, risk_tolerance):
        """Generate a summary comparing multiple cryptocurrencies"""
        summary = "### 📋 Comparison Summary\n\n"
        
        try:
            # Get data for comparison
            comparison_data = []
            for crypto_name in crypto_names[:3]:
                crypto_id = self._get_crypto_id(crypto_name)
                if crypto_id:
                    crypto_data = self.analyzer.get_cryptocurrency_data(crypto_id)
                    if crypto_data:
                        market_data = crypto_data.get('market_data', {})
                        sustainability_data = self.sustainability_scorer.calculate_sustainability_score(crypto_id)
                        
                        comparison_data.append({
                            'name': crypto_name.title(),
                            'market_cap_rank': market_data.get('market_cap_rank', 0),
                            'price_change_24h': market_data.get('price_change_percentage_24h', 0),
                            'sustainability_score': sustainability_data['total_score']
                        })
            
            if not comparison_data:
                return summary + "Unable to compare the specified cryptocurrencies."
            
            # Sort by market cap rank (lower is better)
            comparison_data.sort(key=lambda x: x['market_cap_rank'])
            
            summary += "**Market Position Ranking:**\n"
            for i, crypto in enumerate(comparison_data, 1):
                summary += f"{i}. {crypto['name']} (Rank #{crypto['market_cap_rank']})\n"
            
            summary += "\n**24h Performance:**\n"
            performance_sorted = sorted(comparison_data, key=lambda x: x['price_change_24h'], reverse=True)
            for i, crypto in enumerate(performance_sorted, 1):
                change = crypto['price_change_24h']
                emoji = "🟢" if change > 0 else "🔴" if change < 0 else "🟡"
                summary += f"{i}. {crypto['name']}: {change:+.2f}% {emoji}\n"
            
            summary += "\n**Sustainability Ranking:**\n"
            sustainability_sorted = sorted(comparison_data, key=lambda x: x['sustainability_score'], reverse=True)
            for i, crypto in enumerate(sustainability_sorted, 1):
                score = crypto['sustainability_score']
                emoji = "🌱" if score >= 70 else "🟡" if score >= 50 else "🟠"
                summary += f"{i}. {crypto['name']}: {score}/100 {emoji}\n"
            
            # Overall recommendation
            summary += f"\n**For {risk_tolerance} Risk Profile:**\n"
            best_overall = comparison_data[0]  # Highest market cap (most established)
            summary += f"**Recommended:** {best_overall['name']} - Most established with lowest risk\n"
            
            return summary
            
        except Exception as e:
            return summary + f"Error generating comparison: {str(e)}"
    
    def _get_beginner_guidance(self, risk_tolerance):
        """Provide guidance for cryptocurrency beginners"""
        guidance = "Welcome to cryptocurrency investing! Here's what you need to know:\n\n"
        
        guidance += "**🎯 Getting Started Steps:**\n"
        guidance += "1. **Education First** - Understand blockchain technology and crypto basics\n"
        guidance += "2. **Start Small** - Begin with amounts you can afford to lose completely\n"
        guidance += "3. **Choose Reputable Exchanges** - Use well-established platforms with good security\n"
        guidance += "4. **Secure Storage** - Learn about hot vs cold wallets\n"
        guidance += "5. **Diversify** - Don't put everything in one cryptocurrency\n\n"
        
        guidance += f"**📊 For {risk_tolerance} Investors:**\n"
        if risk_tolerance == "Conservative":
            guidance += "- Start with Bitcoin and Ethereum (70-80% of crypto allocation)\n"
            guidance += "- Limit crypto to 5-10% of total portfolio\n"
            guidance += "- Focus on established cryptocurrencies (top 10 by market cap)\n"
        elif risk_tolerance == "Moderate":
            guidance += "- Core holdings: Bitcoin, Ethereum (60-70% of crypto allocation)\n"
            guidance += "- Add 2-3 alternative cryptocurrencies (20-30%)\n"
            guidance += "- Limit crypto to 10-20% of total portfolio\n"
        else:  # Aggressive
            guidance += "- Diversify across 5-8 different cryptocurrencies\n"
            guidance += "- Include some smaller market cap opportunities\n"
            guidance += "- Can allocate up to 30% of portfolio to crypto\n"
        
        guidance += "\n**⚠️ Essential Reminders:**\n"
        guidance += "- Never invest borrowed money\n"
        guidance += "- Don't FOMO (Fear of Missing Out)\n"
        guidance += "- Set clear entry and exit strategies\n"
        guidance += "- Consider dollar-cost averaging\n"
        guidance += "- Keep detailed records for taxes\n"
        
        return guidance
    
    def _get_market_overview_analysis(self):
        """Provide current market overview and analysis"""
        market_data = self.analyzer.get_market_overview()
        
        if not market_data:
            return "Unable to fetch current market data. Please try again later."
        
        analysis = "**🌍 Current Market Overview:**\n\n"
        
        total_market_cap = market_data.get('total_market_cap', 0)
        total_volume = market_data.get('total_volume', 0)
        market_change = market_data.get('market_cap_change_percentage_24h_usd', 0)
        btc_dominance = market_data.get('market_cap_percentage', {}).get('btc', 0)
        
        analysis += f"**Total Market Cap:** ${total_market_cap:.1f}B\n"
        analysis += f"**24h Volume:** ${total_volume:.1f}B\n"
        analysis += f"**24h Market Change:** {market_change:+.2f}%\n"
        analysis += f"**Bitcoin Dominance:** {btc_dominance:.1f}%\n\n"
        
        # Market sentiment analysis
        if market_change > 3:
            sentiment = "🟢 **Very Bullish** - Strong market optimism"
        elif market_change > 1:
            sentiment = "🟢 **Bullish** - Positive market sentiment"
        elif market_change > -1:
            sentiment = "🟡 **Neutral** - Balanced market conditions"
        elif market_change > -3:
            sentiment = "🟠 **Bearish** - Market showing caution"
        else:
            sentiment = "🔴 **Very Bearish** - Strong selling pressure"
        
        analysis += f"**Market Sentiment:** {sentiment}\n\n"
        
        # Bitcoin dominance analysis
        if btc_dominance > 50:
            btc_analysis = "Bitcoin maintains strong dominance - 'Bitcoin season'"
        elif btc_dominance > 40:
            btc_analysis = "Moderate Bitcoin dominance - balanced crypto market"
        else:
            btc_analysis = "Low Bitcoin dominance - 'Altcoin season' potential"
        
        analysis += f"**Dominance Analysis:** {btc_analysis}\n\n"
        
        # Investment implications
        analysis += "**Investment Implications:**\n"
        if market_change > 0:
            analysis += "- Positive momentum may continue in short term\n"
            analysis += "- Consider taking some profits if heavily invested\n"
            analysis += "- Good time for cost averaging if underinvested\n"
        else:
            analysis += "- Market correction may present buying opportunities\n"
            analysis += "- Focus on fundamentally strong projects\n"
            analysis += "- Consider increasing positions gradually\n"
        
        return analysis
    
    def _get_risk_management_advice(self):
        """Provide risk management guidance"""
        advice = "## ⚖️ Cryptocurrency Risk Management\n\n"
        
        advice += "**🛡️ Essential Risk Management Strategies:**\n\n"
        
        advice += "**1. Position Sizing**\n"
        advice += "- Never invest more than you can afford to lose completely\n"
        advice += "- Limit crypto to 5-30% of total portfolio (based on risk tolerance)\n"
        advice += "- Don't put more than 10% in any single cryptocurrency\n\n"
        
        advice += "**2. Diversification**\n"
        advice += "- Spread investments across multiple cryptocurrencies\n"
        advice += "- Include different types: store of value (BTC), platforms (ETH), etc.\n"
        advice += "- Consider geographic and regulatory diversification\n\n"
        
        advice += "**3. Entry and Exit Strategies**\n"
        advice += "- Use dollar-cost averaging for entries\n"
        advice += "- Set clear profit-taking levels\n"
        advice += "- Implement stop-losses for risk management\n"
        advice += "- Have a plan before you invest\n\n"
        
        advice += "**4. Emotional Control**\n"
        advice += "- Avoid FOMO (Fear of Missing Out)\n"
        advice += "- Don't panic sell during crashes\n"
        advice += "- Stick to your predetermined strategy\n"
        advice += "- Take breaks from charts and news\n\n"
        
        advice += "**5. Security Measures**\n"
        advice += "- Use reputable exchanges with insurance\n"
        advice += "- Enable two-factor authentication\n"
        advice += "- Consider hardware wallets for large amounts\n"
        advice += "- Never share private keys or seed phrases\n\n"
        
        advice += "**6. Regulatory Awareness**\n"
        advice += "- Understand tax implications in your jurisdiction\n"
        advice += "- Keep detailed transaction records\n"
        advice += "- Stay informed about regulatory changes\n"
        advice += "- Consider regulatory-compliant projects\n\n"
        
        advice += "**⚠️ Red Flags to Avoid:**\n"
        advice += "- Guaranteed returns or 'get rich quick' schemes\n"
        advice += "- Pressure to invest immediately\n"
        advice += "- Unlicensed or suspicious exchanges\n"
        advice += "- Projects with anonymous teams\n"
        advice += "- Excessive marketing hype without substance\n"
        
        return advice
    
    def _get_technical_analysis(self, crypto_id):
        """Get technical analysis for a cryptocurrency"""
        try:
            # Get historical data
            historical_data = self.analyzer.get_historical_data([crypto_id], 30)
            
            if not historical_data or crypto_id not in historical_data or not historical_data[crypto_id]:
                return "Unable to fetch price data for technical analysis."
            
            prices_data = historical_data[crypto_id].get('prices', [])
            if not prices_data:
                return "Insufficient price data for technical analysis."
            
            # Calculate technical indicators
            volatility = self.analyzer.calculate_volatility(prices_data)
            rsi = self.analyzer.calculate_rsi(prices_data)
            momentum_7d = self.analyzer.get_price_momentum(crypto_id, 7)
            momentum_30d = self.analyzer.get_price_momentum(crypto_id, 30)
            
            # Get current price
            current_price = prices_data[-1][1] if prices_data else 0
            price_7d_ago = prices_data[-7][1] if len(prices_data) >= 7 else current_price
            price_30d_ago = prices_data[0][1] if prices_data else current_price
            
            analysis = ""
            
            # Price levels
            prices = [price[1] for price in prices_data]
            high_30d = max(prices)
            low_30d = min(prices)
            
            analysis += f"**📊 Price Analysis (30 days):**\n"
            analysis += f"- Current Price: ${current_price:,.2f}\n"
            analysis += f"- 30-day High: ${high_30d:,.2f}\n"
            analysis += f"- 30-day Low: ${low_30d:,.2f}\n"
            analysis += f"- Price Range: {((current_price - low_30d) / (high_30d - low_30d) * 100):.1f}% of range\n\n"
            
            # Momentum analysis
            analysis += f"**📈 Momentum Indicators:**\n"
            analysis += f"- 7-day Momentum: {momentum_7d:+.2f}%\n"
            analysis += f"- 30-day Momentum: {momentum_30d:+.2f}%\n"
            analysis += f"- 30-day Volatility: {volatility:.1f}%\n\n"
            
            # RSI analysis
            analysis += f"**⚖️ RSI Analysis:**\n"
            analysis += f"- Current RSI: {rsi:.1f}\n"
            if rsi < 30:
                analysis += "- Signal: **OVERSOLD** - Potential buying opportunity\n"
            elif rsi > 70:
                analysis += "- Signal: **OVERBOUGHT** - Consider taking profits\n"
            else:
                analysis += "- Signal: **NEUTRAL** - No extreme conditions\n"
            
            analysis += "\n**🎯 Technical Signals:**\n"
            
            # Support and resistance levels
            resistance = high_30d * 0.95  # Near recent high
            support = low_30d * 1.05     # Near recent low
            
            analysis += f"- **Resistance Level:** ${resistance:,.2f}\n"
            analysis += f"- **Support Level:** ${support:,.2f}\n"
            
            # Overall technical outlook
            signals = []
            if rsi < 30:
                signals.append("Oversold condition (bullish)")
            elif rsi > 70:
                signals.append("Overbought condition (bearish)")
            
            if momentum_7d > 5:
                signals.append("Strong short-term momentum (bullish)")
            elif momentum_7d < -5:
                signals.append("Weak short-term momentum (bearish)")
            
            if volatility > 30:
                signals.append("High volatility (increased risk)")
            elif volatility < 15:
                signals.append("Low volatility (stable conditions)")
            
            if signals:
                analysis += f"\n**Key Signals:**\n"
                for signal in signals:
                    analysis += f"- {signal}\n"
            
            analysis += "\n**⚠️ Technical Analysis Disclaimer:** Technical analysis is not predictive and should be combined with fundamental analysis. Past performance does not guarantee future results."
            
            return analysis
            
        except Exception as e:
            return f"Error performing technical analysis: {str(e)}"
    
    def _get_general_sustainability_info(self):
        """Provide general information about cryptocurrency sustainability"""
        info = "**🌱 Cryptocurrency Sustainability Overview:**\n\n"
        
        info += "**Energy Consumption Concerns:**\n"
        info += "- Proof-of-Work cryptocurrencies (like Bitcoin) require significant energy\n"
        info += "- Mining operations contribute to carbon emissions\n"
        info += "- Environmental impact varies by energy source used\n\n"
        
        info += "**Sustainable Alternatives:**\n"
        info += "- **Proof-of-Stake (PoS)** - 99% less energy than PoW\n"
        info += "- Examples: Ethereum 2.0, Cardano, Polkadot, Solana\n"
        info += "- **Delegated Proof-of-Stake (DPoS)** - Even more efficient\n\n"
        
        info += "**🏆 Most Sustainable Cryptocurrencies:**\n"
        info += "1. **Cardano (ADA)** - Research-driven PoS blockchain\n"
        info += "2. **Polkadot (DOT)** - Interoperable PoS network\n"
        info += "3. **Solana (SOL)** - High-performance PoS blockchain\n"
        info += "4. **Algorand (ALGO)** - Carbon-negative blockchain\n"
        info += "5. **Ethereum (ETH)** - Transitioned to PoS in 2022\n\n"
        
        info += "**Sustainability Factors to Consider:**\n"
        info += "- **Consensus Mechanism** - PoS vs PoW energy usage\n"
        info += "- **Carbon Footprint** - Direct and indirect emissions\n"
        info += "- **Governance** - Environmental responsibility initiatives\n"
        info += "- **Innovation** - Green technology development\n"
        info += "- **Transparency** - Environmental impact reporting\n\n"
        
        info += "**Making Sustainable Choices:**\n"
        info += "- Prioritize PoS cryptocurrencies\n"
        info += "- Research projects' environmental initiatives\n"
        info += "- Consider carbon offset programs\n"
        info += "- Support renewable energy mining operations\n"
        
        return info
