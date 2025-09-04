from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    columns = []
    summary = ""
    chart_data = {}

    if request.method == 'POST':
        file = request.files['csvfile']
        if file:
            df = pd.read_csv(file, parse_dates=['Date'])
            data = df.head().values.tolist()
            columns = df.columns.tolist()
            summary = df.select_dtypes(include=['number']).describe().to_html(classes="table table-striped table-bordered table-hover", border=0)


            # Grouped data for charts
            chart_data = {
                'product_labels': df['Product'].tolist(),
                'units_sold': df['Units Sold'].tolist(),
                'category_labels': df.groupby('Category')['Revenue'].sum().index.tolist(),
                'category_values': df.groupby('Category')['Revenue'].sum().values.tolist(),
                'region_labels': df.groupby('Region')['Revenue'].sum().index.tolist(),
                'region_values': df.groupby('Region')['Revenue'].sum().values.tolist(),
                'monthly_labels': df['Date'].dt.to_period('M').astype(str).unique().tolist(),
                'monthly_values': df.groupby(df['Date'].dt.to_period('M'))['Revenue'].sum().values.tolist()
            }

    return render_template(
        'index.html',
        data=data,
        columns=columns,
        summary=summary,
        chart_data=chart_data
    )

if __name__ == '__main__':
    app.run(debug=True)
