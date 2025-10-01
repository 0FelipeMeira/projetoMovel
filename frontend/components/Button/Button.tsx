import React from "react";
import { TouchableOpacityProps } from "react-native";
import { BaseText } from "../Text/BaseText";
import styled from "styled-components/native";

type ButtonProps = TouchableOpacityProps & {
  title: string;
  type?: "primary" | "secondary";
  width?: string;
};

const TouchableOpacity = styled.TouchableOpacity<{
  type?: string;
  width?: string;
}>`
  width: ${(props) => props.width || "auto"};
  background-color: ${(props) =>
    props.type === "secondary" ? "transparent" : "#7100b3ff"};
  border-radius: 8px;
  padding-vertical: 12px;
  padding-horizontal: 16px;
  align-items: center;
  font-weight: 900;
`;

export function Button({ title, type, width, ...rest }: ButtonProps) {
  return (
    <TouchableOpacity type={type} width={width} {...rest}>
      <BaseText $color={type === "secondary" ? "#000" : "#FFF"}>
        {title}
      </BaseText>
    </TouchableOpacity>
  );
}
