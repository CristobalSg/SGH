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
  IonList,
  IonModal,
  IonToast,
  IonGrid,
  IonRow,
  IonCol,
  IonIcon
} from '@ionic/react';
import { addCircleOutline, trashOutline, createOutline } from 'ionicons/icons';
import { useState } from 'react';

interface Restriccion {
  dia: string;
  inicio: string;
  fin: string;
  tipo: string;
}

const DIAS = [
  "todos", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"
];

const TIPOS = [
  "todos", "obligatoria", "preferencia", "opcional"
];

const Restricciones: React.FC = () => {
  const [restricciones, setRestricciones] = useState<Restriccion[]>([]);
  const [filtroDia, setFiltroDia] = useState<string>('todos');
  const [filtroTipo, setFiltroTipo] = useState<string>('todos');

  // Modal para agregar restricción
  const [showModal, setShowModal] = useState(false);
  const [nuevoDia, setNuevoDia] = useState('');
  const [nuevoInicio, setNuevoInicio] = useState('');
  const [nuevoFin, setNuevoFin] = useState('');
  const [nuevoTipo, setNuevoTipo] = useState('');
  const [showToast, setShowToast] = useState(false);

  // Modal para editar restricción
  const [showEditModal, setShowEditModal] = useState(false);
  const [editIndex, setEditIndex] = useState<number | null>(null);
  const [editDia, setEditDia] = useState('');
  const [editInicio, setEditInicio] = useState('');
  const [editFin, setEditFin] = useState('');
  const [editTipo, setEditTipo] = useState('');

  const extractHora = (value: string | null): string => {
    if (!value) return '';
    const date = new Date(value);
    const horas = date.getHours().toString().padStart(2, '0');
    const minutos = date.getMinutes().toString().padStart(2, '0');
    return `${horas}:${minutos}`;
  };

  const handleAgregarRestriccion = () => {
    if (!nuevoDia || !nuevoInicio || !nuevoFin || !nuevoTipo) {
      setShowToast(true);
      return;
    }
    setRestricciones([
      ...restricciones,
      { dia: nuevoDia, inicio: nuevoInicio, fin: nuevoFin, tipo: nuevoTipo }
    ]);
    setShowModal(false);
    setNuevoDia('');
    setNuevoInicio('');
    setNuevoFin('');
    setNuevoTipo('');
  };

  const handleEliminar = (index: number) => {
    const nuevas = [...restricciones];
    nuevas.splice(index, 1);
    setRestricciones(nuevas);
  };

  const handleEditar = (index: number) => {
    const r = restricciones[index];
    setEditIndex(index);
    setEditDia(r.dia);
    setEditInicio(r.inicio);
    setEditFin(r.fin);
    setEditTipo(r.tipo);
    setShowEditModal(true);
  };

  const handleGuardarEdicion = () => {
    if (
      editIndex === null ||
      !editDia ||
      !editInicio ||
      !editFin ||
      !editTipo
    ) {
      setShowToast(true);
      return;
    }
    const nuevas = [...restricciones];
    nuevas[editIndex] = {
      dia: editDia,
      inicio: editInicio,
      fin: editFin,
      tipo: editTipo,
    };
    setRestricciones(nuevas);
    setShowEditModal(false);
    setEditIndex(null);
    setEditDia('');
    setEditInicio('');
    setEditFin('');
    setEditTipo('');
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
          {/* Para el botón agregar */}
          <IonButton slot="end" onClick={() => setShowModal(true)}>
            <IonLabel>Agregar</IonLabel>
            <IonIcon icon={addCircleOutline} style={{ marginLeft: 4 }} />
          </IonButton>
        </IonToolbar>
      </IonHeader>

      <IonContent>
        {/* Filtros */}
        <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
          <IonItem style={{ flex: 1 }}>
            <IonLabel>Día</IonLabel>
            <IonSelect value={filtroDia} onIonChange={e => setFiltroDia(e.detail.value!)}>
              {DIAS.map(dia => (
                <IonSelectOption key={dia} value={dia}>{dia.charAt(0).toUpperCase() + dia.slice(1)}</IonSelectOption>
              ))}
            </IonSelect>
          </IonItem>
          <IonItem style={{ flex: 1 }}>
            <IonLabel>Tipo</IonLabel>
            <IonSelect value={filtroTipo} onIonChange={e => setFiltroTipo(e.detail.value!)}>
              {TIPOS.map(tipo => (
                <IonSelectOption key={tipo} value={tipo}>{tipo.charAt(0).toUpperCase() + tipo.slice(1)}</IonSelectOption>
              ))}
            </IonSelect>
          </IonItem>
        </div>

        {/* Lista de restricciones con botones alineados al lado */}
        <IonList>
          {restriccionesFiltradas.map((r, index) => (
            <IonItem key={index} style={{ alignItems: 'flex-start' }}>
              <IonGrid style={{ width: '100%' }}>
                <IonRow>
                  <IonCol size="9" style={{ wordBreak: 'break-word' }}>
                    <IonLabel>
                      <strong>{r.dia.charAt(0).toUpperCase() + r.dia.slice(1)}</strong>: {r.inicio} - {r.fin} ({r.tipo})
                    </IonLabel>
                  </IonCol>
                  <IonCol size="3" style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: '8px' }}>
                    <IonButton color="primary" fill="clear" onClick={() => handleEditar(index)}>
                      <IonIcon icon={createOutline} />
                    </IonButton>
                    <IonButton color="danger" fill="clear" onClick={() => handleEliminar(index)}>
                      <IonIcon icon={trashOutline} />
                    </IonButton>
                  </IonCol>
                </IonRow>
              </IonGrid>
            </IonItem>
          ))}
          {restriccionesFiltradas.length === 0 && (
            <IonItem>
              <IonLabel>No hay restricciones que coincidan con el filtro.</IonLabel>
            </IonItem>
          )}
        </IonList>

        {/* Modal para agregar restricción */}
        <IonModal isOpen={showModal} onDidDismiss={() => setShowModal(false)}>
          <IonHeader>
            <IonToolbar>
              <IonTitle>Agregar Restricción</IonTitle>
            </IonToolbar>
          </IonHeader>
          <IonContent className="ion-padding">
            <IonList>
              <IonItem>
                <IonLabel position="stacked">Día</IonLabel>
                <IonSelect
                  value={nuevoDia}
                  placeholder="Selecciona día"
                  onIonChange={e => setNuevoDia(e.detail.value)}
                >
                  {DIAS.filter(d => d !== "todos").map(dia => (
                    <IonSelectOption key={dia} value={dia}>{dia.charAt(0).toUpperCase() + dia.slice(1)}</IonSelectOption>
                  ))}
                </IonSelect>
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Hora inicio</IonLabel>
                <IonDatetime
                  presentation="time"
                  hourCycle="h23"
                  value={nuevoInicio}
                  onIonChange={e => {
                    const value = Array.isArray(e.detail.value) ? e.detail.value[0] : e.detail.value;
                    setNuevoInicio(extractHora(value ?? null));
                  }}
                />
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Hora fin</IonLabel>
                <IonDatetime
                  presentation="time"
                  hourCycle="h23"
                  value={nuevoFin}
                  onIonChange={e => {
                    const value = Array.isArray(e.detail.value) ? e.detail.value[0] : e.detail.value;
                    setNuevoFin(extractHora(value ?? null));
                  }}
                />
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Tipo</IonLabel>
                <IonSelect
                  value={nuevoTipo}
                  placeholder="Selecciona tipo"
                  onIonChange={e => setNuevoTipo(e.detail.value)}
                >
                  {TIPOS.filter(t => t !== "todos").map(tipo => (
                    <IonSelectOption key={tipo} value={tipo}>{tipo.charAt(0).toUpperCase() + tipo.slice(1)}</IonSelectOption>
                  ))}
                </IonSelect>
              </IonItem>
            </IonList>
            <IonButton expand="block" onClick={handleAgregarRestriccion} className="ion-margin-top">
              Guardar
            </IonButton>
            <IonButton expand="block" color="medium" onClick={() => setShowModal(false)} className="ion-margin-top">
              Cancelar
            </IonButton>
          </IonContent>
        </IonModal>

        {/* Modal para editar restricción */}
        <IonModal isOpen={showEditModal} onDidDismiss={() => setShowEditModal(false)}>
          <IonHeader>
            <IonToolbar>
              <IonTitle>Editar Restricción</IonTitle>
            </IonToolbar>
          </IonHeader>
          <IonContent className="ion-padding">
            <IonList>
              <IonItem>
                <IonLabel position="stacked">Día</IonLabel>
                <IonSelect
                  value={editDia}
                  placeholder="Selecciona día"
                  onIonChange={e => setEditDia(e.detail.value)}
                >
                  {DIAS.filter(d => d !== "todos").map(dia => (
                    <IonSelectOption key={dia} value={dia}>{dia.charAt(0).toUpperCase() + dia.slice(1)}</IonSelectOption>
                  ))}
                </IonSelect>
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Hora inicio</IonLabel>
                <IonDatetime
                  presentation="time"
                  hourCycle="h23"
                  value={editInicio}
                  onIonChange={e => {
                    const value = Array.isArray(e.detail.value) ? e.detail.value[0] : e.detail.value;
                    setEditInicio(extractHora(value ?? null));
                  }}
                />
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Hora fin</IonLabel>
                <IonDatetime
                  presentation="time"
                  hourCycle="h23"
                  value={editFin}
                  onIonChange={e => {
                    const value = Array.isArray(e.detail.value) ? e.detail.value[0] : e.detail.value;
                    setEditFin(extractHora(value ?? null));
                  }}
                />
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Tipo</IonLabel>
                <IonSelect
                  value={editTipo}
                  placeholder="Selecciona tipo"
                  onIonChange={e => setEditTipo(e.detail.value)}
                >
                  {TIPOS.filter(t => t !== "todos").map(tipo => (
                    <IonSelectOption key={tipo} value={tipo}>{tipo.charAt(0).toUpperCase() + tipo.slice(1)}</IonSelectOption>
                  ))}
                </IonSelect>
              </IonItem>
            </IonList>
            <IonButton expand="block" onClick={handleGuardarEdicion} className="ion-margin-top">
              Guardar cambios
            </IonButton>
            <IonButton expand="block" color="medium" onClick={() => setShowEditModal(false)} className="ion-margin-top">
              Cancelar
            </IonButton>
          </IonContent>
        </IonModal>

        <IonToast
          isOpen={showToast}
          message="Completa todos los campos correctamente"
          duration={1500}
          onDidDismiss={() => setShowToast(false)}
        />
      </IonContent>
    </IonPage>
  );
};

export default Restricciones;
