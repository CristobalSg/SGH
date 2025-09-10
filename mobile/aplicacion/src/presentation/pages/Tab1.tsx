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
  const [selectedDate, setSelectedDate] = useState<string>("");

  const handleDateChange = (e: CustomEvent) => {
    const date = e.detail.value; // valor seleccionado en el calendario
    setSelectedDate(date);
    setShowPopover(true); // abrir el popover
  };

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
        
        <div className="calendar-container">
          <IonDatetime
            presentation="date"
            showDefaultButtons={false}
            highlightedDates={[
              {
                date: '2025-09-30', 
                textColor: 'red',
                backgroundColor: '#ffcccc'
              }
            ]}
            onIonChange={handleDateChange}
          />
        </div>

        {/* Popover para opciones del día seleccionado */}
        <IonPopover
          isOpen={showPopover}
          onDidDismiss={() => setShowPopover(false)}
          showBackdrop={true}
          className="custom-popover"
        >
          <IonHeader>
            <IonToolbar>
              <IonTitle>{selectedDate ? new Date(selectedDate).toLocaleDateString() : "Día seleccionado"}</IonTitle>
            </IonToolbar>
          </IonHeader>
          <IonContent>
            <IonList>
              <IonItem button onClick={() => alert("Agregar evento en " + selectedDate)}>
                <IonLabel>➕ Agregar evento</IonLabel>
              </IonItem>
              <IonItem button onClick={() => alert("Editar evento en " + selectedDate)}>
                <IonLabel>✏️ Editar evento</IonLabel>
              </IonItem>
              <IonItem button onClick={() => alert("Eliminar evento en " + selectedDate)}>
                <IonLabel>🗑️ Eliminar evento</IonLabel>
              </IonItem>
            </IonList>
          </IonContent>
        </IonPopover>
      </IonContent>
    </IonPage>
  );
};

export default Tab1;
