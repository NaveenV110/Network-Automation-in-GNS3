from flask import Flask, render_template, request, redirect, url_for, flash
from netmiko import ConnectHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# Define your GNS3 router inventory
routers = {
    "R1": {"device_type": "cisco_ios", "host": "10.1.1.2", "username": "cisco", "password": "cisco123"},
    "R2": {"device_type": "cisco_ios", "host": "192.168.0.1", "username": "nancy", "password": "drew123"},
    "R3": {"device_type": "cisco_ios", "host": "10.1.1.3", "username": "cisco", "password": "cisco123"},
    "R4": {"device_type": "cisco_ios", "host": "10.1.1.5", "username": "kratos", "password": "god123"}
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        device_name = request.form.get("device")
        command = request.form.get("command")
        
        if device_name and command:
            try:
                device = routers[device_name]
                connection = ConnectHandler(**device)
                output = connection.send_command(command)
                connection.disconnect()
                return render_template("result.html", output=output, command=command, device=device_name)
            except Exception as e:
                flash(f"Error: {str(e)}")
                return redirect(url_for("index"))
        else:
            flash("Please select a device and enter a command.")
            return redirect(url_for("index"))
    
    return render_template("index.html", routers=routers)

if __name__ == "__main__":
    app.run(debug=True)