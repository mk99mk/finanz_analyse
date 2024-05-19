from pathlib import Path
import dateutil
import datetime
import time
import pandas as pd
from io import StringIO
from langchain_community.llms import Ollama

from pydantic import BaseModel

from finanz_analyse.config import DATA

class IndexRecognition(BaseModel):
    date: str
    amount: str
    recipient: str
    description: str

llm = Ollama(model="llama3")

def identify_columns(sliced_data: pd.DataFrame, labels: list[str]):
    global llm
    while True:
        try:
            resp = llm.invoke("Identify the columns from this csv of transactions,"
                                " which represent the data: date, amount, recipient, description."
                                "Your answer should contain the following json "
                                '{"date": "data_header", "amount": "amount_header",'
                                ' "recipient": "recipient_header", "description": "description_header"},'
                                " where ..._header corresponds to the column name in the csv."
                                f"\n'{sliced_data}'")
            print('resp ', resp)
            json_start = resp.find('{')
            json_end = resp.find('}')
            json_resp = resp[json_start: json_end + 1]
            result = IndexRecognition.model_validate_json(json_resp)
            if result.date in labels and result.amount in labels \
                and result.recipient in labels and result.description in labels:
                return result
        except Exception as e:
            print("ERROR ", e)
            pass

def add(name: str, path: Path, day_first: bool = True):
    new_data = pd.read_csv(path)
    new_labels = new_data.columns
    with StringIO() as output:
        new_data[:7].to_csv(output)
        sliced_data = output.getvalue()
    
    column_id = identify_columns(sliced_data, new_labels)

    bank_file = DATA / f"{name}.csv"
    data = pd.read_csv(bank_file) if bank_file.exists() else pd.DataFrame(columns=['date', 'amount', 'recipient', 'description'])
    mapping = {
        column_id.date: "date",
        column_id.amount: "amount",
        column_id.recipient: "recipient",
        column_id.description: "description"
    }
    new_data = new_data.rename(columns=mapping)
    new_data['date'] = new_data['date'].map(lambda v: dateutil.parser.parse(v, dayfirst=day_first))
    new_data['amount'] = new_data['amount'].map(lambda v: float(v.replace(',', '.')))
    full_data = pd.concat([data, new_data], join="inner")
    full_data.drop_duplicates(subset=['date', 'amount', 'recipient'])
    full_data = full_data.reset_index(drop=True)
    full_data.to_csv(bank_file)

def load(name: str):
    bank_file = DATA / f"{name}.csv"
    data = pd.read_csv(bank_file)
    data['date'] = data['date'].map(lambda v: dateutil.parser.parse(v).date())
    data = data.drop(columns=['Unnamed: 0'])
    data = data.reset_index(drop=True)
    return data
