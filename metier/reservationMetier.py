# ==============================================================
# metier/reservationMetier.py
# Contient toute la logique métier liée aux réservations.
# Ce fichier gère la recherche, la création, la modification
# et la suppression des réservations dans la base SQL.
# ==============================================================

from __future__ import annotations

from typing import List, Any, Dict
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.db import SessionLocal
from DTO.reservationDTO import (
    CriteresRechercheDTO,
    ReservationDTO,
    ReservationUpdateDTO,
)
from modele.reservation import Reservation
from modele.chambre import Chambre
from modele.usager import Usager

# --------------------------------------------------------------
# ---------- RECHERCHE / LECTURE ----------
# Permet de filtrer les réservations selon différents critères :
# id, chambre, usager, nom, prénom, etc.
# --------------------------------------------------------------
def rechercherReservation(criteres: CriteresRechercheDTO) -> List["ReservationDTO"]:
    """
    Recherche de réservations selon des critères optionnels.
    Retourne une liste de ReservationDTO.
    """
    with SessionLocal() as s:
        s: Session

        # Requête de base : jointure avec la chambre
        stmt = select(Reservation).join(Reservation.chambre)

        # Application des filtres si les critères sont fournis
        if criteres.idReservation:
            stmt = stmt.where(Reservation.id_reservation == criteres.idReservation)
        if criteres.idChambre:
            stmt = stmt.where(Reservation.fk_id_chambre == criteres.idChambre)
        if criteres.idUsager:
            stmt = stmt.where(Reservation.fk_id_usager == criteres.idUsager)
        if criteres.nom and criteres.prenom:
            stmt = stmt.join(Usager).where(
                (Usager.nom == criteres.nom) & (Usager.prenom == criteres.prenom)
            )

        # Exécution et transformation en DTOs
        results: list[ReservationDTO] = []
        for r in s.execute(stmt).scalars():
            results.append(ReservationDTO.from_entity(r))
        return results

# --------------------------------------------------------------
# ---------- CRÉATION ----------
# Deux flux supportés : via un DTO complet ou via des paramètres simples.
# --------------------------------------------------------------


def creerReservation(dto: ReservationDTO) -> ReservationDTO:
    """Crée une réservation à partir d’un DTO complet (selon les exigences du professeur)."""
    # Validation de base des dates
    if dto.dateFin <= dto.dateDebut:
        raise ValueError("La date de fin doit être après la date de début.")

    # Vérification que les sous-objets requis sont bien présents
    if not dto.usager or not getattr(dto.usager, "idUsager", None):
        raise ValueError("UsagerDTO avec idUsager requis.")
    if not dto.chambre or not getattr(dto.chambre, "idChambre", None):
        raise ValueError("ChambreDTO avec idChambre requis.")

    with SessionLocal() as s:
        s: Session

        # Récupère l’usager et la chambre à partir de leur ID
        u = s.get(Usager, str(dto.usager.idUsager))
        ch = s.get(Chambre, str(dto.chambre.idChambre))
        if not u:
            raise ValueError("Usager introuvable.")
        if not ch:
            raise ValueError("Chambre introuvable.")

        # Création de la nouvelle réservation
        r = Reservation(
            date_debut_reservation=dto.dateDebut,
            date_fin_reservation=dto.dateFin,
            prix_jour=Decimal(str(dto.prixParJour)),
            info_reservation=dto.infoReservation,
            fk_id_usager=u.id_usager,
            fk_id_chambre=ch.id_chambre,
        )

        # Enregistrement en base
        s.add(r)
        s.commit()
        s.refresh(r)

        # Retourne le DTO résultant
        return ReservationDTO.from_entity(r)


# --------------------------------------------------------------
# ---------- MISE À JOUR ----------
# Permet de modifier les champs d’une réservation existante
# avec validation des dates et des références.
# --------------------------------------------------------------
def modifierReservation(id_reservation: str, data: ReservationUpdateDTO) -> ReservationDTO:
    with SessionLocal() as s:
        s: Session

        r = s.get(Reservation, id_reservation)
        if not r:
            raise ValueError("Réservation introuvable.")

        # Mise à jour de l’usager s’il est changé
        if data.idUsager:
            u = s.get(Usager, data.idUsager)
            if not u:
                raise ValueError("Usager introuvable.")
            r.fk_id_usager = u.id_usager

        # Mise à jour de la chambre s’il y a changement
        if data.idChambre:
            ch = s.get(Chambre, data.idChambre)
            if not ch:
                raise ValueError("Chambre introuvable.")
            r.fk_id_chambre = ch.id_chambre

        # Validation et mise à jour des dates
        if data.dateDebut:
            if r.date_fin_reservation and data.dateDebut >= r.date_fin_reservation:
                raise ValueError("La date de début doit être avant la date de fin.")
            r.date_debut_reservation = data.dateDebut

        if data.dateFin:
            if r.date_debut_reservation and data.dateFin <= r.date_debut_reservation:
                raise ValueError("La date de fin doit être après la date de début.")
            r.date_fin_reservation = data.dateFin

        # Mise à jour du prix et des infos
        if data.prixParJour is not None:
            r.prix_jour = Decimal(str(data.prixParJour))

        if data.infoReservation is not None:
            r.info_reservation = data.infoReservation

        s.commit()
        s.refresh(r)

        return ReservationDTO.from_entity(r)

# --------------------------------------------------------------
# ---------- SUPPRESSION ----------
# Supprime une réservation de la base (aucune contrainte particulière ici)
# --------------------------------------------------------------
def supprimerReservation(id_reservation: str) -> bool:
    with SessionLocal() as s:
        s: Session
        r = s.get(Reservation, id_reservation)
        if not r:
            return False
        s.delete(r)
        s.commit()
        return True
