#This will utilize the GPT model to analyze the financial statements
from openai import OpenAI
from grabFinStmt import grabFinStmts
import pandas as pd

client = OpenAI()
MODEL = "gpt-4-turbo"

infodump = grabFinStmts("TSLA")

inc_stmt_string = pd.DataFrame.from_dict(infodump[0], orient='index').to_string()
bal_sheet_string = pd.DataFrame.from_dict(infodump[1], orient='index').to_string()
cf_stmt_string = pd.DataFrame.from_dict(infodump[2], orient='index').to_string()
stmt_sh_eqy_string = pd.DataFrame.from_dict(infodump[3], orient='index').to_string()

completion = client.chat.completions.create(
	model=MODEL,
	messages=[
		{"role": "system", "content": "You are a financial analyst and your sole task is to analyze the financial documents in detail and provide all relevant analyses, no matter the verbosity."},
		{"role": "user", "content": inc_stmt_string},
        {"role": "user", "content": bal_sheet_string},
        {"role": "user", "content": cf_stmt_string},
        {"role": "user", "content": stmt_sh_eqy_string}
	],
    seed=0,
    temperature=0
)

print(completion.choices[0].message.content)