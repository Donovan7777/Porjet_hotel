# ==============================================================
# DTO/reservationDTO.py
# Fichier qui contient les objets de transfert de données
# pour gérer les réservations dans le projet d’hôtel.
# Ces classes contrôlent ce que l’API reçoit et envoie.
# ==============================================================

from __future__ import annotations

import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

# Importation des DTOs reliés aux chambres et aux usagers
from DTO.chambreDTO import ChambreDTO
from DTO.usagerDTO import UsagerDTO

# --------------------------------------------------------------
# ---------- DTO pour la recherche de réservations ----------
# Sert à filtrer les réservations selon différents critères
# (par ex. nom, prénom, id, id chambre, etc.)
# --------------------------------------------------------------
class CriteresRechercheDTO(BaseModel):
    idReservation: Optional[str] = None
    idUsager: Optional[str] = None
    idChambre: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None

    # Validation automatique : les UUID doivent avoir 36 caractères
    @field_validator("idReservation", "idUsager", "idChambre")
    @classmethod
    def _validate_uuid_len(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) != 36:
            raise ValueError("Les identifiants doivent contenir 36 caractères (UUID).")
        return v

    # Validation du nom et du prénom (limite de longueur)
    @field_validator("nom", "prenom")
    @classmethod
    def _validate_names(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) > 60:
            raise ValueError("Nom/Prénom trop long (max 60).")
        return v

    def model_post_init(self, __context) -> None:
        # Petite logique : le nom et le prénom doivent venir ensemble
        if (self.nom and not self.prenom) or (self.prenom and not self.nom):
            raise ValueError("Le nom et le prénom doivent être tous les deux présents ou absents.")

# --------------------------------------------------------------
# ---------- DTO principal de réservation ----------
# Sert à la fois pour les entrées (création) et les sorties (retour API)
# Contient les infos de base + les objets Chambre et Usager imbriqués
# --------------------------------------------------------------
class ReservationDTO(BaseModel):
    # idReservation peut être vide lors de la création (il sera généré)
    idReservation: Optional[UUID] = None
    dateDebut: datetime.datetime
    dateFin: datetime.datetime
    prixParJour: float
    infoReservation: Optional[str] = None
    chambre: ChambreDTO
    usager: UsagerDTO

    # Méthode utilitaire pour créer un DTO à partir d’un objet ORM
    # (version demandée par le professeur dans les consignes)
    @classmethod
    def from_entity(cls, r) -> "ReservationDTO":
        # Import local pour éviter les références circulaires entre modules
        from modele.reservation import Reservation as ReservationEntity  # noqa: F401
        return cls(
            idReservation=r.id_reservation,
            dateDebut=r.date_debut_reservation,
            dateFin=r.date_fin_reservation,
            prixParJour=float(r.prix_jour),
            infoReservation=r.info_reservation,
            chambre=ChambreDTO(r.chambre),
            usager=UsagerDTO(r.usager),
        )

# --------------------------------------------------------------
# ---------- DTO de mise à jour partielle ----------
# Sert quand on veut modifier seulement certains champs d’une réservation
# (ex : changer les dates, le prix, ou la chambre associée)
# --------------------------------------------------------------
class ReservationUpdateDTO(BaseModel):
    idUsager: Optional[str] = Field(default=None, min_length=36, max_length=36)
    idChambre: Optional[str] = Field(default=None, min_length=36, max_length=36)
    dateDebut: Optional[datetime.datetime] = None
    dateFin: Optional[datetime.datetime] = None
    prixParJour: Optional[float] = None
    infoReservation: Optional[str] = None

    # Validation des UUID optionnels (doivent avoir 36 caractères si présents)
    @field_validator("idUsager", "idChambre")
    @classmethod
    def _validate_uuid_len_opt(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) != 36:
            raise ValueError("Les identifiants doivent contenir 36 caractères (UUID).")
        return v

    def model_post_init(self, __context) -> None:
        # Vérifie la cohérence entre les dates (la fin doit être après le début)
        if self.dateDebut and self.dateFin and self.dateFin <= self.dateDebut:
            raise ValueError("La date de fin doit être après la date de début.")
