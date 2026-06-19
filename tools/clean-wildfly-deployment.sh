#!/usr/bin/env bash
# ============================================================
#  Nettoyage du déploiement manuel EN DOUBLE de gestion-agences
#  dans WildFly. À lancer si erreur :
#    WFLYSRV0205 ... Duplicate deployment ... will not be processed
#
#  ARRÊTEZ WildFly AVANT de lancer ce script.
#
#  Usage :   ./clean-wildfly-deployment.sh <WILDFLY_HOME>
#  Exemple : ./clean-wildfly-deployment.sh ~/wildfly-31.0.0.Final
# ============================================================
set -e

if [ -z "$1" ]; then
  echo "Usage : $0 <WILDFLY_HOME>"
  echo "Exemple : $0 ~/wildfly-31.0.0.Final"
  exit 1
fi

DEPLOY="$1/standalone/deployments"
if [ ! -d "$DEPLOY" ]; then
  echo "Dossier introuvable : $DEPLOY"
  echo "Vérifiez le chemin de WildFly passé en paramètre."
  exit 1
fi

echo "Nettoyage de : $DEPLOY"
for ext in war war.deployed war.dodeploy war.failed war.undeployed war.isdeploying; do
  f="$DEPLOY/gestion-agences-1.0-SNAPSHOT.$ext"
  if [ -e "$f" ]; then
    rm -f "$f"
    echo "  - supprimé : gestion-agences-1.0-SNAPSHOT.$ext"
  fi
done

echo ""
echo "Terminé. Redémarrez WildFly, puis déployez via IntelliJ UNIQUEMENT"
echo "(ne recopiez plus le WAR à la main dans deployments/)."
