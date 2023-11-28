from comcrawl import IndexClient
import pandas as pd

client = IndexClient()

client.search("https://properm.ru/news")


client.results = (pd.DataFrame(client.results)
                  .sort_values(by="timestamp")
                  .drop_duplicates("urlkey", keep="last")
                  .to_dict("records"))

#first_page_html = client.results[0]["html"]
client.download()
pd.DataFrame(client.results).to_csv("results.csv")

#print(first_page_html)