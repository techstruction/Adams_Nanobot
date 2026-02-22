"""MarketIntel Skill - TradingView + Real-Time Data + News Integration"""

from .market_data import (
    analyze_market,
    get_quick_bias,
    get_full_plan,
    get_risk_assessment,
    get_news_briefing,
    market_intel
)

__all__ = [
    'analyze_market',
    'get_quick_bias',
    'get_full_plan',
    'get_risk_assessment',
    'get_news_briefing',
    'market_intel'
]

__version__ = "1.0.0"
__codename__ = "TradingViewPro"


# Note: Requires external APIs for full functionality
# Currently uses public endpoints and mock fallbacks
