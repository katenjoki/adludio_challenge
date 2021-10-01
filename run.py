from flask import Flask, render_template, request, jsonify
import pandas as pd
import sys

from werkzeug.utils import escape
sys.path.append('scripts')
from campaign import site_scores

app = Flask(__name__)
@app.route('/', methods = ('POST','GET'))

def home():
    output=None
    if request.method == 'POST':
        user_input = request.form.get('campaign')
        out = site_scores(user_input)
        output = pd.DataFrame(out)
    else:
        output = None
    
    return render_template('home.html',tables=[output.to_html(classes='data',escape=False)],titles=output.columns.values)
    #return render_template('home.html',outputs=output)
if __name__=='__main__':
    app.run(debug=True)