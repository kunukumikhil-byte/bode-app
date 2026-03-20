import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    plot = None
    fc = None

    if request.method == "POST":
        # Get values
        R_value = float(request.form["R_value"])
        R_power = int(request.form["R_power"])
        C_value = float(request.form["C_value"])
        C_power = int(request.form["C_power"])

        # Convert to actual values
        R = R_value * (10 ** R_power)
        C = C_value * (10 ** C_power)

        # Cutoff frequency
        fc = 1 / (2 * np.pi * R * C)

        # Frequency range
        w = np.logspace(0, 5, 500)
        H = 1 / (1 + 1j * w * R * C)

        mag = 20 * np.log10(abs(H))
        phase = np.angle(H, deg=True)

        # Plot graph
        plt.figure(figsize=(6,5))

        plt.subplot(2,1,1)
        plt.semilogx(w, mag)
        plt.ylabel("Magnitude (dB)")
        plt.title("Bode Plot")
        plt.grid()

        plt.subplot(2,1,2)
        plt.semilogx(w, phase)
        plt.ylabel("Phase (°)")
        plt.xlabel("Frequency (rad/s)")
        plt.grid()

        plt.tight_layout()
        plot = "static/plot.png"
        plt.savefig(plot)
        plt.close()

    return render_template("index.html", plot=plot, fc=fc)

if __name__ == "__main__":
    app.run(debug=True)