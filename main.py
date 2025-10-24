"""
Application principale FastAPI pour gérer les chambres et les réservations d'hôtel.


Pour lancer le serveur :
    uvicorn main:app --reload


Docs :
    http://127.0.0.1:8000/docs
"""


# Importation des modules principaux de FastAPI
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware


# ------------------------------------------------------------
# Importation des DTOs (objets de transfert de données)
# Ces classes définissent la structure des données échangées
# entre le backend et le frontend (validation automatique)
# ------------------------------------------------------------
from DTO.chambreDTO import (
    ChambreDTO,
    TypeChambreDTO,
    TypeChambreCreateDTO,
    TypeChambreUpdateDTO,
    ChambreCreateDTO,
    ChambreUpdateDTO,
    TypeChambreSearchDTO,
)
from DTO.reservationDTO import (
    CriteresRechercheDTO,
    ReservationDTO,
    ReservationUpdateDTO,
)
from DTO.usagerDTO import (
    UsagerDTO,
    UsagerCreateDTO,
    UsagerUpdateDTO,
    UsagerSearchDTO,
)


# ------------------------------------------------------------
# Importation de la logique métier (fonctions principales)
# C’est ici que se trouvent les opérations avec la base SQL
# ------------------------------------------------------------
from metier.chambreMetier import (
    creerChambre,
    creerTypeChambre,
    getChambreParNumero,
    listerChambres,
    listerTypesChambre,
    modifierChambre,
    supprimerChambre,
    modifierTypeChambre,
    supprimerTypeChambre,
    rechercherTypeChambre,
)
from metier.reservationMetier import (
    rechercherReservation,
    creerReservation,          # version DTO complète exigée par le prof
    modifierReservation,
    supprimerReservation,
)
from metier.usagerMetier import (
    creerUsager,
    modifierUsager,
    supprimerUsager,
    getUsagerParId,
    rechercherUsager,
)


# ------------------------------------------------------------
# Initialisation de l’application FastAPI
# On définit le titre, la description et la version de l’API
# ------------------------------------------------------------
app = FastAPI(
    title="API Hôtel - Projet Partiel",
    description="API permettant de gérer les chambres, les usagers et les réservations d'un hôtel.",
    version="1.0.0",
)


# ------------------------------------------------------------
# Configuration du middleware CORS
# Permet au frontend (ex: React, Vue, etc.) d’accéder à l’API
# En production, il faudrait restreindre les origines autorisées
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------
# Routes utilitaires (diagnostic de base)
# ------------------------------------------------------------
@app.get("/", summary="Statut de l'API")
def root():
    # Simple route pour vérifier que le serveur répond bien
    return {"status": "ok", "docs": "/docs"}




@app.get("/health", summary="Vérification de santé")
def health():
    # Autre route de santé (souvent utilisée pour le monitoring)
    return {"status": "ok"}


# ------------------------------------------------------------
# Routes API - Gestion des chambres
# ------------------------------------------------------------
@app.get(
    "/chambres/{no_chambre}",
    response_model=ChambreDTO,
    summary="Obtenir une chambre par numéro",
    description="Retourne les informations complètes d'une chambre selon son numéro."
)
def api_get_chambre(no_chambre: int):
    # Recherche d'une chambre selon son numéro
    chambre = getChambreParNumero(no_chambre)
    if not chambre:
        # Si non trouvée, on retourne une erreur 404
        raise HTTPException(status_code=404, detail=f"Chambre {no_chambre} non trouvée.")
    return chambre




@app.get(
    "/chambres",
    response_model=list[ChambreDTO],
    summary="Lister les chambres",
    description="Retourne la liste de toutes les chambres."
)
def api_lister_chambres():
    # Retourne toutes les chambres disponibles dans la BD
    return listerChambres()




@app.post(
    "/creerChambre",
    response_model=ChambreDTO,
    summary="Créer une chambre",
    description="Ajoute une chambre avec un type existant."
)
def api_creer_chambre(chambre: ChambreCreateDTO):
    # Création d'une nouvelle chambre à partir d’un DTO
    try:
        return creerChambre(chambre)
    except ValueError as e:
        # Gestion d’erreur si les données sont invalides
        raise HTTPException(status_code=400, detail=str(e))




@app.put(
    "/chambres/{id_chambre}",
    response_model=ChambreDTO,
    summary="Modifier une chambre",
    description="Modifie partiellement une chambre (numéro, disponibilité, infos, type)."
)
def api_modifier_chambre(id_chambre: str, body: ChambreUpdateDTO):
    # Modification d’une chambre existante
    try:
        return modifierChambre(id_chambre, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@app.delete(
    "/chambres/{id_chambre}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une chambre",
    description="Supprime une chambre (échoue si des réservations y sont rattachées)."
)
def api_supprimer_chambre(id_chambre: str):
    # Suppression d’une chambre dans la base
    try:
        ok = supprimerChambre(id_chambre)
        if not ok:
            raise HTTPException(status_code=404, detail="Chambre introuvable.")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------------------------------------------------
# Routes API - Types de chambre
# ------------------------------------------------------------
@app.get(
    "/typesChambre",
    response_model=list[TypeChambreDTO],
    summary="Lister les types de chambre",
    description="Retourne la liste des types de chambre."
)
def api_lister_types_chambre():
    # Retourne tous les types de chambres (simple, double, suite, etc.)
    return listerTypesChambre()




@app.post(
    "/creerTypeChambre",
    response_model=TypeChambreDTO,
    summary="Créer un type de chambre",
    description="Ajoute un nouveau type de chambre (ex: simple, double, suite)."
)
def api_creer_type_chambre(type_chambre: TypeChambreCreateDTO):
    # Création d’un type de chambre
    return creerTypeChambre(type_chambre)




@app.put(
    "/typeChambre/{id_type_chambre}",
    response_model=TypeChambreDTO,
    summary="Modifier un type de chambre",
    description="Modifie un type de chambre (nom, prix, description)."
)
def api_modifier_type_chambre(id_type_chambre: str, body: TypeChambreUpdateDTO):
    # Mise à jour d’un type de chambre existant
    try:
        return modifierTypeChambre(id_type_chambre, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@app.delete(
    "/typeChambre/{id_type_chambre}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un type de chambre",
    description="Supprime un type de chambre (échoue si des chambres y sont rattachées)."
)
def api_supprimer_type_chambre(id_type_chambre: str):
    # Suppression d’un type de chambre
    try:
        ok = supprimerTypeChambre(id_type_chambre)
        if not ok:
            raise HTTPException(status_code=404, detail="Type de chambre introuvable.")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/rechercherTypeChambre",
    response_model=list[TypeChambreDTO],
    summary="Rechercher des types de chambre",
    description="Recherche des types de chambre selon différents critères (id, nom)."
)
def api_rechercher_type_chambre(body: TypeChambreSearchDTO):
    # Permet de faire une recherche filtrée sur les types de chambre
    return rechercherTypeChambre(body)


# ------------------------------------------------------------
# Routes API - Réservations
# ------------------------------------------------------------
@app.post(
    "/rechercherReservation",
    response_model=list[ReservationDTO],
    summary="Rechercher des réservations",
    description="Recherche des réservations selon différents critères (id, nom, prénom, etc.)."
)
def api_rechercher_reservation(critere: CriteresRechercheDTO):
    # Permet de faire une recherche filtrée selon différents critères
    try:
        return rechercherReservation(critere)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@app.post(
    "/reservations",
    response_model=ReservationDTO,
    summary="Créer une réservation (DTO complet)",
    description=(
        "Crée une réservation à partir d'un ReservationDTO complet, "
        "incluant les objets UsagerDTO et ChambreDTO imbriqués, conformément à la consigne du professeur."
    )
)
def api_creer_reservation(body: ReservationDTO):
    # Création complète d’une réservation incluant les sous-objets usager et chambre
    try:
        return creerReservation(body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@app.put(
    "/reservations/{id_reservation}",
    response_model=ReservationDTO,
    summary="Modifier une réservation",
    description="Modifie partiellement une réservation existante."
)
def api_modifier_reservation(id_reservation: str, body: ReservationUpdateDTO):
    # Permet de mettre à jour une réservation déjà existante
    try:
        return modifierReservation(id_reservation, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@app.delete(
    "/reservations/{id_reservation}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une réservation",
    description="Supprime définitivement une réservation existante."
)
def api_supprimer_reservation(id_reservation: str):
    # Supprime une réservation de la base de données
    ok = supprimerReservation(id_reservation)
    if not ok:
        raise HTTPException(status_code=404, detail="Réservation introuvable.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ------------------------------------------------------------
# Routes API - Usagers
# ------------------------------------------------------------
@app.post(
    "/usagers",
    response_model=UsagerDTO,
    summary="Créer un usager",
    description="Ajoute un usager (évite les doublons simples nom+prénom+mobile)."
)
def api_creer_usager(body: UsagerCreateDTO):
    # Création d’un nouvel usager dans la base
    try:
        return creerUsager(body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@app.get(
    "/usagers/{id_usager}",
    response_model=UsagerDTO,
    summary="Obtenir un usager",
    description="Retourne un usager par son identifiant."
)
def api_get_usager(id_usager: str):
    # Recherche d’un usager par ID unique
    u = getUsagerParId(id_usager)
    if not u:
        raise HTTPException(status_code=404, detail="Usager introuvable.")
    return u




@app.put(
    "/usagers/{id_usager}",
    response_model=UsagerDTO,
    summary="Modifier un usager",
    description="Modifie partiellement un usager (profil)."
)
def api_modifier_usager(id_usager: str, body: UsagerUpdateDTO):
    # Modification du profil d’un usager existant
    try:
        return modifierUsager(id_usager, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@app.delete(
    "/usagers/{id_usager}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un usager",
    description="Supprime un usager."
)
def api_supprimer_usager(id_usager: str):
    # Suppression d’un usager de la base de données
    ok = supprimerUsager(id_usager)
    if not ok:
        raise HTTPException(status_code=404, detail="Usager introuvable.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/rechercherUsager",
    response_model=list[UsagerDTO],
    summary="Rechercher des usagers",
    description="Recherche des usagers selon différents critères (id, nom, prénom, mobile, type)."
)
def api_rechercher_usager(body: UsagerSearchDTO):
    # Permet de faire une recherche filtrée sur les usagers
    return rechercherUsager(body)


# ------------------------------------------------------------
# Point d’entrée du serveur (exécution locale)
# Si ce fichier est lancé directement, on démarre uvicorn
# ------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
