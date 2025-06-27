import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import time

class CryptoAnalyzer:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.cache_duration = 300  # 5 minutes cache
        self.last_cache_time = {}
        self.cache = {}
    
    def _get_cached_data(self, cache_key):
        """Get cached data if still valid"""
        if cache_key in self.cache and cache_key in self.last_cache_time:
            if time.time() - self.last_cache_time[cache_key] < self.cache_duration:
                return self.cache[cache_key]
        return None
    
    def _set_cached_data(self, cache_key, data):
        """Cache data with timestamp"""
        self.cache[cache_key] = data
        self.last_cache_time[cache_key] = time.time()
    
    def _make_request(self, endpoint, params=None):
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def get_market_overview(self):
        """Get overall market statistics"""
        cache_key = "market_overview"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        data = self._make_request("global")
        if data and 'data' in data:
            market_data = data['data']
            result = {
                'total_market_cap': market_data.get('total_market_cap', {}).get('usd', 0) / 1e9,  # Convert to billions
                'total_volume': market_data.get('total_volume', {}).get('usd', 0) / 1e9,  # Convert to billions
                'market_cap_percentage': market_data.get('market_cap_percentage', {}),
                'market_cap_change_percentage_24h_usd': market_data.get('market_cap_change_percentage_24h_usd', 0)
            }
            self._set_cached_data(cache_key, result)
            return result
        return None
    
    def get_top_cryptocurrencies(self, limit=10):
        """Get top cryptocurrencies by market cap"""
        cache_key = f"top_cryptos_{limit}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h,7d,30d'
        }
        
        data = self._make_request("coins/markets", params)
        if data:
            self._set_cached_data(cache_key, data)
            return data
        return []
    
    def get_cryptocurrency_data(self, crypto_id):
        """Get detailed data for a specific cryptocurrency"""
        cache_key = f"crypto_data_{crypto_id}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        params = {
            'localization': False,
            'tickers': False,
            'market_data': True,
            'community_data': True,
            'developer_data': True
        }
        
        data = self._make_request(f"coins/{crypto_id}", params)
        if data:
            self._set_cached_data(cache_key, data)
            return data
        return None
    
    def get_historical_data(self, crypto_ids, days=30):
        """Get historical price data for cryptocurrencies"""
        historical_data = {}
        
        for crypto_id in crypto_ids:
            cache_key = f"historical_{crypto_id}_{days}"
            cached_data = self._get_cached_data(cache_key)
            
            if cached_data:
                historical_data[crypto_id] = cached_data
                continue
            
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily' if days > 1 else 'hourly'
            }
            
            data = self._make_request(f"coins/{crypto_id}/market_chart", params)
            if data:
                historical_data[crypto_id] = data
                self._set_cached_data(cache_key, data)
            else:
                historical_data[crypto_id] = None
        
        return historical_data
    
    def get_market_trends(self):
        """Get current market trends"""
        cache_key = "market_trends"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # Get global market data
        global_data = self._make_request("global")
        if global_data and 'data' in global_data:
            result = global_data['data']
            self._set_cached_data(cache_key, result)
            return result
        return None
    
    def get_trending_coins(self):
        """Get trending cryptocurrencies"""
        cache_key = "trending_coins"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        data = self._make_request("search/trending")
        if data and 'coins' in data:
            trending_coins = [coin['item'] for coin in data['coins']]
            self._set_cached_data(cache_key, trending_coins)
            return trending_coins
        return []
    
    def get_sustainability_data(self):
        """Get data relevant for sustainability analysis"""
        # This is a placeholder for sustainability-related data
        # In a real implementation, this would fetch data about energy consumption,
        # consensus mechanisms, etc.
        cache_key = "sustainability_data"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # For now, return basic data structure
        sustainability_data = {
            'energy_efficient_cryptos': ['cardano', 'polkadot', 'solana', 'algorand'],
            'proof_of_stake_cryptos': ['ethereum', 'cardano', 'polkadot', 'solana'],
            'high_energy_cryptos': ['bitcoin', 'litecoin', 'dogecoin']
        }
        
        self._set_cached_data(cache_key, sustainability_data)
        return sustainability_data
    
    def calculate_volatility(self, prices):
        """Calculate price volatility"""
        if not prices or len(prices) < 2:
            return 0
        
        price_changes = []
        for i in range(1, len(prices)):
            if prices[i-1][1] != 0:  # Avoid division by zero
                change = (prices[i][1] - prices[i-1][1]) / prices[i-1][1]
                price_changes.append(change)
        
        if not price_changes:
            return 0
        
        return np.std(price_changes) * 100  # Return as percentage
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        if not prices or len(prices) < period + 1:
            return 50  # Neutral RSI
        
        price_values = [price[1] for price in prices]
        
        gains = []
        losses = []
        
        for i in range(1, len(price_values)):
            change = price_values[i] - price_values[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def get_price_momentum(self, crypto_id, days=7):
        """Calculate price momentum over specified days"""
        historical_data = self.get_historical_data([crypto_id], days)
        
        if not historical_data or crypto_id not in historical_data:
            return 0
        
        data = historical_data[crypto_id]
        if not data or 'prices' not in data or len(data['prices']) < 2:
            return 0
        
        prices = data['prices']
        start_price = prices[0][1]
        end_price = prices[-1][1]
        
        if start_price == 0:
            return 0
        
        momentum = ((end_price - start_price) / start_price) * 100
        return momentum
