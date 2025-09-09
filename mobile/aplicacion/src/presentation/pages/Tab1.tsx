<<<<<<< HEAD
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonDatetime } from '@ionic/react';
=======
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import LoginForm from '../components/LoginForm/LoginForm';
>>>>>>> 83c9c309f672a0e659d6ecb99450568a809dc5de
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
