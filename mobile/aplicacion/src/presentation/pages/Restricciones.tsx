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
  IonButton,
  IonList
} from '@ionic/react';
import { useState } from 'react';
import './Restricciones.css';
interface Restriccion {
  dia: string;
  inicio: string;
  fin: string;
}

const Restricciones: React.FC = () => {
  const [dia, setDia] = useState<string>('');
  const [inicio, setInicio] = useState<string>('');
  const [fin, setFin] = useState<string>('');
  const [restricciones, setRestricciones] = useState<Restriccion[]>([]);

  const handleAgregar = () => {
    if (!dia || !inicio || !fin) {
      alert("Completa todos los campos");
      return;
    }

    const nueva: Restriccion = { dia, inicio, fin };
    setRestricciones([...restricciones, nueva]);

    // reset formulario
    setDia('');
    setInicio('');
    setFin('');
  };

  return (
    <IonPage>
  <IonHeader>
  </IonHeader>
  <IonContent className="restricciones-container">
    <h2>Agregar restricción</h2>

    <div className="form-section">
      <IonItem>
        <IonLabel>Día</IonLabel>
        <IonSelect placeholder="Selecciona un día">
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
        <IonDatetime presentation="time"></IonDatetime>
      </IonItem>

      <IonItem>
        <IonLabel>Hora fin</IonLabel>
        <IonDatetime presentation="time"></IonDatetime>
      </IonItem>

      <IonButton expand="block">Agregar restricción</IonButton>
    </div>

    <div className="saved-restricciones">
      <h2>Restricciones guardadas</h2>
      <div className="saved-item">Miércoles: 08:29 a.m. - 09:31 p.m.</div>
      <div className="saved-item">Sábado: 09:31 a.m. - 11:31 p.m.</div>
    </div>
  </IonContent>
</IonPage>
  );
};

export default Restricciones;
