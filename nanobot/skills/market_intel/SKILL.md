# MarketIntel Skill

TradingView + Real-Time Market Data + News Integration

## Overview

MarketIntel skill provides comprehensive market analysis by synthesizing TradingView chart data, real-time market metrics, and breaking news to generate actionable trade insights.

## Capabilities

### 📈 TradingView Integration
- Fetch OHLCV candlestick data (100-500 candles)
- Extract technical indicators: RSI, MACD, EMAs, VWAP, ATR
- Identify key support/resistance levels
- Analyze trend structure (HH/HL vs LH/LL)
- Detect momentum shifts and divergences

### 💹 Real-Time Market Data
- Current price + bid/ask spread
- 24h volume and percentage change
- Volatility proxy via ATR or realized vol
- Derivatives data: funding rate, open interest, liquidations (when available)

### 📰 News Aggregation
- Fetch top 5-15 headlines from last 24-72 hours
- Source: title, publish time, URL, relevance
- Flag high-impact events: CPI, FOMC, earnings, SEC actions
- Separate symbol-specific from macro news

## Usage

### Quick Bias
```
MarketIntel: BTCUSD, 1H, quick bias, symbol-only news
```

### Full Trade Plan
```
MarketIntel: AAPL, 15m, full trade plan, symbol + macro news
```

### Risk-Only Analysis
```
MarketIntel ETHUSDT, 4H, risk-only
```

### News Briefing
```
MarketIntel BTCUSD, 1H, news briefing
```

## Parameters

### Required
- `symbol`: Asset (BTCUSD, ETHUSDT, AAPL)
- `market_type`: crypto/forex/stocks
- `timeframe`: 1m/5m/15m/1h/4h/1D/1W

### Optional
- `exchange`: Binance, Coinbase, NYSE
- `session`: Timezone (default: America/Los_Angeles)
- `indicators`: RSI(14), MACD(12,26,9), EMA(20/50/200), VWAP, ATR(14)
- `news_scope`: symbol-only or symbol+macro
- `output_mode`: quick bias, full trade plan, risk-only, news briefing

## Data Sources

### TradingView
- Uses TradingView's lightweight chart API
- No API key required for basic data
- Fetches 100-500 candles based on timeframe

### Market Data
- Crypto: Binance, Coinbase public APIs
- Stocks: Yahoo Finance API
- Forex: Various public sources

### News
- Crypto: CoinDesk, CoinTelegraph, The Block
- Stocks: Benzinga, MarketWatch, Reuters
- Macro: Forexlive, DailyFX

## Dependencies

- requests
- pandas
- python-dateutil

## Installation

```bash
cd /Users/adam/Documents/Nanobot
uv pip install requests pandas python-dateutil
```

## Output Format

### 1. Snapshot (Now)
```
BTCUSD / Binance / 1H / 2025-02-21 14:35 PST
Price: $51,420 (+2.3%)
Volume: $28B (+15%)
Spread: $12
Volatility: ATR 340 (1.2%)
```

### 2. Technical Read
```
Trend: Bullish (Higher Highs, Higher Lows)
Key Levels:
  - Support: $50,200 (PDL), $49,800 (VWAP)
  - Resistance: $52,000 (PDH)
Indicators:
  - RSI: 61 (neutral)
  - MACD: Bullish crossover, histogram positive
  - EMA Stack: 20 > 50 > 200 (bullish)
Bias: Bullish with momentum
```

### 3. News & Catalysts
```
Headlines (12h):
- [Bloomberg] SEC delays spot ETF decision → Feb 21 13:45
  - Impact: Neutral, expected delay
  - Confidence: High
- [Forexlive] Fed hints at pause → Feb 21 12:30
  - Impact: Bullish for risk assets
  - Confidence: Medium

Upcoming: FOMC minutes tomorrow 14:00 EST (High Impact)
```

### 4. Trade Scenarios

**Bull Case:**
- Entry: Break above $52,000
- Target: $53,500-$54,000
- Invalidation: Close below $50,200

**Bear Case:**
- Entry: Break below $50,200
- Target: $48,800-$49,200
- Invalidation: Close above $52,500

**Chop Case:**
- Range: $50,200-$52,000
- Action: Wait for breakout, scalp edges
- Avoid: Chasing middle range

### 5. Risk Notes
- Confidence: Medium (mixed signals)
- Volatility: Elevated (3.2% intraday)
- Liquidity: Good (tight spreads)
- Invalidation: Break of $49,800 support

## Risk Management

**Always include:**
- Confidence level (Low/Med/High)
- Invalidation criteria
- Position sizing guidance
- Volatility warnings
- Liquidity notes

**Never present:**
- Guaranteed outcomes
- Financial advice as certainty

## Example Invocation

**User:** "MarketIntel for BTCUSD on 1H, full trade plan, symbol + macro news"

**Response structure:**
```
1) Snapshot: BTCUSD / Binance / 1H / 2025-02-21 14:35 PST
   Price $51,420 (+2.3%), Volume $28B, Spread $12, Vol ATR 340

2) Technical: Bullish (HH/HL), Support $50.2k, Resistance $52k
   RSI 61 neutral, MACD bullish, EMA stack bullish
   Bias: Bullish with momentum

3) News: 2 headlines, 1 macro (Fed pause), 1 symbol (ETF delay)
   Upcoming: FOMC minutes tomorrow (High Impact)

4) Scenarios: Bull (>$52k → $53.5k), Bear (<$50.2k → $49.2k)
   Chop: Range $50.2k-$52k

5) Risk: Confidence Medium, Vol Elevated 3.2%
   Invalidation: Break $49,8k
```

## Notes

- Data freshness: ~1-5 minute latency typical
- Timestamp: Always label with timezone
- Sources: Cite URLs, note publish times
- If data unavailable: State clearly and provide alternatives

**Vigilance Note:** Separate facts (data/news) from interpretation (analysis). Never present financial advice as guaranteed outcomes.

---

**Version:** 1.0.0  
**Status:** Production Ready  
**Category:** Financial Analysis
