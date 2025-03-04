import streamlit as st
from database import DatabaseManager

class Authentication:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def login_page(self):
        st.title("Connexion")
        
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter"):
            if self.db_manager.validate_login(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.rerun()  # Utilisez st.rerun() au lieu de st.experimental_rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")

    def registration_page(self):
        st.title("Créer un compte")
        
        new_username = st.text_input("Choisissez un nom d'utilisateur")
        email = st.text_input("Votre email")
        new_password = st.text_input("Choisissez un mot de passe", type="password")
        confirm_password = st.text_input("Confirmez le mot de passe", type="password")
        
        if st.button("Créer un compte"):
            if new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas")
            elif len(new_password) < 6:
                st.error("Le mot de passe doit faire au moins 6 caractères")
            else:
                success = self.db_manager.register_user(new_username, new_password, email)
                if success:
                    st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                else:
                    st.error("Ce nom d'utilisateur existe déjà")

    def logout(self):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None