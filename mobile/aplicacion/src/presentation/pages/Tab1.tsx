import { 
  IonContent, 
  IonHeader, 
  IonPage, 
  IonTitle, 
  IonToolbar, 
  IonDatetime, 
  IonButtons, 
  IonButton, 
  IonIcon, 
  IonPopover, 
  IonList, 
  IonItem, 
  IonLabel 
} from '@ionic/react';
import { useState } from 'react';
import { notificationsOutline } from 'ionicons/icons';
import './Tab1.css';

const Tab1: React.FC = () => {
  const [showPopover, setShowPopover] = useState(false);

  const mockNotifications = [
    { id: 1, text: "Tu clase de hoy ha sido reprogramada." },
    { id: 2, text: "Nuevo evento agregado al calendario." },
    { id: 3, text: "Recuerda actualizar tu perfil." }
  ];

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Inicio</IonTitle>
          <IonButtons slot="end">
            <IonButton onClick={() => setShowPopover(true)}>
              <IonIcon icon={notificationsOutline} />
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>
      
      <IonContent fullscreen className="ion-padding">
        <IonHeader collapse="condense">
          <IonTitle size="large">Calendario</IonTitle>
        </IonHeader>

        {/* Contenedor para centrar */}
        <div className="calendar-container">
          <IonDatetime
            presentation="date"
            showDefaultButtons={true}
          ></IonDatetime>
        </div>

        {/* Popover centrado */}
        <IonPopover
          isOpen={showPopover}
          onDidDismiss={() => setShowPopover(false)}
          showBackdrop={true}
          className="custom-popover"
        >
          <IonHeader>
            <IonToolbar>
              <IonTitle>Notificaciones</IonTitle>
            </IonToolbar>
          </IonHeader>
          <IonContent>
            <IonList>
              {mockNotifications.map((notif) => (
                <IonItem key={notif.id}>
                  <IonLabel>{notif.text}</IonLabel>
                </IonItem>
              ))}
            </IonList>
          </IonContent>
        </IonPopover>
      </IonContent>
    </IonPage>
  );
};

export default Tab1;
