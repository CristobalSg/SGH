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
  IonList 
} from '@ionic/react';
import './Tab3.css';

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
              <IonLabel style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>{evento.fecha}</IonLabel>

            </IonItem>
            <IonList slot="content">
              {evento.items.map((item, i) => (
                <IonItem key={i}>
                  <IonLabel>{item}</IonLabel>
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
