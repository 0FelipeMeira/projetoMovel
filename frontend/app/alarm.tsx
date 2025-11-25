import { Button } from "@/components/Button/Button";
import { Audio } from "expo-av";
import React, { useEffect, useState } from "react";
import { Platform, Text } from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";
import { styled } from "styled-components/native";
import { setupNotificationPermissions, scheduleAlarmNotification } from "@/services/NotificationService";

const audioSource = require("../assets/audio.mp3");

const LoginView = styled.View`
  flex: 1;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  gap: 16px;
  padding: 10%;
`;

export default function AlarmScreen({ navigation }: any) {
  const [sound, setSound] = useState<Audio.Sound>();
  const [date, setDate] = useState(new Date());
  const [showPicker, setShowPicker] = useState(false);
  const [scheduledTime, setScheduledTime] = useState<Date | null>(null);

  useEffect(() => {
    const configureAudio = async () => {
      try {
        await Audio.setAudioModeAsync({
          staysActiveInBackground: true,
          playsInSilentModeIOS: true,
          shouldDuckAndroid: true,
          playThroughEarpieceAndroid: false,
        });
      } catch (error) {
        console.error("Failed to configure audio:", error);
      }
    };

    configureAudio();
    setupNotificationPermissions();
  }, []);

  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;

    if (scheduledTime) {
      const checkTime = () => {
        const now = new Date();
        if (now >= scheduledTime) {
          ring();
          setScheduledTime(null); // Reset after ringing
        } else {
          // Check again in 1 second
          timer = setTimeout(checkTime, 1000);
        }
      };
      checkTime();
    }

    return () => {
      if (timer) clearTimeout(timer);
    };
  }, [scheduledTime]);

  useEffect(() => {
    return sound
      ? () => {
          console.log("Unloading Sound");
          sound.unloadAsync();
        }
      : undefined;
  }, [sound]);

  const onChange = (event: any, selectedDate?: Date) => {
    const currentDate = selectedDate || date;
    setShowPicker(Platform.OS === "ios");
    setDate(currentDate);
  };

  const scheduleAlarm = () => {
    const now = new Date();
    const alarmDate = new Date(now);
    alarmDate.setHours(date.getHours());
    alarmDate.setMinutes(date.getMinutes());
    alarmDate.setSeconds(0);

    if (alarmDate < now) {
      // If time passed today, schedule for tomorrow
      alarmDate.setDate(alarmDate.getDate() + 1);
    }

    setScheduledTime(alarmDate);
    scheduleAlarmNotification(alarmDate);
    alert(`Alarme agendado para: ${alarmDate.toLocaleTimeString()}`);
  };

  const ring = async () => {
    try {
      const { sound: newSound } = await Audio.Sound.createAsync(audioSource, {
        shouldPlay: true,
      });
      setSound(newSound);
    } catch (error) {
      console.error("Error playing sound", error);
    }
  };

  return (
    <LoginView>
      <Text style={{ fontSize: 32, fontWeight: "bold", marginBottom: 20 }}>
        {date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
      </Text>

      <Button title="Definir Horário" onPress={() => setShowPicker(true)} />

      {showPicker && (
        <DateTimePicker
          testID="dateTimePicker"
          value={date}
          mode="time"
          is24Hour={true}
          display="default"
          onChange={onChange}
        />
      )}

      <Button 
        title={scheduledTime ? "Alarme Agendado" : "Agendar Alarme"} 
        onPress={scheduleAlarm} 
      />
      
      <Button title="Tocar Agora" onPress={ring} />
    </LoginView>
  );
}
