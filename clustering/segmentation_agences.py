# -*- coding: utf-8 -*-
"""
Segmentation des agences BTK par apprentissage non supervisé (clustering).

Pipeline :
  1. Chargement des données (CSV réel si présent, sinon jeu de démonstration réaliste).
  2. Standardisation des variables.
  3. Détermination du nombre de clusters : méthode du coude + score de silhouette.
  4. Comparaison de plusieurs modèles : K-Means, Agglomératif, GMM, DBSCAN.
  5. Sélection du meilleur modèle (silhouette) et profilage des clusters.
  6. Génération des figures et des résultats pour le rapport.

Pour utiliser VOS données : exportez les vues V_BI_* agrégées par agence dans
   clustering/data/agences.csv
avec les colonnes : agence, effectif, nb_gestionnaires, nb_clients,
   total_comptes, production_credits, collecte_epargne, taux_presence
Le script les utilisera automatiquement à la place du jeu de démonstration.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (silhouette_score, davies_bouldin_score,
                             calinski_harabasz_score)
from sklearn.decomposition import PCA

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)
BLUE, CYAN, GREEN, AMBER, RED = "#14507A", "#00AEEF", "#00d2ad", "#ffbc4b", "#ff5e57"
PALETTE = [CYAN, AMBER, GREEN, RED, "#6c5ce7", "#0057B8"]
FEATURES = ["effectif", "nb_gestionnaires", "nb_clients", "total_comptes",
            "production_credits", "collecte_epargne", "taux_presence"]

plt.rcParams.update({"figure.dpi": 150, "font.size": 10, "axes.edgecolor": "#888",
                     "axes.grid": True, "grid.color": "#e6e6e6"})


# --------------------------------------------------------------------------
def charger_donnees():
    """Charge le CSV réel s'il existe, sinon génère un jeu de démonstration."""
    csv = os.path.join(HERE, "data", "agences.csv")
    if os.path.exists(csv):
        df = pd.read_csv(csv)
        print(f"[data] Données réelles chargées : {csv} ({len(df)} agences)")
        return df, False
    print("[data] Aucun CSV réel — génération d'un jeu de démonstration réaliste.")
    rng = np.random.default_rng(42)
    # 3 profils latents : grandes / moyennes / petites agences
    groupes = [("grande", 7, 115, 12), ("moyenne", 16, 56, 8), ("petite", 22, 23, 4)]
    lignes = []
    idx = 1
    for nom, n, mu, sd in groupes:
        for _ in range(n):
            eff = max(5, rng.normal(mu, sd))
            lignes.append({
                "agence": f"Agence {idx:02d}",
                "effectif": round(eff),
                "nb_gestionnaires": round(eff * rng.uniform(0.27, 0.33)),
                "nb_clients": round(eff * rng.normal(8, 0.9)),
                "total_comptes": round(eff * rng.normal(20, 2.2)),
                "production_credits": round(eff * rng.normal(15, 1.8), 1),
                "collecte_epargne": round(eff * rng.normal(10, 1.4), 1),
                "taux_presence": round(np.clip(rng.normal(0.91 if nom != "petite" else 0.84, 0.035), 0.6, 1.0), 3),
            })
            idx += 1
    df = pd.DataFrame(lignes).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(os.path.join(HERE, "data", "agences_demo.csv"), index=False)
    return df, True


# --------------------------------------------------------------------------
def choisir_k(X, kmax=8):
    """Méthode du coude (inertie) + score de silhouette ; renvoie le k optimal."""
    ks = list(range(2, kmax + 1))
    inerties, silhouettes = [], []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        inerties.append(km.inertia_)
        silhouettes.append(silhouette_score(X, km.labels_))
    k_opt = ks[int(np.argmax(silhouettes))]

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    ax[0].plot(ks, inerties, "o-", color=BLUE, lw=2)
    ax[0].set_title("Méthode du coude"); ax[0].set_xlabel("Nombre de clusters k")
    ax[0].set_ylabel("Inertie intra-cluster")
    ax[1].plot(ks, silhouettes, "o-", color=CYAN, lw=2)
    ax[1].axvline(k_opt, color=RED, ls="--", lw=1.2, label=f"k optimal = {k_opt}")
    ax[1].set_title("Score de silhouette"); ax[1].set_xlabel("Nombre de clusters k")
    ax[1].set_ylabel("Silhouette moyenne"); ax[1].legend()
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "choix_k.png")); plt.close(fig)
    print(f"[k] Inerties={[round(i) for i in inerties]}")
    print(f"[k] Silhouettes={[round(s,3) for s in silhouettes]} -> k optimal = {k_opt}")
    return k_opt


# --------------------------------------------------------------------------
def comparer_modeles(X, k):
    """Compare K-Means, Agglomératif, GMM et DBSCAN sur 3 indices internes."""
    modeles = {
        "K-Means": KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X),
        "Agglomératif": AgglomerativeClustering(n_clusters=k).fit_predict(X),
        "GMM": GaussianMixture(n_components=k, random_state=42).fit_predict(X),
        "DBSCAN": DBSCAN(eps=1.7, min_samples=3).fit_predict(X),
    }
    lignes = []
    for nom, labels in modeles.items():
        nb = len(set(labels) - {-1})
        if nb >= 2:
            mask = labels != -1
            sil = silhouette_score(X[mask], labels[mask])
            db = davies_bouldin_score(X[mask], labels[mask])
            ch = calinski_harabasz_score(X[mask], labels[mask])
        else:
            sil, db, ch = np.nan, np.nan, np.nan
        lignes.append({"Modèle": nom, "Clusters": nb, "Silhouette": sil,
                       "Davies-Bouldin": db, "Calinski-Harabasz": ch})
    comp = pd.DataFrame(lignes)
    print("\n=== Comparaison des modèles ===")
    print(comp.to_string(index=False,
          formatters={"Silhouette": lambda v: f"{v:.3f}" if pd.notna(v) else "n/a",
                      "Davies-Bouldin": lambda v: f"{v:.3f}" if pd.notna(v) else "n/a",
                      "Calinski-Harabasz": lambda v: f"{v:.0f}" if pd.notna(v) else "n/a"}))

    fig, ax = plt.subplots(figsize=(7, 3.6))
    sub = comp.dropna(subset=["Silhouette"])
    bars = ax.bar(sub["Modèle"], sub["Silhouette"], color=[CYAN, AMBER, GREEN, RED][:len(sub)])
    ax.set_ylabel("Score de silhouette (↑ meilleur)")
    ax.set_title("Comparaison des modèles de clustering")
    for b, v in zip(bars, sub["Silhouette"]):
        ax.text(b.get_x() + b.get_width()/2, v + 0.01, f"{v:.3f}", ha="center", fontweight="bold")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "comparaison_modeles.png")); plt.close(fig)
    return comp, modeles


# --------------------------------------------------------------------------
def visualiser(X, labels, nom_modele):
    """Projection PCA 2D colorée par cluster."""
    p = PCA(n_components=2, random_state=42).fit(X)
    Z = p.transform(X)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    for c in sorted(set(labels)):
        m = labels == c
        lab = "Bruit" if c == -1 else f"Cluster {c}"
        ax.scatter(Z[m, 0], Z[m, 1], s=55, alpha=0.85,
                   color="#bbb" if c == -1 else PALETTE[c % len(PALETTE)],
                   edgecolor="white", label=lab)
    var = p.explained_variance_ratio_ * 100
    ax.set_xlabel(f"Composante 1 ({var[0]:.0f}%)")
    ax.set_ylabel(f"Composante 2 ({var[1]:.0f}%)")
    ax.set_title(f"Segmentation des agences — {nom_modele} (projection PCA)")
    ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "clusters_pca.png")); plt.close(fig)


# --------------------------------------------------------------------------
def profiler(df, labels):
    """Profil moyen de chaque cluster + interprétation."""
    d = df.copy(); d["cluster"] = labels
    prof = d.groupby("cluster")[FEATURES].mean().round(1)
    prof["nb_agences"] = d.groupby("cluster").size()
    print("\n=== Profil moyen par cluster ===")
    print(prof.to_string())
    return prof


# ============================ MAIN =========================================
def main():
    df, demo = charger_donnees()
    X = StandardScaler().fit_transform(df[FEATURES].values)

    k = choisir_k(X)
    comp, modeles = comparer_modeles(X, k)

    valides = comp.dropna(subset=["Silhouette"])
    best = valides.loc[valides["Silhouette"].idxmax(), "Modèle"]
    labels = modeles[best]
    print(f"\n[best] Meilleur modèle : {best} (silhouette la plus élevée)")

    visualiser(X, labels, best)
    prof = profiler(df, labels)

    out = df.copy(); out["cluster"] = labels
    out.to_csv(os.path.join(HERE, "resultats_segmentation.csv"), index=False)
    comp.to_csv(os.path.join(HERE, "comparaison_modeles.csv"), index=False)
    prof.to_csv(os.path.join(HERE, "profils_clusters.csv"))
    print(f"\n[ok] Source: {'DÉMONSTRATION' if demo else 'données réelles'} | "
          f"k={k} | modèle retenu={best}")
    print("[ok] Figures -> clustering/figures/ ; résultats -> clustering/*.csv")


if __name__ == "__main__":
    main()
