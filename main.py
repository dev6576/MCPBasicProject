# server.py
from mcp.server.fastmcp import FastMCP

# In-memory portfolio storage
portfolio = {}

# Create MCP server
mcp = FastMCP("PortfolioManager")


# ----------------------------
# TOOL: Add asset to portfolio
# ----------------------------
@mcp.tool()
def add_asset(symbol: str, quantity: float, price: float) -> str:
    """Add or update an asset in the portfolio"""
    if symbol in portfolio:
        portfolio[symbol]["quantity"] += quantity
        portfolio[symbol]["price"] = price  # Update to latest price
    else:
        portfolio[symbol] = {"quantity": quantity, "price": price}
    return f"Added {quantity} of {symbol} at ${price}."


# ----------------------------
# TOOL: Remove asset
# ----------------------------
@mcp.tool()
def remove_asset(symbol: str) -> str:
    """Remove an asset from the portfolio"""
    if symbol in portfolio:
        del portfolio[symbol]
        return f"Removed {symbol} from portfolio."
    return f"{symbol} not found in portfolio."


# ----------------------------
# TOOL: List all assets
# ----------------------------
@mcp.tool()
def list_assets() -> dict:
    """List all assets in the portfolio"""
    return portfolio


# --------------------------------------------
# RESOURCE: Summary endpoint
# --------------------------------------------
@mcp.resource("portfolio://summary")
def get_portfolio_summary() -> str:
    """Get total portfolio value summary"""
    if not portfolio:
        return "Portfolio is empty."
    total_value = sum(asset["quantity"] * asset["price"] for asset in portfolio.values())
    return f"Portfolio contains {len(portfolio)} assets worth ${total_value:.2f}."
