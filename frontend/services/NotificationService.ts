import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform, PermissionsAndroid } from 'react-native';

// Configura como a notificação se comporta quando o app está aberto (Foreground)
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

export async function setupNotificationPermissions() {
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('lembrete-medicamento', {
      name: 'Lembrete de Medicamento',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF231F7C',
      sound: 'default', // Você pode customizar o som aqui se tiver o arquivo
      lockscreenVisibility: Notifications.AndroidNotificationVisibility.PUBLIC,
    });

    await Notifications.setNotificationChannelAsync('alarme-geral', {
      name: 'Alarme',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 500, 500, 500],
      lightColor: '#FF0000',
      sound: 'default',
      lockscreenVisibility: Notifications.AndroidNotificationVisibility.PUBLIC,
      audioAttributes: {
        usage: Notifications.AndroidAudioUsage.ALARM,
        contentType: Notifications.AndroidAudioContentType.SONIFICATION,
      }
    });

    // Para Android 13+ (API Level 33+), precisamos pedir permissão explicitamente
    if (Platform.Version >= 33) {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS
      );
      if (granted !== PermissionsAndroid.RESULTS.GRANTED) {
        alert('Permissão de notificação é necessária para o alarme funcionar!');
      }
    }
  } else {
    // iOS e outros
    if (Device.isDevice) {
      const { status: existingStatus } = await Notifications.getPermissionsAsync();
      let finalStatus = existingStatus;
      if (existingStatus !== 'granted') {
        const { status } = await Notifications.requestPermissionsAsync();
        finalStatus = status;
      }
      if (finalStatus !== 'granted') {
        alert('Falha ao obter permissão para notificações!');
        return;
      }
    }
  }
}

export async function scheduleMedicationReminder(nome: string, dosagem: string, date: Date) {
  // Agenda a notificação
  await Notifications.scheduleNotificationAsync({
    content: {
      title: "Hora do Medicamento! 💊",
      body: `Está na hora de tomar ${nome} - ${dosagem}`,
      sound: 'default',
      data: { screen: 'Alarm', nome, dosagem }, // Dados para navegação
      priority: Notifications.AndroidNotificationPriority.MAX,
    },
    trigger: {
      type: Notifications.SchedulableTriggerInputTypes.DATE,
      date: date, // Objeto Date contendo a data e hora exata
    },
  });
}

export async function scheduleAlarmNotification(date: Date) {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: "Alarme! ⏰",
      body: "Seu alarme está tocando!",
      sound: 'default',
      priority: Notifications.AndroidNotificationPriority.MAX,
      data: { screen: 'Alarm' },
      color: '#FF0000',
      vibrate: [0, 500, 500, 500],
    },
    trigger: {
      channelId: 'alarme-geral',
      date: date,
    } as any,
  });
}