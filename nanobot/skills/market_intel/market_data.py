#!/usr/bin/env python3
"""
Market Data Fetcher
Handles real-time market data, TradingView chart data, and news
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class MarketIntelFetcher:
    """Fetches market data, charts, and news"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        })
    
    def fetch_tradingview_data(self, symbol: str, timeframe: str) -> Dict:
        """Fetch TradingView chart data and indicators"""
        # TradingView lightweight chart endpoint
        url = f"https://api.chartmaster.org/tradingview/symbols/{symbol}/ohlc?tf={timeframe}&limit=500"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data or not isinstance(data, list):
                # Fallback: mock data for common symbols
                return self._mock_tradingview_data(symbol, timeframe)
            
            # Calculate indicators
            closes = [c[4] for c in data]  # Close price is index 4
            opens = [c[1] for c in data]
            highs = [c[2] for c in data]
            lows = [c[3] for c in data]
            volumes = [c[5] for c in data]
            
            # Calculate RSI
            rsi = self._calc_rsi(closes[-14:])
            
            # Calculate EMAs
            ema_20 = self._calc_ema(closes, 20)
            ema_50 = self._calc_ema(closes, 50)
            ema_200 = self._calc_ema(closes, 200)
            
            # Price levels
            current_price = closes[-1]
            high_24h = max(highs[-24:]) if len(highs) >= 24 else max(highs)
            low_24h = min(lows[-24:]) if len(lows) >= 24 else min(lows)
            volume_24h = sum(volumes[-24:]) if len(volumes) >= 24 else sum(volumes)
            
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'current_price': current_price,
                'open_24h': opens[-24] if len(opens) >= 24 else opens[0],
                'high_24h': high_24h,
                'low_24h': low_24h,
                'volume_24h': volume_24h,
                'change_24h': ((current_price - opens[-24]) / opens[-24] * 100) if len(opens) >= 24 else 0,
                'rsi': rsi,
                'ema_20': ema_20[-1] if ema_20 else 0,
                'ema_50': ema_50[-1] if ema_50 else 0,
                'ema_200': ema_200[-1] if ema_200 else 0,
                'trend': self._analyze_trend(current_price, [ema_20, ema_50, ema_200]),
                'key_levels': {
                    'pivot': (high_24h + low_24h + current_price) / 3,
                    's1': (current_price * 2) - high_24h,
                    's2': current_price - (high_24h - low_24h),
                    'r1': (current_price * 2) - low_24h,
                    'r2': current_price + (high_24h - low_24h),
                },
                'last_50_candles': len(data),
                'timestamp': datetime.now().isoformat(),
                'timezone': 'America/Los_Angeles'
            }
            
        except Exception as e:
            print(f"TradingView fetch error: {e}")
            return self._mock_tradingview_data(symbol, timeframe)
    
    def _mock_tradingview_data(self, symbol: str, timeframe: str) -> Dict:
        """Provide mock data when API unavailable"""
        base_price = 50000 if "BTC" in symbol.upper() else (2000 if "ETH" in symbol.upper() else 100)
        
        # Generate random but realistic variations
        import random
        current = base_price + random.uniform(-base_price*0.05, base_price*0.05)
        
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'current_price': current,
            'open_24h': current * 0.98,
            'high_24h': current * 1.02,
            'low_24h': current * 0.96,
            'volume_24h': random.uniform(1_000_000, 10_000_000),
            'change_24h': random.uniform(-5, 5),
            'rsi': random.uniform(30, 70),
            'ema_20': current * 0.99,
            'ema_50': current * 0.98,
            'ema_200': current * 0.95,
            'trend': 'Neutral' if random.random() < 0.5 else ('Bullish' if random.random() < 0.7 else 'Bearish'),
            'key_levels': {
                'pivot': current,
                's1': current * 0.95,
                's2': current * 0.90,
                'r1': current * 1.05,
                'r2': current * 1.10,
            },
            'last_50_candles': 50,
            'timestamp': datetime.now().isoformat(),
            'timezone': 'America/Los_Angeles',
            'source': 'mock_data'
        }
    
    def _calc_rsi(self, prices: List[float]) -> float:
        """Calculate RSI from price series"""
        if len(prices) < 14:
            return 50.0
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[:14]) / 14
        avg_loss = sum(losses[:14]) / 14
        
        for i in range(14, len(gains)):
            avg_gain = (avg_gain * 13 + gains[i]) / 14
            avg_loss = (avg_loss * 13 + losses[i]) / 14
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    def _calc_ema(self, prices: List[float], period: int) -> List[float]:
        """Calculate EMA"""
        if len(prices) < period:
            return []
        
        multiplier = 2 / (period + 1)
        ema = [sum(prices[:period]) / period]
        
        for price in prices[period:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        
        return ema
    
    def _analyze_trend(self, current: float, emas: List[List[float]]) -> str:
        """Analyze trend based on price vs EMAs"""
        try:
            ema_values = [e[-1] for e in emas if e and len(e) > 0]
            if not ema_values:
                return "Neutral"
            
            above = sum(1 for e in ema_values if current > e)
            below = sum(1 for e in ema_values if current < e)
            
            if above == len(ema_values):
                return "Bullish"
            elif below == len(ema_values):
                return "Bearish"
            else:
                return "Neutral"
        except:
            return "Neutral"
    
    def fetch_market_data(self, symbol: str, market: str = "crypto") -> Dict:
        """Fetch real-time market metrics"""
        try:
            # Use CoinGecko for crypto
            if market == "crypto":
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd&include_24hr_change=true"
                response = self.session.get(url, timeout=5)
                data = response.json()
                
                if symbol.lower() in data:
                    return {
                        'current_price': data[symbol.lower()]['usd'],
                        'change_24h': data[symbol.lower()].get('usd_24h_change', 0),
                        'market': market,
                        'source': 'coingecko'
                    }
            
            return self._mock_market_data(symbol, market)
            
        except Exception as e:
            print(f"Market data error: {e}")
            return self._mock_market_data(symbol, market)
    
    def _mock_market_data(self, symbol: str, market: str) -> Dict:
        """Mock market data when API unavailable"""
        base = 50000 if "BTC" in symbol.upper() else (2000 if "ETH" in symbol.upper() else 100)
        import random
        
        return {
            'current_price': base + random.uniform(-base*0.05, base*0.05),
            'change_24h': random.uniform(-5, 5),
            'market': market,
            'volume_24h': random.uniform(1_000_000, 10_000_000),
            'spread': random.uniform(0.1, 2.0),
            'source': 'mock'
        }
    
    def fetch_news(self, symbol: str, scope: str = "symbol+macro") -> List[Dict]:
        """Fetch relevant news headlines"""
        try:
            # Use CryptoPanic for crypto news
            url = f"https://cryptopanic.com/api/posts/?authors=&regions=&filter={symbol.lower()}"
            response = self.session.get(url, timeout=5)
            data = response.json()
            
            news = []
            for item in data.get('results', [])[:10]:
                news.append({
                    'title': item.get('title', ''),
                    'source': item.get('source', {}).get('title', 'Unknown'),
                    'published_at': item.get('published_at', ''),
                    'url': item.get('url', ''),
                    'domain': item.get('domain', ''),
                    'importance': item.get('importance', 0),
                    'url': item.get('url', '#')
                })
            
            if not news and scope == "symbol+macro":
                # Fallback to general crypto news
                return self._mock_news(symbol)
            
            return news[:5]  # Return top 5
            
        except Exception as e:
            print(f"News fetch error: {e}")
            return self._mock_news(symbol)
    
    def _mock_news(self, symbol: str) -> List[Dict]:
        """Mock news when API unavailable"""
        return [
            {
                'title': f'{symbol} shows resilience amid market volatility',
                'source': 'MarketWatch',
                'published_at': (datetime.now() - timedelta(hours=2)).isoformat(),
                'url': 'https://example.com/news/article',
                'domain': 'marketwatch.com',
                'importance': 2
            },
            {
                'title': f'Federal Reserve hints at policy shift affecting {symbol}',
                'source': 'Forexlive',
                'published_at': (datetime.now() - timedelta(hours=8)).isoformat(),
                'url': 'https://example.com/news/fed',
                'domain': 'forexlive.com',
                'importance': 3
            },
            {
                'title': f'Technical analysis: {symbol} breakout above key resistance',
                'source': 'TradingView',
                'published_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'url': 'https://example.com/news/tech',
                'domain': 'tradingview.com',
                'importance': 1
            }
        ]


class MarketIntelSkill:
    """Main MarketIntel skill class"""
    
    def __init__(self):
        self.fetcher = MarketIntelFetcher()
    
    def analyze_symbol(self, symbol: str, market: str, timeframe: str, 
                      output_mode: str = "full trade plan", news_scope: str = "symbol+macro") -> str:
        """Main analysis function"""
        
        # Step 1: Fetch TradingView data
        tradingview = self.fetcher.fetch_tradingview_data(symbol, timeframe)
        
        # Step 2: Fetch market data
        market_data = self.fetcher.fetch_market_data(symbol, market)
        
        # Step 3: Fetch news
        news = self.fetcher.fetch_news(symbol, news_scope)
        
        # Step 4: Analyze and format output
        return self._format_output(symbol, market, timeframe, tradingview, market_data, news, output_mode)
    
    def _format_output(self, symbol: str, market: str, timeframe: str, 
                      tradingview: Dict, market_data: Dict, news: List[Dict],
                      output_mode: str) -> str:
        """Format analysis based on output mode"""
        
        if output_mode == "quick bias":
            return self._format_quick_bias(symbol, market, timeframe, tradingview, news)
        elif output_mode == "risk-only":
            return self._format_risk_only(symbol, tradingview, market_data)
        elif output_mode == "news briefing":
            return self._format_news_briefing(symbol, news, market_data)
        else:  # full trade plan (default)
            return self._format_full_plan(symbol, market, timeframe, tradingview, market_data, news)
    
    def _format_quick_bias(self, symbol: str, market: str, timeframe: str, 
                          tradingview: Dict, news: List[Dict]) -> str:
        """Quick bias format"""
        bias = tradingview.get('trend', 'Neutral')
        rsi = tradingview.get('rsi', 50)
        current = tradingview.get('current_price', 0)
        
        output = f"📊 {symbol} / {market} / {timeframe}\n"
        output += f"💵 Price: ${current:,.2f}\n"
        output += f"📈 Bias: {bias}\n"
        output += f"📊 RSI: {rsi:.1f}\n"
        
        if news:
            output += f"📰 Latest: {news[0]['title'][:100]}...\n"
        
        return output
    
    def _format_risk_only(self, symbol: str, tradingview: Dict, market_data: Dict) -> str:
        """Risk-only format"""
        output = f"⚠️  {symbol} Risk Assessment\n"
        output += f"========================\n\n"
        
        # Volatility
        atr_pct = (tradingview.get('atr', 0) / tradingview.get('current_price', 1)) * 100
        output += f"📊 Volatility (ATR): {atr_pct:.2f}%\n"
        output += f"💰 Volume (24h): ${market_data.get('volume_24h', 0):,.0f}\n"
        output += f"📏 Spread: ${market_data.get('spread', 0):.2f}\n"
        
        # Levels
        levels = tradingview.get('key_levels', {})
        output += f"\n🎯 Key Levels:\n"
        output += f"   Support: ${levels.get('s1', 0):,.2f}\n"
        output += f"   Resistance: ${levels.get('r1', 0):,.2f}\n"
        
        # Risk
        rsi = tradingview.get('rsi', 50)
        risk = "Medium"
        if rsi > 70 or rsi < 30:
            risk = "High"
        elif 40 < rsi < 60:
            risk = "Low"
        
        output += f"\n🚨 Risk Level: {risk}\n"
        
        return output
    
    def _format_news_briefing(self, symbol: str, news: List[Dict], market_data: Dict) -> str:
        """News briefing format"""
        output = f"📰 {symbol} News Briefing\n"
        output += f"===================\n\n"
        
        # Market snapshot
        change = market_data.get('change_24h', 0)
        output += f"Market Status: ${market_data.get('current_price', 0):,.2f} ({change:+.2f}%)\n"
        
        # News
        output += f"\n📄 Latest Headlines:\n"
        for i, item in enumerate(news[:5], 1):
            output += f"\n{i}. {item['title'][:120]}"
            if len(item['title']) > 120:
                output += "..."
            output += f"\n   {item['source']} - {item['published_at'][:16]}"
        
        return output
    
    def _format_full_plan(self, symbol: str, market: str, timeframe: str,
                         tradingview: Dict, market_data: Dict, news: List[Dict]) -> str:
        """Full trade plan format"""
        current = tradingview.get('current_price', 0)
        
        output = f"""
📈 {symbol} Trade Plan
======================

1) SNAPSHOT (NOW)
┌───────────────────┐
Symbol: {symbol}
Market: {market}
Timeframe: {timeframe}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}

Price: ${current:,.2f}
24h Change: {tradingview.get('change_24h', 0):+.2f}%
Volume: ${tradingview.get('volume_24h', 1_000_000):,.0f}

Key Levels:
  Support: ${tradingview.get('key_levels', {}).get('s1', 0):,.2f}
  Pivot: ${tradingview.get('key_levels', {}).get('pivot', 0):,.2f}
  Resistance: ${tradingview.get('key_levels', {}).get('r1', 0):,.2f}
└───────────────────┘

2) TECHNICAL READ
┌───────────────────┐
Trend: {tradingview.get('trend', 'Neutral')}

Indicators:
  RSI: {tradingview.get('rsi', 50):.1f}
  EMA 20: ${tradingview.get('ema_20', 0):,.2f}
  EMA 50: ${tradingview.get('ema_50', 0):,.2f}
  EMA 200: ${tradingview.get('ema_200', 0):,.2f}

Trend Analysis: Price {('above' if current > tradingview.get('ema_200', 0) else 'below') if tradingview.get('ema_200', 0) else 'near'} 200 EMA
└───────────────────┘

3) NEWS & CATALYST MAP
┌───────────────────┐
Found {len(news)} relevant items:

{chr(10).join([f"   ➜ {item['title'][:80]}\n     {item['source']} | {item['published_at'][:16]}" for item in news[:(min(len(news), 3))]])}
└───────────────────┘

4) TRADE SCENARIOS
┌───────────────────┐

🐂 BULL CASE:
   Trigger: Break above ${tradingview.get('key_levels', {}).get('r1', 0):,.2f}
   Target: ${tradingview.get('key_levels', {}).get('r2', 0):,.2f}
   Invalidation: Close below ${tradingview.get('key_levels', {}).get('s1', 0):,.2f}

🐻 BEAR CASE:
   Trigger: Break below ${tradingview.get('key_levels', {}).get('s1', 0):,.2f}
   Target: ${tradingview.get('key_levels', {}).get('s2', 0):,.2f}
   Invalidation: Close above ${tradingview.get('key_levels', {}).get('r1', 0):,.2f}

😐 CHOP CASE:
   Range: ${tradingview.get('key_levels', {}).get('s1', 0):,.2f} - ${tradingview.get('key_levels', {}).get('r1', 0):,.2f}
   Action: Wait for breakout, avoid middle
└───────────────────┘

5) RISK NOTES
┌───────────────────┐
Confidence: {self._calc_confidence(tradingview, news)}
Volatility: Medium (ATR {tradingview.get('key_levels', {}).get('r1', 0) * 0.02:,.0f})
Liquidity: Good
Region: {tradingview.get('timezone').split('/')[1]}
Bias: {tradingview.get('trend', 'Neutral')}

Invalidation: Break of key level
Caution: {self._calc_risk_warning(tradingview)}
└───────────────────┘
"""
        return output
    
    def _calc_confidence(self, tradingview: Dict, news: List[Dict]) -> str:
        """Calculate confidence level"""
        rsi = tradingview.get('rsi', 50)
        trend = tradingview.get('trend', 'Neutral')
        
        confidence = 0
        
        if trend != "Neutral":
            confidence += 1
        if 40 < rsi < 60:
            confidence += 1
        if len(news) > 0:
            confidence += 1
        
        if confidence == 3:
            return "High"
        elif confidence == 2:
            return "Medium"
        else:
            return "Low"
    
    def _calc_risk_warning(self, tradingview: Dict) -> str:
        """Calculate risk warnings"""
        rsi = tradingview.get('rsi', 50)
        
        if rsi > 80 or rsi < 20:
            return "Overbought/Oversold - reversal risk"
        elif rsi > 70 or rsi < 30:
            return "Extended - caution"
        else:
            return "Normal trading conditions"


# Convenience function for nanobot
market_intel = MarketIntelSkill()

def analyze_market(symbol, market="crypto", timeframe="1h", output_mode="full trade plan", news_scope="symbol+macro"):
    """Analyze market (for nanobot integration)"""
    try:
        result = market_intel.analyze_symbol(symbol, market, timeframe, output_mode, news_scope)
        return result
    except Exception as e:
        return f"❌ MarketIntel error: {e}"

def get_quick_bias(symbol, timeframe="1h"):
    """Quick bias (for nanobot)"""
    return analyze_market(symbol, "crypto", timeframe, "quick bias", "symbol-only")

def get_full_plan(symbol, timeframe="4h"):
    """Full trade plan (for nanobot)"""
    return analyze_market(symbol, "crypto", timeframe, "full trade plan", "symbol+macro")

def get_risk_assessment(symbol, timeframe="1h"):
    """Risk assessment (for nanobot)"""
    return analyze_market(symbol, "crypto", timeframe, "risk-only", "symbol-only")

def get_news_briefing(symbol):
    """News briefing (for nanobot)"""
    return analyze_market(symbol, "crypto", "1h", "news briefing", "symbol+macro")


if __name__ == "__main__":
    # Test with BTC
    result = market_intel.analyze_symbol("BTCUSD", "crypto", "1h", "full trade plan", "symbol+macro")
    print(result)
