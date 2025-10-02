import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonItem,
  IonLabel,
  IonSelect,
  IonSelectOption,
  IonDatetime,
  IonButton
} from '@ionic/react';
import { useState } from 'react';
import './Restricciones.css';

interface Restriccion {
  dia: string;
  inicio: string;
  fin: string;
  tipo: string;
}

const Restricciones: React.FC = () => {
  const [dia, setDia] = useState<string>('');
  const [inicio, setInicio] = useState<string>('');
  const [fin, setFin] = useState<string>('');
  const [tipo, setTipo] = useState<string>('');
  const [restricciones, setRestricciones] = useState<Restriccion[]>([]);

  const [filtroDia, setFiltroDia] = useState<string>('todos');
  const [filtroTipo, setFiltroTipo] = useState<string>('todos');

  const extractHora = (value: string | null): string => {
    if (!value) return '';
    const date = new Date(value);
    const horas = date.getHours().toString().padStart(2, '0');
    const minutos = date.getMinutes().toString().padStart(2, '0');
    return `${horas}:${minutos}`;
  };

  const handleAgregar = () => {
    if (!dia || !inicio || !fin || !tipo) {
      alert("Completa todos los campos");
      return;
    }

    const [hInicio, mInicio] = inicio.split(":").map(Number);
    const [hFin, mFin] = fin.split(":").map(Number);
    const minutosInicio = hInicio * 60 + mInicio;
    const minutosFin = hFin * 60 + mFin;

    if (minutosInicio >= minutosFin) {
      alert("La hora de inicio debe ser menor a la hora de fin");
      return;
    }

    const nueva: Restriccion = { dia, inicio, fin, tipo };
    setRestricciones([...restricciones, nueva]);

    setDia('');
    setInicio('');
    setFin('');
    setTipo('');
  };

  // Filtrar restricciones
  const restriccionesFiltradas = restricciones.filter(r => {
    const diaMatch = filtroDia === 'todos' || r.dia === filtroDia;
    const tipoMatch = filtroTipo === 'todos' || r.tipo === filtroTipo;
    return diaMatch && tipoMatch;
  });

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Restricciones</IonTitle>
        </IonToolbar>
      </IonHeader>

      <IonContent className="restricciones-container">
        <h2>Agregar restricción</h2>

        <div className="form-section">
          <IonItem>
            <IonLabel>Día</IonLabel>
            <IonSelect
              value={dia}
              placeholder="Selecciona un día"
              onIonChange={e => setDia(e.detail.value!)}
            >
              <IonSelectOption value="lunes">Lunes</IonSelectOption>
              <IonSelectOption value="martes">Martes</IonSelectOption>
              <IonSelectOption value="miercoles">Miércoles</IonSelectOption>
              <IonSelectOption value="jueves">Jueves</IonSelectOption>
              <IonSelectOption value="viernes">Viernes</IonSelectOption>
              <IonSelectOption value="sabado">Sábado</IonSelectOption>
              <IonSelectOption value="domingo">Domingo</IonSelectOption>
            </IonSelect>
          </IonItem>

          <IonItem>
            <IonLabel>Hora inicio</IonLabel>
            <IonDatetime
              presentation="time"
              hourCycle="h23"
              value={inicio}
              onIonChange={e => {
                const value = Array.isArray(e.detail.value) ? e.detail.value[0] : e.detail.value;
                setInicio(extractHora(value ?? null));
              }}
            />
          </IonItem>

          <IonItem>
            <IonLabel>Hora fin</IonLabel>
            <IonDatetime
              presentation="time"
              hourCycle="h23"
              value={fin}
              onIonChange={e => {
                const value = Array.isArray(e.detail.value) ? e.detail.value[0] : e.detail.value;
                setFin(extractHora(value ?? null));
              }}
            />
          </IonItem>

          <IonItem>
            <IonLabel>Tipo</IonLabel>
            <IonSelect
              value={tipo}
              placeholder="Selecciona el tipo"
              onIonChange={e => setTipo(e.detail.value!)}
            >
              <IonSelectOption value="obligatoria">Obligatoria</IonSelectOption>
              <IonSelectOption value="preferencia">Preferencia</IonSelectOption>
              <IonSelectOption value="opcional">Opcional</IonSelectOption>
            </IonSelect>
          </IonItem>

          <IonButton expand="block" onClick={handleAgregar}>
            Agregar restricción
          </IonButton>
        </div>

        <div className="saved-restricciones">
          <h2>Restricciones guardadas</h2>

          {/* Filtros */}
<div className="filtros-container" style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
  <IonItem style={{ flex: 1 }}>
    <IonLabel>Día</IonLabel>
    <IonSelect value={filtroDia} onIonChange={e => setFiltroDia(e.detail.value!)}>
      <IonSelectOption value="todos">Todos</IonSelectOption>
      <IonSelectOption value="lunes">Lunes</IonSelectOption>
      <IonSelectOption value="martes">Martes</IonSelectOption>
      <IonSelectOption value="miercoles">Miércoles</IonSelectOption>
      <IonSelectOption value="jueves">Jueves</IonSelectOption>
      <IonSelectOption value="viernes">Viernes</IonSelectOption>
      <IonSelectOption value="sabado">Sábado</IonSelectOption>
      <IonSelectOption value="domingo">Domingo</IonSelectOption>
    </IonSelect>
  </IonItem>

  <IonItem style={{ flex: 1 }}>
    <IonLabel>Tipo</IonLabel>
    <IonSelect value={filtroTipo} onIonChange={e => setFiltroTipo(e.detail.value!)}>
      <IonSelectOption value="todos">Todos</IonSelectOption>
      <IonSelectOption value="obligatoria">Obligatoria</IonSelectOption>
      <IonSelectOption value="preferencia">Preferencia</IonSelectOption>
      <IonSelectOption value="opcional">Opcional</IonSelectOption>
    </IonSelect>
  </IonItem>
</div>
          {/* Lista filtrada */}
          {restriccionesFiltradas.map((r, index) => (
            <div key={index} className="saved-item">
              {r.dia}: {r.inicio} - {r.fin} ({r.tipo})
            </div>
          ))}
        </div>
      </IonContent>
    </IonPage>
  );
};

export default Restricciones;
