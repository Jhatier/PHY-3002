from outils_analyse.fits import gaussian_fit, gaus, round_any
from outils_analyse.identification_des_pics import get_peaks_indices
from outils_analyse.lecture_des_fichiers import read_csv, crop_ramp
from outils_analyse.conversion_temps_en_potentiel import compute_conversion_factors
import matplotlib.pyplot as plt
import os
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
