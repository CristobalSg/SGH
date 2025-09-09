import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonDatetime } from '@ionic/react';
import './Tab1.css';

const Tab1: React.FC = () => {
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Inicio</IonTitle>
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
      </IonContent>
    </IonPage>
  );
};

export default Tab1;
