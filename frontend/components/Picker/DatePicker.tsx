import DateTimePicker from "@react-native-community/datetimepicker";
import React, { useRef, useState } from "react";
import { Platform } from "react-native";
import { TextInput } from "../Input/TextInput";

export const DatePicker = ({
  date,
  setDate,
}: {
  date: Date;
  setDate: React.Dispatch<React.SetStateAction<Date>>;
}) => {
  const [show, setShow] = useState(false);
  const inputRef = useRef<any>(null);

  const onChange = (event: any, selectedDate: Date | undefined) => {
    setShow(Platform.OS === "ios");
    if (event.type == "set" && selectedDate) {
      setDate(selectedDate);
    }
    inputRef.current?.blur && inputRef.current.blur();
  };

  const showDatePicker = () => {
    setShow(true);
  };
  return (
    <>
      <TextInput
        ref={inputRef}
        value={date.toLocaleDateString("pt-BR")}
        onPress={showDatePicker}
      />

      {show && (
        <DateTimePicker
          testID="dateTimePicker"
          value={date}
          mode={"date"}
          display="default"
          onChange={onChange}
        />
      )}
    </>
  );
};
