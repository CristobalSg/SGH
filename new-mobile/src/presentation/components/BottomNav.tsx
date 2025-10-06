import { IonFooter, IonToolbar, IonButtons, IonButton, IonIcon, IonLabel } from '@ionic/react';
import { homeOutline, searchOutline, addCircleOutline, heartOutline, personOutline } from 'ionicons/icons';

const BottomNav: React.FC = () => {
  return (
    <IonFooter>
      <IonToolbar className="ion-text-center">
        <div style={{ display: 'flex', justifyContent: 'space-around', width: '100%' }}>
          
          <IonButton fill="clear" routerLink="/home">
            <IonIcon icon={homeOutline} />
            <IonLabel>Home</IonLabel>
          </IonButton>

          <IonButton fill="clear" routerLink="/search">
            <IonIcon icon={searchOutline} />
            <IonLabel>Search</IonLabel>
          </IonButton>

          <IonButton fill="clear" routerLink="/add">
            <IonIcon icon={addCircleOutline} />
            <IonLabel>Add</IonLabel>
          </IonButton>

          <IonButton fill="clear" routerLink="/favorites">
            <IonIcon icon={heartOutline} />
            <IonLabel>Favorites</IonLabel>
          </IonButton>

          <IonButton fill="clear" routerLink="/profile">
            <IonIcon icon={personOutline} />
            <IonLabel>Profile</IonLabel>
          </IonButton>

        </div>
      </IonToolbar>
    </IonFooter>
  );
};

export default BottomNav;
