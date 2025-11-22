import styled from "styled-components/native";

export const MedicamentosScrollView = styled.ScrollView`
  width: 95%;
  flex: 1;
  gap: 8px;
  margin-bottom: 5%;
`;

export const MedicamentoItemScrollView = styled.View`
  width: 100%;
  height: 50px;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
`;

export const MedicamentoItemNomeScrollView = styled.Text`
  width: 50%;
  font-size: 18px;
`;
