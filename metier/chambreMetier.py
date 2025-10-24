# ==============================================================
# metier/chambreMetier.py
# Ce module contient toute la logique métier pour la gestion
# des chambres et des types de chambres dans l’application.
# Il s’occupe des opérations CRUD : création, lecture, mise à jour
# et suppression des données en base SQL via SQLAlchemy.
# ==============================================================


from __future__ import annotations


from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from core.db import SessionLocal
from DTO.chambreDTO import (
    ChambreDTO,
    TypeChambreDTO,
    TypeChambreCreateDTO,
    TypeChambreUpdateDTO,
    ChambreCreateDTO,
    ChambreUpdateDTO,
    TypeChambreSearchDTO,
)
from modele.chambre import Chambre
from modele.type_chambre import TypeChambre


# --------------------------------------------------------------
# ---------- CREATE ----------
# Fonctions pour créer un type de chambre ou une chambre
# --------------------------------------------------------------


def creerTypeChambre(data: TypeChambreCreateDTO) -> TypeChambreDTO:
    with SessionLocal() as session:  # ouverture d’une session SQLAlchemy
        exists = session.execute(
            select(TypeChambre).where(TypeChambre.nom_type == data.nom_type)
        ).scalar_one_or_none()


        # Si un type avec le même nom existe déjà, on le retourne tel quel
        if exists:
            return TypeChambreDTO(exists)


        # Création du nouvel objet TypeChambre à partir des données reçues
        new_tc = TypeChambre(
            nom_type=data.nom_type,
            prix_plancher=data.prix_plancher,
            prix_plafond=data.prix_plafond,
            description_chambre=data.description_chambre,
        )
        session.add(new_tc)
        session.commit()
        session.refresh(new_tc)
        return TypeChambreDTO(new_tc)




def creerChambre(data: ChambreCreateDTO) -> ChambreDTO:
    with SessionLocal() as session:  # ouverture d’une session
        # Vérifie si le type de chambre fourni existe dans la BD
        tc = session.execute(
            select(TypeChambre).where(TypeChambre.nom_type == data.nom_type)
        ).scalar_one_or_none()
        if tc is None:
            raise ValueError(f"Type de chambre '{data.nom_type}' introuvable.")


        # Création de la nouvelle chambre avec ses informations
        ch = Chambre(
            numero_chambre=data.numero_chambre,
            disponible_reservation=data.disponible_reservation,
            autre_informations=data.autre_informations,
            type_chambre=tc,
        )
        session.add(ch)
        session.commit()
        session.refresh(ch)
        return ChambreDTO(ch)


# --------------------------------------------------------------
# ---------- READ / LIST ----------
# Fonctions pour lire les chambres et types de chambres
# --------------------------------------------------------------


def getChambreParNumero(no_chambre: int) -> ChambreDTO | None:
    with SessionLocal() as session:
        # Cherche une chambre par son numéro
        ch = session.execute(
            select(Chambre).where(Chambre.numero_chambre == no_chambre)
        ).scalar_one_or_none()
        return ChambreDTO(ch) if ch else None




def listerTypesChambre() -> List[TypeChambreDTO]:
    with SessionLocal() as session:
        # Retourne tous les types de chambres triés par nom
        rows = session.execute(
            select(TypeChambre).order_by(TypeChambre.nom_type)
        ).scalars().all()
        return [TypeChambreDTO(t) for t in rows]




def listerChambres() -> List[ChambreDTO]:
    with SessionLocal() as session:
        # Retourne toutes les chambres triées par numéro
        rows = session.execute(
            select(Chambre).order_by(Chambre.numero_chambre)
        ).scalars().all()
        return [ChambreDTO(c) for c in rows]


# --------------------------------------------------------------
# ---------- SEARCH ----------
# Fonctions pour rechercher un type de chambre selon des critères
# --------------------------------------------------------------
def rechercherTypeChambre(critere: TypeChambreSearchDTO) -> List[TypeChambreDTO]:
    with SessionLocal() as session:
        stmt = select(TypeChambre)
        if critere.idTypeChambre:
            stmt = stmt.where(TypeChambre.id_type_chambre == critere.idTypeChambre)
        if critere.nom_type:
            stmt = stmt.where(TypeChambre.nom_type == critere.nom_type)
        rows = session.execute(stmt).scalars().all()
        return [TypeChambreDTO(t) for t in rows]


# --------------------------------------------------------------
# ---------- UPDATE ----------
# Fonctions pour modifier un type de chambre ou une chambre
# --------------------------------------------------------------


def modifierTypeChambre(id_type_chambre: str, data: TypeChambreUpdateDTO) -> TypeChambreDTO:
    with SessionLocal() as session:
        session: Session
        tc = session.get(TypeChambre, id_type_chambre)
        if not tc:
            raise ValueError("Type de chambre introuvable.")


        # Mise à jour des champs modifiés seulement
        if data.nom_type is not None:
            tc.nom_type = data.nom_type
        if data.prix_plancher is not None:
            tc.prix_plancher = data.prix_plancher
        if data.prix_plafond is not None:
            tc.prix_plafond = data.prix_plafond
        if data.description_chambre is not None:
            tc.description_chambre = data.description_chambre


        session.commit()
        session.refresh(tc)
        return TypeChambreDTO(tc)




def modifierChambre(id_chambre: str, data: ChambreUpdateDTO) -> ChambreDTO:
    with SessionLocal() as session:
        session: Session
        ch = session.get(Chambre, id_chambre)
        if not ch:
            raise ValueError("Chambre introuvable.")


        # Mise à jour des champs si fournis
        if data.numero_chambre is not None:
            ch.numero_chambre = data.numero_chambre
        if data.disponible_reservation is not None:
            ch.disponible_reservation = data.disponible_reservation
        if data.autre_informations is not None:
            ch.autre_informations = data.autre_informations


        # Si le type de chambre change, on valide que le nouveau type existe
        if data.nom_type is not None:
            tc = session.execute(
                select(TypeChambre).where(TypeChambre.nom_type == data.nom_type)
            ).scalar_one_or_none()
            if not tc:
                raise ValueError(f"Type de chambre '{data.nom_type}' introuvable.")
            ch.fk_type_chambre = tc.id_type_chambre
            ch.type_chambre = tc  # garde la relation à jour


        session.commit()
        session.refresh(ch)
        return ChambreDTO(ch)


# --------------------------------------------------------------
# ---------- DELETE ----------
# Fonctions pour supprimer un type de chambre ou une chambre
# avec gestion des contraintes de clé étrangère
# --------------------------------------------------------------


def supprimerTypeChambre(id_type_chambre: str) -> bool:
    with SessionLocal() as session:
        session: Session
        tc = session.get(TypeChambre, id_type_chambre)
        if not tc:
            return False
        try:
            session.delete(tc)
            session.commit()
            return True
        except IntegrityError:
            # Si des chambres utilisent encore ce type, la suppression échoue
            session.rollback()
            raise ValueError(
                "Impossible de supprimer ce type de chambre car des chambres y sont rattachées."
            )




def supprimerChambre(id_chambre: str) -> bool:
    with SessionLocal() as session:
        session: Session
        ch = session.get(Chambre, id_chambre)
        if not ch:
            return False
        try:
            session.delete(ch)
            session.commit()
            return True
        except IntegrityError:
            # Si des réservations sont liées à la chambre, la suppression échoue
            session.rollback()
            raise ValueError(
                "Impossible de supprimer cette chambre car des réservations y sont rattachées."
            )
