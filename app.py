import os
from flask import (
    Flask,
    render_template,
    request
)

from predict import predict_image
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

#Prediction 
@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # Get uploaded file
    file = request.files["image"]

    if file.filename == "":

        return "No file selected."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    predictions = predict_image(
        filepath
    )

    #Best prediction
    pokemon_name = predictions[0][0]

    confidence = predictions[0][1]

    return render_template(
        "result.html",
        pokemon_name=pokemon_name,
        confidence=confidence,
        predictions=predictions,
        image_path=filepath
    )


#run app

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=7860
    )