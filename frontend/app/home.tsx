import { HeroImage, HeroText, HeroView } from "@/components/Hero/Hero";
import {
  ListOptionsButton,
  ListOptionsText,
  ListOptionsView,
} from "@/components/MedicamentoList/ListOptions";
import {
  MedicamentoItemNomeScrollView,
  MedicamentoItemScrollView,
  MedicamentosScrollView,
} from "@/components/MedicamentoList/ScrollView";
import { BaseText } from "@/components/Text/BaseText";
import React from "react";
import { Image, Text, TouchableOpacity } from "react-native";
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

export default function HomeScreen({ navigation }: any) {
  return (
    <HomeView>
      <Logo source={require("../assets/images/logoInLine.png")} />

      <HeroView>
        <HeroImage source={require("../assets/images/logoInLine.png")} />
        <HeroText>Fulano de tal</HeroText>
      </HeroView>

      <ListOptionsView>
        <ListOptionsText>Medicamentos</ListOptionsText>
        <ListOptionsButton>
          <BaseText $color="#29ACB9" $fontSize="16px" $fontWeight="900">
            Novo
          </BaseText>
        </ListOptionsButton>
      </ListOptionsView>

      <MedicamentosScrollView>
        <MedicamentoItemScrollView>
          <MedicamentoItemNomeScrollView>
            Medicamento 1
          </MedicamentoItemNomeScrollView>
          <Text>150mg</Text>
          <Text>8/10</Text>
          <TouchableOpacity onPress={() => {}}>
            <Image
              source={require("../assets/images/edit.png")}
              style={{ height: 35, aspectRatio: 1 }}
            />
          </TouchableOpacity>
        </MedicamentoItemScrollView>
      </MedicamentosScrollView>
    </HomeView>
  );
}
