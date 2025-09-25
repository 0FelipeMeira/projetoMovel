import { Button } from "@/components/Button/Button";
import { TextInput } from "@/components/Input/TextInput";
import { Title } from "@/components/Text/Title";
import React, { useState } from "react";
import { styled } from "styled-components/native";

const LoginView = styled.View`
  flex: 1;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  gap: 16px;
  padding: 10%;
`;

const FlexView = styled.View`
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

export default function LoginScreen({ navigation }: any) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const resetForm = () => {
    setUsername("");
    setPassword("");
  };

  return (
    <LoginView>
      <Title>Login</Title>
      <TextInput
        placeholder="Usuário"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />
      <TextInput
        placeholder="Senha"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <FlexView>
        <Button type={"secondary"} title="Esqueci a senha" onPress={() => {}} />
        <Button type={"secondary"} title="Reset de senha" onPress={resetForm} />
      </FlexView>
      <Button
        width="60%"
        title="Entrar"
        onPress={() => navigation.navigate("Register")}
      />
    </LoginView>
  );
}
