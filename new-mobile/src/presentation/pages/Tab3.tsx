import { 
  IonContent, 
  IonHeader, 
  IonPage, 
  IonTitle, 
  IonToolbar, 
  IonAccordion, 
  IonAccordionGroup, 
  IonItem, 
  IonLabel, 
  IonList, 
  IonButtons, 
  IonButton, 
  IonIcon 
} from '@ionic/react';

import { searchOutline, createOutline, trashOutline } from 'ionicons/icons';


const Tab3: React.FC = () => {
  const eventos = [
    {
      fecha: "2025-09-01",
      items: ["Prueba de Cálculo", "Entrega de trabajo de Robótica"]
    },
    {
      fecha: "2025-09-05",
      items: ["Exposición de Redes", "Avance de Proyecto de Software"]
    },
    {
      fecha: "2025-09-10",
      items: ["Prueba de Física Eléctrica"]
    },
    {
      fecha: "2025-09-15",
      items: ["Entrega de Informe de Laboratorio", "Control de Inglés"]
    }
  ];

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Eventos</IonTitle>
          <IonButtons slot="end">
            <IonButton>
              <IonIcon icon={searchOutline} />
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>
      
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Eventos</IonTitle>
          </IonToolbar>
        </IonHeader>

        <IonAccordionGroup>
          {eventos.map((evento, index) => (
            <IonAccordion key={index} value={evento.fecha}>
              <IonItem slot="header">
                <IonLabel style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>
                  {evento.fecha}
                </IonLabel>
              </IonItem>
              <IonList slot="content">
                {evento.items.map((item, i) => (
                  <IonItem key={i}>
                    <IonLabel>{item}</IonLabel>
                    <IonButtons slot="end">
                      <IonButton fill="clear" color="primary">
                        <IonIcon icon={createOutline} />
                      </IonButton>
                      <IonButton fill="clear" color="danger">
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

export default Tab3;
