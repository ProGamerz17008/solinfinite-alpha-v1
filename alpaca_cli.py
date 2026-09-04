#!/usr/bin/env python3
"""
SOLINFINITE ALPHA V1 - ALPACA CLI UTILITY
Structured JSON CLI for Long-Running AI Agent Sessions, Cron Jobs & CI/CD Pipelines.
"""

import sys
import json
import argparse
from datetime import datetime

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
    ALPACA_SDK_AVAILABLE = True
except ImportError:
    ALPACA_SDK_AVAILABLE = False

DEFAULT_API_KEY = "PK4EAUYBC7UG5NXBR23MAZZWYN"
DEFAULT_SECRET_KEY = "J4eBjKpKWWHvcq8ebpoEemPmWRw6pnmRHwzcBXXEhZ4g"

def get_client(key=None, secret=None):
    k = key or DEFAULT_API_KEY
    s = secret or DEFAULT_SECRET_KEY
    if ALPACA_SDK_AVAILABLE:
        try:
            return TradingClient(k, s, paper=True)
        except Exception as e:
            return None
    return None

def cmd_account(args):
    client = get_client(args.key, args.secret)
    if not client:
        print(json.dumps({"error": "Alpaca SDK not installed or invalid credentials"}))
        return
    try:
        acc = client.get_account()
        res = {
            "id": str(acc.id),
            "status": str(acc.status),
            "currency": str(acc.currency),
            "equity": float(acc.equity),
            "cash": float(acc.cash),
            "buying_power": float(acc.buying_power),
            "options_buying_power": float(getattr(acc, 'options_buying_power', acc.buying_power)),
            "pattern_day_trader": acc.pattern_day_trader,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_positions(args):
    client = get_client(args.key, args.secret)
    if not client:
        print(json.dumps({"error": "Alpaca SDK not installed or invalid credentials"}))
        return
    try:
        raw_pos = client.get_all_positions()
        positions = []
        for p in raw_pos:
            positions.append({
                "symbol": p.symbol,
                "qty": float(p.qty),
                "market_value": float(p.market_value),
                "cost_basis": float(p.cost_basis),
                "unrealized_pl": float(p.unrealized_pl),
                "unrealized_plpc": float(p.unrealized_plpc) * 100,
                "side": str(p.side),
                "current_price": float(p.current_price)
            })
        print(json.dumps({"success": True, "positions": positions, "count": len(positions)}, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_trade(args):
    client = get_client(args.key, args.secret)
    if not client:
        print(json.dumps({"error": "Alpaca SDK not installed or invalid credentials"}))
        return
    try:
        sym = args.symbol.upper().strip()
        is_crypto = "/" in sym or sym in ["BTCUSD", "ETHUSD", "SOLUSD"]
        if "BTC" in sym and not "/" in sym: sym = "BTC/USD"
        elif "ETH" in sym and not "/" in sym: sym = "ETH/USD"
        elif "SOL" in sym and not "/" in sym: sym = "SOL/USD"

        side_val = OrderSide.BUY if args.side.upper() == "BUY" else OrderSide.SELL
        order_qty = float(args.qty)

        req = MarketOrderRequest(
            symbol=sym,
            qty=order_qty,
            side=side_val,
            time_in_force=TimeInForce.GTC if "/" in sym else TimeInForce.DAY
        )
        placed = client.submit_order(req)
        res = {
            "success": True,
            "order_id": str(placed.id),
            "symbol": placed.symbol,
            "qty": order_qty,
            "side": args.side.upper(),
            "status": str(placed.status),
            "submitted_at": datetime.now().isoformat()
        }
        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def main():
    parser = argparse.ArgumentParser(description="Alpaca CLI Utility for AI Agents & Cron Jobs")
    parser.add_argument("--key", type=str, help="Alpaca Paper API Key")
    parser.add_argument("--secret", type=str, help="Alpaca Paper Secret Key")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("account", help="Get Alpaca Paper Account summary")
    subparsers.add_parser("positions", help="List active paper positions")

    trade_p = subparsers.add_parser("trade", help="Submit paper trade order")
    trade_p.add_argument("--symbol", type=str, required=True, help="Ticker symbol e.g. SPY or BTC/USD")
    trade_p.add_argument("--side", type=str, choices=["BUY", "SELL", "buy", "sell"], default="BUY", help="Order side")
    trade_p.add_argument("--qty", type=float, default=1.0, help="Order quantity")

    args = parser.parse_args()

    if args.command == "account":
        cmd_account(args)
    elif args.command == "positions":
        cmd_positions(args)
    elif args.command == "trade":
        cmd_trade(args)

if __name__ == "__main__":
    main()
