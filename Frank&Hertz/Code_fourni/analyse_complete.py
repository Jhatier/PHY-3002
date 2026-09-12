
from outils_analyse.fits import gaussian_fit, gaus, round_any
from outils_analyse.identification_des_pics import get_peaks_indices
from outils_analyse.lecture_des_fichiers import read_csv, crop_ramp
from outils_analyse.conversion_temps_en_potentiel import compute_conversion_factors
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sigfig as sig

matplotlib.rcParams.update({'font.size': 18})

# Indices des colonnes
time = 0
ramp = 1
pico = 2


"""
_______________________________________________________________________________________________________________
"""
# TODO: Copiez le code de l'analyse simple ici

"""
_______________________________________________________________________________________________________________
"""

# TODO: Lire le fichier de mesures et les mettre dans un array numpy

# Mettre votre code ici:

fichier = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "exemples_fichiers",
    "exemple_donnees.csv"
)

# Mettre vos valeurs extraites à la place de l'ellipse
data_array = read_csv(fichier, 10).astype(float)

"""
_______________________________________________________________________________________________________________
"""

# Ne pas modifier cette section

# La figure obtenue devrait correspondre à celle de figures_exemple/étape1
plt.figure()
plt.plot(data_array[:, time], data_array[:, pico], label="Tensions du pico")
plt.plot(data_array[:, time], data_array[:, ramp], label="Tensions entre la G1 et le ground")
plt.xlabel("Temps [s]")
plt.ylabel("Tension [V]")
plt.legend()
plt.show()

"""
_______________________________________________________________________________________________________________
"""

# TODO: 1. Rogner les valeurs pour ne conserver que celles correspondant à l'activation de la rampe de tension.
#       2. Décaler l'axe temporel pour que la première valeur soit à t=0 s.

# Mettre votre code ici

data_cropped_and_shifted = crop_ramp(
    data_array,
    ramp,
    zero_threshold=0.05,
    infinity_threshold=0.1
).copy()

data_cropped_and_shifted[:, time] -= data_cropped_and_shifted[0, time]

"""
_______________________________________________________________________________________________________________
"""

# Ne pas modifier cette section

# La figure obtenue devrait correspondre à celle de figures_exemple/étape2
plt.figure()
plt.plot(data_cropped_and_shifted[:, time], data_cropped_and_shifted[:, pico],
         label="Tensions du pico")
plt.plot(data_cropped_and_shifted[:, time], data_cropped_and_shifted[:, ramp],
         label="Tensions entre la G1 et le ground")
plt.xlabel("Temps [s]")
plt.ylabel("Tension [V]")
plt.legend()
plt.show()

"""
_______________________________________________________________________________________________________________
"""

# TODO: 1. Calculer la pente de la tension du générateur de rampe et son incertitude.
#       2. Convertir les valeurs de temps en valeurs de tension
#       3. Convertir la tension du pico en courant

facteur_valeur, facteur_incertitude = compute_conversion_factors(
    data_cropped_and_shifted,
    time,
    ramp
)

data_converted = data_cropped_and_shifted.copy()

data_converted[:, time] = (
    abs(facteur_valeur) * data_cropped_and_shifted[:, time]
)

data_converted[:, pico] *= 3.0
"""
_______________________________________________________________________________________________________________
"""

# Ne pas modifier cette section

print("Pente = ", f"{facteur_valeur} +- {facteur_incertitude}")

# La figure obtenue devrait correspondre à celle de figures_exemple/étape3
plt.figure()
plt.plot(data_converted[:, time], data_converted[:, pico],
         label="Courant du pico")
plt.xlabel("Tension entre G1 et le ground [V]")
plt.ylabel("Courant mesuré [nA]")
plt.legend()
plt.show()

"""
_______________________________________________________________________________________________________________
"""

# TODO: Déterminer l'emplacement approximatif des maximums

# Mettre votre code ici

pas_tension = np.median(np.diff(data_converted[:, time]))
distance = int(np.ceil(3.0 / pas_tension))

peak_indices_list = get_peaks_indices(
    data_converted,
    pico,
    hauteur_minimum=0.03,
    distance_minumum=distance
)

positions = data_converted[peak_indices_list, time]
V_res = np.mean(np.diff(positions))
W = positions[0] - V_res

print("Potentiel de résonance [V] :", V_res)
print("Potentiel de contact  [V] :", W)
"""
_______________________________________________________________________________________________________________
"""

# Ne pas modifier cette section

print("Estimation des pics:", data_converted[peak_indices_list, time])

# La figure obtenue devrait correspondre à celle de figures_exemple/étape4
plt.figure()
plt.plot(data_converted[:, time],
         data_converted[:, pico],
         label="Courant du pico")
plt.xlabel("Tension entre G1 et le ground [V]")
plt.scatter(data_converted[peak_indices_list, time],
            data_converted[peak_indices_list, pico],
            label="Estimation des pics")
plt.ylabel("Courant mesuré [nA]")
plt.legend()
plt.show()




"""
_______________________________________________________________________________________________________________
"""

# TODO: Faire une régression gaussienne sur chacun des pics et calculer le potentiel de contact.
#       Pour arrondir les valeurs selons leurs incertitudes, regardez la documentation de sigfig.
#       Les résultats devraient être similaires à :
#           Pic 1: Moyenne: 2.52 ± 0.02 STD: 0.85 ± 0.02 Amplitude: 0.069 ± 0.001
#           Pic 2: Moyenne: 7.42 ± 0.01 STD: 0.96 ± 0.01 Amplitude: 0.280 ± 0.003
#           Pic 3: Moyenne: 12.48 ± 0.01 STD: 1.15 ± 0.01 Amplitude: 0.558 ± 0.004
#           Pic 4: Moyenne: 17.653 ± 0.008 STD: 1.35 ± 0.01 Amplitude: 0.782 ± 0.003

# Mettre votre code ici





x = data_converted[:, time]
y = data_converted[:, pico]

# Séparer les pics aux minima entre deux maxima.
bornes = [0]

for gauche, droite in zip(peak_indices_list[:-1], peak_indices_list[1:]):
    minimum = gauche + np.argmin(y[gauche:droite + 1])
    bornes.append(minimum)

bornes.append(len(x) - 1)

# Ajuster chaque pic avec la fonction fournie.
fits = []

for i, indice in enumerate(peak_indices_list):
    debut = bornes[i]
    fin = bornes[i + 1] + 1

    fit = gaussian_fit(
        x[debut:fin],
        y[debut:fin],
        a_estimation=y[indice],
        mu_estimation=x[indice],
        sigma_estimation=1.0
    )

    fits.append(fit)

peak1, peak2, peak3, peak4 = fits

# Calculer l'espacement moyen à partir des centres ajustés.
positions = np.array([fit[0][1] for fit in fits])

V_res = np.mean(np.diff(positions))
W = positions[0] - V_res

print("Potentiel de résonance [V] :", V_res)
print("Potentiel de contact [V] :", W)

"""
_______________________________________________________________________________________________________________
"""

# Ne pas modifier cette section

def rounding_peaks(peaks):
    all_values = []
    for i in range(0, 3):
        all_values.append(round_any(peaks[0][i], uncertainty=peaks[1][i]))

    return all_values

print("Pic 1:", f"Moyenne: {rounding_peaks(peak1)[1]}",
      f"STD: {rounding_peaks(peak1)[2]}",
      f"Amplitude: {rounding_peaks(peak1)[0]}")
print("Pic 2:", f"Moyenne: {rounding_peaks(peak2)[1]}",
      f"STD: {rounding_peaks(peak2)[2]}",
      f"Amplitude: {rounding_peaks(peak2)[0]}")
print("Pic 3:", f"Moyenne: {rounding_peaks(peak3)[1]}",
      f"STD: {rounding_peaks(peak3)[2]}",
      f"Amplitude: {rounding_peaks(peak3)[0]}")
print("Pic 4:", f"Moyenne: {rounding_peaks(peak4)[1]}",
      f"STD: {rounding_peaks(peak4)[2]}",
      f"Amplitude: {rounding_peaks(peak4)[0]}")


"""
_______________________________________________________________________________________________________________
"""

# TODO: Faire un graphique qui contient l'ensemble des données de courants en fonction de la tension, les emplacements
#       approximatifs des maximums et les différents fits gaussiens effectués. Ça devrait ressembler à la figure
#       exemple_de_fichiers/étape5

plt.figure()

plt.plot(x, y, label="Courant mesuré")

plt.scatter(
    x[peak_indices_list],
    y[peak_indices_list],
    label="Estimation des pics"
)

for i, fit in enumerate(fits):
    tensions = np.linspace(
        x[bornes[i]],
        x[bornes[i + 1]],
        300
    )

    plt.plot(
        tensions,
        gaus(tensions, *fit[0]),
        label=f"Gaussienne {i + 1}"
    )

plt.xlabel("Tension entre G1 et le ground [V]")
plt.ylabel("Courant mesuré [nA]")
plt.legend()
plt.show()