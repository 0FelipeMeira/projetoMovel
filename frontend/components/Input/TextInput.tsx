import styled from "styled-components/native";

const TextInputStyle = styled.TextInput`
  width: 100%;
  height: 44px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0 14px;
  margin-bottom: 18px;
  background: #fafafa;
  font-size: 16px;
  color: #222;
`;

export const TextInput = (props: any) => {
  return <TextInputStyle {...props} />;
};
