import App from "./app";
import { useEffect } from "react";
import * as Notifications from "expo-notifications";
import { registerForPushNotificationsAsync } from "../services/NotificationService";
import { useNavigation } from "expo-router"; // Ou useNavigation do React Navigation dependendo da sua config

export default function RootLayout() {
  useEffect(() => {
    registerForPushNotificationsAsync();

    // Ouvinte para quando o usuário toca na notificação
    const subscription = Notifications.addNotificationResponseReceivedListener(
      (response) => {
        const data = response.notification.request.content.data;

        // Aqui você navega para a tela de Alarme/Detalhes
        // Como você usa Stack Navigator no app.tsx, você precisará de acesso à navegação
        // Exemplo genérico (ajuste conforme sua estrutura de rotas):
        // navigation.navigate('Alarm', { nome: data.nome, dosagem: data.dosagem });
        console.log("Notificação tocada:", data);
      }
    );

    return () => subscription.remove();
  }, []);

  return <App />;
}
