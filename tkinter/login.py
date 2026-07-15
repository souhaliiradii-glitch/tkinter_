import tkinter as tk
from tkinter import ttk, messagebox, font
import csv
import os
from datetime import datetime
# CLASSE PRINCIPALE 
class GestionStagiaires:
    def __init__(self):
        # Fenêtre principale
        self.root = tk.Tk()
        self.root.title("📚 Gestion des Stagiaires - Système Intelligent")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)
        
        # Configuration des couleurs et styles
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'danger': '#E74C3C',
            'warning': '#F39C12',
            'light': '#ECF0F1',
            'dark': '#2C3E50',
            'white': '#FFFFFF',
            'hover': '#2980B9'
        }   
        # Variable pour la connexion
        self.logged_in = False
        
        # Fichier CSV
        self.fichier_csv = "stagiaires.csv"
        self.creer_fichier_csv()
        
        # Afficher la page de connexion
        self.page_connexion()
        self.root.mainloop()
    
    # PAGE DE CONNEXION 
    def page_connexion(self):
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal avec dégradé
        main_frame = tk.Frame(self.root, bg=self.colors['primary'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de connexion centré
        login_frame = tk.Frame(main_frame, bg=self.colors['white'], 
                               relief=tk.RAISED, bd=2)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=350)
        
        # Titre
        titre = tk.Label(login_frame, text="🔐 Connexion", font=('Arial', 24, 'bold'), bg=self.colors['white'], fg=self.colors['primary'])
        titre.pack(pady=20)
        
        # Sous-titre
        sous_titre = tk.Label(login_frame, text="Gestion des Stagiaires v2.0", font=('Arial', 10), bg=self.colors['white'], fg=self.colors['secondary'])
        sous_titre.pack(pady=(0, 20))
        
        # Frame pour les champs
        fields_frame = tk.Frame(login_frame, bg=self.colors['white'])
        fields_frame.pack(pady=10)
        
        # Nom d'utilisateur
        tk.Label(fields_frame, text="👤 Nom d'utilisateur :", font=('Arial', 11), bg=self.colors['white'],fg=self.colors['dark']).grid(row=0, column=0, sticky='w', pady=5)
        self.entry_username = tk.Entry(fields_frame, width=25, font=('Arial', 11),
                                       relief=tk.SOLID, bd=1)
        self.entry_username.grid(row=0, column=1, pady=5, padx=10)
        self.entry_username.focus()
        
        # Mot de passe
        tk.Label(fields_frame, text="🔑 Mot de passe :", font=('Arial', 11), bg=self.colors['white'],fg=self.colors['dark']).grid(row=1, column=0, sticky='w', pady=5)
        self.entry_password = tk.Entry(fields_frame, width=25, font=('Arial', 11),
                                       relief=tk.SOLID, bd=1, show="•")
        self.entry_password.grid(row=1, column=1, pady=5, padx=10)
        
        # Bouton de connexion
        btn_login = tk.Button(login_frame, text="Se connecter", font=('Arial', 12, 'bold'),bg=self.colors['secondary'], fg=self.colors['white'],relief=tk.RAISED, bd=2, padx=30, pady=8,cursor='hand2',command=self.verifier_connexion)
        btn_login.pack(pady=20)
        
        # Effet de survol
        def on_enter(e):
            btn_login['background'] = self.colors['hover']
        def on_leave(e):
            btn_login['background'] = self.colors['secondary']
        btn_login.bind("<Enter>", on_enter)
        btn_login.bind("<Leave>", on_leave)
        
        # Informations de connexion (aide)
        info_label = tk.Label(login_frame, text="🔑 Identifiants par défaut : admin / admin123",font=('Arial', 9), bg=self.colors['white'],fg=self.colors['warning'])
        info_label.pack(pady=(10, 0))
        
        # Binder la touche Enter
        self.entry_password.bind('<Return>', lambda e: self.verifier_connexion())
        self.entry_username.bind('<Return>', lambda e: self.verifier_connexion())
    
    # VERIFICATION CONNEXION 
    def verifier_connexion(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        # Identifiants par défaut (vous pouvez modifier ou ajouter une vérification CSV)
        if username == "admin" and password == "admin123":
            self.logged_in = True
            self.page_accueil()
        else:
            messagebox.showerror("Erreur de connexion", 
                                "❌ Nom d'utilisateur ou mot de passe incorrect !\n\n"
                                "Utilisez :\n"
                                "👤 admin\n"
                                "🔑 admin123")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus()
    
    #  PAGE D'ACCUEIL 
    def page_accueil(self):
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configuration de la grille
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        
        #  BARRE LATÉRALE 
        sidebar = tk.Frame(self.root, bg=self.colors['primary'], width=220)
        sidebar.grid(row=0, column=0, sticky='ns')
        sidebar.grid_propagate(False)
        
        # Logo / Titre
        logo_label = tk.Label(sidebar, text="📚 GES", font=('Arial', 18, 'bold'),bg=self.colors['primary'], fg=self.colors['white'])
        logo_label.pack(pady=(30, 10))
        
        sous_logo = tk.Label(sidebar, text="Gestion des Stagiaires", font=('Arial', 10), bg=self.colors['primary'], fg=self.colors['secondary'])
        sous_logo.pack(pady=(0, 30))
        
        # Boutons de la barre latérale
        boutons_sidebar = [
            ("🏠 Accueil", self.accueil_action),
            ("👥 Stagiaires", self.page_gestion),
            ("📊 Statistiques", self.statistiques_action),
            ("⚙️ Paramètres", self.parametres_action),
        ]
        
        for texte, commande in boutons_sidebar:
            btn = tk.Button(sidebar, text=texte, font=('Arial', 11),bg=self.colors['primary'], fg=self.colors['white'],relief=tk.FLAT, anchor='w', padx=20, pady=10,cursor='hand2', command=commande)
            btn.pack(fill=tk.X, pady=2)
            
            # Effet de survol
            def make_hover(b):
                def on_enter(e):
                    b['background'] = self.colors['secondary']
                def on_leave(e):
                    b['background'] = self.colors['primary']
                b.bind("<Enter>", on_enter)
                b.bind("<Leave>", on_leave)
            make_hover(btn)
        
        # Déconnexion en bas
        tk.Frame(sidebar, bg=self.colors['primary'], height=2).pack(fill=tk.X, pady=20)
        btn_deconnexion = tk.Button(sidebar, text="🚪 Déconnexion", font=('Arial', 11),bg=self.colors['danger'], fg=self.colors['white'],relief=tk.FLAT, anchor='w', padx=20, pady=10,cursor='hand2', command=self.deconnexion)
        btn_deconnexion.pack(fill=tk.X, pady=2, side=tk.BOTTOM)
        
        #  CONTENU PRINCIPAL 
        content_frame = tk.Frame(self.root, bg=self.colors['light'])
        content_frame.grid(row=0, column=1, sticky='nsew')
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Affichage de l'accueil
        self.page_accueil_content(content_frame)
    
    # PAGE ACCUEIL CONTENU 
    def page_accueil_content(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()
        # Header
        header = tk.Frame(parent, bg=self.colors['secondary'], height=70)
        header.pack(fill=tk.X, pady=0)
        header.pack_propagate(False)
        tk.Label(header, text="🏠 Tableau de Bord", font=('Arial', 20, 'bold'),bg=self.colors['secondary'], fg=self.colors['white']).pack(side=tk.LEFT, padx=30, pady=15)
        date_label = tk.Label(header, text=datetime.now().strftime("%A, %d %B %Y %H:%M"),font=('Arial', 12),bg=self.colors['secondary'], fg=self.colors['white'])
        date_label.pack(side=tk.RIGHT, padx=30, pady=15)
        
        # Contenu
        main_container = tk.Frame(parent, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Statistiques en cartes
        stats_frame = tk.Frame(main_container, bg=self.colors['light'])
        stats_frame.pack(fill=tk.X, pady=10)
        
        stagiaires = self.compter_stagiaires()
        
        cartes = [
            ("👥 Stagiaires", str(stagiaires), self.colors['secondary'], "Total des stagiaires"),
            ("📚 Formations", "5", self.colors['success'], "Formations disponibles"),
            ("📝 Sessions", "12", self.colors['warning'], "Sessions en cours"),
            ("🎓 Diplomés", "28", self.colors['danger'], "Diplômés cette année"),
        ]
        
        for titre, valeur, couleur, sous_titre in cartes:
            card = tk.Frame(stats_frame, bg=self.colors['white'], 
                           relief=tk.RAISED, bd=1, padx=15, pady=15)
            card.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            
            tk.Label(card, text=titre, font=('Arial', 12),
                    bg=self.colors['white'], fg='#666').pack(anchor='w')
            tk.Label(card, text=valeur, font=('Arial', 32, 'bold'),
                    bg=self.colors['white'], fg=couleur).pack(anchor='w', pady=5)
            tk.Label(card, text=sous_titre, font=('Arial', 9),
                    bg=self.colors['white'], fg='#888').pack(anchor='w')
        
        # Section d'information
        info_frame = tk.Frame(main_container, bg=self.colors['white'],
                             relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        tk.Label(info_frame, text="📌 Actions rapides", font=('Arial', 16, 'bold'),bg=self.colors['white'], fg=self.colors['primary']).pack(anchor='w', padx=20, pady=15)
        
        actions_frame = tk.Frame(info_frame, bg=self.colors['white'])
        actions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        actions = [
            ("➕ Ajouter un stagiaire", self.page_gestion),
            ("🔍 Rechercher", self.page_gestion),
            ("📊 Voir statistiques", self.statistiques_action),
            ("📋 Exporter CSV", self.exporter_csv),
        ]
        for texte, cmd in actions:
            btn = tk.Button(actions_frame, text=texte, font=('Arial', 11),bg=self.colors['secondary'], fg=self.colors['white'],padx=20, pady=8, cursor='hand2', command=cmd)
            btn.pack(side=tk.LEFT, padx=5)
    
    #  PAGE DE GESTION DES STAGIAIRES
    def page_gestion(self):
        # Nettoyer et réorganiser la fenêtre
        for widget in self.root.winfo_children():
            if widget != self.root.grid_slaves(row=0, column=0)[0]:  # Garder la sidebar
                widget.destroy()
            else:
                # Cacher la sidebar
                pass
        # Recréer la sidebar si nécessaire
        content_frame = tk.Frame(self.root, bg=self.colors['light'])
        content_frame.grid(row=0, column=1, sticky='nsew')
        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        # Header
        header = tk.Frame(content_frame, bg=self.colors['secondary'], height=60)
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)
        
        tk.Label(header, text="👥 Gestion des Stagiaires", font=('Arial', 20, 'bold'),bg=self.colors['secondary'], fg=self.colors['white']).pack(side=tk.LEFT, padx=30, pady=10)
        
        # Conteneur principal
        main_container = tk.Frame(content_frame, bg=self.colors['light'])
        main_container.grid(row=1, column=0, sticky='nsew', padx=15, pady=15)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        #  Formulaire d'ajout
        form_frame = tk.LabelFrame(main_container, text="➕ Ajouter un stagiaire", font=('Arial', 12, 'bold'),bg=self.colors['white'], fg=self.colors['primary'],relief=tk.RAISED, bd=2)
        form_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        form_frame.grid_columnconfigure(4, weight=1)
        
        # Champs du formulaire
        champs = [
            ("Nom complet :", "entry_nom", 0, 0),
            ("Filière :", "entry_filiere", 0, 1),
            ("Email :", "entry_email", 1, 0),
            ("Téléphone :", "entry_tel", 1, 1),
            ("Date d'inscription :", "entry_date", 2, 0),
        ]
        self.entries = {}
        for label, attr, row, col in champs:
            tk.Label(form_frame, text=label, font=('Arial', 10),
                    bg=self.colors['white']).grid(row=row, column=col*2, sticky='e', padx=5, pady=8)
            entry = tk.Entry(form_frame, width=20, font=('Arial', 10),
                           relief=tk.SOLID, bd=1)
            entry.grid(row=row, column=col*2+1, sticky='w', padx=5, pady=8)
            self.entries[attr] = entry
        # Date par défaut
        self.entries["entry_date"].insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Boutons du formulaire
        btn_frame = tk.Frame(form_frame, bg=self.colors['white'])
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        btn_ajouter = tk.Button(btn_frame, text="✅ Ajouter", font=('Arial', 11, 'bold'),bg=self.colors['success'], fg=self.colors['white'],padx=20, pady=5, cursor='hand2',command=self.ajouter_stagiaire)
        btn_ajouter.pack(side=tk.LEFT, padx=5)
        
        btn_effacer = tk.Button(btn_frame, text="🗑️ Effacer", font=('Arial', 11, 'bold'),bg=self.colors['warning'], fg=self.colors['white'],padx=20, pady=5, cursor='hand2',command=self.effacer_champs)
        btn_effacer.pack(side=tk.LEFT, padx=5)
        
        # Tableau des stagiaires
        table_frame = tk.LabelFrame(main_container, text="📋 Liste des stagiaires", font=('Arial', 12, 'bold'),bg=self.colors['white'], fg=self.colors['primary'],relief=tk.RAISED, bd=2)
        table_frame.grid(row=1, column=0, sticky='nsew')
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Barre de recherche
        search_frame = tk.Frame(table_frame, bg=self.colors['white'])
        search_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        search_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(search_frame, text="🔍 Rechercher :", font=('Arial', 10),
                bg=self.colors['white']).grid(row=0, column=0, padx=(0, 10))
        
        self.entry_recherche = tk.Entry(search_frame, width=30, font=('Arial', 10),
                                      relief=tk.SOLID, bd=1)
        self.entry_recherche.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        self.entry_recherche.bind('<KeyRelease>', lambda e: self.rechercher_stagiaire())
        
        btn_rechercher = tk.Button(search_frame, text="🔍", font=('Arial', 11),bg=self.colors['secondary'], fg=self.colors['white'],padx=15, cursor='hand2',command=self.rechercher_stagiaire)
        btn_rechercher.grid(row=0, column=2, padx=(0, 10))
        btn_rafraichir = tk.Button(search_frame, text="🔄", font=('Arial', 11),bg=self.colors['success'], fg=self.colors['white'],padx=15, cursor='hand2',command=self.rafraichir_tableau)
        btn_rafraichir.grid(row=0, column=3)
        # Treeview pour le tableau
        columns = ('ID', 'Nom', 'Filière', 'Email', 'Téléphone', "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        self.tree.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        # Définir les en-têtes
        largeurs = [50, 150, 120, 200, 120, 100]
        for col, larg in zip(columns, largeurs):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=larg, anchor='center')
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns', pady=(0, 10))
        self.tree.configure(yscrollcommand=scrollbar.set)
        # Bouton supprimer en bas du tableau
        btn_supprimer = tk.Button(table_frame, text="🗑️ Supprimer le stagiaire sélectionné", font=('Arial', 11, 'bold'),bg=self.colors['danger'], fg=self.colors['white'],padx=20, pady=8, cursor='hand2',command=self.supprimer_stagiaire)
        btn_supprimer.grid(row=2, column=0, pady=10) 
        # Charger les données
        self.rafraichir_tableau()
    # FONCTIONS DE GESTION 
    def creer_fichier_csv(self):
        """Crée le fichier CSV s'il n'existe pas"""
        if not os.path.exists(self.fichier_csv):
            with open(self.fichier_csv, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Nom', 'Filiere', 'Email', 'Telephone', 'DateInscription'])
    def compter_stagiaires(self):
        """Compte le nombre de stagiaires"""
        try:
            with open(self.fichier_csv, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Ignorer l'en-tête
                return sum(1 for _ in reader)
        except:
            return 0
    def ajouter_stagiaire(self):
        """Ajoute un stagiaire dans le CSV"""
        nom = self.entries["entry_nom"].get().strip()
        filiere = self.entries["entry_filiere"].get().strip()
        email = self.entries["entry_email"].get().strip()
        tel = self.entries["entry_tel"].get().strip()
        date = self.entries["entry_date"].get().strip()
        # Validation
        if not all([nom, filiere, email, tel, date]):
            messagebox.showwarning("Champs manquants", 
                                 "⚠️ Veuillez remplir tous les champs !")
            return
        # Générer un ID
        try:
            with open(self.fichier_csv, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                ids = [int(row[0]) for row in reader if row]
                new_id = max(ids) + 1 if ids else 1
        except:
            new_id = 1
        # Ajouter au CSV
        try:
            with open(self.fichier_csv, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([new_id, nom, filiere, email, tel, date])
            messagebox.showinfo("Succès", f"✅ Stagiaire '{nom}' ajouté avec succès !")
            self.effacer_champs()
            self.rafraichir_tableau()
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur lors de l'ajout : {str(e)}")
    def effacer_champs(self):
        """Efface tous les champs du formulaire"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries["entry_date"].insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entries["entry_nom"].focus()
    def rafraichir_tableau(self):
        """Rafraîchit le tableau avec toutes les données"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            with open(self.fichier_csv, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Ignorer l'en-tête
                for row in reader:
                    if row:  # Vérifier que la ligne n'est pas vide
                        self.tree.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur de chargement : {str(e)}")
    def rechercher_stagiaire(self):
        """Recherche un stagiaire dans le tableau"""
        recherche = self.entry_recherche.get().strip().lower()
        if not recherche:
            self.rafraichir_tableau()
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            with open(self.fichier_csv, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if row and any(recherche in champ.lower() for champ in row):
                        self.tree.insert('', tk.END, values=row)
        except:
            pass
    def supprimer_stagiaire(self):
        """Supprime le stagiaire sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", 
                                 "⚠️ Veuillez sélectionner un stagiaire à supprimer !")
            return
        # Récupérer l'ID du stagiaire
        item = self.tree.item(selection[0])
        id_stagiaire = item['values'][0]
        nom_stagiaire = item['values'][1]
        # Confirmation
        if not messagebox.askyesno("Confirmation de suppression", 
                                 f"⚠️ Êtes-vous sûr de vouloir supprimer\n"
                                 f"'{nom_stagiaire}' (ID: {id_stagiaire}) ?"):
            return
        try:
            # Lire tout le fichier
            with open(self.fichier_csv, 'r') as f:
                rows = list(csv.reader(f))
            # Filtrer
            header = rows[0]
            data = [row for row in rows[1:] if row and row[0] != str(id_stagiaire)]
            # Réécrire
            with open(self.fichier_csv, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)
            messagebox.showinfo("Succès", f"✅ Stagiaire '{nom_stagiaire}' supprimé avec succès !")
            self.rafraichir_tableau()
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur lors de la suppression : {str(e)}")
    # AUTRES FONCTIONS 
    def accueil_action(self):
        """Retourne à l'accueil"""
        content_frame = self.root.grid_slaves(row=0, column=1)[0]
        self.page_accueil_content(content_frame)
    def statistiques_action(self):
        """Affiche les statistiques"""
        messagebox.showinfo("Statistiques", 
                          f"📊 Statistiques de la plateforme :\n\n"
                          f"👥 Total des stagiaires : {self.compter_stagiaires()}\n"
                          f"📚 Formations disponibles : 5\n"
                          f"📝 Sessions en cours : 12\n"
                          f"🎓 Diplomés cette année : 28\n\n"
                          f"📈 Taux de réussite : 87%")
    def parametres_action(self):
        """Affiche les paramètres"""
        messagebox.showinfo("Paramètres", 
                          "⚙️ Paramètres de l'application :\n\n"
                          "• Version : 2.0\n"
                          "• Fichier de données : stagiaires.csv\n"
                          "• Identifiants : admin / admin123\n"
                          "• Dernière mise à jour : Janvier 2025")
    def exporter_csv(self):
        """Exporte les données en CSV"""
        try:
            import shutil
            backup = f"backup_stagiaires_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            shutil.copy(self.fichier_csv, backup)
            messagebox.showinfo("Export réussi", 
                              f"✅ Les données ont été exportées avec succès !\n\n"
                              f"📁 Fichier : {backup}")
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur lors de l'export : {str(e)}")
    def deconnexion(self):
        """Déconnecte l'utilisateur"""
        if messagebox.askyesno("Déconnexion", "⚠️ Êtes-vous sûr de vouloir vous déconnecter ?"):
            self.logged_in = False
            self.page_connexion()
if __name__ == "__main__":
    app = GestionStagiaires()