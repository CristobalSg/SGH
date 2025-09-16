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

/* Core CSS required for Ionic components to work properly */
import '@ionic/react/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';

/* Dark mode */
// import '@ionic/react/css/palettes/dark.always.css';
// import '@ionic/react/css/palettes/dark.class.css';
import '@ionic/react/css/palettes/dark.system.css';

/* Theme variables */
import './presentation/theme/variables.css';

setupIonicReact();

const App: React.FC = () => (
  <IonApp>
    <IonReactRouter>
      <IonRouterOutlet>
        {/* Login fuera de los tabs */}
        <Route exact path="/" component={Login} />

        {/* Resto de la app con tabs */}
        <Route
          path="/tabs"
          render={() => (
            <IonTabs>
              <IonRouterOutlet>
                <Route exact path="/tabs/tab1" component={Tab1} />
                <Route exact path="/tabs/tab2" component={Tab2} />
                <Route exact path="/tabs/tab3" component={Tab3} />
                <Route exact path="/tabs/restricciones" component={Restricciones} />
                <Route exact path="/tabs/admin-restricciones" component={AdminRestricciones} />
              </IonRouterOutlet>

              <IonTabBar slot="bottom">
                <IonTabButton tab="tab1" href="/tabs/tab1">
                  <IonIcon aria-hidden="true" icon={home} />
                  <IonLabel>Home</IonLabel>
                </IonTabButton>
                <IonTabButton tab="tab2" href="/tabs/tab2">
                  <IonIcon aria-hidden="true" icon={person} />
                  <IonLabel>Perfil</IonLabel>
                </IonTabButton>
                <IonTabButton tab="tab3" href="/tabs/tab3">
                  <IonIcon aria-hidden="true" icon={calendar} />
                  <IonLabel>Eventos</IonLabel>
                </IonTabButton>
                <IonTabButton tab="restricciones" href="/tabs/restricciones">
                  <IonIcon aria-hidden="true" icon={time} />
                  <IonLabel>Restricciones</IonLabel>
                </IonTabButton>
                <IonTabButton tab="admin" href="/tabs/admin-restricciones">
                  <IonIcon aria-hidden="true" icon={settings} />
                  <IonLabel>Admin</IonLabel>
                </IonTabButton>
              </IonTabBar>
            </IonTabs>
          )}
        />
      </IonRouterOutlet>
    </IonReactRouter>
  </IonApp>
);

export default App;
