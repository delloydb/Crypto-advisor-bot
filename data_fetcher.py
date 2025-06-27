import requests
import time
import streamlit as st
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoAdvisor/1.0'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests
        
        # Cache settings
        self.cache = {}
        self.cache_expiry = {}
        self.default_cache_duration = 300  # 5 minutes
    
    def _respect_rate_limit(self):
        """Ensure we don't exceed API rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _is_cache_valid(self, cache_key):
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        if cache_key not in self.cache_expiry:
            return False
        
        return time.time() < self.cache_expiry[cache_key]
    
    def _get_from_cache(self, cache_key):
        """Get data from cache if valid"""
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        return None
    
    def _store_in_cache(self, cache_key, data, cache_duration=None):
        """Store data in cache"""
        if cache_duration is None:
            cache_duration = self.default_cache_duration
        
        self.cache[cache_key] = data
        self.cache_expiry[cache_key] = time.time() + cache_duration
    
    def _make_request(self, endpoint, params=None, cache_key=None, cache_duration=None):
        """Make API request with caching and error handling"""
        # Check cache first
        if cache_key:
            cached_data = self._get_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        # Make the request
        try:
            self._respect_rate_limit()
            
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, params=params, timeout=15)
            
            # Check for rate limiting
            if response.status_code == 429:
                st.warning("API rate limit reached. Please wait a moment and try again.")
                return None
            
            response.raise_for_status()
            data = response.json()
            
            # Store in cache
            if cache_key:
                self._store_in_cache(cache_key, data, cache_duration)
            
            return data
            
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please check your internet connection and try again.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to the cryptocurrency data service. Please try again later.")
            return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                st.error("Cryptocurrency not found. Please check the name and try again.")
            else:
                st.error(f"API error: {response.status_code}. Please try again later.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}. Please try again later.")
            return None
        except ValueError as e:
            st.error("Invalid response from API. Please try again later.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}. Please try again later.")
            return None
    
    def get_coin_list(self):
        """Get list of all available cryptocurrencies"""
        cache_key = "coin_list"
        return self._make_request(
            "coins/list",
            cache_key=cache_key,
            cache_duration=3600  # Cache for 1 hour
        )
    
    def get_global_data(self):
        """Get global cryptocurrency market data"""
        cache_key = "global_data"
        return self._make_request(
            "global",
            cache_key=cache_key,
            cache_duration=300  # Cache for 5 minutes
        )
    
    def get_coins_markets(self, vs_currency='usd', order='market_cap_desc', 
                         per_page=100, page=1, sparkline=False, 
                         price_change_percentage='24h'):
        """Get market data for cryptocurrencies"""
        params = {
            'vs_currency': vs_currency,
            'order': order,
            'per_page': per_page,
            'page': page,
            'sparkline': sparkline,
            'price_change_percentage': price_change_percentage
        }
        
        cache_key = f"markets_{vs_currency}_{order}_{per_page}_{page}"
        return self._make_request(
            "coins/markets",
            params=params,
            cache_key=cache_key,
            cache_duration=300  # Cache for 5 minutes
        )
    
    def get_coin_data(self, coin_id, localization=False, tickers=False, 
                     market_data=True, community_data=True, developer_data=True):
        """Get detailed data for a specific cryptocurrency"""
        params = {
            'localization': str(localization).lower(),
            'tickers': str(tickers).lower(),
            'market_data': str(market_data).lower(),
            'community_data': str(community_data).lower(),
            'developer_data': str(developer_data).lower()
        }
        
        cache_key = f"coin_data_{coin_id}"
        return self._make_request(
            f"coins/{coin_id}",
            params=params,
            cache_key=cache_key,
            cache_duration=600  # Cache for 10 minutes
        )
    
    def get_coin_history(self, coin_id, date, localization=False):
        """Get historical data for a specific date"""
        params = {
            'date': date,
            'localization': str(localization).lower()
        }
        
        cache_key = f"coin_history_{coin_id}_{date}"
        return self._make_request(
            f"coins/{coin_id}/history",
            params=params,
            cache_key=cache_key,
            cache_duration=3600  # Cache for 1 hour
        )
    
    def get_coin_market_chart(self, coin_id, vs_currency='usd', days=30, interval='daily'):
        """Get market chart data (price, market cap, volume)"""
        params = {
            'vs_currency': vs_currency,
            'days': days,
            'interval': interval
        }
        
        cache_key = f"market_chart_{coin_id}_{vs_currency}_{days}_{interval}"
        cache_duration = 300 if days <= 1 else 600  # Shorter cache for recent data
        
        return self._make_request(
            f"coins/{coin_id}/market_chart",
            params=params,
            cache_key=cache_key,
            cache_duration=cache_duration
        )
    
    def get_coin_market_chart_range(self, coin_id, vs_currency='usd', 
                                   from_timestamp=None, to_timestamp=None):
        """Get market chart data for a specific time range"""
        if not from_timestamp or not to_timestamp:
            # Default to last 30 days
            to_timestamp = int(time.time())
            from_timestamp = to_timestamp - (30 * 24 * 60 * 60)
        
        params = {
            'vs_currency': vs_currency,
            'from': from_timestamp,
            'to': to_timestamp
        }
        
        cache_key = f"market_chart_range_{coin_id}_{vs_currency}_{from_timestamp}_{to_timestamp}"
        return self._make_request(
            f"coins/{coin_id}/market_chart/range",
            params=params,
            cache_key=cache_key,
            cache_duration=600  # Cache for 10 minutes
        )
    
    def get_trending_coins(self):
        """Get trending cryptocurrencies"""
        cache_key = "trending_coins"
        return self._make_request(
            "search/trending",
            cache_key=cache_key,
            cache_duration=300  # Cache for 5 minutes
        )
    
    def search_coins(self, query):
        """Search for cryptocurrencies by name or symbol"""
        params = {'query': query}
        
        # Don't cache search results as they're query-specific
        return self._make_request(
            "search",
            params=params
        )
    
    def get_exchanges(self):
        """Get list of cryptocurrency exchanges"""
        cache_key = "exchanges"
        return self._make_request(
            "exchanges",
            cache_key=cache_key,
            cache_duration=3600  # Cache for 1 hour
        )
    
    def get_exchange_rates(self):
        """Get BTC exchange rates"""
        cache_key = "exchange_rates"
        return self._make_request(
            "exchange_rates",
            cache_key=cache_key,
            cache_duration=300  # Cache for 5 minutes
        )
    
    def get_simple_price(self, ids, vs_currencies='usd', include_market_cap=False,
                        include_24hr_vol=False, include_24hr_change=False):
        """Get simple price data for cryptocurrencies"""
        if isinstance(ids, list):
            ids = ','.join(ids)
        if isinstance(vs_currencies, list):
            vs_currencies = ','.join(vs_currencies)
        
        params = {
            'ids': ids,
            'vs_currencies': vs_currencies,
            'include_market_cap': str(include_market_cap).lower(),
            'include_24hr_vol': str(include_24hr_vol).lower(),
            'include_24hr_change': str(include_24hr_change).lower()
        }
        
        cache_key = f"simple_price_{ids}_{vs_currencies}"
        return self._make_request(
            "simple/price",
            params=params,
            cache_key=cache_key,
            cache_duration=60  # Cache for 1 minute (more frequent updates)
        )
    
    def ping(self):
        """Ping the API to check connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/ping", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.cache_expiry.clear()
        st.success("Cache cleared successfully!")
    
    def get_cache_stats(self):
        """Get cache statistics"""
        total_items = len(self.cache)
        valid_items = sum(1 for key in self.cache if self._is_cache_valid(key))
        expired_items = total_items - valid_items
        
        return {
            'total_items': total_items,
            'valid_items': valid_items,
            'expired_items': expired_items
        }
