from flask import Flask, render_template, request, redirect
from predict import predict_image
import os
import requests

app = Flask(__name__)

def get_pokemon_info(name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")

        if response.status_code == 200:
            data = response.json()
            pokemon_image = data["sprites"][
                "other"
            ]["official-artwork"][
                "front_default"
            ]

            pokemon_id = data["id"]
            pokemon_types = ", ".join([t["type"]["name"].title()
                    for t in data["types"]])
            species_url = data["species"]["url"]
            species_response = requests.get(
                species_url
            )
            species_data = species_response.json()
            description = (
                "No Pokédex description available."
            )
            for entry in species_data[
                "flavor_text_entries"
            ]:
                if (
                    entry["language"]["name"]
                    == "en"
                ):
                    description = (
                        entry["flavor_text"]
                        .replace("\n", " ")
                        .replace("\f", " ")
                    )
                    break
            return (
                pokemon_image,
                pokemon_id,
                pokemon_types,
                description
            )

    except Exception as e:
        print(
            f"Error fetching Pokémon info: {e}"
        )
    return (
        None,
        "???",
        "Unknown",
        "Description unavailable."
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict",methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return redirect("/")
    print("prediction route hit!", flush=True)
    if "image" not in request.files:
        return redirect("/")
    file = request.files["image"]
    if file.filename == "":
        return redirect("/")

    prediction, confidence, top5 = (predict_image(file))
    print("Prediction compelted")
    (
        pokemon_image,
        pokemon_id,
        pokemon_types,
        description
    ) = get_pokemon_info(prediction)

    return render_template(
        "result.html",
        prediction=prediction,
        confidence=confidence,
        top5=top5,
        pokemon_image=pokemon_image,
        pokemon_id=pokemon_id,
        pokemon_types=pokemon_types,
        description=description
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)