import { Redirect, Route } from 'react-router-dom';
import {
  IonApp,
  IonIcon,
  IonLabel,
  IonRouterOutlet,
  IonTabBar,
  IonTabButton,
  IonTabs,
  setupIonicReact
} from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { calendar, home, person, time, settings } from 'ionicons/icons';
import Tab1 from './presentation/pages/Tab1';
import Tab2 from './presentation/pages/Tab2';
import Tab3 from './presentation/pages/Tab3';
import Login from './presentation/pages/login';
import Restricciones from './presentation/pages/Restricciones';
import AdminRestricciones from './presentation/pages/AdminRestricciones';

import '@ionic/react/css/core.css';
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';
import '@ionic/react/css/palettes/dark.system.css';
import './presentation/theme/variables.css';

setupIonicReact();

const App: React.FC = () => {
  const tipoUsuario = localStorage.getItem("tipoUsuario");

  return (
    <IonApp>
      <IonReactRouter>
        <IonRouterOutlet>
          {/* Login fuera de tabs */}
          <Route exact path="/" component={Login} />

          {/* Tabs */}
          <Route path="/tabs">
            <IonTabs>
              <IonRouterOutlet>
                <Route exact path="/tabs/tab1" component={Tab1} />
                <Route exact path="/tabs/tab2" component={Tab2} />
                <Route exact path="/tabs/tab3" component={Tab3} />

                {/* Restricciones → si no es estudiante */}
                <Route
                  exact
                  path="/tabs/restricciones"
                  render={() =>
                    tipoUsuario !== "estudiante" ? (
                      <Restricciones />
                    ) : (
                      <Redirect to="/tabs/tab1" />
                    )
                  }
                />

                {/* AdminRestricciones → solo admin */}
                <Route
                  exact
                  path="/tabs/adminrestricciones"
                  render={() =>
                    tipoUsuario === "admin" ? (
                      <AdminRestricciones />
                    ) : (
                      <Redirect to="/tabs/tab1" />
                    )
                  }
                />

                {/* Redirección por defecto */}
                <Redirect exact from="/tabs" to="/tabs/tab1" />
              </IonRouterOutlet>

<IonTabBar slot="bottom">
  {/* Home → mostrar solo si no es admin */}
  {tipoUsuario !== "admin" && (
    <IonTabButton tab="tab1" href="/tabs/tab1">
      <IonIcon aria-hidden="true" icon={home} />
      <IonLabel>Home</IonLabel>
    </IonTabButton>
  )}

  {/* Perfil → mostrar siempre */}
  <IonTabButton tab="tab2" href="/tabs/tab2">
    <IonIcon aria-hidden="true" icon={person} />
    <IonLabel>Perfil</IonLabel>
  </IonTabButton>

  {/* Eventos → mostrar siempre */}
  <IonTabButton tab="tab3" href="/tabs/tab3">
    <IonIcon aria-hidden="true" icon={calendar} />
    <IonLabel>Eventos</IonLabel>
  </IonTabButton>

  {/* Restricciones → mostrar solo profesor */}
  {tipoUsuario === "profesor" && (
    <IonTabButton tab="restricciones" href="/tabs/restricciones">
      <IonIcon aria-hidden="true" icon={time} />
      <IonLabel>Restricciones</IonLabel>
    </IonTabButton>
  )}

  {/* Admin → mostrar solo admin */}
  {tipoUsuario === "admin" && (
    <IonTabButton tab="adminrestricciones" href="/tabs/adminrestricciones">
      <IonIcon aria-hidden="true" icon={settings} />
      <IonLabel>Admin</IonLabel>
    </IonTabButton>
  )}
</IonTabBar>

            </IonTabs>
          </Route>
        </IonRouterOutlet>
      </IonReactRouter>
    </IonApp>
  );
};

export default App;
