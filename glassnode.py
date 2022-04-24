from datetime import date, datetime, timedelta

import pydf
import pandas as pd
from glassnode_client import GlassnodeClient

GN_API_KEY = "xxx"
gn = GlassnodeClient(api_key=GN_API_KEY)
DAYS = 7


def get_sopr():
    sopr = gn.get(
        "https://api.glassnode.com/v1/metrics/indicators/sopr",
        a="BTC",
        s=(date.today() - timedelta(days=DAYS)).strftime("%Y-%m-%d"),
        i="24h",
        in_df=False,
    )

    d = {
        "Date": [
            datetime.fromtimestamp(entry["t"]).strftime("%Y-%m-%d") for entry in sopr
        ],
        "Value": [entry["v"] for entry in sopr],
    }
    df = pd.DataFrame(data=d)

    return df.to_html(index=False)


def get_resource(uri, asset):
    rsp = gn.get(
        "https://api.glassnode.com/" + uri,
        a=asset,
        s=(date.today() - timedelta(days=DAYS)).strftime("%Y-%m-%d"),
        i="24h",
    )

    if "ssr" in uri:
        return (rsp[-1]["o"]["v"], rsp[-2]["o"]["v"], rsp[0]["o"]["v"])

    return (rsp[-1]["v"], rsp[-2]["v"], rsp[0]["v"])


def get_nupl():
    return get_resource("v1/metrics/indicators/net_unrealized_profit_loss", "BTC")


def get_s_to_f():
    return get_resource("v1/metrics/indicators/stock_to_flow_deflection", "BTC")


def get_mvrv_z():
    return get_resource("v1/metrics/market/mvrv_z_score", "BTC")


def get_puell():
    return get_resource("v1/metrics/indicators/puell_multiple", "BTC")


def get_reserve_risk():
    return get_resource("v1/metrics/indicators/reserve_risk", "BTC")


def get_ssr():
    return get_resource("v1/metrics/indicators/ssr", "BTC")


def get_ex_inflow_volume(asset="BTC"):
    return get_resource(
        "v1/metrics/transactions/transfers_volume_to_exchanges_sum", asset
    )


def get_ex_outflow_volume(asset="BTC"):
    return get_resource(
        "v1/metrics/transactions/transfers_volume_from_exchanges_sum", asset
    )


def get_ex_deposits(asset="BTC"):
    return get_resource("v1/metrics/transactions/transfers_to_exchanges_count", asset)


def get_ex_withdrawals(asset="BTC"):
    return get_resource("v1/metrics/transactions/transfers_from_exchanges_count", asset)


def get_ex_balance(asset="BTC"):
    return get_resource("v1/metrics/distribution/balance_exchanges", asset)


def get_btc_key_stats():
    nupl = get_nupl()
    s_to_f = get_s_to_f()
    mvrz_z = get_mvrv_z()
    puell = get_puell()
    reserve_risk = get_reserve_risk()
    ssr = get_ssr()

    last_value = [nupl[0], s_to_f[0], mvrz_z[0], puell[0], reserve_risk[0], ssr[0]]

    one_day_change = [
        get_change(nupl[1], nupl[0]),
        get_change(s_to_f[1], s_to_f[0]),
        get_change(mvrz_z[1], mvrz_z[0]),
        get_change(puell[1], puell[0]),
        get_change(reserve_risk[1], reserve_risk[0]),
        get_change(ssr[1], ssr[0]),
    ]
    seven_days_change = [
        get_change(nupl[2], nupl[0]),
        get_change(s_to_f[2], s_to_f[0]),
        get_change(mvrz_z[2], mvrz_z[0]),
        get_change(puell[2], puell[0]),
        get_change(reserve_risk[2], reserve_risk[0]),
        get_change(ssr[2], ssr[0]),
    ]
    d = {
        "Metric": [
            "NUPL",
            "Stock-to-Flow Deflection",
            "MVRV Z-Score",
            "Puell Multiple",
            "Reserve Risk",
            "SSR",
        ],
        "Value": last_value,
        "Changes (1D)": one_day_change,
        "Changes (7D)": seven_days_change,
    }
    df = pd.DataFrame(data=d)

    return df.to_html(index=False)


def get_btc_ex_activity():
    return get_ex_activity("BTC")


def get_eth_ex_activity():
    return get_ex_activity("ETH")


def get_ex_activity(asset="BTC"):
    ex_inflow = get_ex_inflow_volume(asset)
    ex_outflow = get_ex_outflow_volume(asset)
    ex_balance = get_ex_balance(asset)

    last_value = [
        f"{'{:,.2f}'.format(ex_inflow[0])} {asset}",
        f"{'{:,.2f}'.format(ex_outflow[0])} {asset}",
        f"{'{:,.2f}'.format(ex_balance[0])} {asset}",
    ]

    one_day_change = [
        get_change(ex_inflow[1], ex_inflow[0]),
        get_change(ex_outflow[1], ex_outflow[0]),
        get_change(ex_balance[1], ex_balance[0]),
    ]
    seven_days_change = [
        get_change(ex_inflow[2], ex_inflow[0]),
        get_change(ex_outflow[2], ex_outflow[0]),
        get_change(ex_balance[2], ex_balance[0]),
    ]
    d = {
        "Metric": [
            "Exchange Inflow Volume (Total)",
            "Exchange Outflow Volume (Total)",
            "Exchange Balance (Total)",
        ],
        "Value": last_value,
        "Changes (1D)": one_day_change,
        "Changes (7D)": seven_days_change,
    }

    pd.set_option("display.float_format", lambda x: "%.2f" % x)
    df = pd.DataFrame(data=d)

    return df.to_html(index=False)


def get_change(base, latest):
    return "{:.2%}".format((latest - base) / base)


if __name__ == "__main__":
    # print(get_ex_activity())
    pdf = pydf.generate_pdf(get_ex_activity(), zoom=2.5)
    with open("sopr.pdf", "wb") as f:
        f.write(pdf)
