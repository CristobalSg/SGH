import { 
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar,
  IonList, IonItem, IonInput, IonButton, IonCard, IonCardContent
} from '@ionic/react';
import './Login.css';
import { useHistory } from 'react-router-dom';

const Login: React.FC = () => {
  const history = useHistory();

  const handleLogin = () => {
    // Aquí puedes validar usuario/contraseña si quieres
    history.push("/tabs/tab1"); // 👉 redirige al Tab1
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Login</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <div className="login-container">
          <IonCard className="login-card">
            <IonCardContent>
              <IonList>
                <IonItem>
                  <IonInput
                    label="Correo"
                    labelPlacement="floating"
                    placeholder="estudiante@alu.uct.cl"
                  ></IonInput>
                </IonItem>

                <IonItem>
                  <IonInput
                    label="Contraseña"
                    labelPlacement="floating"
                    type="password"
                    placeholder="123"
                  ></IonInput>
                </IonItem>
              </IonList>

              <IonButton expand="block" onClick={handleLogin}>
                Ingresar
              </IonButton>
            </IonCardContent>
          </IonCard>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default Login;
