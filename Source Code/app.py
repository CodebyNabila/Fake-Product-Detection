from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from index import BlockChain
import json

app = Flask(__name__)
app.secret_key = "replace_with_secret_key"  # Change this for security


# ---------------- USER HELPER FUNCTIONS ----------------
def load_users():
    """Load users from users.json"""
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_users(users):
    """Save users to users.json"""
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)


# ---------------- ROUTES ----------------
@app.route("/")
def welcome():
    """Landing page (index.html with Admin & Register buttons)"""
    return render_template("index.html")


@app.route("/home")
def home():
    """Dashboard page - only if logged in"""
    if "user" in session:
        return render_template('home.html')
    else:
        flash("Please login to access Verifier")
        return redirect(url_for('login'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        users = load_users()

        if username in users:
            return jsonify({"error": "Username already exists. Please choose a different username."})

        # Add the new user
        users[username] = {"password": password, "email": email}
        save_users(users)

        flash("Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        if username in users and users[username]["password"] == password:
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid login details", "danger")
            return redirect(url_for("login"))

    return render_template('login.html')


@app.route("/verify/<kid>", methods=["GET"])
def verify(kid):
    return render_template('verify.html', keyId=kid)


@app.route("/verify", methods=["POST"])
def success():
    post_data = request.form["keyId"]

    with open('./NODES/N1/blockchain.json', 'r') as bfile:
        n1_data = str(bfile.read())
    with open('./NODES/N2/blockchain.json', 'r') as bfile:
        n2_data = str(bfile.read())
    with open('./NODES/N3/blockchain.json', 'r') as bfile:
        n3_data = str(bfile.read())
    with open('./NODES/N4/blockchain.json', 'r') as bfile:
        n4_data = str(bfile.read())

    if (post_data in n1_data) and (post_data in n2_data) and (post_data in n3_data) and (post_data in n4_data):
        with open('./NODES/N1/blockchain.json', 'r') as bfile:
            for x in bfile:
                if post_data in x:
                    a = json.loads(x)["data"]
                    b = a.replace("'", "\"")
                    data = json.loads(b)

                    return render_template(
                        'success.html',
                        brand=data["Manufacturer"],
                        name=data["ProductName"],
                        batch=data["ProductBatch"],
                        manfdate=data["ProductManufacturedDate"],
                        exprydate=data["ProductExpiryDate"],
                        id=data["ProductId"],
                        price=data["ProductPrice"],
                        size=data["ProductSize"],
                        type=data["ProductType"]
                    )
    else:
        return render_template('fraud.html', message="Fake Product")


@app.route("/addproduct", methods=["POST", "GET"])
def addproduct():
    if request.method == "POST":
        brand = request.form["brand"]
        name = request.form["name"]
        batch = request.form["batch"]
        pid = request.form["id"]
        manfdate = request.form["manfdate"]
        exprydate = request.form["exprydate"]
        price = request.form["price"]
        size = request.form["size"]
        ptype = request.form["type"]

        bc = BlockChain()
        bc.addProduct(brand, name, batch, manfdate, exprydate, pid, price, size, ptype)

        flash("Product added successfully to the Blockchain")
        return redirect(url_for('home'))

    return redirect(url_for('home'))


@app.route("/admin")
def admin():
    if session.get("user") == "Admin":
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))


@app.route("/verifyNodes")
def verifyNodes():
    bc = BlockChain()
    isBV = bc.isBlockchainValid()

    if isBV:
        flash("All Nodes of Blockchain are valid")
    else:
        flash("Blockchain Nodes are not valid")
    return redirect(url_for('admin'))


@app.route("/medicine")
def medicine():
    return render_template('MedicinePage.html')


@app.route("/fertilizer")
def fertilizer():
    return render_template('FertilizersPage.html')


@app.route("/shoes")
def shoes():
    return render_template('ShoesPage.html')


@app.route("/wine")
def wine():
    return render_template('WinePage.html')


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
