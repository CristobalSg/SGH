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
<<<<<<< HEAD
          <IonTitle>Inicio</IonTitle>
=======
          <IonTitle>Login</IonTitle>
>>>>>>> 83c9c309f672a0e659d6ecb99450568a809dc5de
        </IonToolbar>
      </IonHeader>
      
      <IonContent fullscreen className="ion-padding">
        <IonHeader collapse="condense">
<<<<<<< HEAD
          <IonTitle size="large">Calendario</IonTitle>
        </IonHeader>

        {/* Contenedor para centrar */}
        <div className="calendar-container">
          <IonDatetime
            presentation="date"
            showDefaultButtons={true}
          ></IonDatetime>
        </div>
=======
          <IonToolbar>
            <IonTitle size="large">Login</IonTitle>
          </IonToolbar>
        </IonHeader>

        {/* Aquí va el login */}
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
          <LoginForm />
        </div>

>>>>>>> 83c9c309f672a0e659d6ecb99450568a809dc5de
      </IonContent>
    </IonPage>
  );
};

export default Tab1;
