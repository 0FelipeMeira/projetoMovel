import styled from "styled-components/native";

const TextInputStyle = styled.TextInput`
  width: 100%;
  height: 40px;
  border-color: #ccc;
  border-width: 1px;
  border-radius: 8px;
  padding-horizontal: 8px;
`;

export const TextInput = (props: any) => {
  return <TextInputStyle {...props} />;
};
