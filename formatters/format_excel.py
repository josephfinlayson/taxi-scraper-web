import pandas as pds
from io import BytesIO

def getData(metas):
    return [({'supplier': 'myTaxi',
              'id': meta['id'],
              'price': meta['price'],
              'to': meta['to'],
              'from': meta['from'],
              'date': meta['date'].isoformat()}) for meta in metas]

def format_excel(metas):
    output = BytesIO()
    data = getData(metas)
    df = pds.DataFrame(data)

    df = df.drop_duplicates(subset='id')
    df = df.sort_values('date')

    writer = pds.ExcelWriter(output, engine="xlsxwriter")

    df.to_excel(writer, 'Sheet1', columns=['supplier', 'price', 'date', 'to', 'from'])

    writer.save()
    output.seek(0)
    return output.getvalue()
    # return excelWriter

