import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonButton,
  IonIcon,
  IonPopover,
  IonList,
  IonItem,
  IonLabel,
  IonDatetime,
} from "@ionic/react";
import { notificationsOutline } from "ionicons/icons";
import { useState, useEffect } from "react";


interface Events {
  [date: string]: string[];
}

const Tab1: React.FC = () => {
  const [showPopover, setShowPopover] = useState(false);
  const [selectedDate, setSelectedDate] = useState<string>("");
  const [events, setEvents] = useState<Events>({});
  const [tipoUsuario, setTipoUsuario] = useState<string>("");

  useEffect(() => {
    const tipo = localStorage.getItem("tipoUsuario") || "";
    setTipoUsuario(tipo);

    // Eventos falsos de ejemplo
    const fakeEvents: Events = {
      "2025-09-16": ["Reunión de equipo", "Entrega informe"],
      "2025-09-18": ["Clase de Matemática", "Examen parcial"],
      "2025-09-20": ["Conferencia online"],
    };

    // Cargar eventos guardados o usar eventos falsos
    const storedEvents = localStorage.getItem("events");
    if (storedEvents) {
      setEvents(JSON.parse(storedEvents));
    } else {
      setEvents(fakeEvents);
      localStorage.setItem("events", JSON.stringify(fakeEvents));
    }
  }, []);

  const saveEvents = (updatedEvents: Events) => {
    setEvents(updatedEvents);
    localStorage.setItem("events", JSON.stringify(updatedEvents));
  };

  const handleDateChange = (e: CustomEvent) => {
    const isoDate = e.detail.value; 
    if (!isoDate) return;
    const date = isoDate.split('T')[0]; 
    setSelectedDate(date);
    setShowPopover(true);
  };

  const handleAddEvent = () => {
    const text = prompt("Ingrese el nombre del evento:");
    if (!text) return;
    const updatedEvents = { ...events };
    if (!updatedEvents[selectedDate]) updatedEvents[selectedDate] = [];
    updatedEvents[selectedDate].push(text);
    saveEvents(updatedEvents);
  };

  const handleEditEvent = (index: number) => {
    const text = prompt("Editar evento:", events[selectedDate][index]);
    if (!text) return;
    const updatedEvents = { ...events };
    updatedEvents[selectedDate][index] = text;
    saveEvents(updatedEvents);
  };

  const handleDeleteEvent = (index: number) => {
    const updatedEvents = { ...events };
    updatedEvents[selectedDate].splice(index, 1);
    if (updatedEvents[selectedDate].length === 0) delete updatedEvents[selectedDate];
    saveEvents(updatedEvents);
  };

  // Obtener todos los eventos para la campana y ordenarlos por fecha ascendente
  const allEvents: { date: string; name: string }[] = [];
  for (const date in events) {
    events[date].forEach(evt => allEvents.push({ date, name: evt }));
  }
  allEvents.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  // Funciones para editar/eliminar por nombre desde la lista global
  const handleEditEventByName = (date: string, name: string) => {
    const idx = events[date].indexOf(name);
    if (idx === -1) return;
    setSelectedDate(date);
    handleEditEvent(idx);
  };

  const handleDeleteEventByName = (date: string, name: string) => {
    const idx = events[date].indexOf(name);
    if (idx === -1) return;
    setSelectedDate(date);
    handleDeleteEvent(idx);
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Calendario</IonTitle>
          <IonButtons slot="end">
            <IonButton onClick={() => setShowPopover(true)}>
              <IonIcon icon={notificationsOutline} />
              <span className="badge-side">{allEvents.length}</span>
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <IonDatetime
          presentation="date"
          highlightedDates={Object.keys(events).map(date => ({ date, backgroundColor: '#ffcccc' }))}
          onIonChange={handleDateChange}
        />
        <IonPopover
          isOpen={showPopover}
          onDidDismiss={() => setShowPopover(false)}
        >
          <IonHeader>
            <IonToolbar>
              <IonTitle>Eventos</IonTitle>
            </IonToolbar>
          </IonHeader>
          <IonContent>
            <IonList>
              {/* Aquí tu lógica para mostrar eventos */}
              {(!selectedDate ? allEvents : events[selectedDate]?.map((evt, _) => ({ name: evt, date: selectedDate })))
                .map((evt, index) => (
                  <IonItem key={index}>
                    <IonLabel>
                      {new Date(evt.date).toLocaleDateString()} - {evt.name}
                    </IonLabel>
                    {tipoUsuario === "profesor" && (
                      <>
                        <IonButton fill="clear" slot="end" onClick={() => handleEditEventByName(evt.date, evt.name)}>✏️</IonButton>
                        <IonButton fill="clear" slot="end" onClick={() => handleDeleteEventByName(evt.date, evt.name)}>🗑️</IonButton>
                      </>
                    )}
                  </IonItem>
              ))}
              {(!selectedDate && allEvents.length === 0) && (
                <IonItem>
                  <IonLabel>No hay eventos.</IonLabel>
                </IonItem>
              )}
              {/* Mostrar agregar evento solo si es profesor y fecha seleccionada */}
              {tipoUsuario === "profesor" && selectedDate && (
                <IonItem button onClick={handleAddEvent}>
                  <IonLabel>➕ Agregar evento</IonLabel>
                </IonItem>
              )}
              {/* Si estudiante y no hay eventos del día seleccionado */}
              {tipoUsuario !== "profesor" && selectedDate && (!events[selectedDate] || events[selectedDate].length === 0) && (
                <IonItem>
                  <IonLabel>No hay eventos este día.</IonLabel>
                </IonItem>
              )}
            </IonList>
          </IonContent>
        </IonPopover>
      </IonContent>
    </IonPage>
  );
};

export default Tab1;
