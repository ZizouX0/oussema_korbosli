# -*- coding: utf-8 -*-
"""Segmentation des agences BTK sur les DONNÉES RÉELLES (49 entités du réseau).

  1. Chargement du datamart réel (clustering/data/agences_reelles.csv)
  2. Standardisation des six indicateurs
  3. Choix de k : méthode du coude + score de silhouette
  4. Comparaison de quatre modèles : K-Means, Agglomératif, GMM, DBSCAN
  5. Meilleur modèle : projection PCA et profilage des segments
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (silhouette_score, davies_bouldin_score,
                             calinski_harabasz_score)

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.normpath(os.path.join(HERE, "..", "rapport-latex", "images"))
NAVY, CYAN, ORANGE, GREEN = "#14507A", "#1B9CD8", "#E8A33D", "#2E9E6B"
FEATURES = ["effectif", "nb_gestionnaires", "nb_clients",
            "total_comptes", "production_credits", "collecte_epargne"]

brut = pd.read_csv(os.path.join(HERE, "data", "agences_reelles.csv"))
# Le SIÈGE (540 employés) est une structure centrale, pas une agence : conservé
# dans le datamart mais écarté de la segmentation où il constitue un point
# atypique qui écrase toute autre structure.
df = brut[brut["agence"] != "SIEGE"].reset_index(drop=True)
# Les montants et le portefeuille sont très asymétriques : passage au logarithme
# avant standardisation, afin qu'une agence extrême ne domine pas les distances.
T = df[FEATURES].copy()
for c in ["nb_clients", "total_comptes", "production_credits", "collecte_epargne"]:
    T[c] = np.log1p(T[c])
X = StandardScaler().fit_transform(T)
print(f"[data] {len(brut)} entités du réseau, {len(df)} retenues "
      f"(siège écarté) × {len(FEATURES)} indicateurs")

# ---------- 1) choix de k ----------
ks = range(2, 9)
inerties, sils = [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inerties.append(km.inertia_)
    sils.append(silhouette_score(X, km.labels_))
# k = 2 isole trivialement les entités sans activité ; on retient la meilleure
# solution à partir de k = 3, exploitable pour le pilotage.
k_opt = list(ks)[int(np.argmax([s if k >= 3 else -1 for k, s in zip(ks, sils)]))]

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(list(ks), inerties, "o-", color=NAVY, lw=2)
ax[0].set_title("Méthode du coude (inertie)"); ax[0].set_xlabel("Nombre de clusters k")
ax[0].set_ylabel("Inertie intra-cluster"); ax[0].grid(alpha=.3)
ax[1].plot(list(ks), sils, "o-", color=CYAN, lw=2)
ax[1].axvline(k_opt, ls="--", color=ORANGE)
ax[1].set_title("Score de silhouette"); ax[1].set_xlabel("Nombre de clusters k")
ax[1].set_ylabel("Silhouette"); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "clustering_choix_k.png"), dpi=150)
plt.close(fig)
print(f"[k] silhouettes={[round(s,3) for s in sils]} -> k optimal = {k_opt}")

# ---------- 2) comparaison des modèles ----------
modeles = {
    "K-Means": KMeans(n_clusters=k_opt, n_init=10, random_state=42).fit_predict(X),
    "Agglomératif": AgglomerativeClustering(n_clusters=k_opt).fit_predict(X),
    "GMM": GaussianMixture(n_components=k_opt, random_state=42).fit_predict(X),
    "DBSCAN": DBSCAN(eps=1.5, min_samples=3).fit_predict(X),
}
# Protocole d'évaluation équitable : chaque modèle est noté sur LA TOTALITÉ des
# agences. Les points qu'un modèle refuse de classer (bruit DBSCAN) sont comptés
# comme un groupe à part entière : un modèle ne doit pas être avantagé par le
# fait d'avoir écarté les agences les plus difficiles à classer.
lignes = []
for nom, lab in modeles.items():
    lab = lab.copy()
    if (lab == -1).any():
        lab[lab == -1] = lab.max() + 1
    lignes.append([nom, len(set(lab)),
                   silhouette_score(X, lab),
                   davies_bouldin_score(X, lab),
                   calinski_harabasz_score(X, lab)])
comp = pd.DataFrame(lignes, columns=["Modèle", "Clusters", "Silhouette",
                                     "Davies-Bouldin", "Calinski-Harabasz"])
comp.to_csv(os.path.join(HERE, "comparaison_modeles_reelles.csv"), index=False)
print("\n[comparaison]\n", comp.round(3).to_string(index=False))

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(comp["Modèle"], comp["Silhouette"], color=[NAVY, CYAN, ORANGE, GREEN])
for i, v in enumerate(comp["Silhouette"]):
    ax.text(i, v + .01, f"{v:.3f}", ha="center", fontsize=10, weight="bold")
ax.set_ylabel("Score de silhouette (↑ meilleur)")
ax.set_title("Comparaison des modèles de clustering")
ax.set_ylim(0, max(comp["Silhouette"]) * 1.25); ax.grid(axis="y", alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "clustering_comparaison.png"), dpi=150)
plt.close(fig)

# ---------- 3) modèle retenu ----------
# Le modèle retenu est celui qui obtient le meilleur score de silhouette sous le
# protocole d'évaluation ci-dessus (toutes les agences prises en compte).
best = comp.loc[comp["Silhouette"].idxmax(), "Modèle"]
labels = modeles[best]
print(f"\n[best] modèle retenu : {best}")

# ---------- 4) projection PCA ----------
p = PCA(n_components=2).fit(X)
Z = p.transform(X)
fig, ax = plt.subplots(figsize=(7.5, 5.2))
cols = [NAVY, ORANGE, GREEN, CYAN, "#B0489B"]
for c in sorted(set(labels)):
    m = labels == c
    ax.scatter(Z[m, 0], Z[m, 1], s=55, alpha=.85,
               color=cols[c % len(cols)], label=f"Cluster {c}", edgecolor="white")
ax.set_xlabel(f"Composante 1 ({p.explained_variance_ratio_[0]*100:.0f} %)")
ax.set_ylabel(f"Composante 2 ({p.explained_variance_ratio_[1]*100:.0f} %)")
ax.set_title(f"Segmentation des agences — {best} (projection PCA)")
ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "clustering_pca.png"), dpi=150)
plt.close(fig)

# ---------- 5) profils ----------
d = df.copy(); d["cluster"] = labels
prof = d.groupby("cluster")[FEATURES].mean().round(0).astype(int)
prof["nb_agences"] = d.groupby("cluster").size()
prof = prof[["nb_agences"] + FEATURES]
prof.to_csv(os.path.join(HERE, "profils_clusters_reels.csv"))
print("\n[profils]\n", prof.to_string())
for c in sorted(set(labels)):
    noms = d.loc[d.cluster == c, "agence"].tolist()
    print(f"\nCluster {c} ({len(noms)}) : {', '.join(noms[:8])}{' …' if len(noms) > 8 else ''}")
