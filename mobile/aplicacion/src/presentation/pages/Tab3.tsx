import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonDatetime,
  IonAlert,
} from '@ionic/react';
import { useState } from 'react';
import './Tab3.css';

const Tab3: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [alertOpen, setAlertOpen] = useState(false);
  const [eventoActual, setEventoActual] = useState<string>('');

  // Ejemplo de eventos
  const eventos = [
    { fecha: '2025-10-10', nombre: 'Prueba de Matemáticas' },
    { fecha: '2025-10-15', nombre: 'Entrega de Proyecto' },
    { fecha: '2025-10-20', nombre: 'Exposición de Física' },
    { fecha: '2025-10-25', nombre: 'Control de Programación' },
  ];

  const handleDateChange = (value: string) => {
    // Extraemos solo la parte de la fecha YYYY-MM-DD
    const fechaSeleccionada = value.split('T')[0];
    setSelectedDate(fechaSeleccionada);

    const evento = eventos.find((e) => e.fecha === fechaSeleccionada);
    if (evento) {
      setEventoActual(evento.nombre);
      setAlertOpen(true);
    }
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Calendario de Eventos</IonTitle>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen className="calendario-centro">
        <IonDatetime
          onIonChange={(e) => handleDateChange(e.detail.value!)}
          presentation="date"
          locale="es-ES"
          highlightedDates={eventos.map((e) => ({
            date: e.fecha,
            textColor: 'red',
          }))}
        />

        <IonAlert
          isOpen={alertOpen}
          onDidDismiss={() => setAlertOpen(false)}
          header="Evento"
          message={eventoActual}
          buttons={['OK']}
        />
      </IonContent>
    </IonPage>
  );
};

export default Tab3;
