# ==============================================================
# DTO/chambreDTO.py
# Fichier contenant les objets de transfert de données (DTO)
# liés aux chambres et aux types de chambres de l’hôtel.
# Ces classes servent d’intermédiaire entre le modèle (BD)
# et l’API FastAPI, pour contrôler et valider les données.
# ==============================================================

from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from modele.chambre import Chambre
from modele.type_chambre import TypeChambre

# --------------------------------------------------------------
# ---------- OUTPUT DTOs (envoyés par l’API) ----------
# Ces classes servent à formater les données retournées
# au client (souvent du frontend) d’une façon propre et claire.
# --------------------------------------------------------------
class TypeChambreDTO(BaseModel):
    nom_type: str
    prix_plafond: Optional[str] = None
    prix_plancher: float
    description_chambre: Optional[str] = None

    # Le constructeur reçoit un objet TypeChambre du modèle
    # et extrait seulement les champs utiles à exposer à l’API.
    def __init__(self, typeChambre: TypeChambre):
        super().__init__(
            nom_type=typeChambre.nom_type,
            prix_plafond=typeChambre.prix_plafond,
            prix_plancher=float(typeChambre.prix_plancher),
            description_chambre=typeChambre.description_chambre,
        )


class ChambreDTO(BaseModel):
    idChambre: UUID
    numero_chambre: int
    disponible_reservation: bool
    autre_informations: Optional[str] = None
    type_chambre: TypeChambreDTO

    # Ce DTO retourne les infos complètes d’une chambre,
    # incluant son type (imbriqué à l’intérieur du DTO).
    def __init__(self, chambre: Chambre):
        super().__init__(
            idChambre=chambre.id_chambre,
            numero_chambre=chambre.numero_chambre,
            disponible_reservation=chambre.disponible_reservation,
            autre_informations=chambre.autre_informations,
            type_chambre=TypeChambreDTO(chambre.type_chambre),
        )

# --------------------------------------------------------------
# ---------- INPUT DTOs (reçus par l’API) ----------
# Ces classes décrivent les données qu’un client (ex: front-end)
# doit fournir lorsqu’il crée ou modifie des chambres.
# Elles valident aussi automatiquement les formats avec Pydantic.
# --------------------------------------------------------------
class TypeChambreCreateDTO(BaseModel):
    # Champs nécessaires pour créer un type de chambre
    nom_type: str = Field(min_length=1, max_length=50)
    prix_plancher: float
    prix_plafond: Optional[str] = Field(default=None, max_length=10)
    description_chambre: Optional[str] = Field(default=None, max_length=200)


class TypeChambreUpdateDTO(BaseModel):
    # Champs optionnels pour la mise à jour d’un type de chambre
    nom_type: Optional[str] = Field(default=None, min_length=1, max_length=50)
    prix_plancher: Optional[float] = None
    prix_plafond: Optional[str] = Field(default=None, max_length=10)
    description_chambre: Optional[str] = Field(default=None, max_length=200)


class ChambreCreateDTO(BaseModel):
    # Champs utilisés lors de la création d’une nouvelle chambre
    numero_chambre: int
    disponible_reservation: bool
    autre_informations: Optional[str] = None
    # On référence le type par son nom (plus simple à gérer côté client)
    nom_type: str = Field(min_length=1, max_length=50)


class ChambreUpdateDTO(BaseModel):
    # Champs optionnels pour la mise à jour d’une chambre existante
    numero_chambre: Optional[int] = None
    disponible_reservation: Optional[bool] = None
    autre_informations: Optional[str] = None
    # Permet de changer le type en fournissant un nouveau nom
    nom_type: Optional[str] = Field(default=None, min_length=1, max_length=50)
