import os


TELEGRAM_TOKEN = "xxxx"
PORT = int(os.environ.get("PORT", 5000))
CHAT_ID = "@imnotfuckingselling"
TEST_CHAT_ID = "@infstest"

INTRO = """
\U0001F916 A work-in-progress BOT that talks to the smart brains. \U0001F916
"""
HELP = """
Currently supported commands:

\U0001F315 \U0001F680 \U0001F680 Let's gooooooo \U0001F680 \U0001F680 \U0001F315

_You can also enter "/" or press the command button in the input area and select the command from the prompted list._

*/start* _Just an intro._
*/sopr* _Display BTC Spent Output Profit Ratio (SOPR) in the past 7 days._
*/btc* _Display BTC Top/Bottom Indicators._
*/btc_ex* _Display BTC On-Chain Exchange Activity._
*/eth_ex* _Display ETH On-Chain Exchange Activity._
*/glossary* _Terminology look up._
"""
GLOSSARY = """

*Net Unrealized Profit/Loss (NUPL)*
Net Unrealized Profit/Loss is the difference between Relative Unrealized Profit and Relative Unrealized Loss.
Any value above zero indicates that the network is in a state of net profit, while values below zero indicate a state of net loss.

In general, the further NUPL deviates from zero, the closer the market trends towards tops and bottoms. 
As such, NUPL can help investors identify when to take profit (blue) and when to re-enter (red). [-link](https://academy.glassnode.com/indicators/profit-loss-unrealized/net-unrealized-profit-loss)

*Stock-to-Flow Deflection*
The Stock to Flow (S/F) Ratio is a popular model that assumes that scarcity drives value. 
Stock to Flow is defined as the ratio of the current stock of a commodity (i.e. circulating Bitcoin supply) and the flow of new production (i.e. newly mined bitcoins). 
Bitcoin's price has historically followed the S/F Ratio and therefore it is a model that can be used to predict future Bitcoin valuations. This metric was first coined by PlanB.
If deflection is ≥ 1 it means that the asset is overvalued according to the S/F model. If deflection is <1, the asset is undervalued according to this model. [-link](https://academy.glassnode.com/indicators/stock-to-flow/stock-to-flow-deflection)

*MVRV Z-Score*
The MVRV Z-Score is used to assess when Bitcoin is over/undervalued relative to its "fair value". 
When market value is significantly higher than realized value, it has historically indicated a market top (red zone), while the opposite has indicated market bottoms (green zone). [-link](https://academy.glassnode.com/market/mvrv/mvrv-z-score)

*Puell Multiple*
The Puell Multiple examines the fundamentals of mining profitability and the way they shape market cycles. It is a ratio of daily coin issuance (in USD) and the 365 moving average of daily coin issuance.
This metric helps to gauge the market cycles from a mining profitability/compulsory sellers’ perspective. [-link](https://academy.glassnode.com/indicators/coin-issuance/puell-multiple)

*Reserve Risk*
Reserve Risk is used to assess the confidence of long-term holders relative to the price of the native coin at any given point in time. 
When confidence is high and price is low, there is an attractive risk/reward to invest (Reserve Risk is low). When confidence is low and price is high then risk/reward is unattractive at that time (Reserve Risk is high). [-link](https://academy.glassnode.com/indicators/coin-days-destroyed/reserve-risk)

*Stablecoin Supply Ratio (SSR)*
The Stablecoin Supply Ratio (SSR) is the ratio between Bitcoin supply and the supply of stablecoins, denominated in BTC.
When the SSR is low, the current stablecoin supply has more "buying power" to purchase BTC. It serves as a proxy for the supply/demand mechanics between BTC and USD. [-link](https://academy.glassnode.com/indicators/stablecoin/ssr-stablecoin-supply-ratio)

*Exchange Inflow Volume (Total)*
The total amount of coins transferred to exchange addresses.

*Exchange Outflow Volume (Total)*
The total amount of coins transferred from exchange addresses. 

*Exchange Balance (Total)*
The total amount of coins held on exchange addresses.
"""

SOPR = """
<pre>
Spent Output Profit Ratio (SOPR) in the past 7 days

{get_sopr}
</pre>
"""

DIGEST = """
*Metrics for {time} (UTC).*
_All the Glassnode metrics are generated using UTC timestamps._
"""
