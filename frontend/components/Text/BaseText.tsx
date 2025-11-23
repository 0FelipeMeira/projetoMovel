import styled from "styled-components/native";

export const BaseText = styled.Text<{
  $color?: string;
  $fontSize?: string;
  $fontWeight?: string;
}>`
  font-size: ${({ $fontSize }) => $fontSize || "16px"};
  color: ${({ $color }) => $color || "#000"};
  font-weight: ${({ $fontWeight }) => $fontWeight || "500"};
`;
