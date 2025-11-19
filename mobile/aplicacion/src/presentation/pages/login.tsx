import { 
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar,
  IonList, IonItem, IonInput, IonButton, IonCard, IonCardContent, IonAlert
} from '@ionic/react';
import './Login.css';
import { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface TokenPayload {
  sub: string;     // correo
  user_id: number;
  rol: string;
  exp: number;
  type: string;
}

const Login: React.FC = () => {
  const history = useHistory();
  const { login } = useAuth();

  const [correo, setCorreo] = useState('');
  const [contraseña, setPassword] = useState('');
  const [showAlert, setShowAlert] = useState(false);

  const handleLogin = async () => {
  try {
    const loggedUser = await login(correo, contraseña);

    // Redirigir según rol
    if (loggedUser.rol === "administrador") {
      history.push("/tabs/admin");
    } else {
      history.push("/tabs/tab1");
    }
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
      <IonContent>
        <IonCard>
          <IonCardContent>
            <IonList>
              <IonItem>
                <IonInput 
                  type="email" 
                  placeholder="Correo" 
                  value={correo}
                  onIonChange={e => setCorreo(e.detail.value!)} 
                />
              </IonItem>
              <IonItem>
                <IonInput 
                  type="password" 
                  placeholder="Contraseña" 
                  value={contraseña}
                  onIonChange={e => setPassword(e.detail.value!)} 
                />
              </IonItem>
            </IonList>
            <IonButton expand="full" onClick={handleLogin}>Ingresar</IonButton>
          </IonCardContent>
        </IonCard>

        <IonAlert
          isOpen={showAlert}
          onDidDismiss={() => setShowAlert(false)}
          header={'Error'}
          message={'Correo o contraseña incorrectos'}
          buttons={['OK']}
        />
      </IonContent>
    </IonPage>
  );
};

export default Login;
