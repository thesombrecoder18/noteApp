import streamlit as st
from authentication import Authentication
from database import DatabaseManager

def main():
    # Initialisation de l'authentification
    auth = Authentication()
    db_manager = DatabaseManager()

    # Configuration de la page
    st.set_page_config(page_title="Application de Notes", page_icon="📝")

    # Gestion de l'état de connexion
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # Définition des options de menu
    menu_options = ["Accueil"]
    if not st.session_state['authenticated']:
        menu_options.extend(["Connexion", "Créer un compte"])
    else:
        menu_options.extend(["Mes Notes", "Nouvelle Note", "Déconnexion"])

    # Barre latérale de navigation
    menu = st.sidebar.selectbox("Menu", menu_options)

    # Routage des pages
    if menu == "Accueil":
        if not st.session_state['authenticated']:
            st.title("Bienvenue sur l'Application de Notes")
            st.write("Cette application vous permet de gérer vos notes personnelles.")
            st.info("Connectez-vous pour accéder à vos notes privées.")
        else:
            st.title(f"Bienvenue sur votre compte, {st.session_state['username']} !")
            st.write("Vous pouvez maintenant créer et visualiser vos notes.")

    elif menu == "Connexion":
        if not st.session_state['authenticated']:
            auth.login_page()
        else:
            st.warning("Vous êtes déjà connecté.")

    elif menu == "Créer un compte":
        if not st.session_state['authenticated']:
            auth.registration_page()
        else:
            st.warning("Vous êtes déjà connecté.")

    # Pages nécessitant une authentification
    elif st.session_state['authenticated']:
        if menu == "Mes Notes":
            st.title("Mes Notes")
            notes = db_manager.get_user_notes(st.session_state['username'])
            
            if notes:
                for note_id, title, content, created_at in notes:
                    with st.expander(f"{title} - {created_at}"):
                        st.write(content)
            else:
                st.info("Vous n'avez pas encore de notes.")

        elif menu == "Nouvelle Note":
            st.title("Créer une Nouvelle Note")
            title = st.text_input("Titre de la note", key="note_title")
            content = st.text_area("Contenu de la note", key="note_content")
            
            if st.button("Enregistrer"):
                if title and content:
                    db_manager.add_note(st.session_state['username'], title, content)
                    st.success("Note enregistrée avec succès !")
                    
                    # Vider les champs après l'enregistrement
                    st.session_state['note_title'] = ""
                    st.session_state['note_content'] = ""
                    st.rerun()
                else:
                    st.error("Veuillez remplir tous les champs")

        elif menu == "Déconnexion":
            auth.logout()
            st.rerun()

    # Page par défaut si non connecté
    else:
        st.title("Bienvenue")
        st.write("Veuillez vous connecter ou créer un compte pour accéder à vos notes.")

if __name__ == "__main__":
    main()