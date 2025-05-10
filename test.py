import pandas as pd
csv_file = "C:\\Users\\admin\\Desktop\\HsnCodeValidator-main\\HSN_SAC.csv"
hsn_df = pd.read_csv(csv_file)
print(hsn_df.head())

print("Master Data HSN Codes:", hsn_df['HSNCode'].tolist())
print("Uploaded File HSN Codes:", df['HSNCode'].tolist())