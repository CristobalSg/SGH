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
  IonAccordionGroup 
} from '@ionic/react';

import { checkmarkCircleOutline, trashOutline, searchOutline } from 'ionicons/icons';
import './AdminRestricciones.css';

const AdminRestricciones: React.FC = () => {
  // Datos mock
  const profesores = [
    {
      nombre: "Profesor Juan Pérez",
      restricciones: [
        "Restricción: lunes 8:00 - 10:00",
        "Restricción: miércoles 14:00 - 16:00",
      ],
    },
    {
      nombre: "Profesor Ana Torres",
      restricciones: [
        "Restricción: martes 9:00 - 11:00",
        "Restricción: jueves 10:00 - 12:00",
        "Restricción: viernes 15:00 - 17:00",
      ],
    },
    {
      nombre: "Profesor Carlos Díaz",
      restricciones: [
        "Restricción: lunes 10:00 - 12:00",
      ],
    },
  ];

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
        <IonAccordionGroup>
          {profesores.map((profesor, index) => (
            <IonAccordion key={index} value={profesor.nombre}>
              {/* Encabezado: profesor y número de restricciones */}
              <IonItem slot="header">
                <IonLabel>
                  {profesor.nombre} — {profesor.restricciones.length} restricciones
                </IonLabel>
              </IonItem>

              {/* Lista de restricciones */}
              <IonList slot="content">
                {profesor.restricciones.map((res, i) => (
                  <IonItem key={i}>
                    <IonLabel>{res}</IonLabel>
                    <IonButtons slot="end">
                      <IonButton color="success" fill="clear">
                        <IonIcon icon={checkmarkCircleOutline} />
                      </IonButton>
                      <IonButton color="danger" fill="clear">
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
