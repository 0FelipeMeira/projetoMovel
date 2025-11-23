import { Button } from "@/components/Button/Button";
import { TextInput } from "@/components/Input/TextInput";
import { DatePicker } from "@/components/Picker/DatePicker";
import { TimePicker } from "@/components/Picker/TimePicker";
import { BodyText } from "@/components/Text/BodyText";
import { Label } from "@react-navigation/elements";
import React, { useState } from "react";
import {
  FormView,
  HomeView,
  HorariosHeader,
  HorariosItem,
  HorariosViewContainer,
  HorariosWrap,
  Logo,
} from "./edit";

export default function AddScreen({ navigation }: any) {
  const [nome, setNome] = useState("");
  const [dosagem, setDosagem] = useState("");

  const [dataInicio, setDataInicio] = useState<Date>(new Date());
  const [dataFim, setDataFim] = useState<Date>(new Date());

  const [horarios, setHorarios] = useState<string[]>(["03:00"]);
  let sortedHorarios = horarios.sort();

  const removeHorario = (idx: number) => {
    setHorarios(horarios.filter((_, i) => i !== idx));
  };

  const handleSubmit = () => {
    // Aqui você pode tratar o envio do formulário
    // Exemplo: enviar para API ou navegar para outra tela
    // navigation.goBack();
  };

  return (
    <HomeView>
      <Logo source={require("../assets/images/logoInLine.png")} />

      <Button title="Adicionar" onPress={handleSubmit} />

      <FormView>
        <Label>Nome do medicamento</Label>
        <TextInput
          value={nome}
          onChangeText={setNome}
          placeholder="Digite o nome"
          placeholderTextColor="#bdbdbd"
        />

        <Label>Dosagem</Label>
        <TextInput
          value={dosagem}
          onChangeText={setDosagem}
          placeholder="Ex: 150mg"
          placeholderTextColor="#bdbdbd"
        />

        <Label>Data de início</Label>
        <DatePicker date={dataInicio} setDate={setDataInicio} />

        <Label>Data final</Label>
        <DatePicker date={dataFim} setDate={setDataFim} />

        <HorariosHeader>
          <Label style={{ marginBottom: 0 }}>Horários</Label>
          <TimePicker timelist={horarios} setTimeList={setHorarios} />
        </HorariosHeader>

        <HorariosViewContainer showsVerticalScrollIndicator={false}>
          <HorariosWrap>
            {sortedHorarios.map((item, key) => (
              <HorariosItem key={key}>
                <BodyText>{item}</BodyText>
                <Button
                  title={"X"}
                  type="secondary"
                  onPress={() => removeHorario(key)}
                  style={{ marginLeft: 12 }}
                />
              </HorariosItem>
            ))}
          </HorariosWrap>
        </HorariosViewContainer>
      </FormView>
    </HomeView>
  );
}
