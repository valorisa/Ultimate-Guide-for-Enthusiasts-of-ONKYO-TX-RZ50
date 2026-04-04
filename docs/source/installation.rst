Installation & Branchement
==========================

.. note::
   Basé sur le manuel officiel Onkyo TX-RZ50, pages 7-77.

Prérequis de sécurité
---------------------

* Raccordez des enceintes ayant une valeur d'impédance comprise entre **4 Ω et 16 Ω**.
* Le cordon d'alimentation ne devra être branché **qu'après** tous les autres raccordements.
* Assurez-vous que l'appareil dispose d'un espace d'aération suffisant (minimum 10 cm sur les côtés).

.. warning::
   Nous déclinons toute responsabilité concernant des dommages résultant d'une connexion 
   à des équipements fabriqués par d'autres sociétés.

Disposition d'enceinte
----------------------

Cet appareil supporte les configurations suivantes :

.. list-table:: Configurations supportées
   :header-rows: 1
   :widths: 25 75

   * - Configuration
     - Description
   * - **5.1**
     - Système de base : Avant (L/R), Centrale, Surround (L/R), Caisson
   * - **7.1**
     - 5.1 + Surround Back (L/R) pour un champ surround élargi
   * - **5.1.2**
     - 5.1 + 2 enceintes en hauteur (Height/Top/Dolby Enabled)
   * - **7.1.2**
     - 7.1 + 2 enceintes en hauteur
   * - **5.1.4**
     - 5.1 + 4 enceintes en hauteur (2 avant + 2 arrière)
   * - **7.1.4**
     - Configuration maximale : 7.1 + 4 enceintes en hauteur

.. figure:: ../_static/speaker_layout_5.1.png
   :alt: Schéma de disposition 5.1
   :align: center

   Exemple de disposition 5.1 (source : manuel Onkyo p.23)

Branchements d'enceinte
-----------------------

1. **Coupez l'alimentation** de l'appareil avant tout branchement.
2. **Dénudez les câbles** sur environ 12 mm (1/2 pouce).
3. **Connectez la polarité** : `+` avec `+`, `-` avec `-` pour chaque canal.

.. code-block:: text

   Bornes SPEAKERS (panneau arrière) :
   ┌─────────────────────────────────┐
   │ FRONT   CENTER   SURROUND      │
   │ L   R   C   + -   L   R   SBL SBR │
   └─────────────────────────────────┘

.. note::
   * Entortillez fermement les fils exposés pour éviter les courts-circuits.
   * Les fiches banane (4 mm de diamètre) sont supportées.
   * Les fiches Y ne sont **pas** compatibles.

Caisson de basse
~~~~~~~~~~~~~~~~

Raccordez un caisson de basse sous tension aux prises ``SUBWOOFER PRE OUT`` :

.. code-block:: text

   TX-RZ50 [SUBWOOFER PRE OUT] ──(câble RCA)──► [LFE IN] Caisson de basse

* Jusqu'à **2 caissons** peuvent être connectés (signal identique sur les deux prises).
* Réglez le volume du caisson à ~50% avant la calibration AccuEQ/Dirac Live.

.. seealso::
   * :doc:`configuration` — Pour la calibration AccuEQ et Dirac Live
   * :doc:`modes_ecoute` — Pour optimiser les modes selon votre configuration

.. toctree::
   :maxdepth: 1
   :hidden:

   configuration
   modes_ecoute
   depannage
