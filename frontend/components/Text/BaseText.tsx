import styled from "styled-components/native";

export const BaseText = styled.Text<{ $color?: string }>`
  font-size: 16px;
  color: ${({ $color }) => $color || "#000"};
`;
