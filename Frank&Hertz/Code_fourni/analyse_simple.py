from outils_analyse.fits import gaussian_fit, gaus, round_any
from outils_analyse.identification_des_pics import get_peaks_indices
from outils_analyse.lecture_des_fichiers import read_csv, crop_ramp
from outils_analyse.conversion_temps_en_potentiel import compute_conversion_factors
import matplotlib.pyplot as plt
import os
import matplotlib

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





# Mettre vos valeurs extraites à la place de l'ellipse
data_array = ...  # Array de trois colonnes

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





# Mettre vos données rognées et remises à t_0=0 dans cette variable
data_cropped_and_shifted = ...  # Array de trois colonnes

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

# Mettre votre code ici





# Mettre vos données avec les bonnes unités et vos informations par rapport à la pente à la place des ellipses
data_converted = ...  # Array de trois colonnes
facteur_valeur = ...  # Nombre à virgule
facteur_incertitude = ...  # Nombre à virgule

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





# Mettre vos données avec les bonnes unités à la place du None
peak_indices_list = ...  # Liste de nombres entiers

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
