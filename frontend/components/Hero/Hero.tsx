import styled from "styled-components/native";

export const HeroView = styled.View`
  width: 100%;
  height: 25%;
  margin-vertical: 8%;

  justify-content: center;
  align-items: center;
`;

export const HeroImage = styled.Image`
  height: 80%;
  aspect-ratio: 1/1;
  border-radius: 9999px;
  object-fit: cover;
`;

export const HeroText = styled.Text`
  font-size: 24px;
  font-weight: bold;
  margin-top: 16px;
`;
