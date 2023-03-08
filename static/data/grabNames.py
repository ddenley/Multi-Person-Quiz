import pandas as pd

df = pd.read_csv("codes_names.csv")
df = df["name"]
df_list = df.to_list()
file = open('../../stt/phrases.txt', 'w')
for word in df_list:
	file.write(word + "\n")
file.close()
print(df_list)