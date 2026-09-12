from outils_analyse.fits import gaussian_fit, gaus, round_any
import matplotlib.pyplot as plt


"""
_______________________________________________________________________________________________________________
"""
# TODO: Copiez le code de l'analyse simple ici.





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





# Mettre les paramètres des fits gaussiens pour chaque pic en arrays de 3 éléments [Amplitude, Moyenne, STD]
peak1 = ...
peak2 = ...
peak3 = ...
peak4 = ...

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

# Mettre votre code ici
