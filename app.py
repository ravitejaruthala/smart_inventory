import streamlit as st
import pandas as pd

orders = pd.read_csv("orders.csv")
inventory = pd.read_csv("inventory.csv")

RECIPE_MAP = {
    "coffee": {"coffee_beans": 10, "milk": 50},
    "tea": {"tea_leaves": 5, "milk": 30},
    "sandwich": {"bread": 2, "cheese": 20}
}

st.title("☕ Smart Cafe Inventory Management")
st.subheader("Current Orders")
st.dataframe(orders)
used_inventory = {}
for _, row in orders.iterrows():
    item = row["item"]
    qty = row["quantity"]
    for ingredient, amount in RECIPE_MAP[item].items():
        used_inventory[ingredient] = used_inventory.get(ingredient, 0) + qty * amount
if st.button("Check Inventory"):
    st.subheader("Inventory Status")
    alerts = []
    for index, row in inventory.iterrows():
        ingredient = row["ingredient"]
        stock = row["stock"]
        threshold = row["threshold"]
        used = used_inventory.get(ingredient, 0)
        remaining = stock - used
        inventory.loc[index, "stock"] = remaining
        if remaining <= threshold:
            alerts.append((ingredient, remaining, row["supplier_email"]))
    st.dataframe(inventory)
    if alerts:
        st.warning("⚠ Inventory Below Threshold!")
        for ingredient, remaining, email in alerts:
            st.write(f"🔴 {ingredient}: {remaining} units left")
        if st.button("Inform Supplier"):
            st.write("HI")
            for ingredient, remaining, email in alerts:
                st.toast(f"📧 Order sent to {email} for {ingredient}")
    else:
        st.success("✅ Inventory levels are healthy!")
