import { Button } from "@/components/Button/Button";
import { TextInput } from "@/components/Input/TextInput";
import { DatePicker } from "@/components/Picker/DatePicker";
import { TimePicker } from "@/components/Picker/TimePicker";
import { BodyText } from "@/components/Text/BodyText";
import React, { useState } from "react";
import { styled } from "styled-components/native";

const HomeView = styled.View`
  flex: 1;
  background-color: #f5f5f5;
  align-items: center;
`;

const Logo = styled.Image`
  width: 80%;
  height: 10%;
  object-fit: contain;
  margin-top: 5%;
`;

const FormView = styled.View`
  width: 90%;
  background: transparent;
  border-radius: 0px;
  padding: 0;
  margin-top: 32px;
  margin-bottom: 32px;
  align-items: flex-start;
`;

const Label = styled.Text`
  font-size: 16px;
  font-weight: 900;
  color: #222;
  margin-bottom: 6px;
  margin-left: 2px;
`;

const HorariosViewContainer = styled.ScrollView`
  border: 1px solid #e0e0e0;
  width: 100%;
  height: 225px;
  border-radius: 12px;
  background: #f9f9f9;
  padding: 12px 8px;
  margin-top: 8px;
  margin-bottom: 12px;
`;

const HorariosWrap = styled.View`
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
`;

const HorariosHeader = styled.View`
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  margin-bottom: 4px;
  width: 100%;
`;

const HorariosItem = styled.View`
  border: 1px solid #29acb9;
  border-radius: 18px;
  flex-direction: row;
  align-items: center;
  margin-right: 10px;
  padding: 4px 10px;
`;

export default function EditScreen({ navigation }: any) {
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

      <Button title="Salvar" onPress={handleSubmit} />

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
