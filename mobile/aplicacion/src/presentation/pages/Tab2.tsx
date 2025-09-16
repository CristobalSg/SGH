import { 
  IonContent, 
  IonHeader, 
  IonPage, 
  IonTitle, 
  IonToolbar, 
  IonList, 
  IonItem, 
  IonLabel, 
  IonText, 
  IonButton, 
  IonIcon, 
  IonAvatar 
} from '@ionic/react';

import { personCircleOutline, createOutline, logOutOutline } from 'ionicons/icons';
import { useHistory } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './Tab2.css';

const Tab2: React.FC = () => {
  const history = useHistory();

  // Estados para los datos del usuario
  const [nombre, setNombre] = useState('');
  const [correo, setCorreo] = useState('');
  const [tipoUsuario, setTipoUsuario] = useState('');

  useEffect(() => {
    // Cargar datos desde localStorage
    const nombreStored = localStorage.getItem('nombre') || '';
    const correoStored = localStorage.getItem('correo') || '';
    const tipoStored = localStorage.getItem('tipoUsuario') || '';

    setNombre(nombreStored);
    setCorreo(correoStored);
    setTipoUsuario(tipoStored);
  }, []);

  const handleLogout = () => {
    localStorage.clear(); // limpiar datos del usuario
    history.push("/"); // redirigir al login
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Perfil</IonTitle>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen className="ion-padding">
        
        {/* Foto de perfil */}
        <div className="profile-container">
          <IonAvatar className="profile-avatar">
            <IonIcon icon={personCircleOutline} style={{ fontSize: "120px" }} />
          </IonAvatar>
          <IonButton fill="clear" className="edit-avatar-btn">
            <IonIcon icon={createOutline} />
          </IonButton>
        </div>

        {/* Datos del perfil */}
        <IonList>
          <IonItem>
            <IonLabel position="stacked">Nombre</IonLabel>
            <IonText>{nombre}</IonText>
          </IonItem>

          <IonItem>
            <IonLabel position="stacked">Tipo de perfil</IonLabel>
            <IonText>{tipoUsuario}</IonText>
          </IonItem>

          <IonItem>
            <IonLabel position="stacked">Correo</IonLabel>
            <IonText>{correo}</IonText>
          </IonItem>

          <IonItem>
            <IonLabel position="stacked">Contraseña</IonLabel>
            <IonText>********</IonText>
            <IonButton fill="clear" slot="end">
              <IonIcon icon={createOutline} />
            </IonButton>
          </IonItem>
        </IonList>

        {/* Botón de Logout */}
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <IonButton color="danger" onClick={handleLogout}>
            <IonIcon icon={logOutOutline} slot="start" />
            Cerrar Sesión
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default Tab2;
