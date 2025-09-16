import { 
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar,
  IonList, IonItem, IonInput, IonButton, IonCard, IonCardContent, IonAlert
} from '@ionic/react';
import './Login.css';
import { useState } from 'react';
import { useHistory } from 'react-router-dom';

const Login: React.FC = () => {
  const history = useHistory();

  // Estados para inputs
  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');
  const [showAlert, setShowAlert] = useState(false);

  // Cuentas de prueba con datos completos
  const cuentas: { 
    [key: string]: { 
      password: string; 
      tipo: string; 
      nombre: string; 
    } 
  } = {
    "estudiante@uct.cl": { password: "estudiante", tipo: "estudiante", nombre: "Benjamin Carrasco" },
    "admin@uct.cl": { password: "admin", tipo: "admin", nombre: "Administrador" },
    "profesor@uct.cl": { password: "profesor", tipo: "profesor", nombre: "Profesor Pérez" },
  };

  const handleLogin = () => {
    const cuenta = cuentas[correo.trim().toLowerCase()]; // normaliza correo
    if (cuenta && cuenta.password === password) {
      // Guardar datos en localStorage
      localStorage.setItem('tipoUsuario', cuenta.tipo);
      localStorage.setItem('nombre', cuenta.nombre);
      localStorage.setItem('correo', correo.trim().toLowerCase());
      // Redirigir según tipo de usuario
      switch (cuenta.tipo) {
        case "estudiante":
          history.push("/tabs/tab1"); 
          break;
        case "admin":
          history.push("/tabs/adminrestricciones"); 
          break;
        case "profesor":
          history.push("/tabs/tab1"); 
          break;
      }
    } else {
      setShowAlert(true); // Mostrar alerta de error
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
                    value={password}
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
