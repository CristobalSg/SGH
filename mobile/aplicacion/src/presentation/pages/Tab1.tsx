import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonButtons,
  IonButton,
  IonIcon,
  IonPopover,
  IonList,
  IonItem,
  IonLabel,
  IonGrid,
  IonRow,
  IonCol
} from '@ionic/react';
import { useState, useEffect } from 'react';
import { notificationsOutline } from 'ionicons/icons';
import './Tab1.css';

interface Events {
  [day: string]: { [hour: string]: string[] }; // Ej: { lunes: { "08:00": ["Clase"] } }
}

const DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes"];
const HORAS = [
  "08:00", "09:00", "10:00", "11:00", "12:00",
  "13:00", "14:00", "15:00", "16:00", "17:00"
];

const Tab1: React.FC = () => {
  const [showPopover, setShowPopover] = useState(false);
  const [selectedCell, setSelectedCell] = useState<{ day: string; hour: string } | null>(null);
  const [events, setEvents] = useState<Events>({});
  const [tipoUsuario, setTipoUsuario] = useState<string>("");

  useEffect(() => {
    const tipo = localStorage.getItem("tipoUsuario") || "";
    setTipoUsuario(tipo);

    // Eventos falsos de ejemplo
const fakeEvents: Events = {
  lunes: { 
    "08:00": ["Matematica"], 
    "10:00": ["Fisica"] 
  },
  martes: { 
    "09:00": ["Quimica"], 
    "11:00": ["Lenguaje"] 
  },
  miércoles: { 
    "08:00": ["Historia"], 
    "14:00": ["Ingles"] 
  },
  jueves: { 
    "10:00": ["Biologia"], 
    "13:00": ["Artes"] 
  },
  viernes: { 
    "09:00": ["Matematica"], 
    "15:00": ["Fisica"] 
  }
};


    const storedEvents = localStorage.getItem("eventsHorario");
    if (storedEvents) {
      setEvents(JSON.parse(storedEvents));
    } else {
      setEvents(fakeEvents);
      localStorage.setItem("eventsHorario", JSON.stringify(fakeEvents));
    }
  }, []);

  const saveEvents = (updatedEvents: Events) => {
    setEvents(updatedEvents);
    localStorage.setItem("eventsHorario", JSON.stringify(updatedEvents));
  };

  const handleCellClick = (day: string, hour: string) => {
    setSelectedCell({ day, hour });
    setShowPopover(true);
  };

  const handleAddEvent = () => {
    const text = prompt("Ingrese el nombre del evento:");
    if (!text || !selectedCell) return;
    const updatedEvents = { ...events };
    if (!updatedEvents[selectedCell.day]) updatedEvents[selectedCell.day] = {};
    if (!updatedEvents[selectedCell.day][selectedCell.hour]) updatedEvents[selectedCell.day][selectedCell.hour] = [];
    updatedEvents[selectedCell.day][selectedCell.hour].push(text);
    saveEvents(updatedEvents);
  };

  const handleEditEvent = (idx: number) => {
    if (!selectedCell) return;
    const eventos = events[selectedCell.day]?.[selectedCell.hour] || [];
    const text = prompt("Editar evento:", eventos[idx]);
    if (!text) return;
    const updatedEvents = { ...events };
    updatedEvents[selectedCell.day][selectedCell.hour][idx] = text;
    saveEvents(updatedEvents);
  };

  const handleDeleteEvent = (idx: number) => {
    if (!selectedCell) return;
    const updatedEvents = { ...events };
    updatedEvents[selectedCell.day][selectedCell.hour].splice(idx, 1);
    if (updatedEvents[selectedCell.day][selectedCell.hour].length === 0) {
      delete updatedEvents[selectedCell.day][selectedCell.hour];
    }
    saveEvents(updatedEvents);
  };

  // Para la campana: contar todos los eventos
  const allEventsCount = DIAS.reduce((acc, day) => {
    if (!events[day]) return acc;
    return acc + Object.values(events[day]).reduce((sum, arr) => sum + arr.length, 0);
  }, 0);

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Horario Semanal</IonTitle>
          <IonButtons slot="end">
            <IonButton onClick={() => setShowPopover(true)} style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
              <IonIcon icon={notificationsOutline} />
              <span className="badge-side">{allEventsCount}</span>
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen className="ion-padding">
        <IonHeader collapse="condense">
          <IonTitle size="large">Horario Semanal</IonTitle>
        </IonHeader>

        <div style={{ overflowX: 'auto' }}>
          <IonGrid>
            <IonRow>
              <IonCol size="2"><strong>Hora</strong></IonCol>
              {DIAS.map(day => (
                <IonCol key={day} size="2" style={{ textAlign: 'center' }}>
                  <strong>{day.charAt(0).toUpperCase() + day.slice(1)}</strong>
                </IonCol>
              ))}
            </IonRow>
            {HORAS.map(hour => (
              <IonRow key={hour}>
                <IonCol size="2" style={{ fontWeight: 'bold', textAlign: 'center' }}>{hour}</IonCol>
                {DIAS.map(day => (
                  <IonCol
                    key={day + hour}
                    style={{
                      border: '1px solid #eee',
                      minHeight: '48px',
                      cursor: 'pointer',
                      background: events[day]?.[hour]?.length ? '#ffe4e1' : 'white'
                    }}
                    onClick={() => handleCellClick(day, hour)}
                  >
                    {events[day]?.[hour]?.map((evt, idx) => (
                    <div key={idx} className={`evento ${evt.replace(/\s/g, '')}`}>
                      {evt}
                    </div>
                  ))}

                  </IonCol>
                ))}
              </IonRow>
            ))}
          </IonGrid>
        </div>

        {/* Popover para ver/agregar/editar/eliminar eventos en la celda seleccionada */}
        <IonPopover
          isOpen={showPopover}
          onDidDismiss={() => setShowPopover(false)}
          showBackdrop={true}
          className="custom-popover"
        >
          <IonHeader>
            <IonToolbar>
              <IonTitle>
                {selectedCell
                  ? `${selectedCell.day.charAt(0).toUpperCase() + selectedCell.day.slice(1)} ${selectedCell.hour}`
                  : "Eventos"}
              </IonTitle>
            </IonToolbar>
          </IonHeader>
          <IonContent>
            <IonList>
              {selectedCell && events[selectedCell.day]?.[selectedCell.hour]?.length
                ? events[selectedCell.day][selectedCell.hour].map((evt, idx) => (
                  <IonItem key={idx}>
                    <IonLabel>{evt}</IonLabel>
                    {tipoUsuario === "profesor" && (
                      <>
                        <IonButton fill="clear" slot="end" onClick={() => handleEditEvent(idx)}>
                          ✏️
                        </IonButton>
                        <IonButton fill="clear" slot="end" onClick={() => handleDeleteEvent(idx)}>
                          🗑️
                        </IonButton>
                      </>
                    )}
                  </IonItem>
                ))
                : (
                  <IonItem>
                    <IonLabel>No hay eventos en este horario.</IonLabel>
                  </IonItem>
                )
              }
              {/* Mostrar agregar evento solo si es profesor y hay celda seleccionada */}
              {tipoUsuario === "profesor" && selectedCell && (
                <IonItem button onClick={handleAddEvent}>
                  <IonLabel>➕ Agregar evento</IonLabel>
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
