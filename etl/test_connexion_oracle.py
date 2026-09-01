# -*- coding: utf-8 -*-
"""Étape 1 de la chaîne ETL : vérifier la connexion à la base Oracle BTK.

Le script ouvre une connexion, affiche la version du serveur, puis compte les
lignes des cinq tables sources. Il ne modifie rien. En cas d'échec, il indique
la cause probable et la manœuvre à faire.

    python3 etl/test_connexion_oracle.py

Paramètres (mêmes valeurs que src/main/resources/META-INF/persistence.xml) :
    BTK_DB_USER   défaut SYSTEM
    BTK_DB_DSN    défaut localhost:1521/FREEPDB1
    BTK_DB_PWD    demandé à la saisie s'il n'est pas défini
"""
import os
import sys

# La table de diagnostic est partagée avec la chaîne ETL (etl_agences.py),
# situé dans le même dossier : une seule liste de causes à tenir à jour.
from etl_agences import conseil

TABLES = ["AGENCE", "B_UTILISATEURS", "CLIENT_BTK", "B_OBJECTIF", "POINTAGE"]


def parametres():
    user = os.environ.get("BTK_DB_USER", "SYSTEM")
    dsn = os.environ.get("BTK_DB_DSN", "localhost:1521/FREEPDB1")
    pwd = os.environ.get("BTK_DB_PWD")
    if not pwd:
        from getpass import getpass
        pwd = getpass(f"Mot de passe Oracle de {user}@{dsn} : ")
    return user, pwd, dsn


def main():
    try:
        import oracledb
    except ImportError:
        sys.exit("Le pilote « oracledb » n'est pas installé.\n"
                 "Dans l'invite Anaconda :  pip install oracledb")

    user, pwd, dsn = parametres()
    print(f"Connexion à {user}@{dsn} …")
    try:
        cn = oracledb.connect(user=user, password=pwd, dsn=dsn)
    except Exception as err:
        print("\nÉCHEC :", str(err).splitlines()[0])
        print("  →", conseil(err))
        sys.exit(1)

    print("Connecté. Serveur Oracle", cn.version)
    with cn.cursor() as cur:
        cur.execute("SELECT USER, SYS_CONTEXT('USERENV','CON_NAME') FROM DUAL")
        schema, conteneur = cur.fetchone()
    print(f"Schéma courant : {schema} | conteneur : {conteneur}\n")

    print(f"{'Table source':<18}{'Lignes':>10}   État")
    print("-" * 52)
    manquantes = []
    for table in TABLES:
        try:
            with cn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                print(f"{table:<18}{cur.fetchone()[0]:>10}   OK")
        except Exception as err:
            manquantes.append(table)
            print(f"{table:<18}{'—':>10}   {str(err).splitlines()[0][:40]}")
    cn.close()

    print()
    if not manquantes:
        print("Les cinq tables sources sont lisibles : la chaîne ETL peut tourner.")
        print("Étape suivante :  python3 etl/etl_agences.py --source oracle")
    elif manquantes == ["POINTAGE"]:
        print("POINTAGE est absente : la chaîne fonctionnera, sans le taux de présence.")
        print("Pour la créer :  sql/setup_pointage.sql")
    else:
        print("Tables illisibles :", ", ".join(manquantes))
        print("Connectez-vous au schéma qui porte ces tables, ou accordez les droits "
              "de lecture (GRANT SELECT).")
        sys.exit(1)


if __name__ == "__main__":
    main()
