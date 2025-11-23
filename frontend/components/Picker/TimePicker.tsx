import DateTimePicker from "@react-native-community/datetimepicker";
import React, { useState } from "react";
import { Platform } from "react-native";
import { Button } from "../Button/Button";

export const TimePicker = ({
  timelist,
  setTimeList,
}: {
  timelist: string[];
  setTimeList: React.Dispatch<React.SetStateAction<string[]>>;
}) => {
  const [show, setShow] = useState(false);

  const onChange = (event: any, selectedTime: Date | undefined) => {
    if (
      event.type == "set" &&
      selectedTime &&
      selectedTime?.toLocaleTimeString() != ""
    ) {
      setTimeList([...timelist, selectedTime?.toLocaleTimeString()]);
    }

    setShow(Platform.OS === "ios");
  };

  const showDatePicker = () => {
    setShow(true);
  };

  return (
    <>
      <Button title={"Adicionar horário"} onPress={showDatePicker} />

      {show && (
        <DateTimePicker
          testID="dateTimePicker"
          value={new Date()}
          mode={"time"}
          display="default"
          onChange={onChange}
        />
      )}
    </>
  );
};
