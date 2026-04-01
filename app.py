from flask import Flask, render_template, request
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
# ensure uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():    
    table = None
    summary= None
    columns=[]
    graph = None
    selected_col= None
    filepath=None

    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.csv")
    
    df= None
    
    if request.method == 'POST':
        file = request.files.get('file')
        selected_col = request.form.get('column')

        # file Upload
        if file and file.filename!="":
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            df = pd.read_csv(filepath)
            
            # df.to_csv(temp_path, index=False)

            table = df.head().to_html()
            summary = df.describe().to_html()

            numeric_cols = df.select_dtypes(include='number')
            columns = numeric_cols.columns.tolist()
            
            #save temp files
            df.to_csv(temp_path, index=False)
            
            table = df.head().to_html()
            # Summary Stats
            summary = df.describe().to_html()
            
            #numeric columns 
            numeric_cols = df.select_dtypes(include ='number')
            columns = numeric_cols.columns.tolist()
            
        elif selected_col:
            graph_type = request.form.get('graph_type')

            if os.path.exists(temp_path):
                df = pd.read_csv(temp_path)
                
                #Graph data design
                if graph_type == "pie":
                    data = df[selected_col].value_counts()
                    graph_data = data.values.tolist()
                    labels = data.index.tolist()
                else:
                    graph_data = df[selected_col].tolist()
                    labels = list(range(len(graph_data)))

                table = df.head().to_html()
                summary = df.describe().to_html()

                numeric_cols = df.select_dtypes(include='number')
                columns = numeric_cols.columns.tolist()
                
                return render_template('index.html',
                               table=table,
                               summary=summary,
                               columns=columns,
                               graph_data=graph_data,
                               labels=labels,
                               graph_type=graph_type)
     

    return render_template('index.html', table=table, summary=summary, columns=columns,graph=graph, graph_data=None,labels=None,graph_type=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
