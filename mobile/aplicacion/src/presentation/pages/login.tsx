import { 
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar,
  IonList, IonItem, IonInput, IonButton, IonCard, IonCardContent, IonAlert
} from '@ionic/react';
import './Login.css';
import { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login: React.FC = () => {
  const history = useHistory();
  const { login } = useAuth();

  const [correo, setCorreo] = useState('');
  const [contraseña, setPassword] = useState('');
  const [showAlert, setShowAlert] = useState(false);

  const handleLogin = async () => {
    try {
      const data = await login(correo, contraseña);
      // puedes guardar más info en localStorage si quieres
      localStorage.setItem("nombre", data.apellido);
      localStorage.setItem("correo", data.email);
      localStorage.setItem("tipoUsuario", data.nombre);

      // redirigir según lógica de negocio
      history.push("/tabs/tab1");
    } catch (error) {
      setShowAlert(true);
    }
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
                    placeholder="ej: estudiante@uct.cl"
                    value={correo}
                    onIonInput={e => setCorreo(e.detail.value!)}
                  ></IonInput>
                </IonItem>

                <IonItem>
                  <IonInput
                    label="Contraseña"
                    labelPlacement="floating"
                    type="password"
                    placeholder="Contraseña"
                    value={contraseña}
                    onIonInput={e => setPassword(e.detail.value!)}
                  ></IonInput>
                </IonItem>
              </IonList>

              <IonButton expand="block" onClick={handleLogin}>
                Ingresar
              </IonButton>
            </IonCardContent>
          </IonCard>
        </div>

        <IonAlert
          isOpen={showAlert}
          onDidDismiss={() => setShowAlert(false)}
          header={'Error'}
          message={'Usuario o contraseña incorrectos'}
          buttons={['OK']}
        />
      </IonContent>
    </IonPage>
  );
};

export default Login;
