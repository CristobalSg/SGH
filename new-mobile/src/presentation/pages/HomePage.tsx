// src/pages/HomePage.tsx
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
} from '@ionic/react';
import BottomNav from '../components/BottomNav';

const HomePage: React.FC = () => {
  return (
    <IonPage>
      {/* Header */}
      <IonHeader>
        <IonToolbar>
          <IonTitle>Home</IonTitle>
        </IonToolbar>
      </IonHeader>

      {/* Main Content */}
      <IonContent fullscreen className="ion-padding">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <h2>Bienvenido a tu App</h2>
          <p>
            Este es un layout básico usando Ionic React. Aquí puedes agregar tus
            tarjetas, listas, o cualquier otro componente.
          </p>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '1rem',
              marginTop: '2rem',
            }}
          >
            <div className="card">Elemento 1</div>
            <div className="card">Elemento 2</div>
            <div className="card">Elemento 3</div>
            <div className="card">Elemento 4</div>
          </div>
        </div>
      </IonContent>

      {/* Bottom Navigation */}
      <BottomNav />
    </IonPage>
  );
};

export default HomePage;
