# ==============================================================
# metier/usagerMetier.py
# Fichier contenant la logique métier pour la gestion des usagers.
# Ce module gère la création, la lecture, la modification et la
# suppression des comptes usagers dans la base de données.
# ==============================================================


from __future__ import annotations


from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID


from core.db import SessionLocal
from modele.usager import Usager
from DTO.usagerDTO import UsagerDTO, UsagerCreateDTO, UsagerUpdateDTO, UsagerSearchDTO


# --------------------------------------------------------------
# ---------- CRÉATION ----------
# Permet d’ajouter un nouvel usager dans la base.
# Évite la création de doublons selon nom + prénom + mobile.
# --------------------------------------------------------------
def creerUsager(data: UsagerCreateDTO) -> UsagerDTO:
    """
    Crée un usager. Évite les doublons simples (nom, prénom, mobile).
    """
    with SessionLocal() as s:  # ouverture d’une session SQLAlchemy
        existing = s.execute(
            select(Usager).where(
                (Usager.nom == data.nom)
                & (Usager.prenom == data.prenom)
                & (Usager.mobile == data.mobile)
            )
        ).scalar_one_or_none()


        # Si un usager avec le même nom/prénom/mobile existe déjà, on le retourne
        if existing:
            return UsagerDTO(existing)


        # Sinon on crée un nouvel usager à partir du DTO
        u = Usager(
            prenom=data.prenom,
            nom=data.nom,
            adresse=data.adresse,
            mobile=data.mobile,
            # Le mot de passe est tronqué/padé à 60 caractères pour respecter CHAR(60)
            mot_de_passe=(data.mot_de_passe[:60]).ljust(60)[:60],
            type_usager=data.type_usager,
        )
        s.add(u)
        s.commit()
        s.refresh(u)
        return UsagerDTO(u)


# --------------------------------------------------------------
# ---------- LECTURE ----------
# Retourne un usager selon son identifiant unique (UUID)
# --------------------------------------------------------------
def getUsagerParId(id_usager: str | UUID) -> UsagerDTO | None:
    with SessionLocal() as s:
        u = s.get(Usager, str(id_usager))
        # Si trouvé, on le retourne en DTO, sinon None
        return UsagerDTO(u) if u else None


# --------------------------------------------------------------
# ---------- RECHERCHE ----------
# Permet de filtrer les usagers selon différents critères.
# --------------------------------------------------------------
def rechercherUsager(critere: UsagerSearchDTO) -> list[UsagerDTO]:
    with SessionLocal() as s:
        stmt = select(Usager)
        if critere.idUsager:
            stmt = stmt.where(Usager.id_usager == critere.idUsager)
        if critere.nom:
            stmt = stmt.where(Usager.nom == critere.nom)
        if critere.prenom:
            stmt = stmt.where(Usager.prenom == critere.prenom)
        if critere.mobile:
            stmt = stmt.where(Usager.mobile == critere.mobile)
        if critere.type_usager:
            stmt = stmt.where(Usager.type_usager == critere.type_usager)

        rows = s.execute(stmt).scalars().all()
        return [UsagerDTO(u) for u in rows]


# --------------------------------------------------------------
# ---------- MISE À JOUR ----------
# Permet de modifier un ou plusieurs champs d’un usager existant
# sans devoir tout remplacer.
# --------------------------------------------------------------
def modifierUsager(id_usager: str, data: UsagerUpdateDTO) -> UsagerDTO:
    """
    Met à jour partiellement un usager. Retourne l'UsagerDTO mis à jour.
    """
    with SessionLocal() as s:
        s: Session


        u = s.get(Usager, id_usager)
        if not u:
            raise ValueError("Usager introuvable.")


        # Mise à jour seulement des champs fournis dans le DTO
        if data.prenom is not None:
            u.prenom = data.prenom
        if data.nom is not None:
            u.nom = data.nom
        if data.adresse is not None:
            u.adresse = data.adresse
        if data.mobile is not None:
            u.mobile = data.mobile
        if data.mot_de_passe is not None:
            # Même logique de longueur fixe pour CHAR(60)
            u.mot_de_passe = (data.mot_de_passe[:60]).ljust(60)[:60]
        if data.type_usager is not None:
            u.type_usager = data.type_usager


        s.commit()
        s.refresh(u)
        return UsagerDTO(u)


# --------------------------------------------------------------
# ---------- SUPPRESSION ----------
# Supprime un usager de la base s’il existe.
# Retourne True si supprimé, False si aucun trouvé.
# --------------------------------------------------------------
def supprimerUsager(id_usager: str) -> bool:
    """
    Supprime un usager. Retourne True si supprimé, False si non trouvé.
    """
    with SessionLocal() as s:
        s: Session
        u = s.get(Usager, id_usager)
        if not u:
            return False
        s.delete(u)
        s.commit()
        return True
