from flask import Flask,render_template,request
import pickle
import pandas as pd
df=pd.read_csv("Processed.csv")

app = Flask(__name__)

model=pickle.load(open('Model.pkl','rb'))

@app.route('/',methods=['GET'])
def home():
    locations=sorted(df["location"].unique())
    return render_template('index.html',locations=locations)

@app.route("/predict",methods=['POST'])
def predict():
    if request.method == "POST":
        Location = request.form["Location"]
        total_sqft = float(request.form["total_sqft"])
        bath = float(request.form["bath"])
        balcony = float(request.form["balcony"])
        bhk = float(request.form["bhk"])

        inp=pd.DataFrame([[Location,total_sqft,bath,balcony,bhk]],columns=["location","total_sqft","bath","balcony","bhk"])
        prediction=model.predict(inp)

        ans=prediction[0]
        ans=round(ans,2)

        if ans>0:
            return render_template("index.html",prediction_text="Price in L:{}".format(ans))
        else:
            return render_template("index.html",prediction_text="Cannot be sold")
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
