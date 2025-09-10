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

import { personCircleOutline, createOutline } from 'ionicons/icons';
import './Tab2.css';

const Tab2: React.FC = () => {
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
            <IonText>Benjamin Carrasco</IonText>
          </IonItem>

          <IonItem>
            <IonLabel position="stacked">Tipo de perfil</IonLabel>
            <IonText>Estudiante</IonText>
          </IonItem>

          <IonItem>
            <IonLabel position="stacked">Correo</IonLabel>
            <IonText>estudiante@alu.uct.cl</IonText>
          </IonItem>

          <IonItem>
            <IonLabel position="stacked">Contraseña</IonLabel>
            <IonText>********</IonText>
            <IonButton fill="clear" slot="end">
              <IonIcon icon={createOutline} />
            </IonButton>
          </IonItem>
        </IonList>
      </IonContent>
    </IonPage>
  );
};

export default Tab2;
