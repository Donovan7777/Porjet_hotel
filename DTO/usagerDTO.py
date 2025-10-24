# ==============================================================
# DTO/usagerDTO.py
# Fichier contenant les objets de transfert (DTO)
# pour gérer les usagers (clients ou admin) dans l’application.
# Les DTO servent à valider les données reçues et à formater
# celles qui sont envoyées vers le frontend.
# ==============================================================


from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from modele.usager import Usager


# --------------------------------------------------------------
# ---------- INPUT (création d’un nouvel usager) ----------
# Sert à valider les champs lors de l’ajout d’un nouveau compte.
# Tous les champs sont obligatoires ici.
# --------------------------------------------------------------
class UsagerCreateDTO(BaseModel):
    prenom: str = Field(min_length=1, max_length=50)
    nom: str = Field(min_length=1, max_length=50)
    adresse: str = Field(min_length=1, max_length=100)
    mobile: str = Field(min_length=1, max_length=15)
    mot_de_passe: str = Field(min_length=1, max_length=60)
    type_usager: str = Field(min_length=1, max_length=50)
    # type_usager pourrait être "Admin" ou "Usager" selon les rôles du système


# --------------------------------------------------------------
# ---------- INPUT (mise à jour d’un usager existant) ----------
# Sert à modifier un usager partiellement (ex: changement d’adresse)
# Tous les champs sont optionnels pour permettre un patch.
# --------------------------------------------------------------
class UsagerUpdateDTO(BaseModel):
    prenom: Optional[str] = Field(default=None, min_length=1, max_length=50)
    nom: Optional[str] = Field(default=None, min_length=1, max_length=50)
    adresse: Optional[str] = Field(default=None, min_length=1, max_length=100)
    mobile: Optional[str] = Field(default=None, min_length=1, max_length=15)
    mot_de_passe: Optional[str] = Field(default=None, min_length=1, max_length=60)
    type_usager: Optional[str] = Field(default=None, min_length=1, max_length=50)
    # Ces champs optionnels permettent de ne modifier que ce qu’on veut


# --------------------------------------------------------------
# ---------- OUTPUT (retour API) ----------
# Sert à renvoyer un usager au frontend sans exposer d’informations sensibles
# comme le mot de passe. On affiche seulement les infos publiques utiles.
# --------------------------------------------------------------
class UsagerDTO(BaseModel):
    idUsager: UUID
    prenom: str
    nom: str
    adresse: str
    mobile: str
    type_usager: str


    # Constructeur : convertit un objet Usager (ORM) en DTO pour l’API
    def __init__(self, u: Usager):
        super().__init__(
            idUsager=u.id_usager,
            prenom=u.prenom,
            nom=u.nom,
            adresse=u.adresse,
            mobile=u.mobile,
            type_usager=u.type_usager,
        )


# --------------------------------------------------------------
# ---------- INPUT (recherche d’usagers) ----------
# Sert à filtrer les usagers selon différents critères (facultatifs).
# --------------------------------------------------------------
class UsagerSearchDTO(BaseModel):
    idUsager: Optional[str] = Field(default=None, min_length=36, max_length=36)
    prenom: Optional[str] = Field(default=None, max_length=50)
    nom: Optional[str] = Field(default=None, max_length=50)
    mobile: Optional[str] = Field(default=None, max_length=15)
    type_usager: Optional[str] = Field(default=None, max_length=50)
