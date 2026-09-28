from nav_api.fetch import get_nav_history

df = get_nav_history("120503")

print(df.head())
print("\nRows:", len(df))