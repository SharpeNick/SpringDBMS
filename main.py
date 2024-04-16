from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Database Configuration
DATABASE_CONFIG = {
    'host': 'Mysql@localhost:3306',
    'user': 'root',
    'password': '1234',
    'database': 'NotSureYet',
}

def connect_db():
    return pymysql.connect(**DATABASE_CONFIG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/insert_shipment_s2p3")
def insert_shipment_s2p3():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO SHIPMENT (Sno, Pno, Qty, Price) VALUES ('s2', 'p3', 200, 0.006)")
        conn.commit()
        result = "Success"
    except:
        conn.rollback()
        result = "Fail"
    conn.close()
    return render_template("result.html", result=result)

@app.route("/insert_shipment_s4p2")
def insert_shipment_s4p2():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO SHIPMENT (Sno, Pno, Qty, Price) VALUES ('s4', 'p2', 100, 0.005)")
        conn.commit()
        result = "Success"
    except:
        conn.rollback()
        result = "Fail"
    conn.close()
    return render_template("result.html", result=result)

@app.route("/increase_supplier_status")
def increase_supplier_status():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE SUPPLIER SET Status = Status * 1.1")
    conn.commit()
    conn.close()
    return redirect(url_for("display_all_suppliers"))

@app.route("/display_all_suppliers")
def display_all_suppliers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SUPPLIER")
    suppliers = cursor.fetchall()
    conn.close()
    return render_template("display_suppliers.html", suppliers=suppliers)

@app.route("/supplier_info_by_part", methods=["GET", "POST"])
def supplier_info_by_part():
    if request.method == "POST":
        part_no = request.form["part_no"]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SUPPLIER WHERE Sno IN (SELECT Sno FROM SHIPMENT WHERE Pno = %s)", (part_no,))
        suppliers = cursor.fetchall()
        conn.close()
        return render_template("display_suppliers.html", suppliers=suppliers)
    return render_template("supplier_part_input.html")

if __name__ == "__main__":
    app.run(debug=True)
