import { 
  IonContent, 
  IonHeader, 
  IonPage, 
  IonTitle, 
  IonToolbar, 
  IonList, 
  IonItem, 
  IonLabel, 
  IonButtons, 
  IonButton, 
  IonIcon, 
  IonAccordion, 
  IonAccordionGroup, 
  IonSelect, 
  IonSelectOption, 
  IonInput 
} from '@ionic/react';
import { checkmarkCircleOutline, trashOutline, searchOutline } from 'ionicons/icons';
import { useState } from 'react';
import './AdminRestricciones.css';

interface Restriccion {
  dia: string;
  horario: string; // ejemplo: "8:00 - 10:00"
  tipo: string; // "obligatoria", "preferencia", "opcional"
}

interface Profesor {
  nombre: string;
  restricciones: Restriccion[];
}

const AdminRestricciones: React.FC = () => {
  const [profesores, setProfesores] = useState<Profesor[]>([
    {
      nombre: "Profesor Juan Pérez",
      restricciones: [
        { dia: "lunes", horario: "8:00 - 10:00", tipo: "obligatoria" },
        { dia: "miércoles", horario: "14:00 - 16:00", tipo: "preferencia" },
      ],
    },
    {
      nombre: "Profesor Ana Torres",
      restricciones: [
        { dia: "martes", horario: "9:00 - 11:00", tipo: "obligatoria" },
        { dia: "jueves", horario: "10:00 - 12:00", tipo: "preferencia" },
        { dia: "viernes", horario: "15:00 - 17:00", tipo: "opcional" },
      ],
    },
    {
      nombre: "Profesor Carlos Díaz",
      restricciones: [
        { dia: "lunes", horario: "10:00 - 12:00", tipo: "obligatoria" },
      ],
    },
  ]);

  const [filtroProfesor, setFiltroProfesor] = useState<string>('');
  const [filtroDia, setFiltroDia] = useState<string>('todos');
  const [filtroTipo, setFiltroTipo] = useState<string>('todos');

  const handleEliminar = (profIndex: number, resIndex: number) => {
    const nuevosProfesores = [...profesores];
    nuevosProfesores[profIndex].restricciones.splice(resIndex, 1);
    const profesoresFiltrados = nuevosProfesores.filter(p => p.restricciones.length > 0);
    setProfesores(profesoresFiltrados);
  };

  const handleAceptar = (profIndex: number, resIndex: number) => {
    const nuevosProfesores = [...profesores];
    nuevosProfesores[profIndex].restricciones.splice(resIndex, 1);
    const profesoresFiltrados = nuevosProfesores.filter(p => p.restricciones.length > 0);
    setProfesores(profesoresFiltrados);
  };

  // Función para normalizar texto (quitar tildes y pasar a minúsculas)
  const normalizar = (texto: string) =>
    texto.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, "");

  // Filtrar profesores y restricciones
  const profesoresFiltrados = profesores
    .filter(p => normalizar(p.nombre).includes(normalizar(filtroProfesor)))
    .map(p => ({
      ...p,
      restricciones: p.restricciones.filter(r => 
        (filtroDia === 'todos' || normalizar(r.dia) === normalizar(filtroDia)) &&
        (filtroTipo === 'todos' || normalizar(r.tipo) === normalizar(filtroTipo))
      )
    }))
    .filter(p => p.restricciones.length > 0);

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Restricciones (Admin)</IonTitle>
          <IonButtons slot="end">
            <IonButton>
              <IonIcon icon={searchOutline} />
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen className="ion-padding">
        {/* Filtros */}
        <div style={{ display: 'flex', gap: '10px', marginBottom: '10px', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <IonLabel>Profesor</IonLabel>
            <IonInput
              placeholder="Escribe nombre del profesor"
              value={filtroProfesor}
              onIonInput={e => setFiltroProfesor(e.detail.value!)}
            />
          </div>

          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
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
          </div>

          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <IonLabel>Tipo</IonLabel>
            <IonSelect value={filtroTipo} onIonChange={e => setFiltroTipo(e.detail.value!)}>
              <IonSelectOption value="todos">Todos</IonSelectOption>
              <IonSelectOption value="obligatoria">Obligatoria</IonSelectOption>
              <IonSelectOption value="preferencia">Preferencia</IonSelectOption>
              <IonSelectOption value="opcional">Opcional</IonSelectOption>
            </IonSelect>
          </div>
        </div>

        {/* Lista de profesores y restricciones */}
        <IonAccordionGroup>
          {profesoresFiltrados.map((profesor, profIndex) => (
            <IonAccordion key={profIndex} value={profesor.nombre}>
              <IonItem slot="header">
                <IonLabel>
                  {profesor.nombre} — {profesor.restricciones.length} restricciones
                </IonLabel>
              </IonItem>

              <IonList slot="content">
                {profesor.restricciones.map((res, resIndex) => (
                  <IonItem key={resIndex}>
                    <IonLabel>{res.dia}: {res.horario} ({res.tipo})</IonLabel>
                    <IonButtons slot="end">
                      <IonButton
                        color="success"
                        fill="clear"
                        onClick={() => handleAceptar(profIndex, resIndex)}
                      >
                        <IonIcon icon={checkmarkCircleOutline} />
                      </IonButton>
                      <IonButton
                        color="danger"
                        fill="clear"
                        onClick={() => handleEliminar(profIndex, resIndex)}
                      >
                        <IonIcon icon={trashOutline} />
                      </IonButton>
                    </IonButtons>
                  </IonItem>
                ))}
              </IonList>
            </IonAccordion>
          ))}
        </IonAccordionGroup>
      </IonContent>
    </IonPage>
  );
};

export default AdminRestricciones;
