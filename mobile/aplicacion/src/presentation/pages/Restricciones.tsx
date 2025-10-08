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
import { useEffect, useState } from "react";

// Casos de uso y repositorio
import { RestriccionesUseCase } from "../../application/usecases/RestriccionesUseCase";
import { RestriccionesApiRepository } from "../../infrastructure/repositories/RestriccionesApiRepository";
import { Restriccion } from "../../domain/entities/Restriccion";

const repo = new RestriccionesApiRepository();
const useCase = new RestriccionesUseCase(repo);

const DIAS = ["todos", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"];
const TIPOS = ["todos", "obligatoria", "preferencia", "opcional"];

const Restricciones: React.FC = () => {
  const [restricciones, setRestricciones] = useState<Restriccion[]>([]);
  const [filtroDia, setFiltroDia] = useState<string>('todos');
  const [filtroTipo, setFiltroTipo] = useState<string>('todos');
  const [showModal, setShowModal] = useState(false);
  const [nuevoDia, setNuevoDia] = useState('');
  const [nuevoInicio, setNuevoInicio] = useState('');
  const [nuevoFin, setNuevoFin] = useState('');
  const [nuevoTipo, setNuevoTipo] = useState('');
  const [showToast, setShowToast] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editIndex, setEditIndex] = useState<number | null>(null);
  const [editDia, setEditDia] = useState('');
  const [editInicio, setEditInicio] = useState('');
  const [editFin, setEditFin] = useState('');
  const [editTipo, setEditTipo] = useState('');

  // 🟢 Cargar restricciones desde el backend
  useEffect(() => {
    const cargarRestricciones = async () => {
      try {
        const data = await useCase.getAllRestricciones();
        setRestricciones(data);
      } catch (error) {
        console.error("Error al cargar restricciones:", error);
      }
    };
    cargarRestricciones();
  }, []);

  const extractHora = (value: string | null): string => {
    if (!value) return '';
    const date = new Date(value);
    const horas = date.getHours().toString().padStart(2, '0');
    const minutos = date.getMinutes().toString().padStart(2, '0');
    return `${horas}:${minutos}`;
  };

  // 🟢 Crear restricción en backend
  const handleAgregarRestriccion = async () => {
    if (!nuevoDia || !nuevoInicio || !nuevoFin || !nuevoTipo) {
      setShowToast(true);
      return;
    }

    try {
      const nueva = await useCase.createRestriccion({
        dia: nuevoDia,
        inicio: nuevoInicio,
        fin: nuevoFin,
        tipo: nuevoTipo,
      });
      setRestricciones([...restricciones, nueva]);
      setShowModal(false);
      setNuevoDia('');
      setNuevoInicio('');
      setNuevoFin('');
      setNuevoTipo('');
    } catch (error) {
      console.error("Error al crear restricción:", error);
    }
  };

  // 🟢 Eliminar restricción del backend
  const handleEliminar = async (index: number) => {
    const restriccion = restricciones[index];
    if (!restriccion || !(restriccion as any).id) {
      console.error("La restricción no tiene un ID válido para eliminar.");
      return;
    }

    try {
      await useCase.deleteRestriccion((restriccion as any).id);
      const nuevas = restricciones.filter((_, i) => i !== index);
      setRestricciones(nuevas);
    } catch (error) {
      console.error("Error al eliminar restricción:", error);
    }
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

  // 🟢 Actualizar restricción en backend
  const handleGuardarEdicion = async () => {
    if (editIndex === null || !editDia || !editInicio || !editFin || !editTipo) {
      setShowToast(true);
      return;
    }

    const restriccion = restricciones[editIndex];
    if (!(restriccion as any).id) {
      console.error("No se puede actualizar una restricción sin ID");
      return;
    }

    try {
      const actualizada = await useCase.updateRestriccion((restriccion as any).id, {
        dia: editDia,
        inicio: editInicio,
        fin: editFin,
        tipo: editTipo,
      });
      const nuevas = [...restricciones];
      nuevas[editIndex] = actualizada;
      setRestricciones(nuevas);
      setShowEditModal(false);
      setEditIndex(null);
    } catch (error) {
      console.error("Error al actualizar restricción:", error);
    }
  };

  // 🟢 Filtrar restricciones
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

        {/* Lista de restricciones */}
        <IonList>
          {restriccionesFiltradas.map((r, index) => (
            <IonItem key={index} style={{ alignItems: 'flex-start' }}>
              <IonGrid style={{ width: '100%' }}>
                <IonRow>
                  <IonCol size="9">
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

        {/* Modal agregar */}
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
                <IonSelect value={nuevoDia} placeholder="Selecciona día" onIonChange={e => setNuevoDia(e.detail.value)}>
                  {DIAS.filter(d => d !== "todos").map(dia => (
                    <IonSelectOption key={dia} value={dia}>{dia.charAt(0).toUpperCase() + dia.slice(1)}</IonSelectOption>
                  ))}
                </IonSelect>
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Hora inicio</IonLabel>
                <IonDatetime presentation="time" hourCycle="h23" value={nuevoInicio}
                  onIonChange={e => setNuevoInicio(extractHora(e.detail.value as string))} />
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Hora fin</IonLabel>
                <IonDatetime presentation="time" hourCycle="h23" value={nuevoFin}
                  onIonChange={e => setNuevoFin(extractHora(e.detail.value as string))} />
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Tipo</IonLabel>
                <IonSelect value={nuevoTipo} placeholder="Selecciona tipo" onIonChange={e => setNuevoTipo(e.detail.value)}>
                  {TIPOS.filter(t => t !== "todos").map(tipo => (
                    <IonSelectOption key={tipo} value={tipo}>{tipo.charAt(0).toUpperCase() + tipo.slice(1)}</IonSelectOption>
                  ))}
                </IonSelect>
              </IonItem>
            </IonList>
            <IonButton expand="block" onClick={handleAgregarRestriccion} className="ion-margin-top">Guardar</IonButton>
            <IonButton expand="block" color="medium" onClick={() => setShowModal(false)} className="ion-margin-top">Cancelar</IonButton>
          </IonContent>
        </IonModal>

        {/* Modal editar */}
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
                <IonSelect value={editDia} placeholder="Selecciona día" onIonChange={e => setEditDia(e.detail.value)}>
                  {DIAS.filter(d => d !== "todos").map(dia => (
                    <IonSelectOption key={dia} value={dia}>{dia.charAt(0).toUpperCase() + dia.slice(1)}</IonSelectOption>
                  ))}
                </IonSelect>
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Hora inicio</IonLabel>
                <IonDatetime presentation="time" hourCycle="h23" value={editInicio}
                  onIonChange={e => setEditInicio(extractHora(e.detail.value as string))} />
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Hora fin</IonLabel>
                <IonDatetime presentation="time" hourCycle="h23" value={editFin}
                  onIonChange={e => setEditFin(extractHora(e.detail.value as string))} />
              </IonItem>
              <IonItem>
                <IonLabel position="stacked">Tipo</IonLabel>
                <IonSelect value={editTipo} placeholder="Selecciona tipo" onIonChange={e => setEditTipo(e.detail.value)}>
                  {TIPOS.filter(t => t !== "todos").map(tipo => (
                    <IonSelectOption key={tipo} value={tipo}>{tipo.charAt(0).toUpperCase() + tipo.slice(1)}</IonSelectOption>
                  ))}
                </IonSelect>
              </IonItem>
            </IonList>
            <IonButton expand="block" onClick={handleGuardarEdicion} className="ion-margin-top">Guardar cambios</IonButton>
            <IonButton expand="block" color="medium" onClick={() => setShowEditModal(false)} className="ion-margin-top">Cancelar</IonButton>
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
